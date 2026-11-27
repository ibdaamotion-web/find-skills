#!/usr/bin/env bash
# One-time setup for the RoFormer de-reverb (free, open source). Installs PyTorch (~3 GB with deps) on the
# machine it runs on, vendors the Mel-Band RoFormer code from the `audio-separator` wheel, downloads the model.
# Usage: bash setup.sh [WORKDIR]   (default WORKDIR=~/.cache/ibdaa-dereverb)
set -euo pipefail
W="${1:-$HOME/.cache/ibdaa-dereverb}"; mkdir -p "$W/lib/roformer" "$W/models" "$W/whl"
python3 -c "import torch" 2>/dev/null || pip install -q torch
pip install -q einops "rotary-embedding-torch>=0.6.1,<0.7.0" beartype pyyaml librosa soundfile scipy huggingface_hub
if [ ! -f "$W/lib/roformer/mel_band_roformer.py" ]; then
  pip download -q --no-deps -d "$W/whl" audio-separator
  python3 - "$W" <<'PY'
import sys,zipfile,glob,os,re
W=sys.argv[1]; whl=sorted(glob.glob(W+'/whl/audio_separator-*.whl'))[-1]
z=zipfile.ZipFile(whl); pre='audio_separator/separator/uvr_lib_v5/roformer/'
for n in z.namelist():
    if n.startswith(pre) and n.endswith('.py'):
        src=z.read(n).decode().replace('from audio_separator.separator.uvr_lib_v5.device_utils import','from .devstub import')
        open(os.path.join(W,'lib/roformer',os.path.basename(n)),'w').write(src)
open(os.path.join(W,'lib/roformer/__init__.py'),'w').write('')
open(os.path.join(W,'lib/roformer/devstub.py'),'w').write(
 "import contextlib\ndef should_fallback_to_cpu_for_complex_ops(device): return False\n@contextlib.contextmanager\ndef autocast_disabled(*a,**k):\n    yield\n")
PY
fi
python3 - "$W" <<'PY'
import sys; from huggingface_hub import hf_hub_download
for f in ['dereverb_mel_band_roformer_anvuew.yaml','dereverb_mel_band_roformer_mono_anvuew_sdr_20.4029.ckpt']:
    print(hf_hub_download('anvuew/dereverb_mel_band_roformer',f,local_dir=sys.argv[1]+'/models'))
PY
echo "ready: $W"
