import numpy as np, pilot as p
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
DT=1/60
def body2(drive, rng, T, wall=1.0):
    ang=om=0.0; S=np.zeros((T,3))
    for t in range(T):
        om += 0.3*(drive[t]-om); ang += om*DT; c=0.0
        if abs(ang)>wall: c=abs(om)*5; ang=np.sign(ang)*wall; om=0.0
        S[t]=[ang,om,c]
    return S+rng.normal(0,0.01,S.shape)
def dec(X,L):
    T=len(L); idx=np.arange(T//2,T); idx=idx[L[idx]>=0]; cut=int(len(idx)*.7)
    clf=LogisticRegression(max_iter=2000,class_weight='balanced').fit(X[idx[:cut]],L[idx[:cut]])
    return balanced_accuracy_score(L[idx[cut:]],clf.predict(X[idx[cut:]]))
T=30000; res=[]
for s in range(5):
    cmd=p.babble(np.random.default_rng(s),T)
    push=p.babble(np.random.default_rng(s+50),T)   # external mover: same profile as motor
    S=body2(cmd+push,np.random.default_rng(s+100),T)
    cy=p.babble(np.random.default_rng(s+999),T)
    L=np.full(T,-1); L[(cmd!=0)&(push==0)]=1; L[(cmd==0)&(push!=0)]=0   # ground truth: who moved the arm
    W0=np.random.default_rng(s+7).normal(0,.5,(16,4))
    r={'sens only':dec(S,L)}
    for nm,c in [('real',cmd),('yoked',cy)]:
        for nl in [False,True]:
            for pl in [False,True]:
                r[f"{nm} {'relu' if nl else 'lin'} {'plastic' if pl else 'frozen'}"]=dec(p.run_agent(S,c,W0,pl,nl),L)
    res.append(r)
for k in res[0]:
    v=np.array([r[k] for r in res]); print(f"{k:24s} mean {v.mean():.3f}  min {v.min():.3f} max {v.max():.3f}")
