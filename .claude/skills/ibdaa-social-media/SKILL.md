---
name: ibdaa-social-media
description: Social media for the Ibdaa Motion agency (إبداع بيتحرك) and its clients on Facebook and Instagram - Egyptian Arabic captions, hooks, hashtags, carousels, Reels/Stories copy, monthly content calendars, post-project portfolio posts, comment/DM replies, boosted-post briefs and monthly performance reviews. Use for "بوست", "كابشن", "خطة نشر", "كالندر", "ريلز", "ستوري", "كاروسيل", "الصفحة", "فيسبوك", "إنستجرام", "رد على كومنت", or any Facebook/Instagram content request.
---

# Ibdaa Social Media

Write like a sharp Egyptian creative, not a translated brochure.

**Two kinds of pages — never mix them:**
- **صفحة إبداع بيتحرك** = the agency's own showroom page. Posts here sell the agency: portfolio
  boards, behind the scenes, tips, offers. Apply `ibdaa-motion-brand` (colors, voice, board).
- **Client pages** = content we produce for clients. Written in the client's voice, designed in the
  client's brand, signed by the client. No Ibdaa branding, logo or hashtags unless the user asks.
When a request doesn't say which page, ask once.

## 1. Before writing: 4 questions (skip what's already known)
1. Page: Ibdaa Motion or a client? (client name, field, audience, city)
2. Goal of the post: awareness / engagement / messages (leads) / sale / portfolio.
3. Format: single image, carousel, Reel, Story, text-only, video.
4. Offer or must-say details: price, discount, deadline, phone/WhatsApp, link.

## 2. Caption structure (default)
```
[Hook: line 1 — must work alone before "See more", ≤ 8–10 words]
[Value: 2–4 short lines — the idea, the result, or the problem we solved]
[Proof/detail: number, before/after, client, duration — optional]
[CTA: one clear action]
[3–5 hashtags]
```
Rules:
- Egyptian colloquial, short lines, one idea per line. Emojis: 0–3, purposeful, never a row of them.
- One CTA only. Lead CTAs: «ابعتلنا رسالة», «كلمنا واتساب», «اكتب "عايز" في الكومنتات».
- No clickbait the post can't deliver; no fake numbers or fake testimonials. Only real results the user gives.
- Always deliver **3 hook options** + the full caption with the recommended hook, plus a short version (for Stories/ads).
- Hook formulas and Egyptian examples: `references/hooks-and-ctas.md`.

## 3. Hashtags
3–5 per post: 1 brand (#إبداع_بيتحرك), 1–2 service (#موشن_جرافيك #تصميم_جرافيك #مونتاج_فيديو),
1–2 audience/location (#مصر #القاهرة #تسويق_إلكتروني). Arabic hashtags use `_` between words. No hashtag walls.

## 4. Formats & specs
| Format | Size | Copy notes |
|---|---|---|
| Feed image / project board | 1080×1350 (4:5) | Text on image ≤ 7 words; caption carries the detail |
| Carousel | 1080×1350, 3–10 slides | Slide 1 = hook, last = CTA; one idea per slide; give slide-by-slide text |
| Reel | 1080×1920 (9:16), 15–45 s | Hook in first 2 s on screen + VO; keep text inside the center safe area (~250 px free top & bottom); caption 1–3 lines |
| Story | 1080×1920 | 1 message per frame; use poll/question sticker for engagement; CTA frame last |
| Cover / profile | follow platform's current guide | Re-check sizes on Meta before export — they change |

For video specs and exports, defer to `video-delivery-specs` and `ffmpeg-skill`.

## 5. Content pillars for the Ibdaa Motion page (starting mix, adjust from results)
| Pillar | Share | Examples |
|---|---|---|
| شغلنا (portfolio) | 35% | project board after every job, before/after, the finished Reel |
| ورا الكواليس (process) | 20% | from idea → storyboard → Flow prompt → final; timelapse of the edit |
| نصايح وتعليم (value) | 20% | «3 غلطات في إعلانك», AI tools tips, colors/fonts tips |
| آراء العملاء (proof) | 10% | real quotes only, with permission (`testimonial-video`) |
| عروض وخدمات (sales) | 15% | packages, seasonal offers (Ramadan, Eid, Black Friday, back-to-school) |

Cadence default: 3–4 feed posts + 2 Reels + daily Stories per week. Reduce rather than drop quality.

## 6. Monthly content calendar
Output a table (and the CSV in `templates/content-calendar.csv` filled in) with:
`date | day | pillar | format | topic | hook | visual brief | CTA | status`.
- Plan around Egyptian/Arab occasions in that month (Ramadan, Eid al-Fitr, Eid al-Adha, Mother's Day 21 March, national holidays, back-to-school, Black Friday / الجمعة البيضاء). Verify the exact dates for the year before scheduling.
- Mix pillars so no two sales posts are back to back.
- Mark which posts need: a project board (`ibdaa-motion-brand`), a Reel (`short-form-video`), a Flow prompt, or an ElevenLabs VO (`ibdaa-studio-workflow`).
- Posting times: no universal best time — start with the page's Meta Business Suite insights ("when your audience is online"); if none, test evening slots and compare after 4 weeks.

## 7. After every finished project (portfolio post)
1. Render the board with `ibdaa-motion-brand` (1080×1350).
2. Cut a 10–20 s Reel from the final video (best moment first) with `ffmpeg-skill`.
3. Caption: hook about the client's problem or the result → what we made → services used → CTA «عايز فكرتك تتحرك؟ ابعتلنا».
4. Ask the user to confirm the client agreed to be shown publicly; if not, write it without the client's name.
5. Story set: teaser frame → board → «اكتب "عايز" وهنبعتلك الأسعار».

## 8. Comments & DMs
Reply templates in `references/replies.md`. Principles: answer fast, warm, short; move price questions to DM/WhatsApp; never argue publicly; complaints → apologize, take to DM, solve.

## 9. Boosted posts / Meta ads brief (when the user will pay for ads)
Deliver: objective (Messages / Engagement / Video views), audience (city, age, interests — e.g. business owners, e-commerce, restaurants), placement (Feed + Reels), 2–3 creative variants with different hooks, budget split suggestion for a test week, and what metric decides the winner (cost per message for leads). Use `ad-creative-video` for the video variants.

## 10. Monthly review
Ask for Meta Business Suite numbers (reach, engagement, shares, saves, messages, Reel plays, average watch time, follower change). Return: top 3 and bottom 3 posts and why, which pillar and format performed best, 3 concrete changes for next month. Never invent numbers; if data is missing, say what to export.
