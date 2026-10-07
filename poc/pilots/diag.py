import numpy as np, pilot as p
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
DT=1/60
def body(drive,rng,T,wall=1.0):
    ang=om=0.0;S=np.zeros((T,3))
    for t in range(T):
        om+=0.3*(drive[t]-om);ang+=om*DT;c=0.0
        if abs(ang)>wall:c=abs(om)*5;ang=np.sign(ang)*wall;om=0.0
        S[t]=[ang,om,c]
    return S+rng.normal(0,0.01,S.shape)
def run(S,cmd,W0,plastic,N):
    T=len(S);W=W0.copy();mu=np.zeros(4);var=np.ones(4);tr=0.;a=np.zeros(N);R=np.zeros(N+1);sd=1.;A=np.zeros((T,N))
    for t in range(T-1):
        tr=.95*tr+.05*cmd[t];x=np.array([S[t,0],S[t,1],S[t,2],tr])
        mu+=(x-mu)/1000;var+=((x-mu)**2-var)/1000;x=(x-mu)/np.sqrt(var+1e-6)
        y=np.maximum(W@x,0);a=.9*a+.1*y;A[t]=a;z=np.append(a,cmd[t]);e=S[t+1,1]-R@z;R+=1e-3*e*z;sd+=(abs(e)-sd)/1000
        if plastic:W+=2e-3*min(abs(e)/(sd+1e-6),3)*(np.outer(y,x)-np.tril(np.outer(y,y))@W)
    return A,W
def dec(X,L,tr_frac=.7,late=False):
    T=len(L);idx=np.arange(T//2,T);idx=idx[L[idx]>=0];cut=int(len(idx)*tr_frac)
    clf=LogisticRegression(max_iter=2000,class_weight='balanced').fit(X[idx[:cut]],L[idx[:cut]])
    return balanced_accuracy_score(L[idx[cut:]],clf.predict(X[idx[cut:]]))
def dec_shuffled(X,L):  # random split: removes drift between train and test
    T=len(L);idx=np.arange(T//2,T);idx=idx[L[idx]>=0];rng=np.random.default_rng(0);rng.shuffle(idx);cut=int(len(idx)*.7)
    clf=LogisticRegression(max_iter=2000,class_weight='balanced').fit(X[idx[:cut]],L[idx[:cut]])
    return balanced_accuracy_score(L[idx[cut:]],clf.predict(X[idx[cut:]]))
T=30000;rows=[]
for s in range(5):
    cmd=p.babble(np.random.default_rng(s),T);push=p.babble(np.random.default_rng(s+50),T)
    drive=np.where(push!=0,push,cmd)                     # override variant
    S=body(drive,np.random.default_rng(s+100),T)
    L=np.full(T,-1);L[(cmd!=0)&(push==0)]=1;L[push!=0]=0  # external incl. while commanding
    r={}
    for N in [16,4]:
        W0=np.random.default_rng(s+7).normal(0,.5,(N,4))
        Af,_=run(S,cmd,W0,False,N);Ap,Wp=run(S,cmd,W0,True,N)
        r[f'N{N} frozen']=dec(Af,L);r[f'N{N} plastic']=dec(Ap,L)
        r[f'N{N} plastic shuffled-split']=dec_shuffled(Ap,L);r[f'N{N} frozen shuffled-split']=dec_shuffled(Af,L)
        live=(np.linalg.norm(Wp,axis=1)>0.1).sum()
        r[f'N{N} live nodes after learning']=live
        # how much do learned weights load on the trace vs velocity?
        r[f'N{N} |trace wt| share']=np.abs(Wp[:,3]).sum()/np.abs(Wp).sum()
    rows.append(r)
for k in rows[0]:
    v=np.array([r[k] for r in rows],float);print(f'{k:32s} {v.mean():.3f}  ({v.min():.2f}-{v.max():.2f})')

def dec_blocked(X,L,nb=10,gap=200):   # interleaved contiguous blocks with gaps: tracks drift without neighbour leakage
    T=len(L);idx=np.arange(T//2,T);blocks=np.array_split(idx,nb);tr=[];te=[]
    for i,b in enumerate(blocks):
        b=b[gap:] if i else b
        (tr if i%2==0 else te).append(b)
    tr=np.concatenate(tr);te=np.concatenate(te);tr=tr[L[tr]>=0];te=te[L[te]>=0]
    clf=LogisticRegression(max_iter=2000,class_weight='balanced').fit(X[tr],L[tr])
    return balanced_accuracy_score(L[te],clf.predict(X[te]))
print('--- blocked CV (drift-tracking, no neighbour leakage), N16')
out={'frozen':[],'plastic':[]}
for s in range(5):
    cmd=p.babble(np.random.default_rng(s),T);push=p.babble(np.random.default_rng(s+50),T)
    S=body(np.where(push!=0,push,cmd),np.random.default_rng(s+100),T)
    L=np.full(T,-1);L[(cmd!=0)&(push==0)]=1;L[push!=0]=0
    W0=np.random.default_rng(s+7).normal(0,.5,(16,4))
    out['frozen'].append(dec_blocked(run(S,cmd,W0,False,16)[0],L));out['plastic'].append(dec_blocked(run(S,cmd,W0,True,16)[0],L))
for k,v in out.items(): print(k,np.round(v,3),'mean',round(np.mean(v),3))
