#!/usr/bin/env bash
# Usage: mix.sh <voice.wav> <music> <out.wav> [music_gain_dB=-8] [target_LUFS=-14]
# Mixes VO + music with sidechain ducking, music fade in/out, then two-pass loudness + true-peak ceiling.
set -euo pipefail
vo="$1"; music="$2"; out="$3"; mg="${4:--8}"; target="${5:--14}"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$vo"); fo=$(awk -v d="$dur" 'BEGIN{s=d-2; if(s<0)s=0; print s}')
tmp="$(mktemp --suffix=.wav)"; trap 'rm -f "$tmp"' EXIT
ffmpeg -hide_banner -loglevel error -y -i "$vo" -stream_loop -1 -i "$music" -filter_complex \
"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=${mg}dB,equalizer=f=3000:t=q:w=1:g=-3,afade=t=in:d=1.5,afade=t=out:st=${fo}:d=2[m];\
 [0:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[v][sc];\
 [m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];\
 [v][md]amix=inputs=2:duration=first:normalize=0[mix]" -map "[mix]" -c:a pcm_s24le "$tmp"
"$(dirname "$0")/loudnorm2.sh" "$tmp" "$out" "$target" "anull"
