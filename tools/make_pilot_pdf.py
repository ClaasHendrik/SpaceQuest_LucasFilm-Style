"""Builds docs/pilot_samples.pdf: a short sheet of example screens for the new Lucasfilm-style look.
Usage: python3 tools/make_pilot_pdf.py <pilot_shots_dir> <old_style_pod_png>"""
import sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader, simpleSplit
from PIL import Image

SH, OLD = sys.argv[1], sys.argv[2]
PW, PH = A4
M = 15 * mm
IW = PW - 2 * M
c = canvas.Canvas("docs/pilot_samples.pdf", pagesize=A4)
c.setTitle("Space Quest III (LucasFilm-style) - art pilot")


def para(text, y, size=10, font="Helvetica", width=IW, lead=5.0):
    for ln in simpleSplit(text, font, size, width):
        c.setFont(font, size)
        c.drawString(M, y, ln)
        y -= lead * mm
    return y


def footer(n):
    c.setFont("Helvetica", 8)
    c.setFillGray(0.45)
    c.drawString(M, 8 * mm, "Space Quest III, LucasFilm-style remake - art pilot")
    c.drawRightString(PW - M, 8 * mm, str(n))
    c.setFillGray(0)


def shot(name, y, caption, w=IW * 0.8):
    h = w * 960 / 1280
    x0 = M + (IW - w) / 2
    c.drawImage(ImageReader(os.path.join(SH, name)), x0, y - h, w, h)
    c.setStrokeGray(0.5)
    c.rect(x0, y - h, w, h)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(x0, y - h - 4.5 * mm, caption)
    return y - h - 11 * mm


# ---- page 1: what changed + before/after
y = PH - 25 * mm
c.setFont("Helvetica-Bold", 20)
c.drawString(M, y, "Art pilot: the Lucasfilm look")
y -= 8 * mm
c.setFont("Helvetica", 11)
c.drawString(M, y, "Two rooms, the new interface and the new Roger. Screens are taken from the running game.")
y -= 11 * mm
c.setFont("Helvetica-Bold", 11)
c.drawString(M, y, "What changed")
y -= 6 * mm
for b in [
    "View is now 640x480 (4:3), like your screenshots: a black strip for speech on top, the scene, then the panel.",
    "Scenes are painted with gradients, lighting, glow and texture, then reduced to a 190-colour palette with a light dither. No more flat EGA shapes.",
    "Interface: cyan sentence line, five green verb columns (Push/Pull/Give, Open/Close/Look, Walk to/Pick up/What is, Use/Turn on/Turn off, Talk to/Travel), magenta inventory with scroll arrows. Talk to and Travel are greyed out unless something in the room responds to them.",
    "Speech appears in the top strip in Roger's yellow.",
    "Roger is a new, larger sprite (about a third of the scene height) with an outline and a 4-frame walk cycle, in underwear and in the uniform.",
]:
    y = para("- " + b, y, 9.5, width=IW - 4 * mm)
    y -= 1.5 * mm
y -= 4 * mm
c.setFont("Helvetica-Bold", 11)
c.drawString(M, y, "Before (EGA draft) and after (pilot)")
y -= 4 * mm
hw = (IW - 4 * mm) / 2
old_h = hw * 800 / 1280
new_h = hw * 960 / 1280
c.drawImage(ImageReader(OLD), M, y - old_h, hw, old_h)
c.drawImage(ImageReader(os.path.join(SH, "pilot_1_pod.png")), M + hw + 4 * mm, y - new_h, hw, new_h)
c.setStrokeGray(0.5)
c.rect(M, y - old_h, hw, old_h)
c.rect(M + hw + 4 * mm, y - new_h, hw, new_h)
y -= new_h + 5 * mm
c.setFont("Helvetica-Oblique", 9)
c.drawString(M, y, "Left: previous EGA-style draft.   Right: new pilot.")
y -= 10 * mm
c.setFont("Helvetica-Bold", 11)
c.drawString(M, y, "Roger, new sprite sheet (enlarged)")
y -= 4 * mm
sheet = Image.open("assets/sprites/roger.png").convert("RGBA")
bg = Image.new("RGBA", sheet.size, (52, 62, 84, 255))
bg.alpha_composite(sheet)
bg = bg.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).convert("RGB")
sw = IW
sh_ = sw * bg.height / bg.width
c.drawImage(ImageReader(bg), M, y - sh_, sw, sh_)
footer(1)
c.showPage()

# ---- page 2
y = PH - 20 * mm
y = shot("pilot_2_locker_open.png", y, "Escape pod: locker open, pointing at the uniform ('Pick up uniform').")
y = shot("pilot_3_uniform_in_inventory.png", y, "The uniform is in the inventory (magenta). 'Use' puts it on.")
footer(2)
c.showPage()

# ---- page 3
y = PH - 20 * mm
y = shot("pilot_4_garbage_mountain.png", y, "Garbage mountain: speech in the top strip, in Roger's yellow, wearing the uniform.")
y = shot("pilot_5_with_wire.png", y, "After picking up the wire: +5 points, wire in the inventory.")
y -= 2 * mm
c.setFont("Helvetica-Bold", 11)
c.drawString(M, y, "Honest limits of this draft")
y -= 6 * mm
y = para("The art is painted by code, not by hand, so it has the lighting, depth and texture of the Lucasfilm look but not the fine hand-drawn detail. "
         "The pod and the fighter wreck in the garbage mountain are a little cleaner than the junk around them. Treat all of it as strong placeholder art. "
         "The other 29 rooms still use the earlier EGA draft until this style is approved.", y, 9.5)
footer(3)
c.showPage()
c.save()
print("ok")
