"""Build the Slacking with Swift app icon from the shipped PaulFront sprite.

Takes the front-facing (he's looking at you) pose, crops the head, upscales it with
nearest-neighbour so the 8-bit pixels stay hard-edged, and lights it like a horror
poster: cold desaturated skin, red uplight from below, glowing eyes, heavy vignette.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math, sys

SRC = "/Users/nickmelekian/Desktop/PaulAIWorkshop/PaulGame/PaulGame/PaulGame/Assets.xcassets/PaulFront.imageset/PaulFront.png"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/private/tmp/icon.png"
S = 1024

INK = (14, 10, 18)
ALARM = (255, 45, 40)

# Head bounding box in the source sprite (measured from the alpha silhouette).
HEAD = (340, 8, 528, 232)


def radial(size, cx, cy, radius, inner=255, outer=0):
    """Grayscale radial falloff mask, smoothstepped."""
    m = Image.new("L", (size, size), outer)
    px = m.load()
    for y in range(size):
        dy = (y - cy) ** 2
        for x in range(size):
            d = math.sqrt((x - cx) ** 2 + dy) / radius
            if d >= 1.0:
                continue
            t = 1.0 - d
            t = t * t * (3 - 2 * t)  # smoothstep
            px[x, y] = int(outer + (inner - outer) * t)
    return m


def main():
    src = Image.open(SRC).convert("RGBA")
    head = src.crop(HEAD)

    # --- recolour the head: cold, drained, slightly sickly -------------------
    hw, hh = head.size
    px = head.load()
    eyes = []
    for y in range(hh):
        for x in range(hw):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            # blue iris pixels -> collect, then burn them out to hot red
            if b > 105 and b > r + 28 and not (r > 200 and g > 200):
                eyes.append((x, y))
                px[x, y] = (150, 12, 8, a)
                continue
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            # desaturate hard, crush the midtones, tint the shadows cold blue
            r2 = lum * 0.90 + r * 0.10
            g2 = lum * 0.94 + g * 0.06
            b2 = lum * 0.90 + b * 0.10
            k = 0.20 + 0.80 * (lum / 255.0) ** 2.6
            px[x, y] = (
                int(min(255, r2 * k * 0.86)),
                int(min(255, g2 * k * 0.94)),
                int(min(255, b2 * k * 1.00 + 4)),
                a,
            )

    # --- scale up, nearest neighbour so the pixel art stays blocky ----------
    scale = 5
    head = head.resize((hw * scale, hh * scale), Image.NEAREST)
    HW, HH = head.size

    # where the head lands on the canvas: large, low, cropped by the bottom edge
    hx = (S - HW) // 2
    hy = int(S * -0.06)
    ex_scale = lambda p: (hx + p[0] * scale + scale // 2, hy + p[1] * scale + scale // 2)

    # --- background: ink + red bloom behind the head ------------------------
    canvas = Image.new("RGBA", (S, S), INK + (255,))
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    glow.paste(ALARM + (255,), (0, 0, S, S), radial(S, S // 2, int(S * 0.52), int(S * 0.44), 78, 0))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    canvas = Image.alpha_composite(canvas, glow)

    # a hard red floor-light under the chin, so he's lit from below
    floor = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    floor.paste((255, 70, 35, 255), (0, 0, S, S), radial(S, S // 2, int(S * 1.06), int(S * 0.52), 205, 0))
    floor = floor.filter(ImageFilter.GaussianBlur(60))
    canvas = Image.alpha_composite(canvas, floor)

    # --- silhouette rim glow: red light leaking around his outline ----------
    rim = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    solid = Image.new("RGBA", (S, S), (255, 60, 45, 255))
    alpha = Image.new("L", (S, S), 0)
    alpha.paste(head.getchannel("A"), (hx, hy))
    rim.paste(solid, (0, 0), alpha)
    rim = rim.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, rim)
    canvas = Image.alpha_composite(canvas, rim)

    # --- the head itself ----------------------------------------------------
    canvas.paste(head, (hx, hy), head)

    # uplight pass: brighten the lower half of the face toward red
    up = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    upmask = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(upmask)
    for y in range(S):
        t = max(0.0, (y - S * 0.38) / (S * 0.62))
        d.line([(0, y), (S, y)], fill=int(150 * min(1.0, t) ** 2.2))
    upmask = ImageChops.multiply(upmask, alpha)
    up.paste((255, 70, 50, 255), (0, 0, S, S), upmask)
    up = up.filter(ImageFilter.GaussianBlur(6))
    canvas = Image.alpha_composite(canvas, up)

    # top-down shadow: kill the light on his brow and hair
    shade = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    smask = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(smask)
    for y in range(S):
        t = max(0.0, 1.0 - y / (S * 0.74))
        d.line([(0, y), (S, y)], fill=int(246 * t ** 0.80))
    smask = ImageChops.multiply(smask, alpha)
    shade.paste((3, 2, 7, 255), (0, 0, S, S), smask)
    canvas = Image.alpha_composite(canvas, shade)

    # --- glowing eyes -------------------------------------------------------
    if eyes:
        xs = [e[0] for e in eyes]
        mid = (min(xs) + max(xs)) / 2
        left = [e for e in eyes if e[0] < mid]
        right = [e for e in eyes if e[0] >= mid]
        bloom = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bloom)
        for cluster in (left, right):
            if not cluster:
                continue
            cx = sum(e[0] for e in cluster) / len(cluster)
            cy = sum(e[1] for e in cluster) / len(cluster)
            cx, cy = ex_scale((cx, cy))
            for rad, col in ((96, (255, 26, 18, 140)), (46, (255, 62, 34, 210)), (17, (255, 170, 140, 235))):
                bd.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=col)
        bloom = bloom.filter(ImageFilter.GaussianBlur(14))
        canvas = Image.alpha_composite(canvas, bloom)
        # one hot pupil per eye, sitting on top of the bloom
        core = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        cd = ImageDraw.Draw(core)
        for cluster in (left, right):
            if not cluster:
                continue
            cx = sum(e[0] for e in cluster) / len(cluster)
            cy = sum(e[1] for e in cluster) / len(cluster)
            cx, cy = ex_scale((cx, cy))
            cd.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 228, 214, 255))
        core = core.filter(ImageFilter.GaussianBlur(3))
        canvas = Image.alpha_composite(canvas, core)

    # --- horizontal flare streaks off each eye ------------------------------
    if eyes:
        streak = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        sd = ImageDraw.Draw(streak)
        for cluster in (left, right):
            if not cluster:
                continue
            cx = sum(e[0] for e in cluster) / len(cluster)
            cy = sum(e[1] for e in cluster) / len(cluster)
            cx, cy = ex_scale((cx, cy))
            sd.rectangle([cx - 150, cy - 4, cx + 150, cy + 4], fill=(255, 60, 40, 120))
        streak = streak.filter(ImageFilter.GaussianBlur(12))
        canvas = Image.alpha_composite(canvas, streak)

    # --- security-camera grot: scanlines, then grain ------------------------
    lines = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lines)
    for y in range(0, S, 4):
        ld.line([(0, y), (S, y)], fill=(0, 0, 0, 46))
        ld.line([(0, y + 1), (S, y + 1)], fill=(0, 0, 0, 22))
    canvas = Image.alpha_composite(canvas, lines)

    import random
    random.seed(7)
    grain = Image.new("L", (S // 2, S // 2))
    grain.putdata([random.randint(0, 255) for _ in range((S // 2) ** 2)])
    grain = grain.resize((S, S), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.6))
    noise = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    noise.paste((255, 240, 235, 255), (0, 0, S, S), grain.point(lambda v: 26 if v > 210 else 0))
    noise.paste((0, 0, 0, 255), (0, 0, S, S), grain.point(lambda v: 30 if v < 44 else 0))
    canvas = Image.alpha_composite(canvas, noise)

    # --- vignette -----------------------------------------------------------
    vig = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    vmask = radial(S, S // 2, int(S * 0.44), int(S * 0.72), 0, 252)
    vig.paste((5, 3, 10, 255), (0, 0, S, S), vmask)
    canvas = Image.alpha_composite(canvas, vig)

    canvas.convert("RGB").save(OUT)
    print("wrote", OUT)


main()
