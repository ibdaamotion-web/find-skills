# Broast Chicken — فيديو شاشة الطريق (افتتاح فرع الزرقا)

**المواصفات:** 16:9 أفقي · صامت · لوب · ماستر 1920×1080 @ 30fps (هنصدّر بعد كده بدقة الشاشة بالظبط) · المدة 45 ث + نسخة قصيرة 15 ث

---

## 1. القواعد اللي ماشيين عليها (شاشة طريق)
- **رسالة واحدة في كل لقطة**: اسم المنتج + السعر، وبحد أقصى 5 كلمات على الشاشة.
- **حجم النص:** أقل حاجة 9% من ارتفاع الشاشة، يعني حوالي 100px على 1080. الأسعار 15–18%.
- **مدة النص:** أي نص يفضل ظاهر 2 ثانية على الأقل.
- **اللوجو كل 8–10 ثواني** في شكل فاصل الديك، عشان أي حد يلحق حتة من الفيديو يعرف البراند.
- **الخلفيات غامقة** (أحمر غامق لحد أسود)، لأن الأبيض بيعمي العين بالليل. فلاشات الضربة لونها برتقالي، مش أبيض.
- **مفيش صوت:** الإحساس بالضربة والقرمشة بيوصل بالصورة، يعني اهتزاز كاميرا وفتافيت طايرة وموشن بلر ورامب سرعة.
- **الألوان:** أحمر #B71C1C · برتقالي #F28C28 · أصفر الأسعار #FFC400 · كرافت #A47A4F · أسود #0D0505
- **الخطوط (مجانية):** العناوين Lalezar، والأسعار اللاتيني (130 L.E) Montserrat Black. كروت الأسعار شكلها شرايط ورق ممزق زي المنيو بالظبط.

## 2. تكنيك كسر الإطار (Frame-Break)
- في الإديت بنرسم إطار برتقالي جوه الشاشة، بسُمك حوالي 40px وبعيد عن الحافة 6%.
- أي حاجة طالعة ناحية الطريق (الديك، القطع الطايرة، الفتافيت) بتتحط **فوق** الإطار. كده الجزء اللي فوق الإطار بيبان كأنه خارج من الشاشة، والباقي جوه، فيطلع إيهام 3D.
- لقطات الديك تتولّد على **خلفية خضرا (كروما)**.
- لقطات الأكل تتولّد على **خلفية سودا**، وأنا هفصلها هنا بأداة مفتوحة المصدر (BiRefNet/rembg) فريم بفريم.

---

## 3. البلوكات الثابتة (بتتنسخ زي ما هي جوه كل برومت)

**[MASCOT]**
> the Broast Chicken mascot — a cheerful cartoon rooster rendered as a polished 3D animated-feature character: glossy pure-white fluffy feathers, a bright red three-lobed comb on top of the head, a small red wattle, large expressive white oval eyes with big black pupils, a wide open glossy orange-yellow beak in a huge happy grin showing a red tongue, feathery white wings ending in white four-finger cartoon gloves, a subtle dark toon outline on the silhouette, matching the reference image exactly

**[GREEN]**
> isolated on a perfectly flat, evenly lit pure chroma-key green background, no shadows on the background, no green spill on the subject, the whole subject stays fully inside the frame

**[FOOD LOOK]**
> high-end food commercial cinematography, macro detail, hyper-real textures, glistening sauces, crispy golden fried coating with visible crumbs, warm key light with a strong orange rim light, deep dark-red to black background, shallow depth of field, 4K, ultra slow motion look

**[END]**
> No text, no subtitles, no logos, no watermark, no music, no dialogue.

**إعدادات Flow:**
- اللقطات الهيرو (S01 · S04 · S05) بموديل Veo **Quality**، والباقي بـ **Fast**.
- كل لقطة 2–3 نسخ، ونختار أحسنهم.
- لقطات الديك: Ingredients to Video، والمرجع هو اللوجو المقصوص.
- لقطات البرجر: Ingredients أو Frames to Video، والمرجع صورة المنتج من المنيو.

---

## 4. الستوري بورد (الماستر 45 ث)

| # | الوقت | المشهد | المصدر | النص على الشاشة | الانتقال |
|---|---|---|---|---|---|
| S01 | 0:00–0:04 | **الهوك:** الإطار البرتقالي بيتنفخ ويتشقق، والديك بيكسره ويطلع ناحية الطريق ويرفع صباعه | Flow (أخضر) + إطار وشروخ موشن | — | الديك يلف ويرمي العلبة |
| S02 | 0:04–0:07 | الديك بيرمي علبة كرافت، الغطا بيتفتح، وقطع البروست والبطاطس بتطير برّه الإطار (Bullet-time) | Flow ×2 | — | القطع تتجمد |
| S03 | 0:07–0:09 | **لوجو 1:** اللوجو ينزل بضربة وسط القطع المتجمدة | موشن جرافيك | **افتتاح الفرع الجديد** | Whip pan |
| S04 | 0:09–0:17 | **هيرو 1:** طبقات الهاوس برجر طايرة ومنفصلة، الكاميرا بتلف حواليها، وبعدين الطبقات بتقفل على بعض بضربة | Flow ×2 | هاوس برجر **140 L.E** | قطع على الضربة |
| S05 | 0:17–0:23 | **هيرو 2:** كريمي لافا = بركان، الجبنة بتسيل زي الحمم ومعاها جمر طاير | Flow | كريمي لافا **140 L.E** | الديك يطل |
| S06 | 0:23–0:25 | **لوجو 2:** الديك يطل من يمين الشاشة، يغمز، ويشاور على السعر | Flow (أخضر) | بيف برجر **من 100** | مسحة ورق ممزق |
| S07 | 0:25–0:37 | **بليتز الأقسام:** 5 لقطات، كل واحدة 2.4 ث | Flow ×5 | (جدول تحت) | مسحات ورق ممزق |
| S08 | 0:37–0:41 | **الوجبات:** العلب بتدخل ورا بعض والعداد بيزيد من 2 لـ 12 قطعة | موشن جرافيك من صور المنيو | **وجبات بروست من 130 L.E** | — |
| S09 | 0:41–0:45 | **الإند كارد:** الديك يقص شريط الافتتاح، كونفيتي، واللوجو بالحجم الكامل | Flow (أخضر) + موشن | تحت | يقفل على الإطار ← يرجع لـ S01 |

**نصوص S07:**

| اللقطة | القسم | النص |
|---|---|---|
| 7a | بيف برجر | **بيف برجر · من 100 L.E** |
| 7b | تشيكن برجر | **تشيكن برجر · من 100 L.E** |
| 7c | بروست | **بروست مقرمش** |
| 7d | ريزو | **ريزو · من 75 L.E** |
| 7e | كريبات | **كريبات · من 60 L.E** |

> لما S06 يتعرض، النص بتاع 7a «بيف برجر من 100» بيظهر جنب الديك، وبعدين البليتز يكمل.

**الإند كارد (S09b):**
- اللوجو كبير في النص، بارتفاع حوالي 45% من الشاشة.
- **افتتاح الفرع الجديد**
- **الزرقا – كورنيش النيل بجوار صيدلية د. السيد زيو**
- **01127923826**
- [تاريخ الافتتاح / العرض لو موجود]

**نسخة 15 ث:** S01 (3 ث) ← S02b (2 ث) ← S04b (4 ث) ← S05 (3 ث) ← الإند كارد (3 ث).

---

## 5. برومتات Flow (إنجليزي، كل برومت مستقل بذاته)

### S01 — الديك بيكسر الإطار · Ingredients: اللوجو · 8 ث (هنستخدم أول 4)
```
Medium shot, 35mm lens, static camera at chest height. [MASCOT] stands very close to the camera as if pressed against an invisible glass wall. 0–2s: he presses both gloved hands flat against the invisible wall, squishing his cheeks and beak playfully against it. 2–3s: he leans back and bursts forward through it toward the lens with arms spread wide, feathers ruffling, small white feathers flying toward the camera. 3–5s: he lands in a confident pose, leans into the lens and gives a big thumbs up with his right glove while his left glove opens in a welcoming gesture, exactly like the reference logo pose. 5–8s: he holds the pose and gives a cheeky wink. [GREEN]. Bright soft studio key light with a warm orange rim light from behind. Premium 3D animated feature film style, vibrant saturated colors. Mood: energetic, funny, welcoming. [END]
```

### S02a — الديك بيرمي العلبة · Ingredients: اللوجو · 8 ث (هنستخدم 1.5)
```
Medium-wide shot, 35mm lens, static camera. [MASCOT] holds a closed plain brown kraft-paper takeaway food box with both gloves, grins, winds up like a baseball pitcher and throws the box straight toward the camera; the box spins and flies past the lens with motion blur. After the throw he points at the camera and laughs. [GREEN]. Bright soft studio key light with a warm orange rim light. Premium 3D animated feature film style, vibrant colors. Mood: playful and explosive. [END]
```

### S02b — انفجار العلبة · Bullet-time · 8 ث
```
Extreme close-up, 24mm wide lens, camera starts static. A plain brown kraft-paper takeaway box flies toward the camera in slow motion and its lid bursts open just in front of the lens. 0–2s: the box flies in. 2–4s: golden crispy broasted fried chicken pieces (drumsticks and thighs with craggy crunchy coating), golden french fries and a soft bread bun explode out of the box toward and past the camera, crumbs and steam trails spraying. 4–8s: everything hangs almost frozen mid-air (bullet-time) while the camera slowly orbits 30 degrees around the floating pieces. Pure black background. [FOOD LOOK]. Mood: explosive, mouth-watering. [END]
```

### S04a — هاوس برجر طبقاته طايرة · Ingredients: صورة هاوس برجر · 8 ث
```
Product hero shot, 50mm lens at eye level; the camera slowly orbits 180 degrees around the subject over 8 seconds. A gourmet burger deconstructed in zero gravity: every layer floats separately in a vertical stack with even gaps, gently bobbing and rotating. From top to bottom: glossy toasted sesame brioche top bun; bright green pickled jalapeño slices; thick slices of grilled red beef sausage; crispy spicy fried chicken strips glazed in red hot sauce; a stretchy sheet of melted white mozzarella with long cheese strings; a thick juicy chargrilled beef patty with dark grill crust and glistening juices; fresh red tomato slices; ruffled green lettuce leaves; a layer of creamy brown burger sauce; toasted brioche bottom bun. Sesame seeds, hot sauce droplets and crumbs float between the layers. Deep dark-red background fading to black with soft drifting smoke. [FOOD LOOK]. Mood: epic, premium, hypnotic. [END]
```

### S04b — الطبقات بتقفل بضربة · Frames to Video: أول فريم = آخر فريم من S04a · آخر فريم = صورة هاوس برجر من المنيو بعد ما نشيل خلفيتها · 8 ث
```
Product hero shot, 50mm lens, eye level. The same gourmet burger with all its layers floating apart in zero gravity: sesame brioche top bun, jalapeño slices, grilled beef sausage slices, spicy fried chicken strips in red hot sauce, melted mozzarella, chargrilled beef patty, tomato slices, green lettuce, brown sauce, brioche bottom bun. 0–1s: the layers hang floating. 1–2s: all layers rush together and slam into one assembled tall burger with a heavy impact; a burst of crumbs, sesame seeds and sauce droplets sprays outward toward the camera, mozzarella squishes out of the sides and red hot sauce drips down. 2–3s: hard camera shake that settles. 3–8s: slow push-in on the finished burger as steam rises and sauce slowly drips. Deep dark-red background fading to black. [FOOD LOOK]. Mood: powerful, satisfying. [END]
```

### S05 — كريمي لافا = بركان · Ingredients: صورة كريمي لافا · 8 ث
```
Low-angle hero shot, 85mm lens, slow dolly-in from medium shot to close-up over 8 seconds. A towering crispy chicken burger standing on a dark black volcanic rock like a volcano: glossy sesame brioche top bun, a layer of creamy white lava sauce, thin slices of tender roast beef glazed with dark barbecue sauce, a thick crispy golden fried chicken fillet, a melting slice of orange cheddar, crisp green lettuce, toasted brioche bottom bun. 0–3s: the top bun lifts slightly and thick molten golden cheddar and creamy sauce begin to overflow from the top. 3–8s: the sauce cascades down the sides in slow motion like glowing volcanic lava with bright orange-gold highlights, small glowing ember sparks rise around the burger, heat haze shimmers, and the crispy coating crackles. Pitch-black background with an orange lava glow from below. [FOOD LOOK]. Mood: hot, dramatic, irresistible. [END]
```

### S06 — الديك بيطل ويغمز · Ingredients: اللوجو · 8 ث (هنستخدم 2.5)
```
Medium close-up, 50mm lens, static camera. [MASCOT] pops in diagonally from the right edge of the frame (only his head and upper body visible), leaning in with a springy cartoon bounce. 0–1s: pop in. 1–3s: he looks straight at the camera, winks, and points his gloved finger toward the left side of the frame with an excited grin. 3–4s: he pops back out of frame to the right with a quick bounce. 4–8s: empty green frame. [GREEN]. Bright soft studio light with an orange rim light. Premium 3D animated feature film style. Mood: cheeky, fun. [END]
```

### S07a — بيف برجر · 8 ث (هنستخدم 2.4)
```
Macro close-up, 100mm lens, slow push-in. A thick juicy beef patty slams down onto a flaming charcoal grill and flames flare up around it; then a slice of orange cheddar drops onto the patty and melts, dripping over the edges in slow motion, juices sizzling, smoke curling up. Dark background with a fiery orange glow. [FOOD LOOK]. Mood: hot, intense. [END]
```

### S07b — تشيكن برجر (كاوبوي تشيكن) · Ingredients: صورة كاوبوي تشيكن · 8 ث
```
Product hero shot, 50mm lens, camera orbits 90 degrees. A tall crispy chicken burger: glossy sesame brioche top bun, dark barbecue sauce, a stack of golden crispy onion rings, slices of smoked beef bacon, a thick crispy golden fried chicken fillet, thin red onion rings, pickles, green lettuce, pink burger sauce, toasted bottom bun. Two golden crispy onion rings spin around the burger in slow motion like a cowboy lasso, then drop and land on top of the bun as barbecue sauce drips down. Deep dark-red background fading to black. [FOOD LOOK]. Mood: bold, playful. [END]
```

### S07c — بروست مقرمش · 8 ث
```
Extreme macro, 100mm lens, static camera then slow push-in. A golden crispy broasted fried chicken drumstick floats in mid-air and breaks apart into two pieces in ultra slow motion, revealing juicy white steaming meat; crunchy coating shards and crumbs fly outward toward the camera and a burst of steam rises. Pure black background with an orange rim light. [FOOD LOOK]. Mood: crunchy, juicy. [END]
```

### S07d — ريزو · Ingredients: صورة ريزو شيش · 8 ث
```
45-degree overhead angle, 50mm lens, slow descending camera. A matte black ceramic bowl filled with fluffy yellow saffron basmati rice; golden grilled chicken shish cubes tumble down into the bowl in slow motion and bounce on the rice, followed by a zigzag drizzle of dark red sauce and creamy white garlic sauce; steam rises. Dark red background fading to black. [FOOD LOOK]. Mood: warm, hearty. [END]
```

### S07e — كريبات · 8 ث
```
Close-up, 85mm lens, slow push-in. A golden crispy rolled crepe stuffed with chicken, melted mozzarella and colorful vegetables separates into two halves in slow motion, revealing the filling, with a long stretchy melted mozzarella cheese pull between the halves and steam rising. Dark background with a warm orange rim light. [FOOD LOOK]. Mood: cheesy, comforting. [END]
```

### S09a — الديك بيقص شريط الافتتاح · Ingredients: اللوجو · 8 ث
```
Medium-wide shot, 35mm lens, static camera. [MASCOT] stands behind a wide red satin ribbon stretched horizontally across the whole frame, holding a giant pair of golden scissors. 0–2s: he looks at the camera with excited eyes. 2–3s: he cuts the ribbon with a big snap; both halves fly away to the sides. 3–5s: red, orange and yellow confetti bursts everywhere while he jumps with joy. 5–8s: he lands and gives a big thumbs up to the camera. [GREEN]. Bright festive studio lighting with an orange rim light. Premium 3D animated feature film style. Mood: celebration, grand opening. [END]
```

---

## 6. اللي هعمله أنا هنا بعد ما تبعت لقطات Flow
1. **فصل الخلفية:** الأخضر بالكروما، والأسود بـ BiRefNet. كله أدوات مجانية.
2. **طبقات الموشن جرافيك بألفا:**
   - الإطار والشروخ
   - كروت الأسعار بشكل الورق الممزق
   - فواصل اللوجو
   - عداد الوجبات (S08)
   - مسحات الورق الممزق
   - الإند كارد
   - كونفيتي وجمر إضافي
3. **التجميع الكامل** والانتقالات على الضربات واهتزاز الكاميرا، وتظبيط اللوب عشان آخر فريم يكمّل في أول فريم.
4. **التصدير:** ماستر 45 ث + نسخة 15 ث بدقة الشاشة، وبعدها مراجعة جودة: حجم النص، والسطوع بالليل، وعيوب AI.

## 7. لسه ناقص (مش بيوقف الشغل)
- **ملف اللوجو الأصلي** (PNG شفاف أو AI): ضروري للإديت النهائي.
- **تاريخ الافتتاح والعرض لو موجود:** حاليًا مكانه فاضي في الإند كارد.
- **دقة الشاشة بالبيكسل بالظبط:** الماستر 1920×1080.
- **اسم المطعم:** حاليًا بالإنجليزي بس زي اللوجو.
