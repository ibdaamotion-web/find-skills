#!/bin/bash
# v3: brighter/clearer EQ + effects that bloom in gaps (ducked wet) so tails never smear over new notes
IN=$1; OUT=$2
VOX="adeclip=w=55:o=75:a=8:t=10,highpass=f=85:p=2,afftdn=nf=-55:nr=8:tn=1,\
equalizer=f=280:t=q:w=1.3:g=-2.5,equalizer=f=480:t=q:w=1.4:g=-2.5,equalizer=f=715:t=q:w=4:g=-1.5,equalizer=f=1119:t=q:w=4:g=-1.5,\
equalizer=f=140:t=q:w=1:g=1.2,equalizer=f=3800:t=q:w=1:g=3,highshelf=f=8000:g=4,deesser=i=0.4:f=0.5,\
acompressor=threshold=-22dB:ratio=3:attack=10:release=160:makeup=2.2:knee=6,aexciter=amount=1:drive=4:freq=5500:blend=0:ceil=12000,alimiter=limit=0.9:level=disabled"
ffmpeg -v error -y -i "$IN" -i mosque_ir.wav -i hall_ir.wav -filter_complex "\
[0:a]$VOX,aformat=channel_layouts=stereo,asplit=5[dry][k1][k2][s1][s2];\
[s1]highpass=f=300,lowpass=f=7000,asplit[r1][r2];\
[r1][1:a]afir=dry=0:wet=1:irgain=-10dB[room];\
[r2][2:a]afir=dry=0:wet=1:irgain=-10dB[hall0];[hall0][k1]sidechaincompress=threshold=0.03:ratio=6:attack=25:release=380:makeup=1[hall];\
[s2]highpass=f=500,lowpass=f=4200,aecho=0.8:0.6:345|690:0.28|0.16,volume=0.7[dl0];[dl0][k2]sidechaincompress=threshold=0.03:ratio=8:attack=15:release=300[dly];\
[dry][room][hall][dly]amix=inputs=4:weights=1 0.14 0.55 0.22:normalize=0[mix]" -map "[mix]" -c:a pcm_s24le -ar 48000 pre3.wav
L=$(ffmpeg -hide_banner -i pre3.wav -af loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
g(){ echo "$L" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i pre3.wav -af "loudnorm=I=-14:TP=-1.5:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 -c:a pcm_s24le "$OUT"
