# sad SFX bus: smooth wind bed, heartbeats on heart lines, reverse-reverb swells of the singer's own voice
# before chorus lines, soft deep swells on key lines. Output aligned to the reel timeline.
import numpy as np, wave, json, sys
P=sys.argv[1]; PRE=2.5; OFF2=108.0; DUR=212.11; sr=48000; rng=np.random.default_rng(9)
n=int(DUR*sr); bus=np.zeros((n,2))
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,w.getnchannels()).astype(float)/32768; w.close(); return x
def filt(x,lo=None,hi=None):
    F=np.fft.rfft(x,axis=0); f=np.fft.rfftfreq(len(x),1/sr); H=np.ones_like(f)
    if hi: H/=np.sqrt(1+(f/hi)**4)
    if lo: H/=np.sqrt(1+(lo/np.maximum(f,1))**4)
    return np.fft.irfft(F*H[:,None],n=len(x),axis=0)
def put(x,t,g):
    i=int(t*sr); j=min(n,i+len(x)); 
    if i<n: bus[i:j]+=x[:j-i]*g
L=json.load(open(P+'/lyrics.json'))
T1=lambda s:s+PRE; T2=lambda s:s+PRE+OFF2
# 1) wind bed: brown-ish noise, band 150-1200Hz, slow gusts (no clicks)
w=np.cumsum(rng.standard_normal((n,2)),0); w-=np.convolve(w[:,0],np.ones(4801)/4801,'same')[:,None]
w=filt(w,150,1200); w/=np.abs(w).max()
tt=np.arange(n)/sr; gust=0.55+0.25*np.sin(2*np.pi*tt*0.05)+0.2*np.sin(2*np.pi*tt*0.13+1.3)
bus+=w*gust[:,None]*0.10
# 2) heartbeat (lub-dub) ~56 bpm
def beat():
    m=int(0.9*sr); t=np.arange(m)/sr; y=np.zeros(m)
    for d,a in [(0,1.0),(0.22,0.7)]:
        k=t>=d; u=t[k]-d; y[k]+=a*np.sin(2*np.pi*(48-18*u)*u)*np.exp(-u/0.07)
    return np.stack([y,y],1)
hb=beat()
heart=[T1(55.5),T1(65.0),T2(7.3),T2(20.2),T2(57.6),T2(87.6)]
for h in heart:
    for k in range(5): put(hb,h-0.3+k*1.07,0.55*(1-0.12*k))
# 3) reverse-reverb swell of his own voice before chorus lines
vw=rd(P+'/sfx/voice_wet.wav')
chor=[s for s,e,t in L['p1'] if t.startswith('كفاية')]+[s+OFF2 for s,e,t in L['p2'] if t.startswith('اعذريني')]
for s in chor:
    a=int(s*sr); seg=vw[a:a+int(1.6*sr)][::-1].copy()
    env=np.linspace(0,1,len(seg))**2; seg*=env[:,None]
    i=int((s+PRE)*sr)-len(seg)
    if i>0: bus[i:i+len(seg)]+=seg*0.9
# 4) soft deep swells (sub + filtered noise rising then fading)
def swell():
    m=int(4*sr); t=np.arange(m)/sr; env=np.minimum(t/1.2,1)*np.exp(-np.maximum(t-1.2,0)/1.0)
    sub=np.sin(2*np.pi*(38+6*np.exp(-t))*t)*env
    nz=filt(rng.standard_normal((m,1)),60,400)[:,0]; nz/=np.abs(nz).max()
    y=sub*0.8+nz*env*0.35; return np.stack([y,y],1)
sw=swell()
for s in [T1(6.7),T1(49.7),T2(93.1)]: put(sw,s-1.2,0.6)
bus=np.clip(bus,-1,1)
o=wave.open(P+'/sfx/sad_bus.wav','wb'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(sr); o.writeframes((bus*32767).astype(np.int16).tobytes()); o.close()
print('heart',len(heart),'swells',len(chor))
