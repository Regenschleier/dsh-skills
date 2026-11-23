"""Seamless 4K live-wallpaper loop from one portrait still.

Composition: sharp figure centred on a blurred, brightness-matched bed of the same
image (oval feather -> reads as depth of field, not a pasted panel).
Motion: breathing push on the figure, slow drift on the bed, two snow layers,
pulsing warm bloom. All periodic over N_FRAMES.

Usage: python make_wallpaper.py <src> <out.mp4> [only_N_frames]
"""
import math
import os
import sys
import random
from PIL import Image, ImageFilter, ImageDraw

W, H = 3840, 2160
FPS = 24
SECONDS = 20
N_FRAMES = FPS * SECONDS

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\uniform-rain\AppData\Local\Comfy-Desktop\ComfyUI-Shared\input\ref_wallpaper_src.png"
OUT_MP4 = sys.argv[2] if len(sys.argv) > 2 else r"C:\Users\uniform-rain\Desktop\ai图\壁纸_紫发少女_雪林_4K.mp4"
ONLY = int(sys.argv[3]) if len(sys.argv) > 3 else 0


def oval_mask(size, cx=0.5, cy=0.5, rx=0.52, ry=0.57, plateau=0.46):
    gw, gh = 200, 200
    grad = Image.new("L", (gw, gh), 0)
    gp = grad.load()
    for yy in range(gh):
        ny = (yy / (gh - 1) - cy) / ry
        for xx in range(gw):
            nx = (xx / (gw - 1) - cx) / rx
            r = math.sqrt(nx * nx + ny * ny)
            if r <= plateau:
                a = 255
            elif r >= 1.0:
                a = 0
            else:
                u = (r - plateau) / (1.0 - plateau)
                a = int(255 * (1 - u * u * (3 - 2 * u)))
            gp[xx, yy] = a
    return grad.resize(size, Image.BICUBIC)


def build():
    src = Image.open(SRC).convert("RGB")

    # --- bed: cover-fill the canvas, heavy blur (softness is invisible after blur)
    cover = max(W / src.width, H / src.height) * 1.06
    bw, bh = int(src.width * cover), int(src.height * cover)
    bed = Image.eval(src.resize((bw, bh), Image.LANCZOS), lambda v: int(v * 0.86)).filter(ImageFilter.GaussianBlur(22))

    # --- figure: 99% of canvas height, oval-feathered
    sub_h = int(H * 0.99)
    sub_w = int(round(src.width * sub_h / src.height))
    sub = src.resize((sub_w, sub_h), Image.LANCZOS).convert("RGBA")
    sub.putalpha(oval_mask((sub_w, sub_h)))

    # --- bloom (kept inside its tile so no square edge)
    glow = Image.new("RGBA", (1600, 1600), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(24, 0, -1):
        r = 30 + i * 27
        alpha = int(9 * (1 - i / 24) ** 0.6) + 2
        gd.ellipse([800 - r, 800 - r, 800 + r, 800 + r], fill=(255, 206, 140, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    levels = []
    for k in range(6):
        g = glow.copy()
        g.putalpha(g.split()[3].point(lambda v, k=k: min(255, int(v * (0.22 + 0.11 * k)))))
        levels.append(g)
    return bed, sub, levels


def vignette():
    vg = Image.new("L", (160, 90), 0)
    vp = vg.load()
    for yy in range(90):
        for xx in range(160):
            dx = (xx / 159 - 0.5) * 1.28
            dy = (yy / 89 - 0.5) * 1.28
            r = min(1.0, math.sqrt(dx * dx + dy * dy) / 0.90)
            vp[xx, yy] = int(255 * (1 - 0.42 * r * r))
    return vg.resize((W, H), Image.BICUBIC)


def snow():
    rnd = random.Random(20260101)
    return [(rnd.uniform(0, W), rnd.uniform(0, H),
             rnd.uniform(26, 130) * (H / 1080),
             rnd.choice([2, 2, 3, 3, 4, 5, 7]),
             rnd.randint(70, 190),
             rnd.uniform(-18, 26)) for _ in range(260)]


def frame(t):
    ph = 2 * math.pi * t
    bed, sub, levels = LAYERS

    # bed drift (parallax, small)
    bx = int(round((bed.width - W) / 2 + 26 * math.sin(ph)))
    by = int(round((bed.height - H) / 2 + 14 * math.sin(ph + 0.8)))
    img = bed.crop((bx, by, bx + W, by + H)).copy()

    # figure: breathing push + slight independent drift
    s = 1.0 + 0.022 * math.sin(ph)
    tx = int(round(9 * math.sin(ph + 0.4)))
    ty = int(round(11 * math.sin(ph + 1.7)))
    bcx, bcy = W // 2 + tx, H // 2 + ty
    a = 1.0 / s
    c = sub.width / 2 - bcx * a
    f = sub.height / 2 - bcy * a
    layer = sub.transform((W, H), Image.AFFINE, (a, 0, c, 0, a, f),
                          resample=Image.BILINEAR, fillcolor=(0, 0, 0, 0))

    img = img.convert("RGBA")
    img.alpha_composite(layer)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for (x0, y0, spd, size, alpha, drift) in SNOW:
        x = (x0 + drift * SECONDS * t) % W
        y = (y0 + spd * SECONDS * t) % (H + 200) - 100
        aa = int(alpha * (0.55 + 0.45 * math.sin(ph * 3 + x0)))
        d.ellipse([x - size, y - size, x + size, y + size], fill=(255, 255, 255, max(0, aa)))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(1.2)))

    img.alpha_composite(levels[int((0.5 + 0.5 * math.sin(ph)) * 5)], (int(W * 0.58), int(H * 0.01)))

    out = img.convert("RGB")
    out = Image.composite(out, Image.new("RGB", (W, H), (4, 4, 6)), VIGNETTE)
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    LAYERS = build()
    SNOW = snow()
    VIGNETTE = vignette()
    print("built in %.1fs bed=%s sub=%s" % (time.time() - t0, LAYERS[0].size, LAYERS[1].size), flush=True)

    if ONLY:
        for i in range(ONLY):
            frame(i / N_FRAMES).save(os.path.join(os.path.dirname(OUT_MP4), "_test_%02d.png" % i))
        print("test %d frames in %.1fs (%.2f s/frame)" % (ONLY, time.time() - t0, (time.time() - t0) / ONLY), flush=True)
        sys.exit(0)

    import av
    container = av.open(OUT_MP4, mode="w")
    stream = container.add_stream("libx264", rate=FPS)
    stream.width, stream.height = W, H
    stream.pix_fmt = "yuv420p"
    stream.options = {"crf": "19", "preset": "medium", "profile": "high", "level": "5.1"}
    t1 = time.time()
    for i in range(N_FRAMES):
        for pkt in stream.encode(av.VideoFrame.from_image(frame(i / N_FRAMES))):
            container.mux(pkt)
        if i % 48 == 0:
            print("frame %d/%d  %.0fs" % (i, N_FRAMES, time.time() - t1), flush=True)
    for pkt in stream.encode():
        container.mux(pkt)
    container.close()
    print("done %s in %.0fs" % (OUT_MP4, time.time() - t1), flush=True)
