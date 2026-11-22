# دليل سكيلز استوديو «إبداع بيتحرك»

كل حاجة هنا **مجانية**: سكيلز مفتوحة المصدر على GitHub (رخص MIT / Apache غالبًا) وبرامج مجانية.
اتجنب أي حاجة بتطلب اشتراك أو API key مدفوع (زي iArt MCP — السكيلز بتاعتهم مجانية لكن الـ MCP بتاعهم مدفوع).

---

## 1) إزاي تضيف سكيل لـ Claude

السكيل = فولدر فيه ملف `SKILL.md` (تعليمات) + ملفات مساعدة. Claude بيقراه تلقائيًا لما الشغل يناسبه.

**الطريقة الأسهل (أي جهاز عليه Node.js):**
```bash
npx skills add <owner/repo>            # يثبت كل السكيلز اللي في الريبو
npx skills add <owner/repo>@<skill>    # يثبت سكيل واحد
npx skills add <owner/repo> -g -y      # تثبيت عام لكل المشاريع
```

**يدويًا:** انسخ فولدر السكيل جوه:
- `~/.claude/skills/` ← يشتغل في كل المشاريع على جهازك
- `.claude/skills/` جوه الريبو ← يشتغل مع أي جلسة على الريبو ده (حتى جلسات Claude Code على الويب)

**في Claude Code كـ plugin:** `/plugin marketplace add <owner/repo>`

**في claude.ai:** Settings → Capabilities → Skills → Upload (ارفع الفولدر مضغوط ZIP).

> مهم لجلسات الويب: الجلسة بتبدأ من الريبو كل مرة، فعشان السكيلز تفضل معايا دايمًا خليها جوه
> `.claude/skills/` في الريبو (أنا عملت كده لسكيلز الهوية والاستوديو).

---

## 2) السكيلز اللي عملتهالك (موجودة في الريبو ده)

| السكيل | بيعمل إيه |
|---|---|
| `ibdaa-motion-brand` | هوية «إبداع بيتحرك» كاملة: الألوان والنسب، خط Alexandria، اللوجو SVG، نبرة الكلام، **وقالب بورد فيسبوك 1080×1350** بيطلع PNG بأمر واحد |
| `ibdaa-studio-workflow` | خط الإنتاج: من البريف → أفكار → سكريبت → **برومبتات Flow دقيقة لكل شوت** → **سكريبت صوت ElevenLabs** → مونتاج ببرامج مجانية → مراجعة جودة → البورد |

رسم البورد:
```bash
node .claude/skills/ibdaa-motion-brand/scripts/render_board.js board.json board.png
```

---

## 3) من السكيلز اللي إنت ضايفها على GitHub — إيه المفيد؟

| الريبو | الحكم | ليه |
|---|---|---|
| **motion-skills** (iart-ai) | ⭐ مفيد جدًا | فهرس لـ 19 باك (56 سكيل) موشن مجانية MIT. الريبو نفسه فهرس بس — ثبّت الباكات نفسها (تحت) |
| **stickman-video-director** | ⭐ مفيد | فيديوهات ستيك مان/إكسبلينر، ومصمم أصلًا يكتب برومبتات لـ **Google Flow** — مناسب جدًا لشغلك |
| **youtube-agent-skill** | ⭐ مفيد | 11 سكيل: سكريبت بهوكس، عناوين وثمبنيل، تحليل retention، EDL للمونتاج، استخراج Shorts. مجاني بدون API |
| **skills** (anthropics) | ⭐ مفيد جزئيًا | استخدم: `canvas-design`, `brand-guidelines`, `theme-factory`, `algorithmic-art`, `frontend-design`, `slack-gif-creator` (GIFs), `pptx`/`pdf` للعروض |
| agent-skills (addyosmani) | ❌ مش لشغلك | سكيلز هندسة برمجيات |
| ponytail | ❌ | أسلوب كتابة كود |
| graphify | ❌ | خريطة لكود المشاريع |
| OmniRoute | ❌ | بوابة موديلات AI — مش جرافيك |
| MemoryCloud | ⚠️ اختياري | ذاكرة للإيجنت؛ مش ضروري — الهوية محفوظة كسكيل خلاص |
| find-skills (الريبو ده) | ✅ أداة | بيساعدني أدوّر على سكيلز جديدة |

---

## 4) سكيلز مجانية أنصح تنزلها (اتأكدت منها على GitHub)

### الموشن جرافيك والفيديو بالكود
| الريبو | ★ | الرخصة | الاستخدام |
|---|---|---|---|
| `remotion-dev/skills` | 7.7k | رسمي من Remotion | فيديو بالكود (React) — إعلانات، تايبوجرافي، داتا |
| `heygen-com/hyperframes` | 88k | Apache-2.0 | فيديو من HTML قابل للتعديل — موشن جرافيك عالي الجودة |
| `Sunwood-ai-labs/hyperframes-motion-reel-skill` | 203 | MIT | شوريل موشن متزامن مع البيت |
| `howseen-ai/claude-motion-design` | 882 | MIT | موشن ديزاين بـ HTML + Playwright + FFmpeg (يشتغل هنا عندي مباشرة) |
| `nexu-io/html-video` | 4.9k | Apache-2.0 | HTML/CSS/داتا → فيديو |
| `adithya-s-k/manim_skill` | 1.3k | MIT | إكسبلينر تعليمي بأسلوب 3Blue1Brown |
| `Tejashmakwana/motionmaxxing` | 1.7k | Apache-2.0 | يحسّن جودة الحركة والتوقيت |

باكات iart-ai (كلها MIT، ثبّت اللي محتاجه بس):
```bash
npx skills add iart-ai/ad-video-skills          # إعلانات براندات
npx skills add iart-ai/motion-design-skills     # موشن ديزاين
npx skills add iart-ai/kinetic-typography-skills
npx skills add iart-ai/tiktok-video-skills      # ريلز/تيك توك
npx skills add iart-ai/ecommerce-video-skills   # فيديوهات منتجات
npx skills add iart-ai/lower-thirds-skills      # لوار ثيردز شفافة
npx skills add iart-ai/b-roll-skills
npx skills add iart-ai/freelance-motion-skills  # شغل العملاء
```

### المونتاج
| الريبو | ★ | الرخصة | الاستخدام |
|---|---|---|---|
| `kajisho5/ffmpeg-skill` | 9.5k | MIT | 42 أداة مونتاج بـ FFmpeg — قص، دمج، ترجمة، تحويل مقاسات |
| `Jaycheng1103/chatgpt-video-editing-skills` | 635 | MIT | خطوات مونتاج قصير قابلة للتحقق |

### الصوت (ElevenLabs)
| الريبو | ★ | الرخصة | الاستخدام |
|---|---|---|---|
| `elevenlabs/skills` | 581 | MIT (رسمي) | كتابة وضبط الأصوات مع ElevenLabs |

### الهوية والتصميم
| الريبو | ★ | الرخصة | الاستخدام |
|---|---|---|---|
| `fatihaydost/brand-identity-skill` | 423 | MIT | تصميم هويات للعملاء (لوجو + خط + ألوان كنظام واحد) |
| `asasemahmed/MasrKit` | جديد | MIT | تصميم بطابع مصري عربي (قليل النجوم — جرّبه بحذر) |

### مجمّعات تدور فيها
- `zhuyansen/awesome-claude-video-skills` — قائمة سكيلز فيديو
- `OpenMontageInc/OpenMontage` (82k ★) — نظام إنتاج فيديو كامل مفتوح المصدر، **رخصة AGPL**: تمام للاستخدام الداخلي، بس لو عدّلته ووزعته لازم تنشر الكود

> قبل ما تثبت أي سكيل: بص على عدد النجوم والرخصة، واقرا `SKILL.md` — السكيل تعليمات بتتنفذ، فمتثبتش حاجة من مصدر مش واثق فيه.

---

## 5) البرامج المجانية اللي هشتغل عليها معاك

| المجال | البرنامج |
|---|---|
| مونتاج وكلر | DaVinci Resolve (المجاني)، Kdenlive، Shotcut |
| أوامر الفيديو | FFmpeg |
| 3D وموشن | Blender |
| فيكتور | Inkscape |
| رسم وصور | Krita، GIMP، Photopea (أونلاين) |
| كومبوزيتنج | Natron |
| صوت | Audacity |
| ترجمة/تفريغ | Whisper / faster-whisper |
| موشن بالكود | Remotion، HyperFrames، GSAP، Manim، Lottie |
| توليد فيديو | Google Flow (عندك) |
| توليد أصوات | ElevenLabs (عندك) |
| موسيقى ومؤثرات | YouTube Audio Library، Pixabay Music، Freesound |

---

## 6) طريقة شغلنا مع بعض

1. تبعتلي البريف (العميل، المنتج، المنصة، المدة، اللهجة).
2. أديك 3 أفكار → تختار.
3. أكتب السكريبت + **برومبت Flow لكل شوت** (بالإنجليزي، بنفس وصف الشخصية/المنتج في كل شوت) + **نص ElevenLabs** بالعامية المصرية.
4. إنت تولّد الفيديو والصوت، وتبعتهملي.
5. أعمل المونتاج/الموشن جرافيك بالكود أو أديك خطة مونتاج على Resolve، وأراجع الجودة.
6. أطلّع **بورد الفيسبوك** بالهوية + الكابشن.
