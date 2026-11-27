#!/usr/bin/env bash
# Usage: video_look.sh <video> [outdir] [max_frames=12]
# Gives Claude "eyes" on a video: metadata, scene-change keyframes, one contact sheet, and the audio track.
set -euo pipefail
v="$1"; out="${2:-${v%.*}_look}"; n="${3:-12}"; mkdir -p "$out"
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate,sample_rate,channels -of compact=p=0:nk=0 "$v" | tee "$out/info.txt"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
# scene-change frames (fallback to evenly spaced if too few)
ffmpeg -hide_banner -loglevel error -y -i "$v" -vf "select='gt(scene,0.3)',scale=640:-2,showinfo" -vsync vfr -frames:v "$n" "$out/scene_%02d.jpg" 2>"$out/scenes.log" || true
cnt=$(ls "$out"/scene_*.jpg 2>/dev/null | wc -l)
if [ "$cnt" -lt 4 ]; then rm -f "$out"/scene_*.jpg
  ffmpeg -hide_banner -loglevel error -y -i "$v" -vf "fps=$(awk -v d="$dur" -v n="$n" 'BEGIN{printf "%.4f", n/d}'),scale=640:-2" -frames:v "$n" "$out/frame_%02d.jpg"; fi
grep -o "pts_time:[0-9.]*" "$out/scenes.log" 2>/dev/null | cut -d: -f2 > "$out/scene_times.txt" || true
# contact sheet with timestamps (one image to look at first)
ffmpeg -hide_banner -loglevel error -y -i "$v" -vf "fps=$(awk -v d="$dur" 'BEGIN{printf "%.4f", 12/d}'),scale=480:-2,drawtext=text='%{pts\:hms}':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6,tile=4x3:padding=6" -frames:v 1 "$out/contact_sheet.jpg" 2>/dev/null || true
# audio track for transcription / analysis
if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$v" | grep -q .; then
  ffmpeg -hide_banner -loglevel error -y -i "$v" -vn -ac 1 -ar 16000 "$out/audio.wav"; fi
echo "Saved to $out: contact_sheet.jpg, keyframes, audio.wav"
