#!/bin/bash
# v4 (client taste): voice upfront, clearly audible nasheed echo (bright plate + L/R ping-pong delay), light ducking only
IN=$1; OUT=$2
VOX="adeclip=w=55:o=75:a=8:t=10,highpass=f=85:p=2,afftdn=nf=-55:nr=8:tn=1,\
equalizer=f=280:t=q:w=1.3:g=-2.5,equalizer=f=480:t=q:w=1.4:g=-2.5,equalizer=f=715:t=q:w=4:g=-1.5,equalizer=f=1119:t=q:w=4:g=-1.5,\
equalizer=f=140:t=q:w=1:g=1.5,equalizer=f=3800:t=q:w=1:g=3,highshelf=f=8000:g=3,deesser=i=0.45:f=0.5,\
acompressor=threshold=-24dB:ratio=3.5:attack=8:release=150:makeup=3:knee=6,alimiter=limit=0.9:level=disabled"
ffmpeg -v error -y -i "$IN" -i plate_ir.wav -filter_complex "\
[0:a]$VOX,asplit=4[d][k1][k2][s];\
[d]aformat=channel_layouts=stereo[dry];\
[s]aformat=channel_layouts=stereo,asplit[sr][sd];\
[sr]highpass=f=250,lowpass=f=9000[ri];[ri][1:a]afir=dry=0:wet=1:irgain=-8dB[rv0];[k1]aformat=channel_layouts=stereo[kk1];[rv0][kk1]sidechaincompress=threshold=0.08:ratio=2:attack=30:release=500[rev];\
[sd]highpass=f=400,lowpass=f=5500,channelsplit[dl][dr];[dl]aecho=0.9:0.8:345|1035:0.5|0.22[el];[dr]aecho=0.9:0.8:690|1380:0.38|0.16[er];[el][er]join=inputs=2:channel_layout=stereo,volume=0.8[dl0];\
[k2]aformat=channel_layouts=stereo[kk2];[dl0][kk2]sidechaincompress=threshold=0.06:ratio=2.5:attack=20:release=400[dly];\
[dry][rev][dly]amix=inputs=3:weights=1 0.42 0.30:normalize=0" -c:a pcm_s24le -ar 48000 pre4.wav
L=$(ffmpeg -hide_banner -i pre4.wav -af loudnorm=I=-12:TP=-1:LRA=9:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
g(){ echo "$L" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i pre4.wav -af "loudnorm=I=-12:TP=-1:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 -c:a pcm_s24le "$OUT"
