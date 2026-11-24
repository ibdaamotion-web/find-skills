#!/usr/bin/env bash
# Usage: loudnorm2.sh <in> <out.wav> <target_LUFS> <pre-filter-chain|anull>
# Two-pass EBU R128 loudness normalization to target, true peak -1 dBTP, 48 kHz 24-bit WAV.
set -euo pipefail
in="$1"; out="$2"; I="$3"; pre="$4"
j=$(ffmpeg -hide_banner -nostats -i "$in" -map a:0 -af "${pre},loudnorm=I=${I}:TP=-1:LRA=9:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$j" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -hide_banner -loglevel error -y -i "$in" -map a:0 -af "${pre},loudnorm=I=${I}:TP=-1:LRA=9:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a pcm_s24le "$out"
echo "Saved $out (target ${I} LUFS, -1 dBTP)"
