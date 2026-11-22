---
name: ibdaa-studio-workflow
description: Production workflow for the Ibdaa Motion agency - turning a client brief into ideas, scripts, storyboards, precise Google Flow (Veo) video prompts, ElevenLabs voice-over scripts, an edit plan with free tools (FFmpeg, DaVinci Resolve, Kdenlive, Blender, Inkscape, Krita, Audacity), and a final project board. Use for any ad, motion graphic, reel, explainer, product video, voice-over or AI-content request from the agency.
---

# Ibdaa Motion Studio Workflow

The director (the user) generates video in **Google Flow** and voices in **ElevenLabs**.
Claude's job: ideas, scripts, storyboards, prompts, edit plans, code-driven motion graphics,
and quality review. Always apply the `ibdaa-motion-brand` skill when the work is for the agency's
own channels; for client work use the client's brand if given.

Everything recommended must be free: open-source tools or free tiers the user already has.

## 1. Brief → plan (ask only what's missing)
Client, product, goal (awareness / sales / launch), platform + aspect ratio
(Reels/TikTok 9:16, Feed 4:5, YouTube 16:9), duration, language/dialect, voice gender + tone,
must-say items (price, offer, phone), deadline.

## 2. Idea + script
- Give 3 distinct concepts (one line each + why it works), recommend one.
- Script as a table: `# | time | visual | on-screen text | voice-over | SFX/music`.
- Hook in the first 2 seconds. 30-s ad ≈ 60–75 Egyptian Arabic words of voice-over.

## 3. Flow (Veo) prompts — one prompt per shot (clips are ~8 s)
Write prompts in **English** (models follow it best), each self-contained, in this order:

```
[Shot type & lens], [subject + exact appearance], [action, beat by beat with timing],
[setting], [lighting], [camera movement], [style/look + palette], [mood],
[audio: ambience/SFX only], no text, no subtitles, no logos.
```
Rules:
- Repeat the full character/product description in EVERY prompt for continuity (same clothes, colors, props). Use Flow "ingredients"/reference images for products and characters when possible.
- One main action per shot. State the camera move explicitly (slow dolly-in, static, orbit 90°…).
- Never ask the model to write Arabic text or logos; add text/logo in the edit.
- Give a first-frame / last-frame note when shots must cut together.
- Deliver a shot list with: shot id, duration, prompt, transition into the next shot.

## 4. ElevenLabs voice script
- Write the VO in Egyptian Arabic with **full tashkeel only on ambiguous words**, numbers written as words, and brand names spelled phonetically if mispronounced.
- Mark pauses with `...` or line breaks; one paragraph per scene so it can be generated and replaced per scene.
- Suggested settings: Multilingual v2 / latest v3 model, stability ≈ 0.4–0.5, similarity ≈ 0.75, style low. Recommend generating 2–3 takes of the hook.
- Free-tier credits are limited: keep VO tight and regenerate only the scene that changes.

## 5. Edit & finishing (free tools)
- **DaVinci Resolve (free)** or **Kdenlive**: assembly, color, Fairlight audio.
- **FFmpeg**: conversions, frame grabs, loudness, captions burn-in, resizing between ratios.
  - Loudness for social: `ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1:LRA=11 -c:v copy out.mp4`
  - 16:9 → 9:16 blurred background: `ffmpeg -i in.mp4 -vf "split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" out.mp4`
  - Frame for the board: `ffmpeg -ss 3 -i in.mp4 -frames:v 1 shot.png`
- **Whisper / faster-whisper** (open-source): Arabic transcription → SRT captions.
- **Audacity**: VO cleanup. Music/SFX: YouTube Audio Library, Pixabay Music, Freesound (check license).
- **Blender** (3D, product shots), **Inkscape** (vector), **Krita / GIMP** (raster), **Natron** (compositing).
- Code-driven motion graphics (Claude can build these fully): **Remotion**, **HyperFrames**, HTML + GSAP rendered with Playwright + FFmpeg, **Manim** for explainers.

## 6. Quality check before delivery
- Watch/inspect: text safe area (9:16 keep 250 px top/bottom free), Arabic shaping correct, captions synced, audio −14 LUFS, no AI artifacts (hands, warped products, flicker), brand colors correct.
- Export: H.264 MP4, 1080×1920 (Reels) / 1080×1350 (Feed) / 1920×1080 (YouTube), 30 fps, ~12–20 Mbps.

## 7. After delivery
Render the Facebook project board with the `ibdaa-motion-brand` skill and write the caption.
