"""PDF overview of the Act 1 reference screens where Roger blocks part of the picture, so that second screenshots (Roger elsewhere)
can be collected. Usage: python3 roger_overview.py <dir with sNNN.png> <out.pdf>"""
import sys, json
import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.lib.units import mm
from restyle import load_indices, figure_mask

SRC, OUT = sys.argv[1], sys.argv[2]
# room name, screen, box around Roger (screen coordinates 320x200), what Roger is doing, note, second screenshot already there?
ROOMS = [
    ("Crash site (start of the game)", 14, (129, 92, 152, 121), "sitting in the pod's window", "", None),
    ("Junk field", 15, (102, 95, 132, 145), "standing on the floor, left of the middle", "", None),
    ("Junk field with the lift tower", 16, (232, 38, 262, 82), "standing on the lift platform", "the magenta lift platform is partly caught in the yellow area", None),
    ("Top of the lift", 17, (245, 92, 268, 122), "standing on the small magenta platform", "this screen is not in the room plan yet", None),
    ("The conveyor", 18, (4, 136, 34, 158), "crouching at the left end of the belt", "", None),
    ("On the rail", 19, (152, 98, 174, 136), "walking on the rail", "", None),
    ("The rail by the window", 20, None, "standing on the rail in front of the control room window", "", None),
    ("The rail tower", 21, (232, 140, 256, 158), "riding on the grabber at the right", "the grabber itself stays; only Roger is marked", None),
    ("Entrance to the tube", 25, (48, 120, 68, 150), "standing in the left arch", "", None),
    ("Inside the tube", 26, ("outline", 155, 125, 172, 152), "standing at the left of the creature", "the grey creature right of him is the 'rat'; it is not marked", None),
    ("The robot head", 27, None, "standing at the left of the green panel", "", None),
    ("The dark room", 23, (78, 106, 100, 130), "standing at the left", "screen 24 shows the same room with Roger at the right, but in different lighting, so the two cannot be merged directly: a third screenshot with the same lighting as 23 would help", 24),
    ("Shuttle yard with the ladder", 28, (190, 64, 212, 106), "climbing the ladder", "screen 22 shows the yard without him: already solved", 22),
]
R = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}


def mask_for(n, box):
    if box is not None and box[0] == 'outline':       # the scenery has Roger's skin colour here: mark his box instead of exact pixels
        idx = load_indices(f"{SRC}/s{n:03d}.png", 10, 190)
        m = np.zeros(idx.shape, bool)
        _, x0, y0, x1, y1 = box
        m[y0 - 10:y1 - 10 + 1, x0:x1 + 1] = True
        m[y0 - 9:y1 - 10, x0 + 1:x1] = False
        return idx, m
    idx = load_indices(f"{SRC}/s{n:03d}.png", 10, 190)
    if box is None:
        m = np.zeros(idx.shape, bool)
        for b, _ in R.get(str(n), []):
            m |= figure_mask(idx, tuple(b))
        return idx, m
    return idx, figure_mask(idx, box)


PW, PH = landscape(A4)
M = 12 * mm
c = canvas.Canvas(OUT, pagesize=landscape(A4))
c.setTitle("Act 1: where Roger blocks the picture")
rows = []
for name, n, box, what, note, second in ROOMS:
    idx, m = mask_for(n, box)
    ys, xs = np.nonzero(m)
    rows.append((name, n, idx, m, what, note, second, (xs.mean() if len(xs) else 160.0), int(m.sum())))

# ---------------------------------------------------------------- page 1: what I need
c.setFont("Helvetica-Bold", 20)
c.drawString(M, PH - 18 * mm, "Act 1: where Roger blocks the original screens")
c.setFont("Helvetica", 10.5)
y = PH - 27 * mm
for ln in simpleSplit(
    "Idea: for every room where Roger hides part of the picture, one more screenshot of the SAME room with Roger standing somewhere else is enough. "
    "I then fill each hidden pixel from the other screenshot, so that no pixel has to be invented, and I paint the whole room from the combined picture.", "Helvetica", 10.5, PW - 2 * M):
    c.drawString(M, y, ln); y -= 5 * mm
y -= 2 * mm
c.setFont("Helvetica-Bold", 11); c.drawString(M, y, "What a good second screenshot looks like"); y -= 6 * mm
c.setFont("Helvetica", 10)
for t in ["- Same room, same lighting, same things on the screen (the claw, the ladder, the pod, and so on in the same places). Only Roger has moved.",
          "- Roger must NOT stand on the yellow area of the room's first screenshot. The farther from it the better; the far left or far right of the room is ideal.",
          "- If Roger can leave the screen, a screenshot without him is best.",
          "- The room's walk area is usually a strip along the floor, so 'stand at the other end' is normally easy.",
          "- Pages 2 to 8 show each room: the original, and in yellow the exact pixels Roger covers."]:
    for ln in simpleSplit(t, "Helvetica", 10, PW - 2 * M - 4 * mm):
        c.drawString(M + 3 * mm, y, ln); y -= 4.6 * mm
y -= 4 * mm
c.setFont("Helvetica-Bold", 11); c.drawString(M, y, "Summary"); y -= 6 * mm
c.setFont("Helvetica-Bold", 9)
c.drawString(M, y, "Room"); c.drawString(M + 78 * mm, y, "Screen"); c.drawString(M + 98 * mm, y, "Roger hides"); c.drawString(M + 126 * mm, y, "What I need")
y -= 5 * mm
c.setFont("Helvetica", 9)
for name, n, idx, m, what, note, second, cx, npx in rows:
    side = "the left" if cx < 106 else ("the middle" if cx < 214 else "the right")
    need = "nothing: already solved" if (second == 22) else ("a 3rd screenshot, same lighting" if second else "Roger on the %s" % ("right" if cx < 160 else "left"))
    c.drawString(M, y, name); c.drawString(M + 78 * mm, y, "s%03d" % n); c.drawString(M + 98 * mm, y, "%d px (%s)" % (npx, side)); c.drawString(M + 126 * mm, y, need)
    y -= 4.8 * mm
c.setFont("Helvetica-Oblique", 8.5)
y -= 3 * mm
c.drawString(M, y, "Roger's hidden pixels are small (a few hundred of 60,800 per picture), but they sit in the middle of the action, which is why they were hard to patch.")
c.showPage()

# ---------------------------------------------------------------- pages 2..: two rooms per page
tw = 118 * mm
for i in range(0, len(rows), 2):
    y0 = PH - M
    for name, n, idx, m, what, note, second, cx, npx in rows[i:i + 2]:
        box_ok = n != 26
        im = np.asarray(Image.open(f"{SRC}/s{n:03d}.png").convert("RGB"))[10:200].copy()
        ov = im.copy()
        ov[m] = (255, 255, 0)
        # a thin outline of the mask so the shape is visible even over yellow scenery
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M, y0 - 4 * mm, "%s   (screen s%03d)" % (name, n))
        th = tw * 190 / 320
        yy = y0 - 8 * mm - th
        c.drawImage(ImageReader(Image.fromarray(im).resize((640, 380), Image.NEAREST)), M, yy, tw, th)
        c.drawImage(ImageReader(Image.fromarray(ov).resize((640, 380), Image.NEAREST)), 2 * M + tw + 4 * mm, yy, tw, th)
        c.setFont("Helvetica", 8); c.setFillGray(0.4)
        c.drawString(M, yy - 3.5 * mm, "original"); c.drawString(2 * M + tw + 4 * mm, yy - 3.5 * mm, "the %d pixels Roger covers (yellow)" % npx if box_ok else "Roger (yellow outline)"); c.setFillGray(0)
        c.setFont("Helvetica", 9)
        txt = "Roger is %s." % what
        if note:
            txt += " " + note + "."
        side = "right" if cx < 160 else "left"
        if second == 22:
            txt += " Nothing more needed."
        elif second:
            pass
        else:
            txt += " Please send a screenshot of this room with Roger standing on the %s side, away from the yellow area." % side
        ty = yy - 8 * mm
        for ln in simpleSplit(txt, "Helvetica", 9, PW - 2 * M):
            c.drawString(M, ty, ln); ty -= 4.2 * mm
        y0 = yy - 24 * mm
    c.showPage()
c.save()
print(len(rows), "rooms")
