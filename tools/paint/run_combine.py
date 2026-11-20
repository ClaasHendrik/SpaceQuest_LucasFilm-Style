import sys, json, numpy as np
from PIL import Image
from restyle import load_indices
import combine as C
M = "/tmp/claude-0/-home-user-SpaceQuest-LucasFilm-Style/7db01b00-b598-5261-b0ff-421f4ab3058d/scratchpad/multi/"
OUT = sys.argv[1]
# base screen -> (manual Roger boxes or None = detect, new screenshots)
JOBS = {
    14: ([(129, 92, 152, 121)], ["s014-2", "s014-3", "s014-1"]),
    15: ([(102, 95, 132, 145)], ["s015-1"]),
    16: ([(232, 38, 262, 82)], ["s016-1"]),
    17: ([(245, 92, 268, 122)], ["s017-1", "s020b-1"]),
    18: ([(4, 136, 34, 158)], ["s019-1", "s020c-1"]),
    19: ([(152, 98, 174, 136)], ["s020a-1"]),
    20: (None, ["s020-1", "s020-2"]),
    21: ([(232, 140, 256, 158)], ["s021-1"]),
    23: ([(78, 106, 100, 130)], ["s023-1"]),
    25: ([(48, 120, 68, 150)], ["s025-1"]),
    26: ([(155, 125, 172, 152)], ["s026-1"]),
    27: (None, ["s027-1"]),
}
R = json.load(open(M + "roger.json"))
report = {}
for n, (boxes, names) in JOBS.items():
    base = np.zeros((200, 320), int)
    base[10:200] = load_indices(f"/tmp/claude-0/sq3/s{n:03d}.png", 10, 190)
    if boxes is None:
        boxes = [tuple(b) for b, _ in R[str(n)]]
    srcs = [(nm, np.load(M + "new_" + nm + ".npy")) for nm in names]
    merged, hidden, filled, used = C.merge(base, boxes, srcs)
    C.save_idx(merged, f"{OUT}/m{n:03d}.png")
    C.save_idx(base, f"{OUT}/b{n:03d}.png")
    Image.fromarray(filled).save(f"{OUT}/f{n:03d}.png")
    report[n] = (int(hidden.sum()), int(filled.sum()), used)
    print("s%03d: hidden %4d px, filled %4d px (%.0f%%)  from %s" % (n, hidden.sum(), filled.sum(), 100 * filled.sum() / max(1, hidden.sum()), used))
json.dump(report, open(OUT + "/report.json", "w"))
