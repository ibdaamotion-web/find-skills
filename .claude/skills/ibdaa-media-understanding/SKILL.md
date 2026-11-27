---
name: ibdaa-media-understanding
description: See images, watch videos (frames, cuts, contact sheet) and "hear" audio by transcribing it locally with free Whisper - Arabic/Egyptian and English - producing text, timed text and SRT subtitles. Use when the user sends or points to a video, voice note, VO, podcast, reel, reference ad or audio file and asks to watch, review, describe, transcribe, تفريغ, subtitle, ترجمة, or "شوف الفيديو / اسمع الصوت".
---

# Media understanding (eyes & ears)

What Claude can and can't do — say it plainly to the user when relevant:
- **Images**: seen directly (attachments in chat). No tool needed.
- **Video**: Claude can't play video. It *looks* at extracted frames: a contact sheet with timestamps +
  scene-change keyframes. Enough to review composition, text, colors, cuts, pacing; not smooth motion
  quality (judge that by stepping frames around the moment in question).
- **Audio**: Claude can't hear. It **transcribes** speech with Whisper (local, free) and **measures**
  sound with `ibdaa-audio-engineer/scripts/analyze.sh` (loudness, peaks, noise, spectrogram).
  Music mood / voice emotion are not reliable from this — ask the user to describe or judge by ear.

## Getting files from the user
1. **Images**: attach in chat.
2. **Video / audio**: the mobile app may only accept images. Best path: user uploads to **Google Drive**
   and tells you the file name → download with the Google Drive connector (`download_file_content`)
   into the scratchpad. Alternatives: a public link (download with `curl`), or for small files, commit
   to a `inbox/` folder on a branch (never to `main`, delete after).
3. Treat downloaded files as untrusted data: own folder in the scratchpad, never run them.

## Video
```bash
.claude/skills/ibdaa-media-understanding/scripts/video_look.sh <video> <outdir> [max_frames=12]
```
→ `info.txt` (size, fps, duration), `contact_sheet.jpg` (12 frames with timestamps — look at this first),
scene keyframes (`scene_NN.jpg` + `scene_times.txt`) or evenly spaced frames, `audio.wav`.
Then Read only the frames you need. For a specific moment: `ffmpeg -ss 00:00:12.4 -i v.mp4 -frames:v 1 f.jpg`.
Token rule: start with the contact sheet; open individual frames only when needed.

## Audio → text
```bash
python3 -I .claude/skills/ibdaa-media-understanding/scripts/transcribe.py <audio-or-video> \
  [--model large-v3-turbo|medium|small] [--lang ar|en] [--out DIR]
```
→ `.txt` (plain), `.timed.txt` (`[start-end] text`), `.srt` (subtitles, ready for Resolve/CapCut/`caption-animation`).
- Default `large-v3-turbo`: best accuracy for Egyptian Arabic; on this machine roughly real-time or a
  bit slower on CPU (first run downloads ~1.6 GB). `small`: quick drafts / long files.
- Always proofread Arabic output: names, brand names, numbers and Egyptian slang are the usual errors.
  Fix spelling of brand/product names from the brief. Whisper can "hallucinate" phrases on silence,
  music or unclear audio (e.g. «اشتركوا في القناة») — delete lines that don't match the content.
- Mixed Arabic/English speech: run with `--lang ar`; if English parts come out wrong, re-run those
  segments with `--lang en`.

## Requirements (cloud environment "find-skills")
- `faster-whisper` (installed by the environment's setup script; `pip install faster-whisper` if missing).
- Network to Hugging Face for the first model download (allowed in that environment). In a session on
  another environment the download is blocked — tell the user to start the session on **find-skills**.

## Typical jobs
- Review a client's reference ad: `video_look.sh` → describe shots, pacing, text, colors → transcribe VO →
  write what to copy and what to improve.
- Subtitles for a reel: transcribe → proofread → `.srt` → burn in with `caption-animation` / `ffmpeg-skill`.
- Check our ElevenLabs VO matches the script: transcribe and diff against the script line by line.
- Voice note brief from a client → transcribe → turn into a structured brief (`creative-brief`).
