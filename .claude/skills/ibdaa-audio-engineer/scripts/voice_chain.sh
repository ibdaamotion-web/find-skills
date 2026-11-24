#!/usr/bin/env bash
# Usage: voice_chain.sh <in> <out.wav> [target_LUFS=-16] [--clean]
# Default broadcast-style voice chain + two-pass loudness. --clean skips noise reduction (ElevenLabs/clean studio VO).
set -euo pipefail
in="$1"; out="$2"; target="${3:--16}"; clean="${4:-}"
nr="afftdn=nr=8:nf=-55,"; [[ "$clean" == "--clean" ]] && nr=""
chain="highpass=f=90,${nr}equalizer=f=250:t=q:w=1.2:g=-2.5,deesser=i=0.4:m=0.5:f=0.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,equalizer=f=3500:t=q:w=1:g=2,equalizer=f=11000:t=h:w=0.7:g=1.5"
"$(dirname "$0")/loudnorm2.sh" "$in" "$out" "$target" "$chain"
