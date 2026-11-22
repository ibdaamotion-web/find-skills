# Skills on demand (not installed — install only when a job needs it)

Rule: when a task would clearly benefit from one of these (or any other free skill), tell the user
**which skill, why, and the install command**, and wait for approval before installing.
Install into the repo: `npx skills add <source> -a claude-code --copy -y -s <skill>` then commit.

| Skill | Source | Use it when |
|---|---|---|
| remotion-docs | remotion-dev/skills | need exact Remotion API docs |
| remotion-license | remotion-dev/skills | agency grows past 3 people (Remotion company license) |
| remotion-studio | remotion-dev/skills | live preview of a Remotion project on the user's own computer |
| remotion-maps | remotion-dev/skills | animated map videos in Remotion |
| remotion-multimedia | remotion-dev/skills | low-level media decoding (Mediabunny) |
| manimgl-best-practices | adithya-s-k/manim_skill | 3b1b ManimGL instead of Manim Community |
| reverse-any-video | heygen-com/hyperframes | rebuild a reference video as an editable project |
| slideshow | heygen-com/hyperframes | live presentation decks in HyperFrames |
| music | elevenlabs/skills | generate music via ElevenLabs API (uses credits) |
| voice-isolator | elevenlabs/skills | clean noisy voice via ElevenLabs API |
| setup-api-key | elevenlabs/skills | ElevenLabs API key not working |
| countdown-video | iart-ai/tiktok-video-skills | countdown / timer videos |
| algorithmic-art, theme-factory | anthropics/skills | generative p5.js art / preset themes for decks |
| yt-plan, yt-audit, yt-retention, yt-viral, yt-comment | Jakeschincariol/youtube-agent-skill | serious YouTube channel work (planning, audits, retention, trends, comments) |
| after-effects | iart-ai/motion-design-skills | only if the user gets After Effects (paid) |
| directing-stickman-videos Code Engine (B) media | kaomei/stickman-video-director | stickman mode B (full ~500 MB install) |
| full caveman suite | JuliusBrussee/caveman | deeper token analytics |

Other free sources to search when something is missing: `npx skills find <query>`, skills.sh,
`zhuyansen/awesome-claude-video-skills`, `iart-ai/motion-skills` (index of 19 motion packs).
