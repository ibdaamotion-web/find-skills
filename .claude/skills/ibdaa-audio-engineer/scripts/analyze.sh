#!/usr/bin/env bash
# Usage: analyze.sh <audio-or-video> [spectrogram.png]
# Prints format, loudness (LUFS/LRA/true peak), RMS/peak/noise floor, clipping; writes a spectrogram.
set -euo pipefail
in="$1"; spec="${2:-${in%.*}_spectrum.png}"
echo "== Format"; ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels,duration -of default=nw=1 "$in"
echo "== Loudness (EBU R128)"
ffmpeg -hide_banner -nostats -i "$in" -map a:0 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|LRA:|Peak:)" | sed 's/^ */  /'
echo "== Levels"
ffmpeg -hide_banner -nostats -i "$in" -map a:0 -af astats=metadata=0:measure_perchannel=none -f null - 2>&1 \
  | grep -E "(RMS level|Peak level|Noise floor|Number of samples clipped) dB|clipped" | sed 's/.*\] /  /' | head -6
ffmpeg -hide_banner -loglevel error -y -i "$in" -lavfi showspectrumpic=s=1400x500:legend=1 "$spec"
echo "== Spectrogram: $spec"
