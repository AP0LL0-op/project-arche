import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score

DT = 1/60

def babble(rng, T):
    cmd = np.zeros(T); t = 0
    while t < T:
        hold = rng.integers(30, 181)
        cmd[t:t+hold] = rng.choice([-2.0, 0.0, 2.0]); t += hold
    return cmd

def body(cmd_drive, rng, T, wall=1.0):
    """Proxy arm: motor drives omega toward commanded rate; walls at +/-wall; random ball kicks."""
    ang, om = 0.0, 0.0
    S = np.zeros((T, 3)); kick = 0.0
    for t in range(T):
        om += 0.3 * (cmd_drive[t] - om)
        if rng.random() < 0.004: kick = rng.normal(0, 3)       # ball contact
        contact = abs(kick)
        om += kick; kick *= 0.5
        ang += om * DT
        if abs(ang) > wall:                                   # wall contact
            contact += abs(om) * 5; ang = np.sign(ang) * wall; om = 0.0
        S[t] = [ang, om, contact]
    return S + rng.normal(0, 0.01, S.shape)

def run_agent(S, cmd_own, W0, plastic, nonlin, eta=2e-3, N=16):
    T = len(S); W = W0.copy()
    mu = np.zeros(4); var = np.ones(4)
    tr = 0.0; a = np.zeros(N)
    R = np.zeros(N + 1); errsd = 1.0                          # readout: [a, cmd] -> next omega
    A = np.zeros((T, N))
    for t in range(T - 1):
        tr = 0.95 * tr + 0.05 * cmd_own[t]
        x = np.array([S[t, 0], S[t, 1], S[t, 2], tr])
        mu += (x - mu) / 1000; var += ((x - mu) ** 2 - var) / 1000
        x = (x - mu) / np.sqrt(var + 1e-6)
        u = W @ x
        y = np.maximum(u, 0) if nonlin else u
        a = 0.9 * a + 0.1 * y
        A[t] = a
        z = np.append(a, cmd_own[t])
        err = S[t + 1, 1] - R @ z
        R += 1e-3 * err * z                                    # local delta rule
        errsd += (abs(err) - errsd) / 1000
        if plastic:
            m = min(abs(err) / (errsd + 1e-6), 3.0)            # error-gated modulator
            W += eta * m * (np.outer(y, x) - np.tril(np.outer(y, y)) @ W)   # Sanger (GHA)
    return A

def labels(S, cmd_own, K=30, dead=0.2):
    T = len(S); L = np.full(T, -1)
    mov = (np.abs(S[:, 1]) > dead) & (cmd_own != 0)
    agree = (np.sign(S[:, 1]) == np.sign(cmd_own)) & mov
    for t in range(K, T):
        n = mov[t-K:t].sum()
        if n >= 10: L[t] = int(agree[t-K:t].sum() / n >= 2/3)
    return L

def decode(A, L):
    T = len(L); idx = np.arange(T // 2, T)                    # second half of run
    idx = idx[L[idx] >= 0]
    if len(np.unique(L[idx])) < 2: return np.nan
    cut = int(len(idx) * 0.7); tr_i, te_i = idx[:cut], idx[cut:]
    if len(np.unique(L[tr_i])) < 2 or len(np.unique(L[te_i])) < 2: return np.nan
    clf = LogisticRegression(max_iter=2000, class_weight="balanced").fit(A[tr_i], L[tr_i])
    return balanced_accuracy_score(L[te_i], clf.predict(A[te_i]))

def seed_run(seed, T, nonlin):
    rng = np.random.default_rng(seed)
    cmd_real = babble(rng, T)
    S = body(cmd_real, np.random.default_rng(seed + 100), T)   # yoked gets identical stream
    cmd_yoked = babble(np.random.default_rng(seed + 999), T)
    W0 = np.random.default_rng(seed + 7).normal(0, 0.5, (16, 4))
    out = {}
    for name, cmd in [("real", cmd_real), ("yoked", cmd_yoked)]:
        L = labels(S, cmd)
        for p in [True, False]:
            out[(name, p)] = decode(run_agent(S, cmd, W0, p, nonlin), L)
    did = (out[("real", True)] - out[("real", False)]) - (out[("yoked", True)] - out[("yoked", False)])
    return out, did

if __name__ == "__main__":
    import sys
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    for nonlin in [False, True]:
        print("=== population:", "NONLINEAR (relu)" if nonlin else "LINEAR")
        dids = []
        for s in range(5):
            out, did = seed_run(s, T, nonlin)
            dids.append(did)
            print(f"seed {s}: real plastic {out[('real',True)]:.3f} frozen {out[('real',False)]:.3f} | "
                  f"yoked plastic {out[('yoked',True)]:.3f} frozen {out[('yoked',False)]:.3f} | DiD {did:+.3f}")
        print(f"mean DiD {np.nanmean(dids):+.3f}  positive in {np.sum(np.array(dids)>0)}/5\n")
