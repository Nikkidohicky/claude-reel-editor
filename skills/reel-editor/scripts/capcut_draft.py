#!/usr/bin/env python3
"""Build an editable CapCut Web draft: the finished video (graphics baked in) + native caption layers + CapCut library
sound effects. Reads upload.json, captions.json, sfx.json from the reel folder and brand.json; writes draft.json.
Push it with the CapCut tools (start_stdraft_session -> push_stdraft_snapshot). See references/capcut.md.
Usage: CAPCUT_SKILLS_DIR=/path/to/capcut/skills python3 capcut_draft.py <reel-folder>"""
import json, os, sys
from collections import Counter
from pathlib import Path

reel = Path(sys.argv[1]).expanduser()
home = Path(os.environ.get("REELS_HOME", "~/reels")).expanduser()
skills = os.environ.get("CAPCUT_SKILLS_DIR")
if not skills:
    sys.exit("Set CAPCUT_SKILLS_DIR to the CapCut plugin's skills folder (see references/capcut.md)")
sys.path.insert(0, str(Path(skills).expanduser() / "capcut-stdraft-builder/scripts"))
from apply_materials import apply_video, apply_audio  # noqa: E402  (CapCut's own draft helpers)
from _draft import load  # noqa: E402

brand = json.load(open(home / "brand.json"))
up = json.load(open(reel / "upload.json"))
W, H = brand.get("resolution", [1080, 1920])
DUR = int(up["result"]["VideoMeta"]["Duration"] * 1000)
col = brand["colors"]
BASE, ACCENT, ON_LIGHT = col.get("caption", "#FFFFFF"), col.get("caption_accent", col["pop"]), col["pop"]
FONT = brand.get("capcut_font") or "vimo://7200959526265164290"   # Work Sans Medium, a clean default from CapCut's library

# Layout is worked out on a 1080x1920 grid; CapCut positions are -1..1 so it scales to any canvas.
PX = 4.8                                  # CapCut font_size 1 ~= 4.8 px on a 1080-wide frame
CHAR_W = 0.62                             # average character width in em (Work Sans measured wider than 0.56 in CapCut)
SIZE = {"sm": 58, "big": 104, "acc": 140}

# CapCut library sounds (sid, length ms). Add more by searching the library with search_capcut_material.
SFX = {"whoosh": ("sid://6993230936988977154", 566), "whoosh-short": ("sid://6993230936993204226", 566),
       "pop": ("sid://6926910425934071810", 700), "snap": ("sid://6926910425934071810", 300),
       "typing": ("sid://6990639268376905730", 1466), "click": ("sid://7005595075288532994", 333),
       "sparkle": ("sid://6995835233664763905", 1766), "coin": ("sid://6926878562561558530", 566),
       "chime": ("sid://6990639268369385474", 766), "impact": ("sid://7005595087811905537", 1000)}
SFX |= {"impact-bass-1": SFX["impact"], "click-soft": SFX["click"]}   # older names, still accepted
ms = lambda s: int(round(s * 1000))

def text_seg(sid, content, cx, cy, px, color, t0, t1, layer):
    attrs = {"content": content, "font": FONT, "font_size": round(px / PX, 1), "alignment": 1, "text_color": color,
             "line_max_width": 1.0, "shadow_alpha": 0.0, "border_width": 0.0}   # shadow 0: CapCut adds one on save otherwise
    return {"id": sid, "type": "TEXT", "parent_id": "draft", "attributes": attrs,
            "layout": {"position_x": round(cx / 540 - 1, 3), "position_y": round(1 - cy / 960, 3), "layer": layer},
            "timeline": {"start.ms": ms(t0), "duration.ms": ms(t1 - t0)}}

def patch(sid, k, a, b, px, color):   # restyles letters a..b inside one caption (mixed sizes / accent colour)
    return {"id": f"{sid}p{k}", "type": "PATCH", "parent_id": sid,
            "attributes": {"letter_start": a, "letter_end": b, "font_size": round(px / PX, 1), "font_color": color}}

def grouped(caps, n=3):
    """One-word captions become 2-3 word layers in CapCut: half the layers to tweak, and pushes stay under the size limit."""
    if not caps or max(len(c["lines"][0]) for c in caps) > 1: return caps
    out, cur = [], []
    for c in caps:
        chars = sum(len(x["lines"][0][0]["text"]) + 1 for x in cur) + len(c["lines"][0][0]["text"])
        if cur and (len(cur) == n or chars > 16 or c["start"] - cur[-1]["end"] > 0.25 or c.get("over_light") != cur[0].get("over_light")):
            out.append({"start": cur[0]["start"], "end": cur[-1]["end"], "over_light": cur[0].get("over_light", False),
                        "lines": [[w for x in cur for w in x["lines"][0]]]}); cur = []
        cur.append(c)
    if cur: out.append({"start": cur[0]["start"], "end": cur[-1]["end"], "over_light": cur[0].get("over_light", False),
                        "lines": [[w for x in cur for w in x["lines"][0]]]})
    return out

def captions(layers=(2, 3, 4, 5)):
    out = []
    for g, c in enumerate(grouped(json.load(open(reel / "captions.json")))):
        light = c.get("over_light", False)
        scale = 0.88 if light else 1.0
        base, acc = (ON_LIGHT, ON_LIGHT) if light else (BASE, ACCENT)
        y = 1240 if light else 1180
        for li, line in enumerate(c["lines"]):
            sid = f"c{g}l{li}"
            kinds = {w["kind"] for w in line}
            main = kinds.pop() if len(kinds) == 1 else "big"
            text, pos, pats = "", 0, []
            for wi, w in enumerate(line):
                s = ("" if wi == 0 else " ") + w["text"]
                a, b = pos + (0 if wi == 0 else 1), pos + len(s)
                if w["kind"] != main:
                    pats.append((a, b, SIZE[w["kind"]] * scale, acc if w["kind"] == "acc" else base))
                text += s; pos += len(s)
            tallest = max(SIZE[w["kind"]] for w in line) * scale
            width = sum((len(w["text"]) + 1) * CHAR_W * SIZE[w["kind"]] * scale for w in line)   # +1 = the space
            if width > 900:                                    # guardrail: shrink any line that would leave the 900 px safe area
                k = 900 / width; scale *= k; width = 900; tallest *= k
                pats = [(a, b, px * k, col) for a, b, px, col in pats]
            cx = 540                                           # always centred: offsets pushed long lines off-frame
            out.append(text_seg(sid, text, cx, y + tallest * 0.5, SIZE[main] * scale, acc if main == "acc" else base,
                                max(line[0]["t"] - 0.04, c["start"]), c["end"], layers[li % len(layers)]))
            out += [patch(sid, k, a, b, px, colr) for k, (a, b, px, colr) in enumerate(pats)]
            y += tallest * 0.95
    return out

d = {"version": "0.1.0", "segments": [{"id": "draft", "type": "DRAFT", "attributes": {"width": W, "height": H, "ratio_type": "custom"}}]}
d = apply_video(d, source=f"vid://{up['vid']}", start_ms=0, duration_ms=DUR, volume=1.0, layer=0)["draft"]
d["segments"] += captions()
sfx_file = reel / "sfx.json"
for e in (json.load(open(sfx_file)) if sfx_file.exists() else []):
    if e["name"] not in SFX:
        print("skip unknown sound:", e["name"]); continue
    src, length = SFX[e["name"]]; t = ms(e["t"]); dur = min(length, int(e.get("dur", 99) * 1000), DUR - t)   # "dur" trims long sounds (typing)
    if dur > 100:
        d = apply_audio(d, meta_type="SOUND", source=src, start_ms=t, duration_ms=dur, volume=e.get("vol", 0.4))["draft"]

model, _, _ = load(d); res = model.check()
print("valid:", res["valid"], "" if res["valid"] else res.get("errors", "")[:3])
print(dict(Counter(s["type"] for s in d["segments"])))
for k, seg in enumerate(x for x in d["segments"] if x["type"] == "AUDIO"): seg["id"] = f"a{k}"   # short ids keep the push small
json.dump(d, open(reel / "draft.json", "w"), separators=(",", ":"))
print(f"{len(json.dumps(d, separators=(',', ':'))) // 1000} KB (pushes over ~60 KB can fail)")
print(reel / "draft.json")
