"""Export a fresh-board Canvas Composer source from the reviewed live snapshot.

proposal-01-promotion.miro.svg is canonical and carries the current Miro widget identities.
Use those identities for edits to the existing board. The exported canvas.svg is
for a NEW composition only; creating it on the existing board would duplicate it.
"""
from pathlib import Path
import copy
import math
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
NS = "{http://www.w3.org/2000/svg}"
ET.register_namespace("", NS[1:-1])
live = ET.parse(ROOT / "proposal-01-promotion.miro.svg").getroot()
svg = copy.deepcopy(live)
ids = {e.get("id"): e for e in svg.iter() if e.get("id")}
assert len(ids) == sum(bool(e.get("id")) for e in svg.iter())
assert sum("data-frame" in e.attrib for e in svg) == 2

def point(e, side):
    x, y, w, h = [float(e.get(k)) for k in ("x", "y", "width", "height")]
    return {"left": (x, y+h/2), "right": (x+w, y+h/2),
            "top": (x+w/2, y), "bottom": (x+w/2, y+h)}[side]

for e in svg.iter():
    assert e.get("data-deleted") is None
    for attr in ("data-miro-id", "data-rendered-bounds", "data-group"):
        e.attrib.pop(attr, None)
    if e.tag == NS+"rect" and e.get("stroke") not in (None, "none"):
        e.set("stroke-width", "2")
    if e.tag == NS+"line" and e.get("data-start"):
        a, b = e.get("data-start"), e.get("data-end")
        assert a in ids and b in ids
        x1, y1 = point(ids[a], e.get("data-start-side", "right"))
        x2, y2 = point(ids[b], e.get("data-end-side", "left"))
        for k, v in zip(("x1", "y1", "x2", "y2"), (x1, y1, x2, y2)):
            e.set(k, str(v))
        e.set("stroke-width", "2")
assert not any(e.tag in {NS+"image", NS+"foreignObject"} for e in svg.iter())
svg.attrib.clear()
frame_bounds = []
for frame in svg:
    if frame.get("data-frame"):
        x, y = map(float, re.search(r"translate\(([^,]+),([^\)]+)\)", frame.get("transform")).groups())
        frame_bounds.append((x + float(frame[0].get("width")), y + float(frame[0].get("height"))))
svg.set("width", str(math.ceil(max(x for x, y in frame_bounds))))
svg.set("height", str(math.ceil(max(y for x, y in frame_bounds))))
ET.indent(svg)
ET.ElementTree(svg).write(ROOT / "proposal-01-promotion.canvas.svg", encoding="utf-8", xml_declaration=True)
print("Exported 2 frames; identities removed for fresh-board creation; native widgets and connector references checked.")
