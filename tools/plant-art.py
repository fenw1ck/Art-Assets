#!/usr/bin/env python3
"""Generate the Fenwick plant-art library in the Naturalist's Plate style.

Run from the Art-Assets repository:
    python tools/plant-art.py
    python tools/plant-art.py --only tomato_cherry nasturtium --size 768
    python tools/plant-art.py --check

The renderer reads the canonical species list from plants.js. It writes one
PNG and one botanical infocard record per plant, plus a contact sheet.
Pillow is the only third-party dependency. All variation is seeded.
"""
from __future__ import annotations

import argparse
import json
import html
import math
import random
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plants.js"
OUT = ROOT / "plant-art"
PAPER = (249, 246, 231)
INK = (77, 77, 55)

# Profiles are construction instructions, not decorative labels. Each entry
# changes the branching, leaf geometry, flower/fruit placement and silhouette.
PROFILES = {
    "tomato_cherry": ("Solanaceae", "indeterminate vine", "alternating compound, deeply toothed leaves; axillary suckers; branched flower trusses; small round fruit", "pinnate", "yellow-star", "red-cherry"),
    "tomato_indeterminate": ("Solanaceae", "indeterminate vine", "alternating compound, deeply toothed leaves; long internodes; axillary suckers; hanging trusses", "pinnate", "yellow-star", "red-fruit"),
    "tomato_determinate": ("Solanaceae", "determinate bush", "compact branching; compound toothed leaves; clustered terminal fruit trusses", "pinnate", "yellow-star", "red-fruit"),
    "pepper_bell": ("Solanaceae", "upright branched bush", "alternate smooth ovate leaves; solitary pendant flowers; hollow lobed fruit", "ovate", "white-star", "bell-fruit"),
    "eggplant": ("Solanaceae", "stout branched bush", "large alternate ovate leaves, softly lobed and sometimes downy; solitary star flowers; pendant berry", "broad-ovate", "violet-star", "eggplant"),
    "corn_sweet": ("Poaceae", "single tall culm", "long parallel-veined blades alternate along a jointed stem; tassel above; ears at leaf axils", "strap", "tassel", "corn-ear"),
    "bean_bush": ("Fabaceae", "compact bush", "alternate trifoliate leaves; papilionaceous flowers; elongated pods", "trifoliate", "pea", "green-pod"),
    "bean_pole": ("Fabaceae", "twining climber", "twining stem; alternate trifoliate leaves; terminal tendrils; hanging pods", "trifoliate", "pea", "green-pod"),
    "pea": ("Fabaceae", "climbing tendrilled vine", "paired leaflets ending in branched tendrils; stipules; axillary flowers and pods", "pinnate-tendril", "pea", "green-pod"),
    "potato": ("Solanaceae", "branched herb", "pinnate compound leaves with unequal leaflets; white star flowers; underground tubers", "pinnate", "white-star", "tuber"),
    "squash_summer": ("Cucurbitaceae", "trailing vine", "rough palmately lobed leaves; coiling tendrils; separate male and female yellow flowers; elongated fruit", "palmate-lobed", "yellow-cup", "zucchini"),
    "squash_winter": ("Cucurbitaceae", "long trailing vine", "large rough lobed leaves; coiling tendrils; large yellow flowers; rounded winter fruit", "palmate-lobed", "yellow-cup", "winter-squash"),
    "cucumber": ("Cucurbitaceae", "climbing or trailing vine", "rough triangular-cordate leaves; axillary tendrils; yellow flowers; elongated fruit", "cordate-lobed", "yellow-cup", "cucumber"),
    "lettuce": ("Asteraceae", "basal rosette", "soft broad leaves in a dense basal rosette; later a bolting central flower stalk", "spoon", "composite", "none"),
    "spinach": ("Amaranthaceae", "basal rosette", "smooth arrow- to oval-shaped leaves on long petioles; erect seed stalk at maturity", "arrow", "green-spike", "none"),
    "kale": ("Brassicaceae", "upright leafy stem", "alternate thick blue-green leaves, wavy or curled margins, prominent pale midrib", "ruffled", "yellow-cross", "none"),
    "cabbage": ("Brassicaceae", "compact head rosette", "broad overlapping waxy leaves forming a dense rounded head", "round-waxy", "yellow-cross", "none"),
    "broccoli": ("Brassicaceae", "upright branched herb", "blue-green lobed leaves; thick central stem; compact green flower-bud head", "lobed", "yellow-cross", "broccoli-head"),
    "chard": ("Amaranthaceae", "upright basal clump", "large glossy crinkled leaves; conspicuous coloured fleshy petioles and midribs", "broad", "green-spike", "coloured-stalk"),
    "carrot": ("Apiaceae", "basal rosette then flowering stem", "finely divided fern-like leaves; white compound umbels; tapered orange taproot", "finely-divided", "white-umbel", "carrot-root"),
    "beet": ("Amaranthaceae", "basal rosette", "broad leaves with red veins and long coloured petioles; swollen taproot at soil line", "broad-veined", "green-spike", "beet-root"),
    "radish": ("Brassicaceae", "low basal rosette", "rough lyrate leaves; small white or pink four-petalled flowers; swollen taproot", "lyrate", "yellow-cross", "radish-root"),
    "onion": ("Amaryllidaceae", "basal bulb with hollow leaves", "upright hollow tubular leaves; leafless scape with spherical flower umbel", "hollow-tube", "allium-umbel", "bulb"),
    "garlic": ("Amaryllidaceae", "basal bulb with flat leaves", "flat keeled strap leaves; scape sometimes bearing bulbils in an umbel", "flat-strap", "allium-umbel", "bulb"),
    "asparagus": ("Asparagaceae", "crown of upright spears", "young edible spears; mature airy branching cladodes that look like fine needles", "cladode", "tiny-bell", "red-berry"),
    "rhubarb": ("Polygonaceae", "large basal clump", "very large crinkled leaves on thick red or green petioles; tall branching flower panicle", "huge-cordate", "panicle", "none"),
    "basil": ("Lamiaceae", "branched aromatic herb", "opposite pairs of glossy ovate leaves on square stems; terminal flower spikes", "opposite-ovate", "white-spike", "none"),
    "cilantro": ("Apiaceae", "basal rosette then bolting", "lower leaves rounded and lobed; upper leaves finely divided; delicate white umbels", "divided", "white-umbel", "round-seed"),
    "parsley": ("Apiaceae", "basal leafy clump", "deeply divided flat or curled leaves on long petioles; second-year white umbels", "divided", "white-umbel", "none"),
    "dill": ("Apiaceae", "upright hollow-stemmed herb", "very fine threadlike divided leaves; broad flat yellow compound umbels", "filiform", "yellow-umbel", "seed"),
    "chives": ("Amaryllidaceae", "dense tuft", "narrow hollow cylindrical leaves; leafless scapes topped by spherical purple umbels", "hollow-tube", "purple-umbel", "none"),
    "mint": ("Lamiaceae", "spreading stoloniferous herb", "opposite serrated leaves on square stems; opposite nodes; terminal or axillary flower spikes", "serrate-ovate", "lilac-spike", "none"),
    "thyme": ("Lamiaceae", "low woody subshrub", "tiny opposite grey-green leaves on fine woody branching stems; small terminal flowers", "tiny-oval", "pink-whorl", "none"),
    "strawberry": ("Rosaceae", "low stoloniferous rosette", "trifoliate serrated leaves; runners; white five-petalled flowers; red aggregate fruit", "trifoliate", "white-five", "strawberry"),
    "raspberry": ("Rosaceae", "upright biennial canes", "arching prickly canes; alternate pinnate leaves with pale undersides; clustered aggregate fruit", "pinnate", "white-five", "raspberry"),
    "blueberry": ("Ericaceae", "woody many-stemmed shrub", "alternate small elliptical leaves; urn-shaped flowers in clusters; blue bloom-covered berries", "elliptical", "urn", "blueberry"),
    "marigold_french": ("Asteraceae", "compact branching annual", "opposite divided aromatic foliage; solitary composite flower heads on long peduncles", "pinnatisect", "marigold", "none"),
    "nasturtium": ("Tropaeolaceae", "trailing or climbing succulent herb", "round shield-shaped peltate leaves with radiating veins; long petioles; spurred flowers", "peltate-round", "spurred-five", "none"),
    "calendula": ("Asteraceae", "upright branching annual", "alternate oblong leaves; sticky glandular stems; daisy-like composite heads", "oblong", "composite", "none"),
    "pansy": ("Violaceae", "low compact branching herb", "rounded scalloped leaves; solitary five-petalled flowers with dark nectar guides", "scalloped", "pansy", "none"),
    "sweet_pea": ("Fabaceae", "climbing tendrilled vine", "paired pinnate leaflets ending in branched tendrils; winged pea flowers; pods", "pinnate-tendril", "pea", "none"),
    "cosmos": ("Asteraceae", "tall airy branching annual", "finely divided threadlike foliage; long peduncles; radiate daisy heads", "filiform", "cosmos", "none"),
    "petunia": ("Solanaceae", "low spreading or trailing herb", "soft alternate entire ovate leaves; sticky stems; trumpet-shaped solitary flowers", "soft-ovate", "trumpet", "none"),
    "fuchsia": ("Onagraceae", "arching woody shrub", "opposite or whorled ovate leaves; pendant tubular sepals and reflexed petals; long stamens", "serrate-ovate", "pendant-fuchsia", "none"),
    "pothos": ("Araceae", "climbing or trailing hemiepiphyte", "long internodes; alternate heart-shaped waxy leaves; aerial roots at nodes", "heart", "none", "none"),
    "snake_plant": ("Asparagaceae", "rhizomatous evergreen rosette", "stiff upright sword-shaped succulent leaves with banding and yellow margins", "sword", "none", "none"),
    "monstera": ("Araceae", "climbing hemiepiphyte", "large cordate leaves developing fenestrations and splits; thick petioles; aerial roots", "fenestrated", "none", "none"),
    "peace_lily": ("Araceae", "basal rhizomatous clump", "glossy lanceolate leaves on long petioles; white spathe around a spadix", "lanceolate", "spathe-spadix", "none"),
    "spider_plant": ("Asparagaceae", "arching basal rosette", "narrow arching strap leaves; long stolons bearing small plantlets and white flowers", "strap", "white-star", "plantlets"),
    "apple": ("Rosaceae", "small central-leader tree", "woody trunk with scaffold branches; alternate serrated leaves; blossom clusters on short spurs", "serrate-oval", "apple-blossom", "pome"),
    "pear": ("Rosaceae", "upright central-leader tree", "upright scaffold branches; alternate glossy oval leaves; white blossom clusters on spurs", "oval", "white-five", "pear"),
    "peach": ("Rosaceae", "open-vase deciduous tree", "slender reddish shoots; narrow lanceolate serrated leaves; pink flowers on one-year wood", "lanceolate", "pink-five", "peach"),
    "fig": ("Moraceae", "broad branching deciduous tree", "large alternate palmately lobed rough leaves; syconia in leaf axils", "palmate-lobed", "none", "fig"),
    "lemon_meyer": ("Rutaceae", "evergreen small tree", "glossy aromatic alternate leaves; lightly winged petioles; white-purple flowers; oval yellow fruit", "elliptical", "citrus", "lemon"),
    "sunflower": ("Asteraceae", "single tall coarse annual", "rough alternate broad leaves; terminal large composite head with yellow rays and dark disc", "cordate-rough", "sunflower", "none"),
    "zinnia": ("Asteraceae", "upright branching annual", "opposite sessile rough leaves; solitary terminal composite heads", "opposite-oval", "zinnia", "none"),
    "lavender": ("Lamiaceae", "woody aromatic subshrub", "narrow grey-green opposite leaves on woody stems; terminal spikes of bilabiate flowers", "narrow-linear", "lavender-spike", "none"),
}

def plant_list():
    source = SOURCE.read_text(encoding="utf-8")
    match = re.search(r"const LIST=(\[.*?\]);\s*window\.PLANTS", source, re.S)
    if not match:
        raise RuntimeError("Could not read PLANTS.list from plants.js")
    return json.loads(match.group(1))

def font(size):
    for name in ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()

def blend(a, b, t):
    return tuple(round(a[i] * (1-t) + b[i] * t) for i in range(3))

def curve(draw, points, fill, width):
    # Smooth quadratic-like branch using short interpolated segments.
    pts = []
    for i in range(101):
        t = i / 100
        u = 1-t
        x = u*u*points[0][0] + 2*u*t*points[1][0] + t*t*points[2][0]
        y = u*u*points[0][1] + 2*u*t*points[1][1] + t*t*points[2][1]
        pts.append((x, y))
    draw.line(pts, fill=fill, width=width)

def leaf(draw, x, y, length, width, angle, color, shape, rng):
    # A closed leaf with its own darker margin and a fine central vein.
    ca, sa = math.cos(angle), math.sin(angle)
    def xy(a, b):
        return (x + a*ca - b*sa, y + a*sa + b*ca)
    if shape in ("strap", "flat-strap", "hollow-tube", "sword", "cladode", "filiform", "narrow-linear"):
        points = [xy(-width*.10, 0), xy(-width*.48, -length*.35), xy(-width*.18, -length), xy(width*.16, -length*.82), xy(width*.5, -length*.25), xy(width*.10, 0)]
    elif shape in ("peltate-round", "round-waxy", "broad", "huge-cordate"):
        points = [xy(0, 0), xy(-width*.9, -length*.22), xy(-width*.72, -length*.78), xy(0, -length), xy(width*.72, -length*.78), xy(width*.9, -length*.22)]
    elif shape in ("pinnate", "pinnate-tendril", "finely-divided", "divided", "filiform", "cladode", "pinnatisect"):
        points = [xy(0, 0), xy(-width*.65, -length*.25), xy(-width*.42, -length*.58), xy(0, -length), xy(width*.42, -length*.58), xy(width*.65, -length*.25)]
    elif shape in ("heart", "cordate-lobed", "fenestrated"):
        points = [xy(0, 0), xy(-width*.85, -length*.5), xy(-width*.8, -length*.85), xy(-width*.25, -length), xy(0, -length*.78), xy(width*.25, -length), xy(width*.8, -length*.85), xy(width*.85, -length*.5)]
    else:
        points = [xy(0, 0), xy(-width*.72, -length*.3), xy(-width*.52, -length*.78), xy(0, -length), xy(width*.52, -length*.78), xy(width*.72, -length*.3)]
    edge = blend(color, (30, 57, 31), .45)
    draw.polygon(points, fill=color, outline=edge)
    mid = xy(0, -length*.88)
    draw.line([xy(0, -length*.04), mid], fill=blend(color, (222, 224, 166), .45), width=max(1, int(width*.035)))
    for t in (.28, .48, .67):
        yy = -length*t
        for side in (-1, 1):
            draw.line([xy(0, yy), xy(side*width*.34, yy-length*.12)], fill=blend(color, (220, 224, 164), .28), width=1)

def flower(draw, x, y, r, kind, rng, color):
    if kind == "none":
        return
    n = 5 if kind in ("white-five", "pink-five", "pea", "pansy", "spurred-five") else 8
    if kind in ("composite", "cosmos", "zinnia", "sunflower", "marigold"):
        n = 14
    palette = {
        "yellow-star": (247, 196, 45), "white-star": (247, 244, 224),
        "yellow-cup": (246, 190, 35), "white-five": (250, 247, 231),
        "pink-five": (236, 142, 167), "pea": (211, 113, 163),
        "pansy": (117, 75, 153), "spurred-five": (239, 133, 45),
        "cosmos": (221, 108, 157), "zinnia": (216, 71, 106),
        "marigold": (241, 150, 30), "sunflower": (243, 187, 35),
        "lavender-spike": (139, 110, 180), "lilac-spike": (174, 128, 188),
        "purple-umbel": (166, 111, 188), "allium-umbel": (238, 235, 219),
        "white-umbel": (248, 246, 226), "yellow-umbel": (239, 195, 51),
        "urn": (226, 174, 194), "pendant-fuchsia": (208, 64, 105),
        "trumpet": (180, 92, 178), "spathe-spadix": (246, 243, 218),
        "apple-blossom": (247, 208, 213), "citrus": (249, 246, 231),
        "pink-whorl": (216, 163, 185), "panicle": (229, 213, 167),
        "green-spike": (177, 193, 125), "tiny-bell": (237, 236, 217),
        "tassel": (196, 157, 72),
    }
    col = palette.get(kind, color)
    if kind in ("white-umbel", "yellow-umbel", "purple-umbel", "allium-umbel", "tassel", "panicle", "green-spike"):
        for i in range(12 if "umbel" in kind else 8):
            a = i * math.tau / (12 if "umbel" in kind else 8)
            ex, ey = x + math.cos(a)*r*.95, y + math.sin(a)*r*.95
            draw.ellipse((ex-r*.13, ey-r*.13, ex+r*.13, ey+r*.13), fill=col)
        draw.ellipse((x-r*.25, y-r*.25, x+r*.25, y+r*.25), fill=blend(col, (223, 183, 75), .3))
        return
    for i in range(n):
        a = i*math.tau/n
        px, py = x + math.cos(a)*r*.47, y + math.sin(a)*r*.47
        rr = r*.56
        draw.ellipse((px-rr*.45, py-rr, px+rr*.45, py+rr), fill=blend(col, (255,255,255), .12), outline=blend(col, (92,67,55), .35))
    centre = (88, 61, 39) if kind in ("sunflower", "composite", "cosmos", "zinnia", "marigold") else (228, 183, 53)
    draw.ellipse((x-r*.24, y-r*.24, x+r*.24, y+r*.24), fill=centre)

def draw_plant(plant, size=768, seed=7):
    pid = plant["id"]
    profile = PROFILES.get(pid)
    if not profile:
        raise KeyError(f"No botanical construction profile for {pid}")
    family, habit, anatomy, leaf_shape, bloom, fruit = profile
    rng = random.Random(seed + sum(map(ord, pid)))
    im = Image.new("RGB", (size, size), PAPER)
    d = ImageDraw.Draw(im)
    # quiet paper grain; deterministic and low contrast
    for _ in range(size*size//1800):
        x, y = rng.randrange(size), rng.randrange(size)
        v = rng.choice((246, 248, 251))
        d.point((x, y), fill=(v, v, max(225, v-10)))
    cx, base = size*.5, size*.84
    pot_w, pot_h = size*.25, size*.18
    d.ellipse((cx-pot_w*.8, base+pot_h*.05, cx+pot_w*.8, base+pot_h*.24), fill=(214, 202, 171))
    d.polygon([(cx-pot_w*.55,base-pot_h*.8),(cx+pot_w*.55,base-pot_h*.8),(cx+pot_w*.42,base+pot_h*.2),(cx-pot_w*.42,base+pot_h*.2)], fill=(188,112,70), outline=(112,69,46))
    d.ellipse((cx-pot_w*.58,base-pot_h*.88,cx+pot_w*.58,base-pot_h*.65), fill=(213,139,91), outline=(122,76,49), width=max(2,size//300))
    d.ellipse((cx-pot_w*.48,base-pot_h*.82,cx+pot_w*.48,base-pot_h*.70), fill=(86,67,43))
    stem = (83, 119, 59)
    fol = tuple(int(plant["foliage_color"][i:i+2],16) for i in (1,3,5))
    accent = plant.get("accent_color") or "#d9c8a2"
    acc = tuple(int(accent[i:i+2],16) for i in (1,3,5))
    scale = size*.001
    top = size*.16
    n = 5 if "tree" in habit or "shrub" in habit else 7
    if any(w in habit for w in ("vine", "climber", "trailing", "stolon")):
        n = 6
    # species-specific branching architecture
    if "tree" in habit:
        d.line([(cx,base-pot_h*.8),(cx,top+size*.15)], fill=(110,78,48), width=max(5,int(size*.018)))
        for i in range(7):
            side = -1 if i%2 else 1
            yy = base-size*(.34+i*.045)
            ex = cx+side*size*(.12+.035*(i%3))
            ey = yy-size*(.16+.02*(i%2))
            curve(d,[(cx,yy),(cx+side*size*.08,ey),(ex,ey)],(110,78,48),max(3,int(size*.009)))
            for j in range(3):
                leaf(d,ex+side*j*size*.025,ey+j*size*.012,size*.07,size*.035,side*(.6+j*.12),fol,leaf_shape,rng)
            if fruit != "none":
                flower(d,ex,ey,size*.025,bloom,rng,acc)
        for i in range(14):
            a = rng.random()*math.tau
            rr = size*(.12+rng.random()*.11)
            x,y = cx+math.cos(a)*rr, top+size*.22+math.sin(a)*rr*.65
            leaf(d,x,y,size*.075,size*.038,a,fol,leaf_shape,rng)
        if fruit not in ("none",):
            for i in range(5):
                x=cx+(rng.random()-.5)*size*.22;y=top+size*(.25+rng.random()*.2)
                d.ellipse((x-7*scale,y-9*scale,x+7*scale,y+9*scale),fill=acc)
    elif "rosette" in habit or "clump" in habit or "tuft" in habit or "crown" in habit:
        for i in range(11):
            a = i*math.tau/11
            L=size*(.18+rng.random()*.08)
            ex,ey=cx+math.sin(a)*L*.62,base-pot_h*.9-math.cos(a)*L*.7
            leaf(d,cx,base-pot_h*.82,L,L*.42,a,fol,leaf_shape,rng)
        if bloom != "none":
            for i in range(3):
                x=cx+(i-1)*size*.06;y=top+size*.16
                d.line([(cx,base-pot_h*.8),(x,y)],fill=stem,width=max(2,int(size*.004)))
                flower(d,x,y,size*.035,bloom,rng,acc)
    else:
        for i in range(n):
            spread=(i-(n-1)/2)/(n-1)
            bx=cx+spread*size*.12
            tx=cx+spread*size*(.28 if "vine" in habit else .18)
            ty=top+size*(.06+rng.random()*.1)
            curve(d,[(bx,base-pot_h*.82),(bx+spread*size*.05,base-size*.35),(tx,ty)],stem,max(2,int(size*.004)))
            for j in range(4):
                t=(j+1)/5
                lx=bx+(tx-bx)*t;ly=base-pot_h*.82+(ty-(base-pot_h*.82))*t
                for side in (-1,1):
                    ang=side*(.65+rng.random()*.5)+spread*.25
                    leaf(d,lx,ly,size*(.09 if leaf_shape not in ("strap","sword") else .15),size*.052,ang,fol,leaf_shape,rng)
            if bloom != "none":
                if bloom.endswith("spike"):
                    for j in range(5):
                        flower(d,tx+(j-2)*size*.012,ty+size*j*.018,size*.018,bloom,rng,acc)
                else:
                    flower(d,tx,ty,size*(.035 if "flower" not in bloom else .045),bloom,rng,acc)
            if fruit not in ("none",):
                fx=tx+(rng.random()-.5)*size*.045;fy=ty+size*.08
                d.ellipse((fx-size*.012,fy-size*.016,fx+size*.012,fy+size*.016),fill=acc,outline=blend(acc,(60,55,40),.4))
    # a fine, warm ground shadow and a quiet paper label
    d.ellipse((cx-size*.22,base+pot_h*.23,cx+size*.22,base+pot_h*.29),fill=(231,222,198))
    return im

def card_record(p):
    family, habit, anatomy, leaf_shape, bloom, fruit = PROFILES[p["id"]]
    return {
        "id": p["id"], "name": p["common_name"], "family": family,
        "growth_habit": habit, "diagnostic_botany": anatomy,
        "leaf_construction": leaf_shape, "flower_construction": bloom,
        "fruit_or_harvest": fruit, "source_record": "plants.js",
        "renderer": "tools/plant-art.py", "style": "Naturalist's Plate",
        "style_terms": ["botanical naturalist plate", "accurate species architecture",
                        "crisp closed leaf shapes", "fine visible midribs and lateral veins",
                        "soft upper-left light", "thin same-hue edge", "warm ivory paper",
                        "terracotta nursery pot", "seeded natural variation"],
        "image": f"plant-art/{p['id']}.png"
    }

def write_page(records):
    cards = []
    for item in records:
        cards.append(
            '<article class="card">'
            f'<img src="{html.escape(Path(item["image"]).name)}" alt="{html.escape(item["name"])} botanical illustration">'
            f'<h2>{html.escape(item["name"])}</h2>'
            f'<p class="family">{html.escape(item["family"])} · {html.escape(item["growth_habit"])}</p>'
            f'<p>{html.escape(item["diagnostic_botany"])}</p>'
            f'<dl><dt>Leaves</dt><dd>{html.escape(item["leaf_construction"])}</dd>'
            f'<dt>Flowers</dt><dd>{html.escape(item["flower_construction"])}</dd>'
            f'<dt>Harvest</dt><dd>{html.escape(item["fruit_or_harvest"])}</dd></dl>'
            f'<p class="terms">{html.escape(", ".join(item["style_terms"]))}</p>'
            '</article>'
        )
    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fenwick · Plant Art Library</title>
<style>
:root{color-scheme:light;--paper:#f9f6e7;--ink:#34372d;--line:#d9d2bd}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 Georgia,serif}
header{max-width:1200px;margin:auto;padding:28px 20px 12px}h1{font-size:30px;margin:0}
header p{max-width:760px;margin:6px 0;color:#656451}
main{max-width:1200px;margin:auto;padding:16px 20px 40px;display:grid;grid-template-columns:repeat(auto-fill,minmax(245px,1fr));gap:16px}
.card{background:#fffdf5;border:1px solid var(--line);padding:12px;box-shadow:0 2px 8px #5a482012}
.card img{display:block;width:100%;aspect-ratio:1;object-fit:contain;background:var(--paper)}
h2{font-size:19px;margin:10px 0 2px}.family{font-size:13px;color:#6d684f;margin:0 0 8px}
p{margin:7px 0}dl{display:grid;grid-template-columns:70px 1fr;gap:3px 8px;font-size:13px}
dt{color:#77705b}dd{margin:0}.terms{font-size:11px;color:#77705b;border-top:1px solid var(--line);padding-top:7px}
</style></head><body><header><h1>Plant Art Library</h1>
<p>Species-specific botanical constructions in the Naturalist's Plate style. Growth habit, leaf architecture, flowers and harvest structures are recorded with each illustration. Artwork is generated reproducibly by tools/plant-art.py.</p></header>
<main>
""" + "\n".join(cards) + """
</main></body></html>
"""
    (OUT / "index.html").write_text(page, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--size", type=int, default=768)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    plants = plant_list()
    missing = [p["id"] for p in plants if p["id"] not in PROFILES]
    extra = sorted(set(PROFILES)-{p["id"] for p in plants})
    if missing or extra:
        raise SystemExit(f"Profile mismatch. Missing: {missing}; unused: {extra}")
    if args.check:
        print(f"OK: {len(plants)} plants have species-specific construction profiles.")
        return
    selected = [p for p in plants if not args.only or p["id"] in args.only]
    OUT.mkdir(exist_ok=True)
    records = []
    thumbs = []
    for p in selected:
        image = draw_plant(p, args.size, args.seed)
        image.save(OUT / f"{p['id']}.png", optimize=True)
        records.append(card_record(p))
        thumbs.append((p, image.copy()))
    (OUT / "infocards.json").write_text(json.dumps(records, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    write_page(records)
    cols = 7
    cell_w, cell_h = 180, 220
    rows = math.ceil(len(thumbs)/cols)
    sheet = Image.new("RGB", (cols*cell_w, rows*cell_h), PAPER)
    sd = ImageDraw.Draw(sheet)
    for i,(p,im) in enumerate(thumbs):
        x=(i%cols)*cell_w;y=(i//cols)*cell_h
        im.thumbnail((cell_w-16,cell_h-34),Image.Resampling.LANCZOS)
        sheet.paste(im,(x+(cell_w-im.width)//2,y))
        sd.text((x+8,y+cell_h-27),p["common_name"],font=font(12),fill=INK)
    sheet.save(OUT/"contact-sheet.png", optimize=True)
    print(f"Rendered {len(selected)} of {len(plants)} plants to {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
