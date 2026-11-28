# procedural SFX: indoor rain on window (stereo loop) + candle blow-out
import numpy as np, wave, sys
sr=48000; rng=np.random.default_rng(11)
def lp(x,fc):  # one-pole lowpass via FFT for speed
    X=np.fft.rfft(x,axis=0); f=np.fft.rfftfreq(len(x),1/sr); H=1/np.sqrt(1+(f/fc)**4)
    return np.fft.irfft(X*(H[:,None] if x.ndim>1 else H),n=len(x),axis=0)
def bp(x,lo,hi):
    X=np.fft.rfft(x,axis=0); f=np.fft.rfftfreq(len(x),1/sr); H=((f>lo)&(f<hi)).astype(float)
    H=np.convolve(H,np.hanning(301)/np.hanning(301).sum(),'same')
    return np.fft.irfft(X*(H[:,None] if x.ndim>1 else H),n=len(x),axis=0)
def save(p,x):
    x=x/np.abs(x).max()*0.7; x=(x*32767).astype(np.int16)
    w=wave.open(p,'wb'); w.setnchannels(x.shape[1] if x.ndim>1 else 1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x.tobytes()); w.close()
# --- rain 40s
T=40; n=sr*T; t=np.arange(n)/sr
bed=lp(rng.standard_normal((n,2)).cumsum(0)*0.02 + rng.standard_normal((n,2)),3500)  # soft hiss
bed=bp(bed,120,9000)
bed*= (1+0.15*np.sin(2*np.pi*t*0.07)[:,None]+0.08*np.sin(2*np.pi*t*0.23+1)[:,None])
drops=np.zeros((n,2))
for _ in range(T*55):
    i=rng.integers(0,n-3000); c=rng.integers(0,2); L=rng.integers(400,2500)
    env=np.exp(-np.arange(L)/(L/6)); fq=rng.uniform(1800,5500)
    d=np.sin(2*np.pi*fq*np.arange(L)/sr*(1-0.3*np.arange(L)/L))*env*rng.uniform(0.05,0.35)
    drops[i:i+L,c]+=d; drops[i:i+L,1-c]+=d*0.35
rain=bed/np.abs(bed).max()*0.8 + drops*0.6
fade=int(sr*2); rain[:fade]*=np.linspace(0,1,fade)[:,None]; rain[-fade:]*=np.linspace(1,0,fade)[:,None]
save(sys.argv[1]+'/rain.wav',rain)
# --- candle blow-out 2.2s
n=int(sr*2.2); tt=np.arange(n)/sr
breath=bp(rng.standard_normal(n),250,2600)
env=np.clip(tt/0.06,0,1)*np.exp(-np.clip(tt-0.06,0,None)/0.28)
fwip=lp(rng.standard_normal(n),700)*np.exp(-np.clip(tt-0.18,0,None)/0.12)*(tt>0.15)
hiss=bp(rng.standard_normal(n),3000,8000)*np.exp(-np.clip(tt-0.2,0,None)/0.5)*(tt>0.2)*0.05
c=breath*env+fwip*0.8+hiss
c=np.stack([c,c*0.9],1); save(sys.argv[1]+'/candle.wav',c)
print('ok')
