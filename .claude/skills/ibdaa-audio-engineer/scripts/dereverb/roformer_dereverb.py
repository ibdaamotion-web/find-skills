import sys,yaml,numpy as np,soundfile as sf,librosa,torch,warnings; warnings.filterwarnings('ignore')
# Mel-Band RoFormer de-reverb (anvuew mono model, SDR 20.4). Runs on CPU (~8 min per minute of audio, 4 cores).
# Usage: python3 roformer_dereverb.py WORKDIR WORKDIR/models/dereverb_mel_band_roformer_anvuew.yaml WORKDIR/models/dereverb_mel_band_roformer_mono_anvuew_sdr_20.4029.ckpt in.wav dry.wav
sys.path.insert(0,sys.argv[1]+'/lib')
from roformer.mel_band_roformer import MelBandRoformer
P,cfgf,ckf,inp,out=sys.argv[1:6]  # WORKDIR, config.yaml, model.ckpt, input, output.wav
class L(yaml.SafeLoader): pass
L.add_constructor('tag:yaml.org,2002:python/tuple',lambda l,n:tuple(l.construct_sequence(n)))
cfg=yaml.load(open(cfgf),Loader=L)
m=dict(cfg['model']); m.pop('multi_stft_resolution_loss_weight',None); m.pop('multi_stft_resolutions_window_sizes',None); m.pop('multi_stft_hop_size',None); m.pop('multi_stft_normalized',None)
m['flash_attn']=False
sd=torch.load(ckf,map_location='cpu',weights_only=False); sd=sd.get('state_dict',sd)
ok=False
for st in [True,False]:
    m['stereo']=st
    try:
        net=MelBandRoformer(**m); net.load_state_dict(sd,strict=True); ok=True; print('loaded stereo=',st); break
    except Exception as e: print('stereo',st,'fail',str(e)[:160])
assert ok
net.eval(); torch.set_num_threads(4)
y,sr=sf.read(inp,always_2d=True); x=librosa.resample(y[:,0],orig_sr=sr,target_sr=44100)
mix=np.stack([x,x]) if m['stereo'] else x[None]
C=cfg['audio']['chunk_size']; step=C//2; n=mix.shape[1]
pad=C; mp=np.pad(mix,((0,0),(pad,pad+C)),mode='constant')
outa=np.zeros_like(mp); wsum=np.zeros(mp.shape[1]); win=np.hanning(C)+1e-3
with torch.no_grad():
    for i in range(0,mp.shape[1]-C+1,step):
        seg=torch.tensor(mp[:,i:i+C][None],dtype=torch.float32)
        o=net(seg)[0].numpy()
        if o.ndim==3: o=o[0]
        outa[:,i:i+C]+=o*win; wsum[i:i+C]+=win
        print(f"{i/44100:.0f}s",end=' ',flush=True)
o=(outa/wsum)[:,pad:pad+n].mean(0)
o=librosa.resample(o,orig_sr=44100,target_sr=48000)
sf.write(out,o,48000,subtype='FLOAT'); print('\ndone')
