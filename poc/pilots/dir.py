import numpy as np, pilot as p, importlib, sys
sys.argv=['x'];
exec(open('diag.py').read().split("T=30000;rows=[]")[0])
T=30000
sum_d=np.array([0,1,0,1])/np.sqrt(2); diff_d=np.array([0,-1,0,1])/np.sqrt(2)
for s in range(5):
    cmd=p.babble(np.random.default_rng(s),T);push=p.babble(np.random.default_rng(s+50),T)
    S=body(np.where(push!=0,push,cmd),np.random.default_rng(s+100),T)
    W0=np.random.default_rng(s+7).normal(0,.5,(16,4)); _,Wp=run(S,cmd,W0,True,16)
    f=lambda W,d: np.linalg.norm(W@d)/np.linalg.norm(W)
    print(f"seed {s}: frozen  sum {f(W0,sum_d):.2f} diff {f(W0,diff_d):.2f} | plastic sum {f(Wp,sum_d):.2f} diff {f(Wp,diff_d):.2f}")
