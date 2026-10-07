"""Pilot P6: fixed random sparse input mask on the population (numpy proxy).

One variable against the P4 proxy setup (diag.py): each node is wired to
exactly k of the 4 inputs, chosen at random without replacement.
W = dense Gaussian init x mask, and every plastic update is multiplied by
the mask, so masked weights stay exactly zero (asserted every tick).
Conditions: dense, sparse k=2, sparse k=3; each plastic and frozen.

Held fixed from diag.py: proxy body with overriding external mover, 16 nodes,
W0 ~ N(0, 0.5), theta = 0, leak 0.9, error-gated Sanger at eta = 2e-3,
modulator |e| / running SD on omega (proxy, not the PREREG 3b form),
delta-rule readout, blocked interleaved CV decoder on the second half.
Label: trailing "who moved it" per PREREG 4 (P3/P4 used the during-motion label).

Reports per condition, mean (min-max) over seeds:
  - BA real plastic, BA real frozen, plastic - frozen gap
  - collapse: median pairwise cosine of node weight rows at the 5-minute mark
  - dead nodes: never active (relu output > 0) in the decoder's half of the run
  - validity: "external while commanding" share of trailing label-0 ticks (>= 25%)

Seeds: s in 100..104 (pilot range; never governed seeds 0-4). Agent babble s,
mover s + 50, body noise s + 100, W0 s + 7, mask s + 13.
Run from pilots/: python3 p6_sparse_mask.py
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score

import pilot as p

DT = 1 / 60
T = 30000
N = 16
N_IN = 4
ETA = 2e-3
FIVE_MIN = round(300 / DT)
DEADBAND = 0.1   # rad/s, PREREG proposed
K_TRAIL = 30     # ticks, PREREG proposed
SEEDS = range(100, 105)
KS = [None, 2, 3]   # None = dense


def body(drive, rng, T, wall=1.0):
    ang = om = 0.0
    S = np.zeros((T, 3))
    for t in range(T):
        om += 0.3 * (drive[t] - om)
        ang += om * DT
        c = 0.0
        if abs(ang) > wall:
            c = abs(om) * 5
            ang = np.sign(ang) * wall
            om = 0.0
        S[t] = [ang, om, c]
    return S + rng.normal(0, 0.01, S.shape)


def make_mask(k, seed):
    if k is None:
        return np.ones((N, N_IN), bool)
    rng = np.random.default_rng(seed + 13)
    mask = np.zeros((N, N_IN), bool)
    for i in range(N):
        mask[i, rng.choice(N_IN, k, replace=False)] = True
    return mask


def run(S, cmd, W0, mask, plastic):
    W = W0 * mask
    mu = np.zeros(N_IN)
    var = np.ones(N_IN)
    tr = 0.0
    a = np.zeros(N)
    R = np.zeros(N + 1)
    sd = 1.0
    A = np.zeros((T, N))
    active = np.zeros(N, bool)
    W_5min = None
    for t in range(T - 1):
        if t == FIVE_MIN:
            W_5min = W.copy()
        tr = 0.95 * tr + 0.05 * cmd[t]
        x = np.array([S[t, 0], S[t, 1], S[t, 2], tr])
        mu += (x - mu) / 1000
        var += ((x - mu) ** 2 - var) / 1000
        x = (x - mu) / np.sqrt(var + 1e-6)
        y = np.maximum(W @ x, 0)
        a = 0.9 * a + 0.1 * y
        A[t] = a
        if t >= T // 2:
            active |= y > 0
        z = np.append(a, cmd[t])
        e = S[t + 1, 1] - R @ z
        R += 1e-3 * e * z
        sd += (abs(e) - sd) / 1000
        if plastic:
            m = min(abs(e) / (sd + 1e-6), 3)
            W += ETA * m * (np.outer(y, x) - np.tril(np.outer(y, y)) @ W) * mask
        assert np.all(W[~mask] == 0), f"masked weight nonzero at tick {t}"
    return A, W_5min, active


def trailing_labels(S, cmd, push):
    """PREREG 4 trailing label on the proxy: 1 = self, 0 = external, -1 = none."""
    L = np.full(T, -1)
    last = None            # (driver, agent_was_commanding) of last moving tick
    since = None
    ext_cmd = 0
    for t in range(T):
        if abs(S[t, 1]) > DEADBAND:
            if push[t] != 0:
                driver = 0
            elif cmd[t] != 0:
                driver = 1
            else:
                driver = None
            last = (driver, cmd[t] != 0)
            since = 0
        elif since is not None:
            since += 1
            if since <= K_TRAIL and last[0] is not None:
                L[t] = last[0]
                if last[0] == 0 and last[1]:
                    ext_cmd += 1
    n0 = (L == 0).sum()
    return L, ext_cmd / n0 if n0 else np.nan


def dec_blocked(X, L, nb=10, gap=200):   # as diag.py
    idx = np.arange(T // 2, T)
    blocks = np.array_split(idx, nb)
    tr, te = [], []
    for i, b in enumerate(blocks):
        b = b[gap:] if i else b
        (tr if i % 2 == 0 else te).append(b)
    tr = np.concatenate(tr)
    te = np.concatenate(te)
    tr = tr[L[tr] >= 0]
    te = te[L[te] >= 0]
    clf = LogisticRegression(max_iter=2000, class_weight="balanced").fit(X[tr], L[tr])
    return balanced_accuracy_score(L[te], clf.predict(X[te]))


def median_cosine(W):
    norms = np.linalg.norm(W, axis=1)
    Wn = W[norms > 0] / norms[norms > 0, None]
    C = Wn @ Wn.T
    return np.median(C[np.triu_indices(len(Wn), 1)])


def main():
    rows = {k: [] for k in KS}
    validity = []
    for s in SEEDS:
        cmd = p.babble(np.random.default_rng(s), T)
        push = p.babble(np.random.default_rng(s + 50), T)
        S = body(np.where(push != 0, push, cmd), np.random.default_rng(s + 100), T)
        L, ext_cmd = trailing_labels(S, cmd, push)
        validity.append(ext_cmd)
        W0 = np.random.default_rng(s + 7).normal(0, 0.5, (N, N_IN))
        for k in KS:
            mask = make_mask(k, s)
            r = {}
            for plastic in [True, False]:
                A, W5, active = run(S, cmd, W0, mask, plastic)
                tag = "plastic" if plastic else "frozen"
                r[f"BA {tag}"] = dec_blocked(A, L)
                r[f"cos {tag}"] = median_cosine(W5)
                r[f"dead {tag}"] = N - active.sum()
            r["gap"] = r["BA plastic"] - r["BA frozen"]
            rows[k].append(r)
            print(f"seed {s} k={k}: " + "  ".join(f"{m} {v:.3f}" for m, v in r.items()))

    v = np.array(validity)
    print(f"\next-while-commanding share of label 0: {v.mean():.2f} ({v.min():.2f}-{v.max():.2f})")
    for k in KS:
        print(f"\n--- {'dense' if k is None else f'sparse k={k}'}")
        for m in rows[k][0]:
            x = np.array([r[m] for r in rows[k]], float)
            print(f"{m:12s} {x.mean():.3f} ({x.min():.3f}-{x.max():.3f})")


if __name__ == "__main__":
    main()
