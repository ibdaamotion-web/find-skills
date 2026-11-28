# Nasheed reel renderer: still image(s) -> living 9:16 video (slow push-in, breathing light,
# flicker, dust, rain on window, smoke waver) + synced lyric cards. Frames piped to ffmpeg.
# usage: python3 render_nasheed.py <project_dir> <config.json> [--preview SECONDS_START DUR]
import cv2, numpy as np, json, sys, subprocess, math, os
P = sys.argv[1]; C = json.load(open(sys.argv[2]))
W, H, FPS = 1080, 1920, 30
PRE = C['pre']; DUR = C['duration']
preview = '--preview' in sys.argv
if preview:
    i = sys.argv.index('--preview'); T0 = float(sys.argv[i+1]); TD = float(sys.argv[i+2])
else:
    T0, TD = 0.0, DUR
rng = np.random.default_rng(3)

def load_scene(sc):
    im = cv2.imread(os.path.join(P, sc['image']))
    s = W / im.shape[1]
    big = cv2.resize(im, (int(im.shape[1]*s*1.08), int(im.shape[0]*s*1.08)), interpolation=cv2.INTER_LANCZOS4)
    big = cv2.addWeighted(big, 1.25, cv2.GaussianBlur(big, (0, 0), 1.2), -0.25, 0)  # gentle sharpen
    sc['big'] = big.astype(np.float32) / 255
    sc['sx'] = s  # source->output scale
    # precompute glow maps (output coords)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for g in sc.get('glows', []):
        cx, cy = g['x']*s, g['y']*s; r = g['r']
        d = np.sqrt((xx-cx)**2 + ((yy-cy)/g.get('squash', 1.0))**2)
        g['map'] = (np.exp(-(d/r)**2)[..., None] * np.array(g['color'][::-1], np.float32)/255)
    # window mask for rain
    m = np.zeros((H, W), np.float32)
    for (x0, y0, x1, y1) in sc.get('rain_rects', []):
        m[int(y0*s):int(y1*s), int(x0*s):int(x1*s)] = 1
    for (cx, cy, ax, ay) in sc.get('rain_holes', []):
        cv2.ellipse(m, (int(cx*s), int(cy*s)), (int(ax*s), int(ay*s)), 0, 0, 360, 0, -1)
    sc['rainmask'] = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
    # dust particles
    n = sc.get('dust', {}).get('n', 0)
    if n:
        b = sc['dust']['box']
        sc['pp'] = np.c_[rng.uniform(b[0]*s, b[2]*s, n), rng.uniform(b[1]*s, b[3]*s, n),
                         rng.uniform(1.2, 3.2, n), rng.uniform(0, 6.28, n), rng.uniform(0.15, 0.6, n)]
    return sc

scenes = [load_scene(sc) for sc in C['scenes']]
# rain streak texture (tileable), scrolled downward
rain = np.zeros((H*2, W), np.float32)
for _ in range(900):
    x = rng.integers(0, W); y = rng.integers(0, H*2); L = rng.integers(25, 70)
    cv2.line(rain, (x, y), (x+2, y+L), float(rng.uniform(0.25, 0.8)), 1, cv2.LINE_AA)
rain = cv2.GaussianBlur(rain, (0, 0), 0.8)
# vignette + bottom readability gradient
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vig = 1 - 0.38*np.clip(((xx-W/2)/(W*0.72))**2 + ((yy-H*0.45)/(H*0.62))**2, 0, 1)
grad = 1 - 0.58*np.clip((yy - H*0.62)/(H*0.38), 0, 1)**1.4
shade = (vig*grad)[..., None].astype(np.float32)

def load_card(name):
    im = cv2.imread(os.path.join(P, 'txt', name + '.png'), cv2.IMREAD_UNCHANGED)
    return im[..., :3].astype(np.float32)/255, im[..., 3:].astype(np.float32)/255

cards = []  # (start, end, rgb, alpha, y_center, kind)
for c in C['cards']:
    rgb, a = load_card(c['id']); cards.append(dict(c, rgb=rgb, a=a))

def ease(x): x = min(max(x, 0), 1); return x*x*(3-2*x)

def scene_frame(sc, t, tl):
    # tl: local progress 0..1 within scene
    big = sc['big']; bh, bw = big.shape[:2]
    z = (W/bw) * (1 + sc.get('zoom', 0.05)*ease(tl))
    fx, fy = sc['focus'][0]*sc['sx']*1.08, sc['focus'][1]*sc['sx']*1.08  # focus in big coords
    ox, oy = sc['focus'][0]*sc['sx'], sc['focus'][1]*sc['sx']
    # breathing drift
    ox += 6*math.sin(t*0.21); oy += 4*math.sin(t*0.17+1)
    M = np.float32([[z, 0, ox - fx*z], [0, z, oy - fy*z]])
    f = cv2.warpAffine(big, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    # smoke waver
    for (x0, y0, x1, y1) in sc.get('smoke', []):
        X0, Y0, X1, Y1 = [int(v*sc['sx']) for v in (x0, y0, x1, y1)]
        roi = f[Y0:Y1, X0:X1]
        gy, gx = np.mgrid[0:roi.shape[0], 0:roi.shape[1]].astype(np.float32)
        dx = 3.5*np.sin(gy/23 + t*1.7) * (1 - gy/roi.shape[0])
        f[Y0:Y1, X0:X1] = cv2.remap(roi, gx+dx, gy+1.2*np.sin(gx/31+t), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    # glows (screen blend), breathing + flicker
    for g in sc.get('glows', []):
        k = g['base'] + g['amp']*math.sin(t*2*math.pi/g.get('period', 7))
        if g.get('flicker'):
            k += g['flicker']*(0.6*math.sin(t*11.3) + 0.4*math.sin(t*17.9+2) + 0.3*math.sin(t*6.1))
        gm = g['map']*max(k, 0)
        f = 1 - (1 - f)*(1 - gm)
    # rain
    if sc.get('rain_rects'):
        off = int((t*900) % H)
        r = rain[H-off:2*H-off][..., None] * sc.get('rain_amt', 0.16)
        f = f + r*sc['rainmask']*np.array([1.0, 0.92, 0.8], np.float32)
    # dust motes
    if 'pp' in sc:
        layer = np.zeros((H, W), np.float32); pp = sc['pp']
        for x, y, rad, ph, sp in pp:
            px = x + 18*math.sin(t*0.3*sp + ph); py = (y - t*12*sp)
            b = sc['dust']['box']; y0, y1 = b[1]*sc['sx'], b[3]*sc['sx']
            py = y0 + (py - y0) % (y1 - y0)
            a = 0.5 + 0.5*math.sin(t*1.3*sp + ph*3)
            cv2.circle(layer, (int(px), int(py)), int(rad), a, -1, cv2.LINE_AA)
        layer = cv2.GaussianBlur(layer, (0, 0), 1.6)[..., None]*np.array(sc['dust']['color'][::-1], np.float32)/255*sc['dust'].get('amt', 0.5)
        f = 1 - (1 - f)*(1 - layer)
    return f

def compose(t):
    # scene selection with crossfade
    out = None
    for sc in scenes:
        a, b = sc['start'], sc['end']
        if t < a - 0.0001 or t > b: continue
        tl = (t - a)/(b - a)
        fr = scene_frame(sc, t, tl)
        w = 1.0
        xf = C.get('xfade', 1.2)
        if sc is not scenes[0] and t < a + xf: w = ease((t - a)/xf)
        out = fr if out is None else out*(1-w) + fr*w
    f = out*shade
    # global fade in / out
    f *= ease(t/C.get('fade_in', 2.0))*(0.4+0.6*ease((t-C.get('hook_end',0))/1.6)) * (1 - 0.6*ease((t - (DUR-4))/3))*(1 - ease((t-(DUR-0.8))/0.8))
    # light leak sweeps
    for lk in C.get('leaks', []):
        u = (t - lk['t'])/lk['d']
        if 0 <= u <= 1:
            cx = W*(-0.3 + 1.6*u); inten = math.sin(math.pi*u)*lk.get('amt', 0.35)
            m = np.exp(-(((xx-cx)/(W*0.22))**2 + ((yy-H*0.3)/(H*0.6))**2))[..., None]*inten
            f = 1 - (1 - f)*(1 - m*np.array([0.55, 0.78, 1.0], np.float32))
    # text cards
    for c in cards:
        if c['start'] - 0.4 <= t <= c['end'] + 0.4:
            fi = ease((t - c['start'] + 0.15)/0.45); fo = 1 - ease((t - c['end'] + 0.1)/0.4)
            a = min(fi, fo)
            if a <= 0: continue
            rgb, al = c['rgb'], c['a']*a
            if fi < 1:
                k = int(1 + 10*(1-fi)) | 1; rgb = cv2.GaussianBlur(rgb, (k, k), 0); al = cv2.GaussianBlur(al, (k, k), 0)[..., None]*1 if al.ndim == 2 else cv2.GaussianBlur(al[..., 0], (k, k), 0)[..., None]
            h = rgb.shape[0]; y = int(c['y'] - h/2 + 14*(1 - fi))
            y0, y1 = max(y, 0), min(y + h, H)
            f[y0:y1] = f[y0:y1]*(1 - al[y0-y:y1-y]) + rgb[y0-y:y1-y]*al[y0-y:y1-y]
    # grain
    f = f + (rng.standard_normal((H//2, W//2)).astype(np.float32)*0.012).repeat(2, 0).repeat(2, 1)[..., None]
    return np.clip(f*255, 0, 255).astype(np.uint8)

out = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else os.path.join(P, 'video_noaudio.mp4')
if preview: out = os.path.join(P, f'preview_{int(T0)}.mp4')
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
nf = int(TD*FPS)
for i in range(nf):
    ff.stdin.write(compose(T0 + i/FPS).tobytes())
    if i % 300 == 0: print(f'{i}/{nf}', flush=True)
ff.stdin.close(); ff.wait(); print('done', out)
