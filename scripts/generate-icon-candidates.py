# -*- coding: utf-8 -*-
"""Celadon & Frond Theme - icon candidates. Code-drawn, transparent, flat."""
import io, math, os
from PIL import Image, ImageDraw, ImageFont

S = 3
W = 1024
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "logo-candidates")

MINT = (193, 230, 212, 255)
DEEP = (23, 58, 51, 255)
LAV = (186, 192, 227, 255)
PURPLE = (199, 154, 212, 255)
PEACH = (232, 207, 192, 255)
CREAM = (230, 232, 210, 255)
INK = DEEP

LIGHT_BG = (198, 216, 208, 255)
DARK_BG = (23, 45, 40, 255)
LIGHT_INK = (23, 58, 51, 255)
DARK_INK = (230, 232, 210, 255)
FONT_DIR = r"C:\Windows\Fonts"

def font(name, size):
    try: return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception: return ImageFont.load_default()

def scr(p): return (p[0]*S, p[1]*S)
def wd(v): return max(1, int(round(v*S)))
def canvas(): return Image.new("RGBA", (W*S, W*S), (0,0,0,0))
def finish(img): return img.resize((W, W), Image.LANCZOS)

def bez(p0, p1, p2, n=64):
    pts = []
    for i in range(n+1):
        t = i/n; u = 1-t
        pts.append((u*u*p0[0]+2*u*t*p1[0]+t*t*p2[0],
                    u*u*p0[1]+2*u*t*p1[1]+t*t*p2[1]))
    return pts

def poly(d, pts, fill):
    d.polygon([scr(p) for p in pts], fill=fill)

def disc(d, center, r, fill):
    d.ellipse([center[0]*S-r*S, center[1]*S-r*S,
               center[0]*S+r*S, center[1]*S+r*S], fill=fill)

def rrect(d, box, radius, fill):
    d.rounded_rectangle([box[0]*S, box[1]*S, box[2]*S, box[3]*S],
                        radius=radius*S, fill=fill)

def line(d, pts, color, width):
    d.line([scr(p) for p in pts], fill=color, width=wd(width), joint="curve")

def leaf(d, cx, cy, ang, length, width, fill):
    right = bez((0,0), (width, -length*0.5), (0, -length))
    left = bez((0,-length), (-width, -length*0.5), (0,0))
    ca, sa = math.cos(ang), math.sin(ang)
    poly(d, [(cx + x*ca - y*sa, cy + x*sa + y*ca)
             for (x,y) in right + left], fill)

def frond(d, x, y, ang, scale, color):
    ca, sa = math.cos(ang), math.sin(ang)
    tip = (x + 380*scale*ca, y + 380*scale*sa)
    line(d, [(x, y), tip], DEEP, 9)
    for f in (0.34, 0.68):
        bx = x + 380*scale*f*ca
        by = y + 380*scale*f*sa
        ln = 190*scale*(1 - f*0.25)
        leaf(d, bx, by, ang - 0.95, ln, ln*0.5, color)
        leaf(d, bx, by, ang + 0.95, ln, ln*0.5, color)

def arch(d, x0, x1, top, bottom, fill):
    r = (x1-x0)//2
    cx = (x0+x1)//2
    d.pieslice([x0*S, top*S, x1*S, (top+2*r)*S], 180, 360, fill=fill)
    d.rectangle([x0*S, (top+r)*S, x1*S, bottom*S], fill=fill)

def cand_arch_frond():
    img = canvas(); d = ImageDraw.Draw(img)
    arch(d, 300, 724, 200, 830, MINT)
    disc(d, (512, 430), 110, CREAM)
    frond(d, 400, 830, math.radians(-58), 0.72, LAV)
    frond(d, 620, 830, math.radians(-122), 0.72, PURPLE)
    return finish(img)

def cand_twin_frond():
    img = canvas(); d = ImageDraw.Draw(img)
    disc(d, (512, 512), 300, MINT)
    frond(d, 380, 800, math.radians(-62), 0.85, LAV)
    frond(d, 644, 800, math.radians(-118), 0.85, PURPLE)
    return finish(img)

def cand_wreath():
    img = canvas(); d = ImageDraw.Draw(img)
    for i in range(6):
        a = -math.pi/2 + i*math.pi/3
        bx = 512 + 240*math.cos(a)
        by = 512 + 240*math.sin(a)
        leaf(d, bx, by, a + math.pi/2, 150, 58, LAV if i % 2 else PURPLE)
    disc(d, (512, 512), 92, CREAM)
    return finish(img)

def cand_vase():
    img = canvas(); d = ImageDraw.Draw(img)
    poly(d, [(420, 470), (604, 470), (656, 740), (582, 842),
             (442, 842), (368, 740)], MINT)
    rrect(d, (424, 432, 600, 492), 16, DEEP)
    frond(d, 512, 462, math.radians(-72), 0.62, LAV)
    frond(d, 512, 462, math.radians(-108), 0.62, PURPLE)
    return finish(img)

def cand_niche():
    img = canvas(); d = ImageDraw.Draw(img)
    arch(d, 210, 814, 180, 880, MINT)
    arch(d, 268, 756, 240, 880, PEACH)
    arch(d, 326, 698, 300, 880, CREAM)
    disc(d, (512, 470), 90, LAV)
    return finish(img)

def cand_trio():
    img = canvas(); d = ImageDraw.Draw(img)
    rrect(d, (270, 820, 754, 884), 30, PEACH)
    for x, a, c, s in ((386, -64, LAV, 0.7),
                       (512, -90, PURPLE, 0.85),
                       (638, -116, LAV, 0.7)):
        frond(d, x, 840, math.radians(a), s, c)
    return finish(img)

CANDIDATES = [
    ("01", "arch-frond", cand_arch_frond),
    ("02", "twin-frond", cand_twin_frond),
    ("03", "frond-wreath", cand_wreath),
    ("04", "celadon-vase", cand_vase),
    ("05", "nested-arch", cand_niche),
    ("06", "frond-trio", cand_trio),
]

def centered_text(d, center, text, fnt, fill):
    b = d.textbbox((0,0), text, font=fnt)
    d.text((center[0]-(b[2]-b[0])/2-b[0], center[1]-(b[3]-b[1])/2-b[1]),
           text, font=fnt, fill=fill)

def contact_sheet(icons, bg, ink, path):
    cw, ch = 420, 540
    margin, gap, head = 40, 26, 118
    sw = margin*2 + cw*3 + gap*2
    sh = margin + head + ch*2 + gap + margin
    sheet = Image.new("RGBA", (sw, sh), bg)
    d = ImageDraw.Draw(sheet)
    ft = font("segoeuib.ttf", 40); fn = font("segoeuib.ttf", 30)
    fna = font("segoeui.ttf", 26); fs = font("segoeui.ttf", 20)
    centered_text(d, (sw/2, margin+34), "CELADON & FROND THEME", ft, ink)
    centered_text(d, (sw/2, margin+82), "icon candidates", fs, ink)
    for idx, (num, name, icon) in enumerate(icons):
        row, col = divmod(idx, 3)
        gx = margin + col*(cw+gap); gy = margin + head + row*(ch+gap)
        sheet.alpha_composite(icon.resize((260,260), Image.LANCZOS),
                              (gx+(cw-260)//2, gy+30))
        centered_text(d, (gx+cw/2, gy+330), num, fn, ink)
        centered_text(d, (gx+cw/2, gy+372), name, fna, ink)
        centered_text(d, (gx+cw/2, gy+404), "1024 x 1024  PNG", fs, ink)
    save_png(sheet.convert("RGB"), path)

def inline_strip(icons, path):
    size, gap, margin = 150, 18, 30
    sw = margin*2 + size*len(icons) + gap*(len(icons)-1)
    sh = margin*2 + size + 34
    strip = Image.new("RGBA", (sw, sh), LIGHT_BG)
    d = ImageDraw.Draw(strip)
    fn = font("segoeuib.ttf", 20)
    for idx, (num, _n, icon) in enumerate(icons):
        x = margin + idx*(size+gap)
        strip.alpha_composite(icon.resize((size,size), Image.LANCZOS), (x, margin))
        centered_text(d, (x+size/2, margin+size+16), num, fn, LIGHT_INK)
    save_png(strip.convert("RGB"), path)

def save_png(img, path):
    buf = io.BytesIO(); img.save(buf, format="PNG")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh: fh.write(buf.getvalue())

def main():
    os.makedirs(OUT, exist_ok=True)
    icons = []
    for num, name, fn in CANDIDATES:
        icon = fn(); box = icon.getbbox()
        if box is None: raise AssertionError("%s empty" % name)
        if box[0] < 70 or box[1] < 70 or box[2] > 954 or box[3] > 954:
            raise AssertionError("%s out of safe area: %s" % (name, box))
        save_png(icon, os.path.join(OUT, "%s-%s.png" % (num, name)))
        print("wrote", num, name, box)
        icons.append((num, name, icon))
    contact_sheet(icons, LIGHT_BG, LIGHT_INK, os.path.join(OUT, "contact-light.png"))
    contact_sheet(icons, DARK_BG, DARK_INK, os.path.join(OUT, "contact-dark.png"))
    inline_strip(icons, os.path.join(OUT, "inline-strip.png"))
    print("wrote contact sheets")

if __name__ == "__main__": main()


