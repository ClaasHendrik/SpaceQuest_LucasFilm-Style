"""Builds docs/act1_walkthrough.pdf: the Act 1 route with points, plus sample screens.
Usage: python3 tools/make_act1_pdf.py <shots_dir>   (shots from tests/shot_act1.gd)"""
import json, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader, simpleSplit

SH = sys.argv[1]
PW, PH = A4
M = 15 * mm
IW = PW - 2 * M
pts = {e["id"]: e for e in json.load(open("data/points.json"))}
c = canvas.Canvas("docs/act1_walkthrough.pdf", pagesize=A4)
c.setTitle("Space Quest III (LucasFilm-style) - Act 1")


def footer(n):
    c.setFont("Helvetica", 8)
    c.setFillGray(0.45)
    c.drawString(M, 8 * mm, "Space Quest III, LucasFilm-style remake - Act 1: The Garbage Freighter")
    c.drawRightString(PW - M, 8 * mm, str(n))
    c.setFillGray(0)


def para(text, y, size=9.5, font="Helvetica", width=IW, lead=4.6, x=M):
    for ln in simpleSplit(text, font, size, width):
        c.setFont(font, size)
        c.drawString(x, y, ln)
        y -= lead * mm
    return y


STEPS = [
    ("Escape pod", "Open the wall locker, take the uniform, then Use it to put it on. Leaving in your underwear is fatal (frostbite).", []),
    ("Garbage mountain", "Pick up the wire. Go east to the robot head.", ["wire"]),
    ("Robot head", "Use the broken eye to climb in and see the Mallard's open panel. Don't touch the chasm or the metal plate. Go back and south.", ["robot_eye"]),
    ("Conveyor", "A clock is running: the crusher is coming. Use the trash bucket to be carried up to the rail.", ["trash_bucket"]),
    ("Overhead rail", "Use the rail to jump up, then Use the grabber to climb on. Click along the rail to ride it. At the pedestal (left) Push the grabber to lift the warp motivator; ride to the ship's open panel (right) and Push again. Get off, then Use the blue chute at the left end of the rail.", ["jump_rail", "grab_motivator", "install_motivator", "fall_chute"]),
    ("Reactor cavern", "Another clock: the rat. Pick up the portable ladder, then Use the iron ladder to climb to the crane cabin.", ["get_ladder"]),
    ("Crane cabin", "Push the stick until the reticle is over the reactor pit, then Push the red button to grab the reactor. Push the stick again to move to the construction bay and Push the button to drop it. Then use the hatch to climb down.", ["get_reactor"]),
    ("Construction bay", "Pick up the reactor. Use the ladder with the ship, Open the top hatch, then Use the reactor and the wire with the engine panel. Open the ramp to board.", ["ladder_ship_top", "open_hatch", "install_reactor", "install_wire"]),
    ("Cockpit", "Use the pilot's seat to search it for buckazoids. Use the computer: switch on Engines and Radar, then Takeoff; turn on Weapons and Front shields, then Fire. Radar off or shields off is fatal.", ["search_cushion", "escape_freighter"]),
]

y = PH - 25 * mm
c.setFont("Helvetica-Bold", 20)
c.drawString(M, y, "Act 1: The Garbage Freighter")
y -= 8 * mm
c.setFont("Helvetica", 11)
c.drawString(M, y, "Route, points and example screens. Playable from the first screen to the escape.")
y -= 10 * mm
total = 0
for room, text, ev in STEPS:
    c.setFont("Helvetica-Bold", 10)
    p_ = sum(pts[e]["points"] for e in ev)
    total += p_
    c.drawString(M, y, room + ("   (%d points)" % p_ if p_ else ""))
    y -= 4.6 * mm
    y = para(text, y, x=M + 4 * mm, width=IW - 4 * mm)
    for e in ev:
        c.setFont("Helvetica-Oblique", 8.5)
        c.setFillGray(0.35)
        c.drawString(M + 8 * mm, y, "+%d  %s" % (pts[e]["points"], pts[e]["description"]))
        c.setFillGray(0)
        y -= 4.0 * mm
    y -= 2.5 * mm
c.setFont("Helvetica-Bold", 11)
c.drawString(M, y - 2 * mm, "Act 1 total: %d points (of 738)" % total)
y -= 9 * mm
y = para("Deaths in this act: frostbite (no uniform), the chasm, the metal plate, the crusher (too slow), stepping off the rail, "
         "the rat (too slow), taking off without radar, switching the engines off in flight, and firing without front shields. "
         "The game checks the whole route from the first screen to the escape: all 15 events, exactly 145 points.", y, 9)
footer(1)
c.showPage()

SHOTS = [
    ("a1_1_conveyor.png", "Conveyor: the clock is running. The trash bucket (left) is the way up."),
    ("a1_2_rail_ride.png", "Overhead rail: Roger rides the grabber to the pedestal."),
    ("a1_3_motivator_installed.png", "The motivator, lowered into the Mallard's open panel."),
    ("a1_4_rat_lair.png", "Reactor cavern: the portable ladder, and something breathing."),
    ("a1_5_crane.png", "Crane cabin: the reticle hovers over the reactor pit."),
    ("a1_6_bay.png", "Construction bay: the ladder is up and the reactor is on the deck."),
    ("a1_7_computer.png", "The ship's computer: Engines, Radar, Weapons, Takeoff."),
    ("a1_9_death.png", "One of the deaths: 'Deceleration Trauma'."),
]
hw = (IW - 6 * mm) / 2
hh = hw * 960 / 1280
n = 2
for page in range(2):
    y = PH - 20 * mm
    for row in range(2):
        for col in range(2):
            name, cap = SHOTS[page * 4 + row * 2 + col]
            x = M + col * (hw + 6 * mm)
            c.drawImage(ImageReader(os.path.join(SH, name)), x, y - hh, hw, hh)
            c.setStrokeGray(0.5)
            c.rect(x, y - hh, hw, hh)
            c.setFont("Helvetica-Oblique", 8)
            for i, ln in enumerate(simpleSplit(cap, "Helvetica-Oblique", 8, hw)):
                c.drawString(x, y - hh - (4 + 3.6 * i) * mm, ln)
        y -= hh + 16 * mm
    footer(n)
    c.showPage()
    n += 1
c.save()
print("ok")
