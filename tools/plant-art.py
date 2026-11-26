#!/usr/bin/env python3
"""Generate the Fenwick plant-art library in the Naturalist's Plate style.

Run from the Art-Assets repository:
    python tools/plant-art.py
    python tools/plant-art.py --only tomato_cherry nasturtium --size 768
    python tools/plant-art.py --check

The renderer uses plants.js for the legacy render selection and merges the
canonical infocard catalogue as its research-first botanical data source. It
writes one PNG and one infocard record per selected plant, plus a contact sheet.
Pillow is the only third-party dependency. All variation is seeded.
"""
from __future__ import annotations

import argparse
import json
import html
import hashlib
import math
import shutil
import random
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plants.js"
OUT = ROOT / "plant-art" / "derived"
INFOCARDS = ROOT / "plant-art" / "infocards.json"
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

def load_infocard_index():
    """Load the canonical botanical catalogue without modifying its records."""
    if not INFOCARDS.is_file():
        return {}
    try:
        records = json.loads(INFOCARDS.read_text(encoding="utf-8"))
    except (ValueError, TypeError) as exc:
        raise SystemExit(f"Could not safely read botanical infocards: {INFOCARDS}") from exc
    if not isinstance(records, list):
        raise SystemExit(f"Botanical infocards must be a JSON list: {INFOCARDS}")
    index = {}
    for item in records:
        if not isinstance(item, dict) or not item.get("id"):
            raise SystemExit(f"Invalid botanical infocard record in {INFOCARDS}")
        if item["id"] in index:
            raise SystemExit(f"Duplicate botanical infocard ID: {item['id']}")
        index[item["id"]] = item
    return index


def botanical_data(plant, infocard=None):
    """Normalized, research-first data interface for future constructors."""
    card = infocard or {}
    user_data = card.get("user_data") or {}
    taxonomy = ("kingdom", "division", "class", "order", "family", "genus",
                "species", "scientific_name", "accepted_name")
    morphology = (
        "species_dimensions", "species_morphology", "construction_notes",
        "leaf_arrangement", "leaf_architecture", "leaf_type", "leaf_shape",
        "leaf_margin", "leaf_venation", "branching_pattern", "stem_or_root",
        "diagnostic_reproductive", "flower_placement_inflorescence",
        "fruit_structure", "habitat"
    )
    return {
        "taxonomy": {k: card.get(k) or user_data.get(k)
                     for k in taxonomy if card.get(k) or user_data.get(k)},
        "morphology": {k: card.get(k) if card.get(k) is not None else user_data.get(k)
                       for k in morphology
                       if card.get(k) is not None or user_data.get(k) is not None},
        "provenance": {
            "user_data": dict(card.get("user_data_provenance") or {}),
            "research_record": card.get("research_record"),
            "research_sources": list(card.get("research_sources") or []),
            "research_status": card.get("research_status"),
            "research_gaps": list(card.get("research_gaps") or []),
        },
        "catalogue": {k: card.get(k) for k in
                      ("catalogue_type", "coverage_group", "growth_habit")
                      if card.get(k) is not None},
    }


def plant_list():
    source = SOURCE.read_text(encoding="utf-8")
    match = re.search(r"const LIST=(\[.*?\]);\s*window\.PLANTS", source, re.S)
    if not match:
        raise RuntimeError("Could not read PLANTS.list from plants.js")
    plants = json.loads(match.group(1))
    cards = load_infocard_index()
    for plant in plants:
        card = cards.get(plant["id"], {})
        plant["botanical_data"] = botanical_data(plant, card)
        plant["infocard"] = card
    return plants

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


# Flowering species use individual construction routines rather than the
# generic habit-based sketch below. Coordinates are normalized to the plate.
FLOWER_IDS = {"nasturtium", "calendula", "pansy", "sweet_pea", "cosmos", "zinnia", "petunia", "fuchsia"}

def _flower_base(size, rng):
    im = Image.new("RGB", (size, size), PAPER)
    d = ImageDraw.Draw(im)
    for _ in range(size * size // 1800):
        x, y = rng.randrange(size), rng.randrange(size)
        v = rng.choice((246, 248, 251))
        d.point((x, y), fill=(v, v, max(225, v - 10)))
    cx, base = size * .5, size * .84
    pw, ph = size * .25, size * .18
    d.ellipse((cx-pw*.8, base+ph*.05, cx+pw*.8, base+ph*.24), fill=(214,202,171))
    d.polygon([(cx-pw*.55,base-ph*.8),(cx+pw*.55,base-ph*.8),(cx+pw*.42,base+ph*.2),(cx-pw*.42,base+ph*.2)], fill=(188,112,70), outline=(112,69,46))
    d.ellipse((cx-pw*.58,base-ph*.88,cx+pw*.58,base-ph*.65), fill=(213,139,91), outline=(122,76,49), width=max(2,size//300))
    d.ellipse((cx-pw*.48,base-ph*.82,cx+pw*.48,base-ph*.70), fill=(86,67,43))
    return im, d, cx, base, size

def _stem(d, a, b, c, color=(83,119,59), width=4):
    curve(d, [a,b,c], color, width)

def _leaf_form(d, x, y, length, width, angle, color, kind="ovate"):
    ca, sa = math.cos(angle), math.sin(angle)
    def p(u,v): return (x + u*ca - v*sa, y + u*sa + v*ca)
    if kind == "peltate":
        pts=[p(0,0),p(-width*.68,-length*.18),p(-width*.94,-length*.52),p(-width*.62,-length*.86),p(0,-length),p(width*.62,-length*.86),p(width*.94,-length*.52),p(width*.68,-length*.18)]
    elif kind == "oblong":
        pts=[p(0,0),p(-width*.42,-length*.22),p(-width*.48,-length*.72),p(-width*.18,-length),p(width*.18,-length),p(width*.48,-length*.72),p(width*.42,-length*.22)]
    elif kind == "scalloped":
        pts=[p(0,0),p(-width*.45,-length*.18),p(-width*.7,-length*.3),p(-width*.58,-length*.44),p(-width*.78,-length*.56),p(-width*.48,-length*.72),p(-width*.35,-length*.94),p(0,-length),p(width*.35,-length*.94),p(width*.48,-length*.72),p(width*.78,-length*.56),p(width*.58,-length*.44),p(width*.7,-length*.3),p(width*.45,-length*.18)]
    elif kind == "thread":
        pts=[p(0,0),p(-width*.16,-length*.35),p(-width*.08,-length*.78),p(0,-length),p(width*.08,-length*.78),p(width*.16,-length*.35)]
    elif kind == "cordate":
        pts=[p(0,0),p(-width*.8,-length*.42),p(-width*.82,-length*.78),p(-width*.38,-length),p(0,-length*.78),p(width*.38,-length),p(width*.82,-length*.78),p(width*.8,-length*.42)]
    else:
        pts=[p(0,0),p(-width*.68,-length*.22),p(-width*.58,-length*.72),p(-width*.2,-length),p(width*.2,-length),p(width*.58,-length*.72),p(width*.68,-length*.22)]
    edge=blend(color,(34,60,34),.42)
    d.polygon(pts,fill=color,outline=edge)
    d.line([p(0,-length*.04),p(0,-length*.91)],fill=blend(color,(225,229,178),.52),width=max(1,int(width*.035)))
    if kind not in ("thread","peltate"):
        for t in (.28,.48,.67):
            for side in (-1,1):
                d.line([p(0,-length*t),p(side*width*.34,-length*(t+.12))],fill=blend(color,(220,225,170),.28),width=1)
    elif kind=="peltate":
        # Nasturtium veins radiate from the petiole insertion, not from a leaf tip.
        for i in range(12):
            a=i*math.tau/12
            d.line([p(0,-length*.04),p(math.cos(a)*width*.82,-length*.52+math.sin(a)*length*.38)],fill=blend(color,(224,231,177),.5),width=max(1,int(width*.018)))

def _ray_head(d,x,y,r,color,rng,double=False):
    n=24 if double else 14
    for layer in range(2 if double else 1):
        for i in range(n):
            a=math.tau*i/n+layer*.11
            px=x+math.cos(a)*r*.28;py=y+math.sin(a)*r*.28
            rr=r*(.52 if layer else .72)
            col=blend(color,(255,230,164),rng.uniform(.02,.18))
            d.ellipse((px-rr*.24,py-rr,px+rr*.24,py+rr),fill=col,outline=blend(color,(113,74,40),.28))
    d.ellipse((x-r*.28,y-r*.28,x+r*.28,y+r*.28),fill=(116,73,35),outline=(75,54,31))
    for _ in range(22):
        a=rng.random()*math.tau;rr=rng.random()*r*.23
        d.ellipse((x+math.cos(a)*rr-1,y+math.sin(a)*rr-1,x+math.cos(a)*rr+1,y+math.sin(a)*rr+1),fill=(222,174,62))

def _nasturtium_bloom(d,x,y,r,color,rng):
    # Five rounded, unequal petals and a long nectar spur behind the flower.
    for i in range(5):
        a=math.tau*i/5-.35
        px=x+math.cos(a)*r*.48;py=y+math.sin(a)*r*.42
        rw=r*(.31 if i<2 else .36);rh=r*(.47 if i<2 else .39)
        d.ellipse((px-rw,py-rh,px+rw,py+rh),fill=blend(color,(255,191,92),rng.uniform(.02,.16)),outline=blend(color,(119,57,28),.35),width=max(1,int(r*.035)))
    d.ellipse((x-r*.17,y-r*.15,x+r*.17,y+r*.15),fill=(246,207,102))
    d.line([(x+r*.05,y+r*.08),(x+r*.55,y+r*1.15),(x+r*.85,y+r*1.28)],fill=(126,73,39),width=max(2,int(r*.10)))

def _pansy_bloom(d,x,y,r,color,rng):
    # Bilateral viola face: two upper petals, two lateral petals, one broad lower petal.
    d.ellipse((x-r*.62,y-r*.92,x+r*.02,y+r*.28),fill=blend(color,(255,255,255),.08),outline=blend(color,(55,43,80),.5),width=max(1,int(r*.035)))
    d.ellipse((x-r*.02,y-r*.92,x+r*.62,y+r*.28),fill=blend(color,(255,255,255),.14),outline=blend(color,(55,43,80),.5),width=max(1,int(r*.035)))
    d.ellipse((x-r*1.02,y-r*.25,x-r*.12,y+r*.72),fill=blend(color,(255,255,255),.1),outline=blend(color,(55,43,80),.5),width=max(1,int(r*.035)))
    d.ellipse((x+r*.12,y-r*.25,x+r*1.02,y+r*.72),fill=blend(color,(255,255,255),.18),outline=blend(color,(55,43,80),.5),width=max(1,int(r*.035)))
    d.ellipse((x-r*.52,y-r*.08,x+r*.52,y+r*1.05),fill=blend(color,(241,211,93),.42),outline=blend(color,(55,43,80),.5),width=max(1,int(r*.035)))
    d.ellipse((x-r*.23,y-r*.25,x+r*.23,y+r*.20),fill=(244,213,89))
    for side in (-1,0,1):
        d.line([(x,y),(x+side*r*.17,y+r*.72)],fill=(61,47,75),width=max(1,int(r*.045)))

def _pea_bloom(d,x,y,r,color,rng):
    # Papilionaceous standard, paired wings and narrow keel.
    d.ellipse((x-r*.48,y-r*1.02,x+r*.48,y+r*.12),fill=blend(color,(255,255,255),.12),outline=blend(color,(104,48,83),.4))
    d.ellipse((x-r*1.0,y-r*.32,x-r*.05,y+r*.58),fill=color,outline=blend(color,(104,48,83),.4))
    d.ellipse((x+r*.05,y-r*.32,x+r*1.0,y+r*.58),fill=blend(color,(255,255,255),.12),outline=blend(color,(104,48,83),.4))
    d.ellipse((x-r*.25,y+r*.05,x+r*.25,y+r*.82),fill=blend(color,(91,51,92),.12),outline=blend(color,(104,48,83),.4))

def _trumpet_bloom(d,x,y,r,color,rng):
    # Fused corolla tube widens to a five-lobed flared limb.
    d.polygon([(x-r*.18,y+r*.52),(x-r*.16,y-r*.22),(x-r*.62,y-r*.64),(x-r*.9,y-r*.95),(x+r*.9,y-r*.95),(x+r*.62,y-r*.64),(x+r*.16,y-r*.22),(x+r*.18,y+r*.52)],fill=color,outline=blend(color,(67,45,70),.4))
    d.ellipse((x-r*.78,y-r*1.08,x+r*.78,y-r*.60),fill=blend(color,(255,255,255),.18),outline=blend(color,(67,45,70),.35))
    d.ellipse((x-r*.28,y-r*.91,x+r*.28,y-r*.68),fill=(89,56,103))

def _fuchsia_bloom(d,x,y,r,color,rng):
    # Pendant tubular calyx, four reflexed sepals, inner petals and exserted stamens.
    d.polygon([(x-r*.20,y-r*.35),(x+r*.20,y-r*.35),(x+r*.15,y+r*.62),(x+r*.06,y+r*.96),(x-r*.06,y+r*.96),(x-r*.15,y+r*.62)],fill=color,outline=blend(color,(78,40,60),.4))
    for i in range(4):
        a=i*math.pi/2
        ex=x+math.cos(a)*r*.46;ey=y-r*.25+math.sin(a)*r*.25
        d.ellipse((ex-r*.20,ey-r*.60,ex+r*.20,ey+r*.12),fill=blend(color,(255,255,255),.08),outline=blend(color,(78,40,60),.42))
    inner=blend(color,(119,54,142),.48)
    for i in range(4):
        a=i*math.pi/2
        ex=x+math.cos(a)*r*.20;ey=y-r*.34+math.sin(a)*r*.13
        d.ellipse((ex-r*.15,ey-r*.35,ex+r*.15,ey+r*.18),fill=inner)
    for i in range(5):
        xx=x+(i-2)*r*.09
        d.line([(xx,y+r*.55),(xx+(i-2)*r*.11,y+r*1.52)],fill=(238,220,218),width=max(1,int(r*.035)))

def draw_flower_plant(plant, size=768, seed=7):
    pid=plant["id"]
    rng=random.Random(seed+sum(map(ord,pid)))
    im,d,cx,base,size=_flower_base(size,rng)
    fol=tuple(int(plant["foliage_color"][i:i+2],16) for i in (1,3,5))
    accent=plant.get("accent_color") or "#d9c8a2"
    acc=tuple(int(accent[i:i+2],16) for i in (1,3,5))
    stem=(82,119,62); dark=blend(fol,(36,65,38),.28)
    S=size; soil=base-size*.16; potline=base-size*.18
    if pid=="nasturtium":
        # Succulent trailing shoots radiate from the crown and cascade beyond the pot rim.
        paths=[(-.02,.00,-.32,-.22,-.47,-.02),(.02,.00,.30,-.18,.48,-.02),(-.01,.00,-.42,-.04,-.50,.20),(.02,.00,.42,-.04,.52,.18),(.00,.00,-.15,-.30,.12,-.44),(.00,.00,.18,-.26,.34,-.36)]
        for x0,y0,x1,y1,x2,y2 in paths:
            a=(cx+x0*S,soil+y0*S);b=(cx+x1*S,soil+y1*S);c=(cx+x2*S,soil+y2*S)
            _stem(d,a,b,c,stem,max(3,int(S*.006)))
            for t in (.32,.62,.88):
                xx=(1-t)**2*a[0]+2*(1-t)*t*b[0]+t*t*c[0]; yy=(1-t)**2*a[1]+2*(1-t)*t*b[1]+t*t*c[1]
                side=-1 if (x2<0)^(t>.6) else 1
                _stem(d,(xx,yy),(xx+side*S*.055,yy-S*.025),(xx+side*S*.095,yy-S*.005),stem,max(2,int(S*.003)))
                _leaf_form(d,xx+side*S*.09,yy-S*.02,S*(.075+rng.random()*.025),S*.065,side*(.8+rng.random()*.5),blend(fol,(169,194,113),.18),"peltate")
        for x,y,r in [(-.31,-.19,.043),(.30,-.18,.047),(-.39,.02,.038),(.42,.0,.043),(.12,-.40,.039)]:
            _nasturtium_bloom(d,cx+x*S,soil+y*S,r*S,acc,rng)
    elif pid=="calendula":
        # Upright branching annual; alternate oblong leaves, solitary terminal composite heads.
        tips=[]
        for i,spread in enumerate((-.27,-.13,0,.15,.29)):
            x0=cx+spread*S*.13;y0=potline
            tx=cx+spread*S;ty=S*(.20+rng.random()*.07)
            _stem(d,(x0,y0),(cx+spread*S*.40,S*.53),(tx,ty),stem,max(3,int(S*.006)))
            for j in range(1,6):
                t=j/6;lx=x0+(tx-x0)*t;ly=y0+(ty-y0)*t
                side=1 if (j+i)%2 else -1
                _leaf_form(d,lx,ly,S*.105,S*.030,side*(.8+rng.random()*.25),fol,"oblong")
            tips.append((tx,ty))
        for i,(x,y) in enumerate(tips):
            _ray_head(d,x,y,S*(.040+rng.random()*.008),acc,rng)
    elif pid=="pansy":
        # Low compact crown with short petioles; flowers are solitary, not clustered heads.
        for i in range(11):
            a=math.tau*i/11;L=S*(.17+rng.random()*.045)
            x=cx+math.cos(a)*L*.55;y=potline-math.sin(a)*L*.34
            _stem(d,(cx,potline),(cx+math.cos(a)*L*.25,potline-L*.15),(x,y),stem,max(2,int(S*.003)))
            _leaf_form(d,x,y,S*.11,S*.075,a,fol,"scalloped")
        for i in range(5):
            a=math.tau*i/5-.2;L=S*(.20+rng.random()*.04)
            x=cx+math.cos(a)*L*.52;y=S*(.48+math.sin(a)*.04)
            _stem(d,(cx,potline),(cx+math.cos(a)*L*.2,S*.62),(x,y),stem,max(2,int(S*.003)))
            _pansy_bloom(d,x,y,S*.064,acc,rng)
    elif pid=="sweet_pea":
        # Climbing angular stems; paired leaflets, stipules and curling terminal tendrils.
        for i in range(3):
            offset=(i-1)*S*.12
            pts=[(cx+offset*.25,potline),(cx+offset,S*.62),(cx+offset*.45,S*.44),(cx+offset*1.25,S*.28),(cx+offset*.75,S*.17)]
            for a,b in zip(pts,pts[1:]):
                d.line([a,b],fill=stem,width=max(2,int(S*.004)))
            for j,(x,y) in enumerate(pts[1:-1],1):
                for side in (-1,1):
                    _leaf_form(d,x+side*S*.018,y,S*.075,S*.040,side*.8,fol,"ovate")
                # fine curling tendril at each compound-leaf tip
                ex=x+offset*.12+S*.045
                d.arc((ex-S*.035,y-S*.065,ex+S*.035,y+S*.005),190,520,fill=dark,width=max(1,int(S*.002)))
                d.line([(x,y),(x+S*.03,y-S*.05),(ex,y-S*.045)],fill=stem,width=max(1,int(S*.002)))
            # loose axillary raceme with 1–4 papilionaceous flowers
            x,y=pts[3];rac=(x+S*.035,y-S*.025)
            d.line([rac,(rac[0]+S*.025,rac[1]+S*.09)],fill=stem,width=max(1,int(S*.003)))
            for j in range(1+rng.randrange(4)):
                _pea_bloom(d,rac[0]+S*.02,rac[1]+S*(.02+j*.035),S*.028,acc,rng)
    elif pid=="cosmos":
        # Tall, open framework and finely dissected, threadlike bipinnate foliage.
        tips=[]
        for i,spread in enumerate((-.30,-.18,-.06,.09,.22,.32)):
            x0=cx+spread*S*.08;y0=potline
            tx=cx+spread*S;ty=S*(.17+rng.random()*.08)
            _stem(d,(x0,y0),(cx+spread*S*.4,S*.52),(tx,ty),stem,max(2,int(S*.0035)))
            for j in range(1,6):
                t=j/6;lx=x0+(tx-x0)*t;ly=y0+(ty-y0)*t
                for side in (-1,1):
                    for k in range(3):
                        xx=lx+side*S*(.025+k*.004);yy=ly-S*k*.012
                        _stem(d,(lx,yy),(xx,yy-S*.018),(xx+side*S*.014,yy-S*.040),blend(fol,(178,197,132),.08),max(1,int(S*.0015)))
                        d.line([(xx,yy-S*.02),(xx+side*S*.014,yy-S*.043)],fill=fol,width=max(1,int(S*.0013)))
            tips.append((tx,ty))
        for x,y in tips:
            _ray_head(d,x,y,S*.038,acc,rng)
    elif pid=="zinnia":
        # Stout upright branches, opposite sessile rough leaves, terminal layered heads.
        tips=[]
        for i,spread in enumerate((-.28,-.16,-.04,.10,.23,.31)):
            x0=cx+spread*S*.10;y0=potline
            tx=cx+spread*S;ty=S*(.23+rng.random()*.08)
            _stem(d,(x0,y0),(cx+spread*S*.45,S*.55),(tx,ty),stem,max(3,int(S*.006)))
            for j in range(1,5):
                t=j/5;lx=x0+(tx-x0)*t;ly=y0+(ty-y0)*t
                for side in (-1,1):
                    _leaf_form(d,lx,ly,S*.115,S*.070,side*(.9+rng.random()*.18),fol,"ovate")
            tips.append((tx,ty))
        for x,y in tips:
            _ray_head(d,x,y,S*(.045+rng.random()*.008),acc,rng,True)
    elif pid=="petunia":
        # Low spreading/trailing shoots; alternate soft ovate leaves and solitary axillary trumpets.
        tips=[]
        for i,spread in enumerate((-.46,-.30,-.14,.08,.27,.45)):
            x0=cx+spread*S*.08;y0=potline
            tx=cx+spread*S;ty=S*(.57+rng.random()*.07)
            _stem(d,(x0,y0),(cx+spread*S*.60,S*.69),(tx,ty),stem,max(2,int(S*.004)))
            for j in range(1,5):
                t=j/5;lx=x0+(tx-x0)*t;ly=y0+(ty-y0)*t
                _leaf_form(d,lx,ly,S*.085,S*.050,(-1 if j%2 else 1)*(.7+rng.random()*.2),fol,"ovate")
            tips.append((tx,ty))
        for i,(x,y) in enumerate(tips):
            # blooms are in upper leaf axils, not on terminal clusters
            bx=x+(-1 if i%2 else 1)*S*.035;by=y+S*.04
            _trumpet_bloom(d,bx,by,S*.050,acc,rng)
    elif pid=="fuchsia":
        # Arching woody shoots, opposite/whorled serrate leaves, pendant axillary blooms.
        for i,spread in enumerate((-.34,-.20,-.06,.10,.25,.36)):
            x0=cx+spread*S*.08;y0=potline
            tx=cx+spread*S;ty=S*(.28+rng.random()*.09)
            _stem(d,(x0,y0),(cx+spread*S*.65,S*.46),(tx,ty),(112,83,57),max(3,int(S*.006)))
            for j in range(1,6):
                t=j/6;lx=x0+(tx-x0)*t;ly=y0+(ty-y0)*t
                for side in (-1,1):
                    _leaf_form(d,lx,ly,S*.082,S*.050,side*.95,fol,"scalloped")
                if j in (2,4):
                    fx=lx+S*.015;fy=ly+S*.018
                    d.line([(fx,fy),(fx+S*.012,fy+S*.035)],fill=stem,width=max(1,int(S*.0025)))
                    _fuchsia_bloom(d,fx+S*.012,fy+S*.035,S*.026,acc,rng)
    d.ellipse((cx-size*.22,base+size*.18,cx+size*.22,base+size*.23),fill=(231,222,198))
    return im


# Architecture-specific constructors. These are deliberately separate from
# the legacy potted-plant sketch and accept researched infocard morphology.
def _plate_canvas(size, seed):
    rng = random.Random(seed)
    im = Image.new("RGB", (size, size), PAPER)
    d = ImageDraw.Draw(im)
    for _ in range(size * size // 2200):
        x, y = rng.randrange(size), rng.randrange(size)
        v = rng.choice((246, 248, 251))
        d.point((x, y), fill=(v, v, max(225, v - 10)))
    return im, d, rng


def _frond(d, origin, tip, width, pairs, color, rng, sori=False, divided=1):
    """Draw one fern frond with a continuous rachis and paired pinnae."""
    ox, oy = origin
    tx, ty = tip
    dx, dy = tx - ox, ty - oy
    length = math.hypot(dx, dy) or 1
    nx, ny = -dy / length, dx / length
    rachis = (82, 105, 65)
    curve(d, [origin, ((ox + tx) / 2 + nx * width * .08,
                       (oy + ty) / 2 + ny * width * .08), tip],
          rachis, max(2, int(width * .045)))
    for i in range(pairs):
        t = (i + 1) / (pairs + 1)
        px, py = ox + dx * t, oy + dy * t
        taper = math.sin(math.pi * t) ** .72
        plen = width * (.16 + .78 * taper)
        for side in (-1, 1):
            ex = px + nx * side * plen
            ey = py + ny * side * plen
            # Pinnae point slightly toward the frond apex.
            ax = ex + dx / length * plen * .23
            ay = ey + dy / length * plen * .23
            col = blend(color, (190, 203, 142), rng.uniform(.02, .12))
            d.polygon([(px, py), (ex - dx / length * plen * .18,
                                   ey - dy / length * plen * .18),
                       (ax, ay), (px + nx * side * plen * .12,
                                  py + ny * side * plen * .12)],
                      fill=col, outline=blend(col, (42, 72, 42), .42))
            d.line([(px, py), (ax, ay)],
                   fill=blend(col, (220, 226, 174), .42), width=1)
            if divided > 1:
                for j in range(1, divided + 1):
                    q = j / (divided + 1)
                    qx = px + (ax - px) * q
                    qy = py + (ay - py) * q
                    for subside in (-1, 1):
                        sx = qx + nx * subside * plen * .12
                        sy = qy + ny * subside * plen * .12
                        d.line([(qx, qy), (sx, sy)],
                               fill=blend(col, (216, 224, 169), .35), width=1)
            if sori and i % 2 == 0:
                for q in (.35, .65):
                    sx = px + (ax - px) * q
                    sy = py + (ay - py) * q
                    rr = max(1, int(width * .009))
                    d.ellipse((sx-rr, sy-rr, sx+rr, sy+rr),
                              fill=(157, 111, 65))


def draw_fern_architecture(plant, size=768, seed=7):
    """Research-guided fern/fern-ally plate; no pot or generic broadleaf model."""
    data = plant.get("botanical_data", {})
    morph = data.get("morphology", {})
    description = " ".join(str(morph.get(k, "")) for k in
                            ("species_morphology", "construction_notes"))
    pid = plant.get("id", "")
    im, d, rng = _plate_canvas(size, seed + sum(map(ord, pid)))
    green = (91, 126, 76)
    dark = (72, 93, 58)
    cx = size * .5
    base = size * .86
    if pid == "equisetum_arvense":
        # Horsetail is a fern ally: jointed, ridged stems, not fern pinnae.
        for i in range(5):
            x = cx + (i - 2) * size * .055
            top = size * (.23 + rng.random() * .12)
            d.line([(x, base), (x, top)], fill=green, width=max(2, int(size*.009)))
            for t in (.30, .48, .66, .82):
                y = base - (base-top)*t
                d.line([(x-size*.018,y-size*.008),(x+size*.018,y-size*.008)],
                       fill=dark, width=max(1,int(size*.003)))
                for side in (-1,1):
                    d.line([(x,y),(x+side*size*.035,y-size*.045)],
                           fill=green, width=max(1,int(size*.0025)))
            d.polygon([(x-size*.018,top+size*.018),(x,top-size*.035),
                       (x+size*.018,top+size*.018)], fill=(142,119,76))
        return im
    # Frond form is selected from explicit researched architecture terms.
    divided = 3 if any(w in description.lower() for w in
                       ("3–4-pinnate", "3-4-pinnate", "tripinnate")) else (
               2 if "bipinnate" in description.lower() else 1)
    pairs = 23 if pid in ("polystichum_munitum", "dryopteris_filix_mas") else 17
    if pid == "adiantum_pedatum":
        # Distinctive forked, pseudopedate rachis with fan-shaped pinnules.
        for side in (-1, 1):
            _frond(d, (cx, base), (cx + side*size*.31, size*.27),
                   size*.24, 11, green, rng, sori=True)
        d.line([(cx,base),(cx,size*.61)], fill=(65,54,43),
               width=max(2,int(size*.006)))
    elif pid == "pteridium_aquilinum":
        # Broad triangular, highly divided blade on a long stipe.
        _frond(d,(cx,base),(cx,size*.22),size*.38,19,green,rng,sori=True,divided=3)
        for side in (-1,1):
            _frond(d,(cx,base-size*.25),(cx+side*size*.27,size*.34),
                   size*.25,15,green,rng,sori=True,divided=2)
    else:
        count = 5 if pid == "osmunda_regalis" else 7
        for i in range(count):
            angle = math.pi + (i-(count-1)/2)*.22
            reach = size*(.25 if pid=="polypodium_vulgare" else .31)
            tip=(cx+math.cos(angle)*reach, size*(.27+abs(i-(count-1)/2)*.025))
            _frond(d,(cx,base),tip,size*.25,pairs,green,rng,
                   sori=("sori" in description.lower() or pid!="osmunda_regalis"),
                   divided=divided)
        if pid == "osmunda_regalis":
            # Fertile terminal pinnae are contracted and densely sporangiate.
            for side in (-1,1):
                d.line([(cx,base-size*.48),(cx+side*size*.035,size*.19)],
                       fill=(113,91,58),width=max(2,int(size*.008)))
                for j in range(13):
                    y=size*(.20+j*.012)
                    d.ellipse((cx+side*size*.02,y,cx+side*size*.035,y+size*.008),
                              fill=(139,91,54))
    return im


def draw_graminoid_architecture(plant, size=768, seed=7):
    """Sedge/rush/grass plate preserving culm and inflorescence placement."""
    data = plant.get("botanical_data", {})
    morph = data.get("morphology", {})
    description = " ".join(str(morph.get(k, "")) for k in
                            ("species_morphology", "construction_notes"))
    pid = plant.get("id", "")
    im, d, rng = _plate_canvas(size, seed + sum(map(ord, pid)))
    green=(88,123,70); dark=(70,95,58); base=size*.86; cx=size*.5
    n=7 if pid in ("juncus_effusus","luzula_multiflora") else 5
    for i in range(n):
        x=cx+(i-(n-1)/2)*size*.035
        lean=(i-(n-1)/2)*size*.018
        top=size*(.20+rng.random()*.09)
        if pid in ("juncus_effusus","schoenoplectus_tabernaemontani"):
            # Rush/bulrush culms are cylindrical and largely leafless.
            d.line([(x,base),(x+lean,top)],fill=green,
                   width=max(2,int(size*.008)))
        else:
            # Sedge culms and grass-like blades are drawn separately.
            d.line([(x,base),(x+lean,top)],fill=green,
                   width=max(2,int(size*.006)))
            for side in (-1,1):
                y=base-size*(.24+.07*((i+side)%3))
                ex=x+lean*.45+side*size*.13
                ey=y-size*.12
                d.polygon([(x,y),(ex,ey),(x+side*size*.012,y+size*.012)],
                          fill=blend(green,(170,187,119),.18),
                          outline=dark)
        if pid=="juncus_effusus":
            # Inflorescence is pseudolateral, below a continuing bract.
            fy=top+size*.28
            d.line([(x+lean,top),(x+lean,top+size*.34)],
                   fill=green,width=max(2,int(size*.004)))
            for j in range(9):
                a=j*math.tau/9
                ex=x+lean+math.cos(a)*size*.045
                ey=fy+math.sin(a)*size*.025
                d.ellipse((ex-size*.006,ey-size*.006,ex+size*.006,ey+size*.006),
                          fill=(154,137,91))
        elif pid=="carex_aquatilis":
            # Lower pistillate spikes; terminal staminate spikes above them.
            for j in range(3):
                sy=top+size*(.10+j*.075)
                d.ellipse((x+lean-size*.012,sy,x+lean+size*.012,sy+size*.075),
                          fill=(133,111,70),outline=(88,79,54))
            d.ellipse((x+lean-size*.010,top-size*.045,
                       x+lean+size*.010,top+size*.055),
                      fill=(164,142,91),outline=(88,79,54))
        elif pid=="eriophorum_vaginatum":
            # Single terminal cottony spikelet on each flowering culm.
            d.line([(x+lean,top),(x+lean,top-size*.035)],
                   fill=(143,128,93),width=max(2,int(size*.003)))
            for j in range(15):
                a=j*math.tau/15
                ex=x+lean+math.cos(a)*size*.018
                ey=top-size*.045+math.sin(a)*size*.018
                d.line([(x+lean,top-size*.035),(ex,ey-size*.04)],
                       fill=(235,232,211),width=max(1,int(size*.002)))
    return im



def draw_bryophyte_architecture(plant, size=768, seed=7):
    """Nonvascular gametophyte-first construction for mosses and liverworts."""
    pid=plant["id"]
    im,d,rng=_plate_canvas(size,seed+sum(map(ord,pid)))
    green=(91,132,82); light=(142,169,111); dark=(65,96,65)
    cx=size*.5; base=size*.78
    if pid in ("marchantia_polymorpha","riccia_fluitans"):
        # Flat dichotomous thallus; no vascular stems or leaf blades.
        for i in range(9):
            x=cx+(i-4)*size*.012
            y=base+(rng.random()-.5)*size*.04
            direction=-1 if i%2 else 1
            for j in range(4):
                ex=x+direction*size*(.035+j*.012)
                ey=y-size*(.08+j*.035)
                d.line([(x,y),(ex,ey)],fill=green,width=max(3,int(size*.018)))
                d.line([(ex,ey),(ex+direction*size*.07,ey-size*.055)],
                       fill=light,width=max(2,int(size*.014)))
                d.line([(ex,ey),(ex-direction*size*.055,ey-size*.065)],
                       fill=green,width=max(2,int(size*.013)))
                # Air-chamber markings are subtle dorsal polygons.
                for k in range(4):
                    px=ex+direction*size*(.012+k*.009)
                    py=ey-size*(.01+k*.004)
                    rr=size*.004
                    d.ellipse((px-rr,py-rr,px+rr,py+rr),fill=light)
        if pid=="marchantia_polymorpha":
            # Gemma cups on dorsal thallus and stalked female/male receptacles.
            for i in range(5):
                x=cx+(i-2)*size*.10;y=base-size*.20
                d.ellipse((x-size*.025,y-size*.012,x+size*.025,y+size*.012),
                          fill=(111,145,82),outline=dark)
                d.ellipse((x-size*.012,y-size*.008,x+size*.012,y+size*.008),
                          fill=(74,111,67))
                d.line([(x,y-size*.01),(x,y-size*.18)],fill=green,
                       width=max(2,int(size*.006)))
                d.ellipse((x-size*.04,y-size*.22,x+size*.04,y-size*.16),
                          fill=light,outline=dark)
        return im
    if pid=="frullania_tamarisci":
        # Appressed leafy liverwort shoots; paired bilobed leaves with tiny lobules.
        for row in range(7):
            y=base-size*(.08+row*.055)
            x0=cx-size*.27
            d.line([(x0,y),(cx+size*.28,y-size*.035)],fill=dark,
                   width=max(2,int(size*.006)))
            for j in range(17):
                x=x0+j*size*.034
                for side in (-1,1):
                    d.ellipse((x-size*.012,y-size*.025,x+size*.012,y+size*.008),
                              fill=light,outline=dark)
                    d.ellipse((x+side*size*.009,y-size*.012,
                               x+side*size*.020,y+size*.009),
                              fill=green,outline=dark)
        return im
    # Mosses: upright acrocarpous tuft or creeping pleurocarpous mat.
    creeping=pid=="hypnum_cupressiforme"
    for shoot in range(15 if creeping else 11):
        x=cx+(rng.random()-.5)*size*(.55 if creeping else .32)
        y=base
        length=size*(.24+rng.random()*.13)
        endx=x+(rng.random()-.5)*size*(.10 if creeping else .035)
        endy=y-length
        d.line([(x,y),((x+endx)/2,y-length*.52),(endx,endy)],
               fill=dark,width=max(2,int(size*.005)))
        count=13
        for j in range(count):
            t=(j+1)/(count+1)
            px=x+(endx-x)*t;py=y+(endy-y)*t
            ll=size*(.035 if creeping else .045)*(1-.35*t)
            for side in (-1,1):
                ex=px+side*ll*.72;ey=py-ll*.40
                d.polygon([(px,py),(ex-size*.006,ey),(ex,ey-ll*.5),
                           (px+side*size*.004,py-size*.008)],
                          fill=light,outline=dark)
        if pid=="sphagnum_palustre":
            # Capitulum with spreading and pendent fascicle branches.
            d.ellipse((endx-size*.035,endy-size*.025,endx+size*.035,endy+size*.025),
                      fill=light,outline=dark)
            for j in range(4):
                bx=endx+(j-1.5)*size*.018
                d.line([(endx,endy),(bx,endy-size*.10)],fill=green,
                       width=max(2,int(size*.007)))
                d.line([(endx,endy),(bx,endy+size*.075)],fill=dark,
                       width=max(2,int(size*.006)))
        elif pid=="polytrichum_commune":
            # Long seta and four-angled capsule above the leafy gametophyte.
            sx=endx+size*.012
            d.line([(sx,endy),(sx-size*.01,endy-size*.16)],fill=(126,91,54),
                   width=max(2,int(size*.004)))
            d.polygon([(sx-size*.012,endy-size*.20),(sx+size*.012,endy-size*.20),
                       (sx+size*.016,endy-size*.16),(sx-size*.016,endy-size*.16)],
                      fill=(145,111,68),outline=dark)
    return im


def draw_aquatic_architecture(plant, size=768, seed=7):
    """Aquatic growth forms: floating, submerged, emergent and rooted."""
    pid=plant["id"]
    im,d,rng=_plate_canvas(size,seed+sum(map(ord,pid)))
    green=(83,132,91); light=(144,177,125); dark=(60,94,69)
    water_y=size*.59; cx=size*.5
    d.line([(size*.05,water_y),(size*.95,water_y)],fill=(133,177,193),
           width=max(2,int(size*.003)))
    if pid=="lemna_minor":
        # Discrete free-floating fronds, each with one simple root.
        for i in range(24):
            x=size*(.12+rng.random()*.76);y=water_y-size*(.015+rng.random()*.025)
            rx=size*(.012+rng.random()*.009)
            d.ellipse((x-rx,y-rx*.55,x+rx,y+rx*.55),fill=light,outline=dark)
            d.line([(x,y+rx*.45),(x+size*.004,y+rx*2.2)],
                   fill=(111,127,91),width=max(1,int(size*.002)))
        return im
    if pid=="elodea_canadensis":
        # Submerged nodal shoots with three-leaf whorls.
        for i in range(7):
            x=size*(.18+i*.105)
            d.line([(x,water_y+size*.25),(x+size*.02,water_y-size*.30)],
                   fill=green,width=max(2,int(size*.004)))
            for j in range(7):
                y=water_y+size*.18-j*size*.065
                for k in range(3):
                    a=k*math.tau/3
                    ex=x+size*.055*math.cos(a);ey=y-size*.025
                    d.ellipse((ex-size*.012,ey-size*.028,ex+size*.012,ey+size*.028),
                              fill=light,outline=dark)
        return im
    if pid=="vallisneria_americana":
        for i in range(11):
            x=cx+(i-5)*size*.018
            d.line([(cx,water_y+size*.25),(x+size*(i-5)*.018,water_y-size*(.18+rng.random()*.30))],
                   fill=green,width=max(2,int(size*.012)))
        return im
    if pid=="typha_latifolia":
        for i in range(7):
            x=cx+(i-3)*size*.035
            d.line([(x,water_y+size*.25),(x, size*.16)],fill=green,
                   width=max(3,int(size*.009)))
            for side in (-1,1):
                d.polygon([(x,water_y+size*.10),(x+side*size*.12,size*.42),
                           (x+side*size*.018,water_y+size*.10)],fill=light)
            if i in (2,3,4):
                d.line([(x,size*.16),(x,size*.19)],fill=(113,83,52),
                       width=max(8,int(size*.025)))
                d.line([(x,size*.20),(x,size*.29)],fill=(85,66,46),
                       width=max(9,int(size*.028)))
        return im
    if pid=="pistia_stratiotes":
        # Buoyant rosette with ribbed leaves and hanging fibrous root curtain.
        for i in range(9):
            a=i*math.tau/9
            x=cx+math.cos(a)*size*.11;y=water_y+math.sin(a)*size*.045
            ex=cx+math.cos(a)*size*.25;ey=water_y-size*.10+math.sin(a)*size*.11
            d.polygon([(cx,water_y),(x,y),(ex,ey),(cx+math.cos(a+.25)*size*.02,water_y)],
                      fill=light,outline=dark)
            d.line([(cx,water_y),(ex,ey)],fill=(203,211,166),width=2)
        for i in range(25):
            x=cx+(rng.random()-.5)*size*.20
            d.line([(x,water_y),(x+(rng.random()-.5)*size*.08,
                   water_y+size*(.10+rng.random()*.20))],
                   fill=(119,103,79),width=1)
        return im
    if pid in ("nymphaea_odorata","nuphar_variegata","nelumbo_lutea"):
        # Rhizome below substrate, petioles crossing water plane, diagnostic blades.
        substrate=water_y+size*.17
        d.line([(size*.22,substrate),(size*.78,substrate)],fill=(126,104,76),
               width=max(3,int(size*.012)))
        for i in range(4):
            x=cx+(i-1.5)*size*.035
            d.line([(cx,substrate),(x,water_y-size*.06)],fill=green,
                   width=max(2,int(size*.006)))
        for i in range(3):
            x=cx+(i-1)*size*.22;y=water_y-size*.08
            if pid=="nelumbo_lutea":
                d.ellipse((x-size*.09,y-size*.035,x+size*.09,y+size*.035),
                          fill=light,outline=dark,width=2)
                d.ellipse((x-size*.012,y-size*.035,x+size*.012,y+size*.035),fill=dark)
            else:
                d.pieslice((x-size*.10,y-size*.09,x+size*.10,y+size*.09),
                           35,325,fill=light,outline=dark)
                d.line([(x,y),(x+size*.07,y-size*.05)],fill=dark,width=2)
        if pid=="nelumbo_lutea":
            d.ellipse((cx-size*.045,water_y-size*.31,cx+size*.045,water_y-size*.22),
                      fill=(229,213,137),outline=dark)
            d.ellipse((cx-size*.035,water_y-size*.20,cx+size*.035,water_y-size*.16),
                      fill=(149,129,74),outline=dark)
        else:
            d.ellipse((cx-size*.04,water_y-size*.18,cx+size*.04,water_y-size*.10),
                      fill=(239,207,91),outline=dark)
        return im
    if pid=="sagittaria_latifolia":
        for i in range(5):
            x=cx+(i-2)*size*.045
            top=size*(.24+rng.random()*.12)
            d.line([(x,water_y),(x,top)],fill=green,width=max(2,int(size*.006)))
            d.polygon([(x,top),(x-size*.09,top+size*.16),
                       (x,top+size*.09),(x+size*.09,top+size*.16)],
                      fill=light,outline=dark)
        return im
    return im


def draw_plant(plant, size=768, seed=7):
    pid = plant["id"]
    group = (plant.get("botanical_data", {}).get("catalogue", {}).get("coverage_group")
             or plant.get("coverage_group"))
    if group == "fern":
        return draw_fern_architecture(plant, size, seed)
    if group == "graminoid":
        return draw_graminoid_architecture(plant, size, seed)
    if group == "bryophyte":
        return draw_bryophyte_architecture(plant, size, seed)
    if group == "aquatic":
        return draw_aquatic_architecture(plant, size, seed)
    if pid in FLOWER_IDS:
        return draw_flower_plant(plant, size, seed)
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

def card_record(p, previous=None):
    family, habit, anatomy, leaf_shape, bloom, fruit = PROFILES[p["id"]]
    user_data = {
        "common_name": p["common_name"],
        "botanical_family": family,
        "growth_habit": habit,
        "diagnostic_botany": anatomy,
        "leaf_construction": leaf_shape,
        "flower_construction": bloom,
        "fruit_or_harvest": fruit,
        "foliage_colour": p.get("foliage_color")
    }
    provenance = {
        key: ("plants.js" if key in ("common_name", "foliage_colour")
              else "tools/plant-art.py PROFILES")
        for key in user_data
    }
    record = {
        "id": p["id"], "name": p["common_name"], "family": family,
        "growth_habit": habit, "diagnostic_botany": anatomy,
        "leaf_construction": leaf_shape, "flower_construction": bloom,
        "fruit_or_harvest": fruit, "source_record": "plants.js + tools/plant-art.py PROFILES",
        "renderer": "tools/plant-art.py", "style": "Naturalist's Plate",
        "style_terms": ["botanical naturalist plate", "accurate species architecture",
                        "crisp closed leaf shapes", "fine visible midribs and lateral veins",
                        "soft upper-left light", "thin same-hue edge", "warm ivory paper",
                        "terracotta nursery pot", "seeded natural variation"],
        "user_data": user_data,
        "user_data_provenance": provenance,
        "populated_user_data_fields": list(user_data),
        "populated_user_data_count": len(user_data),
        "research_status": "profile-only record; botanical research still needed",
        "artwork_status": "no artwork generated"
    }
    # Preserve every pre-existing research, taxonomy, provenance, and workflow
    # field. Only renderer-owned presentation/profile fields are regenerated.
    if previous:
        record["user_data"].update(previous.get("user_data", {}))
        record["user_data_provenance"].update(previous.get("user_data_provenance", {}))
        record["populated_user_data_fields"] = list(record["user_data"])
        record["populated_user_data_count"] = len(record["user_data"])
        renderer_owned = {
            "id", "name", "diagnostic_botany",
            "leaf_construction", "flower_construction", "fruit_or_harvest",
            "source_record", "renderer", "style", "style_terms", "user_data",
            "user_data_provenance", "populated_user_data_fields",
            "populated_user_data_count"
        }
        for key, value in previous.items():
            if key not in renderer_owned:
                record[key] = value
    else:
        image = ROOT / "plant-art" / f"{p['id']}.png"
        if image.is_file():
            record["image"] = image.relative_to(ROOT).as_posix()
    return record

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
    ap.add_argument("--source-image", action="append", default=[], metavar="PLANT_ID=PATH",
                    help="Use an existing approved raster artwork as the source; duplicate it unchanged.")
    ap.add_argument("--replace-derived", action="store_true",
                    help="Replace files under plant-art/derived only; never changes source artwork.")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--infocards-only", action="store_true",
                    help="Refresh all botanical infocards without drawing or rendering any images.")
    args = ap.parse_args()
    plants = plant_list()
    missing = [p["id"] for p in plants if p["id"] not in PROFILES]
    extra = sorted(set(PROFILES)-{p["id"] for p in plants})
    if missing or extra:
        raise SystemExit(f"Profile mismatch. Missing: {missing}; unused: {extra}")
    if args.check:
        cards = load_infocard_index()
        for plant in plants:
            card = cards.get(plant["id"], {})
            data = botanical_data(plant, card)
            if not isinstance(data["taxonomy"], dict) or not isinstance(data["morphology"], dict):
                raise SystemExit(f"Invalid botanical data interface for {plant['id']}")
            if card:
                for key in ("species_dimensions", "species_morphology", "construction_notes"):
                    if key in card and data["morphology"].get(key) != card[key]:
                        raise SystemExit(f"Research field not passed through for {plant['id']}: {key}")
            probe = dict(card)
            probe["preservation_test_marker"] = "must-survive"
            merged = card_record(plant, probe)
            if merged.get("preservation_test_marker") != "must-survive":
                raise SystemExit(f"Infocard preservation test failed for {plant['id']}")
            for key in ("species_dimensions", "species_morphology", "construction_notes"):
                if key in card and merged.get(key) != card[key]:
                    raise SystemExit(f"Infocard research preservation failed for {plant['id']}: {key}")
        # Exercise the new lineage constructors in memory only. No files are written.
        catalogue = load_infocard_index()
        architecture_checks = 0
        for card in catalogue.values():
            group = card.get("coverage_group")
            if group not in ("fern", "graminoid"):
                continue
            probe = {
                "id": card["id"],
                "botanical_data": botanical_data({}, card),
            }
            if group == "fern":
                preview = draw_fern_architecture(probe, size=192, seed=7)
            else:
                preview = draw_graminoid_architecture(probe, size=192, seed=7)
            if preview.size != (192, 192):
                raise SystemExit(f"Architecture constructor returned invalid image size: {card['id']}")
            architecture_checks += 1
        print(f"OK: {len(plants)} legacy profiles; lossless infocard preservation; "
              f"{architecture_checks} fern/graminoid architecture previews passed in memory.")
        return
    existing_cards = {}
    if INFOCARDS.is_file():
        try:
            existing_cards = {item["id"]: item for item in json.loads(INFOCARDS.read_text(encoding="utf-8"))}
        except (ValueError, KeyError, TypeError):
            raise SystemExit(f"Could not safely read existing infocards: {INFOCARDS}")
    supplemental_path = ROOT / "plant-art" / "diverse-infocards.json"
    supplemental_cards = []
    if supplemental_path.is_file():
        try:
            supplemental_cards = json.loads(supplemental_path.read_text(encoding="utf-8"))
        except (ValueError, TypeError):
            raise SystemExit(f"Could not safely read supplemental infocards: {supplemental_path}")
    if args.infocards_only:
        records = [card_record(p, existing_cards.get(p["id"])) for p in plants]
        known = {item["id"] for item in records}
        records.extend(item for item in supplemental_cards if item.get("id") not in known)
        INFOCARDS.parent.mkdir(parents=True, exist_ok=True)
        INFOCARDS.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Updated {len(records)} botanical infocards ({len(plants)} rendered-plant profiles and {len(supplemental_cards)} diverse-lineage profiles); no images were rendered.")
        return
    selected = [p for p in plants if not args.only or p["id"] in args.only]
    known_ids = {p["id"] for p in plants}
    source_images = {}
    for item in args.source_image:
        if "=" not in item:
            raise SystemExit(f"Invalid --source-image {item!r}; use PLANT_ID=PATH")
        plant_id, source_path = item.split("=", 1)
        if plant_id not in known_ids:
            raise SystemExit(f"Unknown plant ID in --source-image: {plant_id}")
        if plant_id in source_images:
            raise SystemExit(f"More than one source image supplied for {plant_id}")
        source_images[plant_id] = Path(source_path)
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    thumbs = []
    for p in selected:
        pid = p["id"]
        record = card_record(p, existing_cards.get(pid))
        if pid in source_images:
            src = source_images[pid]
            if not src.is_absolute():
                src = ROOT / src
            if not src.is_file():
                raise SystemExit(f"Source artwork does not exist: {src}")
            digest = hashlib.sha256(src.read_bytes()).hexdigest()
            source_dir = OUT / "source"
            source_dir.mkdir(parents=True, exist_ok=True)
            preserved = source_dir / f"{pid}-{digest[:10]}{src.suffix.lower() or '.png'}"
            if preserved.exists():
                if hashlib.sha256(preserved.read_bytes()).hexdigest() != digest:
                    raise SystemExit(f"Refusing to overwrite preserved source: {preserved}")
            else:
                shutil.copy2(src, preserved)
            output = OUT / f"{pid}{src.suffix.lower() or '.png'}"
            if output.exists():
                same = hashlib.sha256(output.read_bytes()).hexdigest() == digest
                if not same and not args.replace_derived:
                    raise SystemExit(f"Derived output exists and differs: {output}. Use --replace-derived to replace this derived file.")
            if not output.exists() or args.replace_derived:
                shutil.copy2(src, output)
            image = Image.open(output).convert("RGB")
            record["render_mode"] = "preserved-source-copy"
            record["source_artwork_path"] = str(src)
            record["source_sha256"] = digest
            record["preserved_source_copy"] = preserved.relative_to(ROOT).as_posix()
            record["image"] = output.relative_to(ROOT).as_posix()
        else:
            output = OUT / f"{pid}.png"
            if output.exists() and not args.replace_derived:
                raise SystemExit(f"Derived output exists: {output}. Use --replace-derived to replace derived output only.")
            image = draw_plant(p, args.size, args.seed)
            image.save(output, optimize=True)
            record["render_mode"] = "procedural-draft"
            record["image"] = output.relative_to(ROOT).as_posix()
        records.append(record)
        thumbs.append((p, image.copy()))
    (OUT / "infocards.json").write_text(json.dumps(records, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    merged_cards = dict(existing_cards)
    for item in records:
        merged_cards[item["id"]] = item
    canonical_records = [merged_cards.get(p["id"], card_record(p)) for p in plants]
    canonical_ids = {item["id"] for item in canonical_records}
    canonical_records.extend(item for item in supplemental_cards if item.get("id") not in canonical_ids)
    INFOCARDS.write_text(json.dumps(canonical_records, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
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
    print(f"Rendered or preserved {len(selected)} of {len(plants)} plants in {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
