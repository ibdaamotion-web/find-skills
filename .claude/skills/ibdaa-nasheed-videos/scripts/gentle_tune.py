# gentle, maqam-safe pitch correction: pull only sustained notes that disagree with their local neighbours
import parselmouth, numpy as np, json, sys
from parselmouth.praat import call
IN,OUT,NOTES,REPORT=sys.argv[1:5]; AMT=0.55
N=json.load(open(NOTES))['notes']
m=np.array([x['m'] for x in N]); s=np.array([x['s'] for x in N]); e=np.array([x['e'] for x in N]); w=e-s
fixes=[]
for i in range(len(N)):
    if w[i]<0.25: continue
    k=(abs(s-s[i])<12)&(np.arange(len(N))!=i)&(abs(m-m[i])<120)
    if k.sum()<2: continue
    g=np.arange(m[i]-120,m[i]+121,1.0)
    kde=sum(wj*np.exp(-0.5*((g-mj)/15)**2) for mj,wj in zip(m[k],w[k]))
    pk=[j for j in range(1,len(g)-1) if kde[j]>kde[j-1] and kde[j]>=kde[j+1] and kde[j]>0.6]
    if not pk: continue
    t=g[min(pk,key=lambda j:abs(g[j]-m[i]))]; dev=m[i]-t
    if 30<=abs(dev)<=60: fixes.append((float(s[i]),float(e[i]),float(dev)))
snd=parselmouth.Sound(IN); sr=snd.sampling_frequency
man=call(snd,"To Manipulation",0.01,70,700); tier=call(man,"Extract pitch tier")
pitch=snd.to_pitch_ac(time_step=0.005,pitch_floor=70,pitch_ceiling=700)
newtier=call("Create PitchTier","t",snd.xmin,snd.xmax)
ts=pitch.xs(); f=pitch.selected_array['frequency']
for tt,ff in zip(ts,f):
    if ff<=0: continue
    r=1.0
    for a,b,dev in fixes:
        if a-0.04<=tt<=b+0.04:
            ramp=min(1,(tt-(a-0.04))/0.06,((b+0.04)-tt)/0.06)
            r=2**(-AMT*dev*ramp/1200)
    call(newtier,"Add point",tt,ff*r)
call([newtier,man],"Replace pitch tier")
res=call(man,"Get resynthesis (overlap-add)")
x=snd.values[0].copy(); y=res.values[0]
xf=int(0.03*sr)
for a,b,dev in fixes:   # splice only corrected regions, 30 ms crossfades
    i0=max(0,int((a-0.06)*sr)); i1=min(len(x),int((b+0.06)*sr))
    seg=y[i0:i1].copy(); fade=np.linspace(0,1,xf)
    seg[:xf]=x[i0:i0+xf]*(1-fade)+seg[:xf]*fade; seg[-xf:]=seg[-xf:]*(1-fade)+x[i1-xf:i1]*fade
    x[i0:i1]=seg
parselmouth.Sound(x,sr).save(OUT,"WAV")
json.dump(fixes,open(REPORT,'w'))
print('notes corrected:',len(fixes),'of',len(N)); print([(round(a,1),round(d)) for a,b,d in fixes])
