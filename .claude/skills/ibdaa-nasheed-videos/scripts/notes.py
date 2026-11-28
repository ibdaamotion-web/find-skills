import parselmouth, numpy as np, sys, json
snd=parselmouth.Sound(sys.argv[1]).convert_to_mono()
p=snd.to_pitch_ac(time_step=0.01, pitch_floor=70, pitch_ceiling=700)
f=p.selected_array['frequency']; t=p.xs()
c=np.where(f>0,1200*np.log2(np.maximum(f,1)/440.0),np.nan)
# note segmentation: runs of voiced frames where |c - running median| < 45 cents
notes=[];i=0;n=len(c)
while i<n:
    if np.isnan(c[i]): i+=1; continue
    j=i; seg=[c[i]]
    while j+1<n and not np.isnan(c[j+1]) and abs(c[j+1]-np.median(seg[-15:]))<45: j+=1; seg.append(c[j])
    if (j-i+1)>=15: # >=150ms
        core=np.array(seg[3:-3]) if len(seg)>10 else np.array(seg)
        notes.append(dict(s=float(t[i]),e=float(t[j]),m=float(np.median(core))))
    i=j+1
med=np.nanmedian(c); notes=[x for x in notes if abs(x['m']-med)<900]
m=np.array([x['m'] for x in notes]); w=np.array([x['e']-x['s'] for x in notes])
# absolute-pitch KDE (not folded) weighted by duration
grid=np.arange(m.min()-100,m.max()+100,1.0)
kde=sum(wi*np.exp(-0.5*((grid-mi)/18)**2) for mi,wi in zip(m,w))
pk=[grid[i] for i in range(1,len(grid)-1) if kde[i]>kde[i-1] and kde[i]>=kde[i+1] and kde[i]>0.08*kde.max()]
pk=sorted(pk,key=lambda g:-kde[int(g-grid[0])]); keep=[]
for g in pk:
    if all(abs(g-k)>=75 for k in keep): keep.append(g)
pk=np.array(sorted(keep))
dev=np.array([mi-pk[np.argmin(abs(pk-mi))] for mi in m])
print('notes',len(m),'scale degrees (cents rel A4):',pk.round(0).tolist())
print('steps between degrees:',np.diff(pk).round(0).tolist())
print('abs dev pct50/80/95:',np.percentile(abs(dev),[50,80,95]).round(1))
bad=[(round(x['s'],2),round(x['e']-x['s'],2),round(d)) for x,d in zip(notes,dev) if abs(d)>25 and x['e']-x['s']>0.3]
print('off notes >25c & >0.3s:',len(bad)); print(bad[:40])
json.dump(dict(scale=pk.tolist(),notes=notes,dev=dev.tolist()),open(sys.argv[2],'w'))
