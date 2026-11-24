# Audio fundamentals (cheat-sheet)

## Levels
- **dBFS**: digital level; 0 dBFS = maximum. Anything above clips (distortion).
- **Peak vs true peak (dBTP)**: true peak includes inter-sample peaks that appear after encoding to AAC/MP3. Keep ≤ −1 dBTP.
- **RMS / LUFS**: perceived loudness. **LUFS integrated** = whole-file loudness (what platforms normalize to). **Short-term** (3 s) and **momentary** (400 ms) for sections.
- **LRA** (loudness range): dynamics in LU. Ads/reels 4–8 LU; cinematic 10–15 LU.
- **Gain staging**: keep healthy levels at every step (voice peaks around −6 dBFS before processing); never boost noise.
- **Noise floor**: level of silence/background. Good VO: below −60 dBFS. −45 dBFS or higher = noticeable noise.

## Frequency map (voice & mix)
| Range | Hz | Character | Typical move |
|---|---|---|---|
| Sub / rumble | 20–80 | AC, traffic, handling noise | high-pass on voice |
| Bass / body | 80–250 | warmth, chest | small boost for thin voices |
| Mud | 200–500 | boomy, cloudy | cut 2–4 dB, Q≈1–2 |
| Box | 500–1000 | nasal, cardboard | narrow cut if needed |
| Presence | 2–5 k | intelligibility, consonants | +2–3 dB if voice is buried |
| Sibilance | 5–9 k | "s", "sh", "ص ش س" | de-esser |
| Air | 10–16 k | sparkle, breath | +1–2 dB shelf, carefully |
Music under voice: dip music 2–4 kHz by 2–4 dB so the voice sits on top ("carving").

## Dynamics
- **Compressor**: threshold (where it starts), ratio (how much), attack (how fast it grabs; 5–20 ms voice), release (how fast it lets go; 50–200 ms), makeup gain. Aim for 3–6 dB gain reduction on peaks.
- **Limiter**: compressor with infinite ratio; last in the chain, sets the ceiling (−1 dBTP).
- **Gate / expander**: mutes or lowers below a threshold — cleans breaths/noise between phrases; can chop word tails if too aggressive.
- **De-esser**: compressor that only reacts to sibilant frequencies.
- **Sidechain / ducking**: one signal (voice) controls the compressor on another (music).

## Time & space
- **Reverb**: pre-delay (gap before the tail, 10–40 ms keeps clarity), decay (0.3–0.8 s room, 1.5–3 s hall), mix (wet 5–15% for realism).
- **Delay/echo**: delay time (sync to tempo: 60000 / BPM ms per beat), feedback (repeats), mix.
- Phase: two copies of the same sound slightly offset = comb filtering (hollow sound). Keep voice mono and centered.

## Formats
- Work: WAV 48 kHz 24-bit. Delivery inside video: AAC 48 kHz 192–320 kbps. Stems for editors: WAV per element (VO, music, SFX).
- Sample rate change → do once. Bit depth: never render final masters at 16-bit with heavy processing without dither (FFmpeg's default resampling is fine for AAC delivery).

## Common problems → fix
| Problem | Likely cause | Fix |
|---|---|---|
| Voice hard to understand | music masking, no presence | duck music, carve 2–4 kHz, +presence |
| Harsh / piercing | 3–6 kHz too hot or sibilance | narrow cut / de-esser |
| Boomy | proximity effect, room | high-pass + cut 200–300 Hz |
| Thin | over-high-passed, small mic | lower HPF, +150–200 Hz |
| Hiss | noisy preamp | afftdn / anlmdn gently |
| Hum 50 Hz (Egypt mains) | ground loop | notch 50, 100, 150 Hz |
| Pumping | compressor release too fast / too much GR | slower release, less ratio |
| Too quiet on phone | low LUFS or too much low end | normalize to −14, reduce sub-bass |
| Distortion | clipping | re-render from source with lower gain + limiter |
