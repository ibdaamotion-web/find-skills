import sys,numpy as np,soundfile as sf
# Smooth pause gate (no hard cuts, gentle -32 dB floor) + subtle warm short hall ("روح").
# Usage: python3 polish_recitation.py dry.wav out.wav WET_DB   (WET_DB -20 = barely there, -16 = a bit more)
from scipy.signal import fftconvolve,butter,sosfilt
inp,out=sys.argv[1],sys.argv[2]; wet_db=float(sys.argv[3])
y,sr=sf.read(inp); y=y if y.ndim==1 else y.mean(1)
# clean band (same as before): HP 80, LP 5.4k
y=sosfilt(butter(2,80,'high',fs=sr,output='sos'),y); y=sosfilt(butter(4,5400,'low',fs=sr,output='sos'),y)
# --- smooth pause gate ---
h=int(0.01*sr); n=len(y)//h
e=20*np.log10(np.sqrt((y[:n*h].reshape(n,h)**2).mean(1))+1e-9)
med=np.median(e[e>-60]); thr=med-22
tgt=np.where(e>thr+6,0.0,np.where(e<thr,-32.0,-32.0*(thr+6-e)/6))
g=np.zeros(n); cur=-32.0
for i in range(n):
    a=0.45 if tgt[i]>cur else 0.06   # fast-ish open (~20ms), slow close (~160ms)
    cur+= a*(tgt[i]-cur); g[i]=cur
gs=np.interp(np.arange(len(y)),np.arange(n)*h+h/2,10**(g/20))
d=y*gs
# --- warm short hall IR (RT60 ~1.15s), stereo ---
rng=np.random.default_rng(11); L=int(1.6*sr); t=np.arange(L)/sr; ir=np.zeros((L,2))
for c in range(2):
    nz=rng.standard_normal(L); lo=sosfilt(butter(2,4200,'low',fs=sr,output='sos'),nz)
    tail=lo*np.exp(-6.91*t/1.15)*np.clip(t/0.04,0,1); pre=int(0.018*sr); x=np.zeros(L); x[pre:]=tail[:L-pre]
    for dd,gg in [(0.009,.45),(0.016,.35),(0.023,.28),(0.034,.2)]: x[int((dd+0.003*c)*sr)]+=gg*(1 if rng.random()>.5 else -1)
    ir[:,c]=sosfilt(butter(2,180,'high',fs=sr,output='sos'),x)
wet=np.stack([fftconvolve(d,ir[:,c])[:len(d)] for c in range(2)],1)
k=np.sqrt((d**2).mean()/(wet**2).mean())*10**(wet_db/20); wet*=k
o=np.stack([d,d],1)+wet
sf.write(out,o,sr,subtype='FLOAT')
print('thr',round(thr,1),'wet_db',wet_db)
