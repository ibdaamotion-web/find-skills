#!/bin/bash
# voice v4 (delayed PRE) + steady clear hum drone + candle at transition. No rain (client: noisy).
DUR=212.11; CANDLE=109.6
ffmpeg -v error -y -i mastered_v4.wav -i sfx/candle.wav -i sfx/hum_track_v4.wav -i sfx/sad_bus.wav -filter_complex "\
[0:a]adelay=2500|2500,apad,atrim=0:$DUR,asplit=3[vox][k][k2];\
[2:a]atrim=0:$DUR,volume='if(lt(t,2.5),1.0,if(lt(t,4),1.0-(t-2.5)/1.5*0.35,if(lt(t,$DUR-5),0.65,0.65+(t-($DUR-5))/3*0.35)))':eval=frame,afade=t=in:d=1.5,afade=t=out:st=209.6:d=2.5[hum];\
[hum][k]sidechaincompress=threshold=0.1:ratio=1.8:attack=150:release=1500[hd];\
[1:a]volume=0.45,adelay=${CANDLE}s:all=1[cd];\
[3:a]atrim=0:$DUR,volume=0.85[sb0];[sb0][k2]sidechaincompress=threshold=0.1:ratio=1.5:attack=80:release=800[sb];[vox][hd][cd][sb]amix=inputs=4:normalize=0:duration=first,alimiter=limit=0.89:level=disabled" -c:a pcm_s24le final_mix_v4.wav
