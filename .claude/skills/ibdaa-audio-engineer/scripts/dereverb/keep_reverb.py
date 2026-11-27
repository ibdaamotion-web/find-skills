# Partial de-reverb: keep a fraction of the ORIGINAL room echo (natural "روح", no artificial reverb).
# out = dry + KEEP * (original - dry). KEEP 0 = fully dry, 0.5 = half the echo, 1 = original.
# Usage: python3 keep_reverb.py original.wav dry.wav KEEP out.wav   (both mono, same rate & start)
import sys,numpy as np,soundfile as sf
from scipy.signal import correlate
o,sr=sf.read(sys.argv[1]); d,sr2=sf.read(sys.argv[2]); keep=float(sys.argv[3]); assert sr==sr2
o=o if o.ndim==1 else o[:,0]; d=d if d.ndim==1 else d.mean(1); n=min(len(o),len(d)); o,d=o[:n],d[:n]
s=min(n-1,10*sr); a,b=o[s:s+5*sr],d[s:s+5*sr]; lag=int(np.argmax(correlate(a,b,'full',method='fft'))-(len(b)-1))
d=np.roll(d,lag)
sf.write(sys.argv[4],d+keep*(o-d),sr,subtype='FLOAT'); print('lag',lag,'keep',keep)
