# Prompts — صور واقعية بناس (النسخة المعتمدة)

## الطريقة المعتمدة: كولاج واحد ونقصه
بنولّد صورة واحدة طولية (1024×1536) فيها التلات مشاهد فوق بعض، وبعدين نقصها:
`python3 split_collage.py path/to/collage.png` ← بيطلّع `img/liver.jpg` و `img/kidney.jpg` و `img/hpylori.jpg`
وبعدين `node render.js export` (مع `NODE_PATH=$(npm root -g)`).

```
A vertical collage image, portrait 2:3 (1024x1536), made of exactly 3 equal horizontal panels stacked from top to bottom, separated by thin pure-white lines (about 10px). All 3 panels are photorealistic, cinematic, editorial-quality photographs in one consistent color grade: warm natural skin and food tones, deep navy blue (#2B3163) shadows, very small red (#E0302A) accents. In every panel the main subject is in the CENTER of the panel with breathing room on the left and right. Authentic Egyptian people and settings. Absolutely no text, letters, logos or signage anywhere.

PANEL 1 (top): An Egyptian father in his early 40s walking on a warm-lit Cairo street at night, carrying his little daughter (about 5) on his shoulders; she is asleep with her head resting on his head, he smiles softly. Slightly low angle, 50mm, shallow depth of field, warm bokeh shop lights.

PANEL 2 (middle): Close-up of the hands of an elderly Egyptian woman with a simple gold ring, pouring clear sparkling water from a traditional Egyptian clay water jar (zeer / ullah) into a clear glass. Morning side light makes the water glow; droplets on the clay; softly blurred navy-and-white home interior. 85mm macro detail.

PANEL 3 (bottom): Top-down bird's-eye flat lay of a warm Egyptian family lunch table — koshari, molokhia, rice, salad, baladi bread, tea — with many hands (adults and children) reaching into the same shared plates at once. White tablecloth, natural daylight, clean and joyful, no faces needed.
```

---

## نفس المشاهد كل واحد لوحده (لو الكولاج طلع ضعيف)

القواعد: صورة **عرضية 3:2 (1536×1024)**، واقعية تماماً، من غير أي كلام أو لوجو. الصورة بتتحفظ في `img/liver.jpg` و `img/kidney.jpg` و `img/hpylori.jpg`.
لون الصورة: درجات دافية هادية مع لمسة كحلي في الظلال، عشان تمشي مع هوية امتياز (كحلي #2B3163 وأحمر #E0302A).

## 1. الكبد: «بيشيل عنك كتير.. ومبيشتكيش»
```
Photorealistic cinematic photograph, 3:2 landscape. An Egyptian father in his early 40s, casual shirt, walking on a warm-lit Cairo street at night, carrying his little daughter (about 5 years old) on his shoulders; she is asleep, resting her head on his head, and he is smiling softly and calmly. Shot from a slightly low angle, 50mm lens, shallow depth of field, background of blurred warm shop lights and string lights (bokeh). Color grade: warm skin tones, deep navy blue shadows, a few small red light accents in the bokeh. The father and daughter are centered slightly to the right, with empty space at the top. Natural, emotional, authentic, editorial quality. No text, no logos, no signage letters.
```

## 2. الكلى: «زي الزير.. كليتك بتصفّي في صمت»
```
Photorealistic close-up photograph, 3:2 landscape. The hands of an elderly Egyptian woman, with a simple gold ring, pouring clear, sparkling water from a traditional Egyptian clay water jar (zeer / ullah) into a clear glass cup. Morning sunlight from a side window makes the water glow and sparkle; tiny droplets on the clay surface. Background: a softly blurred traditional Egyptian home interior in navy and white tones. Macro detail on the water stream and the clay texture, 85mm lens, shallow depth of field. Color grade: clean, fresh, bright whites, navy blue shadows. The water stream is in the center of the frame. Calm, pure, authentic. No text, no logos.
```

## 3. الجرثومة: «في ضيف على السفرة.. مش باين»
```
Photorealistic top-down (flat lay, bird's-eye view) photograph, 3:2 landscape. A warm Egyptian family lunch table with shared dishes: koshari, molokhia, rice, salad, baladi bread, cups of tea; many hands from different family members (adults and children) reaching into the same shared plates at the same time. One shared bowl in the center is slightly emphasized by soft light. White tablecloth, natural daylight, crisp detail, editorial food-photography quality. Color grade: clean whites, natural food colors, subtle navy blue in the shadows. Joyful and normal, not dirty, not scary, no bacteria shown. No text, no logos, no faces needed.
```

## لو النتيجة مش مظبوطة
- ملامح مش مصرية: زوّد `authentic Egyptian features and setting, Cairo, Egypt`.
- شكلها صناعية أو بلاستيك: زوّد `shot on Sony A7IV, natural skin texture, film grain, no AI look`.
- طالع فيها كلام أو يافطات: زوّد `absolutely no text, letters or signage anywhere`.

---

# نسخة الـ 3D القديمة (`post-3d.html`)

صورة مربعة 1:1، على خلفية بيضا، من غير كلام. بتتحفظ في `img/liver.png` و `img/kidney.png` و `img/hpylori.png`.

- **الكبد:** A premium 3D render of a stylized human liver, soft matte clay, navy #2B3163 to white, one red droplet #E0302A, white background, no text.
- **الكلى:** A premium 3D render of a pair of stylized kidneys in frosted navy-tinted glass with water flowing through like a filter, tiny red droplets, white background, no text.
- **الجرثومة:** A premium 3D render of a white clay stomach with a navy magnifying glass revealing a small red spiral H. pylori bacterium, white background, no text.
