---
name: ibdaa-audio-engineer
description: Audio engineering for video work - clean and polish voice-overs (ElevenLabs or recorded), edit audio, mix voice + music + sound effects, add effects (EQ, compression, de-ess, reverb, echo, radio/phone, robot, pitch), loudness for Facebook/Instagram/TikTok/YouTube, and audio QC - all with free FFmpeg. Use for "الصوت", "الفويس", "التعليق الصوتي", "مكس", "مؤثرات صوتية", "الموسيقى عالية", "الصوت واطي", "شوشرة", "صدى", "LUFS", "ماستر", or any audio problem in a video.
---

# Ibdaa Audio Engineer

Think like a mix engineer working on ads and reels: **the voice is king**, music supports it,
SFX punctuate it. Every change is measured before and after — never "by ear" only (Claude can't
listen; it reads meters, stats and spectrograms).

Tools: FFmpeg 6.1+ (installed). Recipes: `references/ffmpeg-audio-recipes.md`.
Theory cheat-sheet: `references/fundamentals.md`. Scripts: `scripts/analyze.sh`,
`scripts/voice_chain.sh` (`--clean` for ElevenLabs), `scripts/mix.sh` (VO + music + ducking), `scripts/loudnorm2.sh` (two-pass loudness). Heavier editing (cut/join/sync video) → `ffmpeg-skill`.
Free GUI tools to suggest to the user: **Audacity**, **DaVinci Resolve Fairlight**, **Ocenaudio**.

## Work loop (always)
1. **Analyze** the input: `scripts/analyze.sh file` → loudness (LUFS), true peak, noise floor,
   clipping, sample rate/channels, and a spectrogram PNG to inspect.
2. **Diagnose** in one line per problem (noise, harsh "s", boomy, thin, too quiet, clipping, music masking voice…).
3. **Process** with the minimum chain that fixes it (order below). Keep the original; write new files with a suffix.
4. **Re-analyze** and compare numbers before/after. Show the user a short before/after table.
5. **Deliver** at the platform target, 48 kHz, AAC 192–320 kbps inside the MP4 (or WAV 24-bit for the editor).
6. Tell the user what to **listen** for (on headphones and on a phone speaker) — final approval is theirs.

## Voice chain order (don't shuffle)
1. Trim / remove long silences
2. High-pass (cut rumble): 70–100 Hz male, 100–120 Hz female
3. Noise reduction (only if noise floor > about −60 dBFS) — gentle; over-doing it sounds watery
4. Corrective EQ (cut mud 200–400 Hz, boxiness 400–800 Hz) — cuts before boosts
5. De-esser (sibilance 5–9 kHz)
6. Compressor (ratio 2:1–4:1, ~3–6 dB gain reduction on peaks)
7. Tone EQ (presence +2–3 dB at 2–5 kHz, air +1–2 dB at 10–12 kHz) — only if needed
8. Creative effects (reverb, echo, radio…) — on purpose, never by default
9. Loudness normalize (two-pass) + true-peak limiter at −1 dBTP

ElevenLabs output is usually clean: skip 3 (noise) and often 4; check sibilance and level.

## Mix levels for ads / reels (starting points, then adjust)
| Element | Level while voice speaks | Notes |
|---|---|---|
| Voice | reference (integrated ≈ −16 to −14 LUFS in the final mix) | always intelligible on a phone speaker |
| Music | voice minus 15–20 dB (ducked) | rise back up in gaps / intro / outro (ducking) |
| SFX (whoosh, hit, pop) | short peaks just under the voice | sync to the cut or motion frame; don't stack on words |
| Ambience | very low, felt not heard | |

## Loudness targets (final export)
| Destination | Integrated | True peak |
|---|---|---|
| Facebook / Instagram / TikTok / Reels | −14 LUFS (−16 if dialogue-only feels loud) | −1 dBTP |
| YouTube | −14 LUFS | −1 dBTP |
| TV / broadcast (Egypt/Arab channels usually follow EBU R128) | −23 LUFS | −1 dBTP |
| Podcast | −16 LUFS (stereo) | −1 dBTP |
Re-check the client's or channel's spec if they give one; theirs wins.

## Effects menu (what each one is for)
- **Reverb** – space (room, hall). Short & low for realism; big for drama/dream. Keep voice mostly dry in ads.
- **Echo/Delay** – repeats; for emphasis on a single word or a "hero" line, not the whole VO.
- **Radio / phone** – band-pass 300–3400 Hz + light distortion: flashbacks, calls, "old ad" feel.
- **Robot / AI voice** – flanger/phaser or ring-mod feel; pitch down for menacing.
- **Pitch / speed** – `rubberband` keeps pitch when changing speed; `asetrate` changes both (chipmunk/monster).
- **Riser / whoosh / impact** – transitions; align the peak exactly on the cut frame.
- **Ducking (sidechain)** – music dips automatically under the voice.
- **Stereo width** – widen music, keep voice centered and mono-compatible.
Recipes for all of these: `references/ffmpeg-audio-recipes.md`.

## Room echo / reverb removal (de-reverb) — tested on Quran recitation
When the voice sounds like it was recorded in an empty room (echo, boxy "وشة", "صوت مايك"), EQ and
gates can't fix it. Use the free Mel-Band RoFormer de-reverb model (anvuew, mono, SDR 20.4, Hugging Face):
1. Setup once (installs PyTorch ~3 GB on the machine it runs on; ask the user first): `bash scripts/dereverb/setup.sh WORKDIR`
2. Pick the cleanest single channel (check L/R correlation — a mono sum of a weird stereo file can sound worse), 48 kHz WAV.
3. Dry voice: `python3 scripts/dereverb/roformer_dereverb.py WORKDIR WORKDIR/models/dereverb_mel_band_roformer_anvuew.yaml WORKDIR/models/dereverb_mel_band_roformer_mono_anvuew_sdr_20.4029.ckpt in.wav dry.wav` (CPU ≈ 8 min per audio minute — test on one minute first).
4. Choose the amount, and send the user 2 short samples to pick from:
   - **Keep part of the original echo** (the most natural "روح"): `scripts/dereverb/keep_reverb.py original.wav dry.wav 0.5 out.wav` (0.35–0.5).
   - **Fully dry + subtle warm hall** with smooth pauses: `scripts/dereverb/polish_recitation.py dry.wav out.wav -20` (−20 barely there, −16 more).
5. Then: gentle denoise (`afftdn`), low-pass at the source's real bandwidth if it's band-limited (removes hiss), light compression ≤1.6:1, two-pass loudnorm −14 LUFS.
What didn't work (don't repeat): UVR `Reverb_HQ_By_FoxJoy.onnx` sounded digital; ElevenLabs Voice Isolator ruined the recitation; notching "room peaks" in recitation cuts the reciter's own harmonics.

**Quran recitation rules:** never auto-tune or change pitch/maqam; never cut the reciter's madd or repetitions; remove only breaths/long silences, and keep pauses smooth (fades, no hard gates).

## Rules
- Never clip: no sample above −1 dBTP after the limiter; check with `analyze.sh`.
- Process the voice alone first, then mix. Effects on the whole mix only for global moves (loudness, final limiter).
- Arabic VO: protect consonant clarity (2–4 kHz); be careful de-essing ش/س/ص — too much makes it lisp.
- Music licensing: only tracks the user has rights to (YouTube Audio Library, Pixabay, Freesound with license checked, ElevenLabs output under their plan).
- Keep 48 kHz throughout for video; resample once at the start if the source differs.
- Client work uses the client's sonic brand (jingle, voice tone) if they have one.
