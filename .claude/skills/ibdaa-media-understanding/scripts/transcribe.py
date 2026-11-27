#!/usr/bin/env python3
"""Transcribe audio/video locally with faster-whisper (free, offline after first model download).
Usage: python3 -I transcribe.py <media> [--model large-v3-turbo|small|medium] [--lang ar] [--out DIR]
Writes <name>.txt (plain), <name>.srt (subtitles), <name>.timed.txt ([start-end] text)."""
import argparse, os, subprocess, time
import numpy as np
from faster_whisper import WhisperModel

p = argparse.ArgumentParser()
p.add_argument("media"); p.add_argument("--model", default="large-v3-turbo")
p.add_argument("--lang", default="ar"); p.add_argument("--out", default=None)
a = p.parse_args()
# Decode with FFmpeg (avoids PyAV version issues), 16 kHz mono float32.
raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", a.media, "-vn", "-ac", "1",
                      "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(raw, np.float32)
t0 = time.time()
model = WhisperModel(a.model, device="cpu", compute_type="int8")
segs, info = model.transcribe(audio, language=a.lang or None, vad_filter=True, beam_size=5,
                              condition_on_previous_text=False)
segs = list(segs)

def ts(s):
    h, r = divmod(s, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"

out = a.out or os.path.dirname(os.path.abspath(a.media))
base = os.path.join(out, os.path.splitext(os.path.basename(a.media))[0])
with open(base + ".txt", "w", encoding="utf-8") as f:
    f.write("\n".join(s.text.strip() for s in segs) + "\n")
with open(base + ".timed.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(f"[{s.start:.1f}-{s.end:.1f}] {s.text.strip()}" for s in segs) + "\n")
with open(base + ".srt", "w", encoding="utf-8") as f:
    for i, s in enumerate(segs, 1):
        f.write(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n\n")
print(f"{len(segs)} segments, {len(audio)/16000:.0f}s audio in {time.time()-t0:.0f}s -> {base}.txt/.srt/.timed.txt")
