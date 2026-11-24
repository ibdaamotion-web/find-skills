# FFmpeg audio recipes

All examples: input `in.wav`, output `out.wav`. Add `-ar 48000` to keep video sample rate.
Video + audio: copy video, process audio → `ffmpeg -i in.mp4 -af "<chain>" -c:v copy -c:a aac -b:a 256k out.mp4`.

## Analysis
```bash
ffmpeg -hide_banner -i in.wav -af ebur128=peak=true -f null - 2>&1 | tail -12      # LUFS, LRA, true peak
ffmpeg -hide_banner -i in.wav -af astats=metadata=0 -f null - 2>&1 | grep -E "RMS level|Peak level|Noise floor|Number of samples clipped" | head
ffmpeg -i in.wav -lavfi showspectrumpic=s=1600x600:legend=1 spec.png             # spectrogram to inspect
ffmpeg -i in.wav -af silencedetect=noise=-45dB:d=0.4 -f null - 2>&1 | grep silence_ # find gaps
```

## Cleanup
| Goal | Filter |
|---|---|
| Rumble | `highpass=f=90` |
| Hiss / broadband noise | `afftdn=nr=10:nf=-50` (raise nr to 15–20 only if needed) |
| Noise (alternative, smoother) | `anlmdn=s=0.0005` |
| 50 Hz hum + harmonics | `equalizer=f=50:t=q:w=8:g=-30,equalizer=f=100:t=q:w=8:g=-20,equalizer=f=150:t=q:w=8:g=-15` |
| Clicks / mouth noise | `adeclick` |
| Breaths/noise between phrases | `agate=threshold=0.02:ratio=3:attack=5:release=150` |
| Remove long silences | `silenceremove=stop_periods=-1:stop_duration=0.6:stop_threshold=-45dB` |

## Voice chain (default; scripts/voice_chain.sh)
```
highpass=f=90,
afftdn=nr=8:nf=-55,                                   # skip for ElevenLabs
equalizer=f=250:t=q:w=1.2:g=-2.5,                     # mud
deesser=i=0.4:m=0.5:f=0.5,                            # sibilance (raise i for more)
acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,
equalizer=f=3500:t=q:w=1:g=2,                         # presence
equalizer=f=11000:t=h:w=0.7:g=1.5                     # air (high shelf)
```
Then loudness (below).

## Loudness (two-pass, accurate)
```bash
# pass 1: measure
ffmpeg -hide_banner -i in.wav -af loudnorm=I=-14:TP=-1:LRA=9:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p'
# pass 2: apply with measured values
ffmpeg -i in.wav -af loudnorm=I=-14:TP=-1:LRA=9:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true -ar 48000 out.wav
```
`scripts/mix.sh` and `scripts/voice_chain.sh` do both passes automatically.
Final safety limiter if needed: `alimiter=limit=0.89:level=false` (≈ −1 dBFS sample peak).

## Mixing
```bash
# VO + music with automatic ducking (music dips under the voice)
ffmpeg -i vo.wav -i music.wav -filter_complex \
"[1:a]volume=-6dB,aformat=channel_layouts=stereo[m];\
 [0:a]aformat=channel_layouts=stereo,asplit=2[v][sc];\
 [m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400:makeup=1[md];\
 [v][md]amix=inputs=2:duration=first:normalize=0[mix]" -map "[mix]" mix.wav

# place an SFX at 3.20 s
ffmpeg -i mix.wav -i whoosh.wav -filter_complex \
"[1:a]adelay=3200|3200,volume=-4dB[s];[0:a][s]amix=inputs=2:duration=first:normalize=0" out.wav

# fade music in/out (2 s in, 3 s out on a 30 s piece)
-af "afade=t=in:d=2,afade=t=out:st=27:d=3"

# carve 3 kHz out of the music so the voice sits on top
-af "equalizer=f=3000:t=q:w=1:g=-3"
```

## Creative effects
| Effect | Filter |
|---|---|
| Small room | `aecho=0.8:0.6:25|45:0.25|0.15` |
| Hall-ish / dreamy | `aecho=0.8:0.7:60|120|180:0.35|0.25|0.15` |
| Real reverb (impulse response WAV) | `-i ir.wav -filter_complex "[0][1]afir=dry=8:wet=3"` (free IRs: OpenAIR library, check license) |
| Echo on one word (t=4.1–4.8 s) | split, trim the word, `aecho=0.8:0.5:300|600:0.4|0.2`, `adelay`, mix back |
| Radio / phone | `highpass=f=300,lowpass=f=3400,acompressor=ratio=6,volume=3dB` (+ `asubboost` off) |
| Megaphone | `highpass=f=500,lowpass=f=3000,aexciter=amount=3,acompressor=ratio=8` |
| Robot | `flanger=delay=2:depth=4:regen=60:speed=0.5,aphaser` |
| Deeper voice (keep speed) | `rubberband=pitch=0.85` |
| Chipmunk / monster | `asetrate=48000*1.3,aresample=48000` / `asetrate=48000*0.75,aresample=48000` |
| Speed without pitch change | `atempo=1.1` (0.5–2.0 per instance) or `rubberband=tempo=1.1` |
| Tremolo / vibrato | `tremolo=f=6:d=0.5` / `vibrato=f=5:d=0.3` |
| Wider music | `extrastereo=m=1.5` or `stereotools=mlev=1:slev=1.3` (check mono!) |
| Warmth / saturation | `aexciter=amount=2:drive=4` (subtle) |
| Mono check | `pan=mono|c0=0.5*c0+0.5*c1` then listen/measure for phase loss |

## Delivery
```bash
# into the video, keep picture untouched
ffmpeg -i video.mp4 -i final_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -shortest out.mp4
# stems for an editor
ffmpeg -i vo_processed.wav -c:a pcm_s24le -ar 48000 stems/VO.wav
```
