#!/bin/bash
# voice (delayed PRE) + rain bed + Eb humming drone (both auto-level + sidechain duck) + candle at transition
DUR=212.11; CANDLE=109.6
ffmpeg -v error -y -i mastered_v2.wav -stream_loop -1 -i sfx/rain_n.wav -i sfx/candle.wav -stream_loop -1 -i sfx/hum_pad.wav -filter_complex "\
[0:a]adelay=2500|2500,apad,atrim=0:$DUR,asplit=3[vox][k1][k2];\
[1:a]atrim=0:$DUR,volume='if(lt(t,2.0),0.85,if(lt(t,3.5),0.85-(t-2.0)/1.5*0.6,if(lt(t,$CANDLE),0.25,if(lt(t,$CANDLE+2),0.25-(t-$CANDLE)/2*0.1,if(lt(t,$DUR-5),0.15,0.15+(t-($DUR-5))/3*0.3)))))':eval=frame,afade=t=in:d=1.2,afade=t=out:st=210.61:d=1.5[rain];\
[3:a]atrim=0:$DUR,volume='if(lt(t,2.5),0.55,if(lt(t,4),0.55-(t-2.5)/1.5*0.25,if(lt(t,$CANDLE),0.30,if(lt(t,$DUR-5),0.38,0.38+(t-($DUR-5))/3*0.35))))':eval=frame,afade=t=in:d=2,afade=t=out:st=209.6:d=2.5[hum];\
[rain][k1]sidechaincompress=threshold=0.05:ratio=3:attack=40:release=600[rd];\
[hum][k2]sidechaincompress=threshold=0.06:ratio=2.5:attack=60:release=900[hd];\
[2:a]volume=0.35,adelay=${CANDLE}s:all=1[cd];\
[vox][rd][hd][cd]amix=inputs=4:normalize=0:duration=first,alimiter=limit=0.84:level=disabled" -c:a pcm_s24le final_mix.wav
