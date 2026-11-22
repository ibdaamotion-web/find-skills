---
name: ibdaa-motion-brand
description: Brand identity of the Egyptian ad agency "إبداع بيتحرك" (Ibdaa Motion) - colors, font, logo, tone of voice - plus a ready template that renders a Facebook project board (1080x1350) after every finished job. Use whenever making any design, motion graphic, video, thumbnail, social post, presentation or board for Ibdaa Motion or when the user says "الهوية", "البورد", "بوست الفيسبوك", "إبداع بيتحرك".
---

# إبداع بيتحرك — Brand Skill

Ibdaa Motion is an Arabic (Egyptian) agency for graphic motion, graphic design, video editing
and AI content. Every output for the agency follows this identity. Reference images:
`assets/logo-reference.png` (main logo) and `assets/brand-guide-reference.png` (official guide).
Machine-readable tokens: `assets/brand-tokens.json`.

## Colors (light version is the official one)

| Name | Hex | Role | Share |
|---|---|---|---|
| كريمي Cream | `#F4F1EA` | main background | 60% |
| ورقي Paper | `#EDE6D6` | second background, paper | – |
| أبيض دافي Warm white | `#FFFDF8` | cards, phone mockups | – |
| حبر Ink | `#161514` | text only | 15% |
| برتقالي Orange | `#FF5A20` | the hero: key word, price, CTA | 15% |
| برتقالي غامق Dark orange | `#E5470F` | orange shadow / pressed state | – |
| تيل Teal | `#13C2B5` | helper: frames and details | 10% |

Rules:
- Default = cream background + ink text (the "بعد" version). The black background version is retired; use dark only for video night scenes or when explicitly asked.
- Orange is reserved for ONE important thing per layout (key word, price, CTA). Never orange body text.
- Teal never carries text on its own; use it for frames, lines, underlines, small details.
- Texture: a light dot grid on the cream + soft shadows. No gradients, no glossy effects.

## Typography
- Font: **Alexandria** (free, Google Fonts) — Arabic + Latin in one family.
- Headlines 900 · sub-headlines 800 · body/description 600.
- Right-to-left layouts; Egyptian colloquial copy, short and punchy.

## Logo
- Mark: a rounded orange triangle pointing left (play/rewind = motion) + three rounded bars on its
  right: teal (short) / orange (long) / teal (short). Files: `assets/logo-mark.svg`,
  `assets/logo-mark-on-orange.svg`.
- Wordmark: «إبداع» in ink + «بيتحرك» in orange, Alexandria 900.
- On light: orange triangle, teal + orange bars. On orange: white triangle, white + ink bars.
- Keep clear space ≥ the height of one bar around the logo; never stretch, rotate or recolor outside these two versions.

## Voice
Friendly, confident Egyptian Arabic. Examples: «عايز فكرتك تتحرك؟ كلمنا», «شغل جديد», «من الفكرة للحركة».

## Facebook project board (after every finished job)

Template: `templates/project-board.html` (1080×1350, 4:5 feed format, renders at 2x).

1. Collect 1–4 stills/frames of the work (export frames from the video with
   `ffmpeg -ss 00:00:03 -i video.mp4 -frames:v 1 shot1.png`).
2. Copy `examples/sample-board.json` next to the images and fill it:
   - `kicker` (service · format), `title`, `highlight` (the word in the title to color orange),
     `client`, `images` (1–4, first one is the hero framed in teal), `isVideo` (adds play button),
     `tags` (first tag is orange), `stats` (up to 3, e.g. duration/quality), `cta`, `contact`,
     optional `"theme": "dark"`.
3. Render: `node scripts/render_board.js path/to/board.json out.png`
   (needs Playwright; if not resolvable run with `NODE_PATH=$(npm root -g)`).
4. Look at the PNG before delivering: Arabic text joined correctly, nothing clipped, only one orange focal point besides the CTA bar.
5. Write the Facebook caption too: hook line, 2–3 lines about the idea/result, services, CTA, 3–5 hashtags in Arabic.

## Applying the brand to motion / video
- End card: cream background, logo animates in (triangle slides from the right, bars draw in one after another teal→orange→teal), 0.8–1.2 s, ease-out.
- Lower thirds and captions: warm-white card, ink text, teal left/right rule, orange only on the keyword.
- AI video prompts (Flow/Veo, etc.): describe palette as "warm cream #F4F1EA background, vivid orange #FF5A20 accents, teal #13C2B5 details, charcoal ink #161514", clean flat-graphic look with soft shadows. Generated video cannot render Arabic text reliably — add all Arabic text in the edit, not in the prompt.
