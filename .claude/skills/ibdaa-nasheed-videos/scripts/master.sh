#!/bin/bash
# usage: master.sh in.wav out.wav
IN=$1; OUT=$2
VOX="adeclip=w=55:o=75:a=8:t=10,highpass=f=80:p=2,afftdn=nf=-55:nr=8:tn=1,\
equalizer=f=140:t=q:w=1:g=1.5,equalizer=f=280:t=q:w=1.3:g=-3,equalizer=f=650:t=q:w=1.5:g=-1,\
equalizer=f=3200:t=q:w=1.2:g=2.5,highshelf=f=9500:g=2.5,deesser=i=0.35:f=0.55,\
acompressor=threshold=-22dB:ratio=2.8:attack=12:release=180:makeup=2:knee=6,alimiter=limit=0.9:level=disabled"
ffmpeg -v error -y -i "$IN" -i mosque_ir.wav -filter_complex "\
[0:a]$VOX,aformat=channel_layouts=stereo,asplit=3[dry][rv][dl];\
[rv]highpass=f=250,lowpass=f=7000[rvin];[rvin][1:a]afir=dry=0:wet=1:irgain=-10dB[rev];\
[dl]highpass=f=400,lowpass=f=5000,aecho=0.8:0.7:330|480:0.22|0.14,volume=0.6[dly];\
[dry][rev][dly]amix=inputs=3:weights=1 0.32 0.12:normalize=0[mix]" -map "[mix]" -c:a pcm_s24le -ar 48000 pre.wav
L=$(ffmpeg -hide_banner -i pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
g(){ echo "$L" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 -c:a pcm_s24le "$OUT"
