#!/usr/bin/env python3
"""Render the contact sheets: every plant in every state, the size ladder, and core.js's test swatches,
on light and dark backgrounds. Optionally compare them pixel by pixel with an earlier run.

Run from the repository folder:
  python3 tools/contact-sheet.py                      write contact/*.png
  python3 tools/contact-sheet.py --out before         write to another folder (e.g. before a change)
  python3 tools/contact-sheet.py --compare before     render, then report how many pixels differ from before/
                                                      (and write contact/diff-*.png where they do)
Needs Python Playwright with Chrome or Chromium, and Pillow for --compare.
The output folders are not committed (see .gitignore).
"""
import argparse, pathlib, shutil, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = (ROOT / "tools" / "contact-sheet.html").as_uri()
SHEETS = ["plants", "ladder", "core", "containers"]


def browser(p):
    exe = next((x for x in ("google-chrome", "chromium", "chromium-browser") if shutil.which(x)), None)
    args = {"args": ["--allow-file-access-from-files"]}
    return p.chromium.launch(executable_path=shutil.which(exe), **args) if exe else p.chromium.launch(**args)


def render(out):
    out.mkdir(parents=True, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        b = browser(p)
        for sheet in SHEETS:
            for bg in ("light", "dark"):
                pg = b.new_page(viewport={"width": 1000, "height": 800})
                pg.on("pageerror", lambda e, s=sheet: errors.append(f"{s}: {e}"))
                pg.goto(f"{PAGE}?sheet={sheet}&bg={bg}")
                pg.wait_for_function("document.title==='done'", timeout=120000)
                pg.locator("#c").screenshot(path=str(out / f"{sheet}-{bg}.png"))
                pg.close()
        b.close()
    for e in errors:
        print("page error:", e)
    print(f"wrote {len(SHEETS) * 2} sheets to {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return not errors


def compare(new, old):
    from PIL import Image, ImageChops
    same = True
    for f in sorted(new.glob("*.png")):
        if f.name.startswith("diff-"):
            continue
        o = old / f.name
        if not o.exists():
            print(f"{f.name}: no earlier copy"); same = False; continue
        a, b = Image.open(f).convert("RGB"), Image.open(o).convert("RGB")
        if a.size != b.size:
            print(f"{f.name}: size changed {b.size} -> {a.size}"); same = False; continue
        d = ImageChops.difference(a, b)
        mask = d.convert("L").point(lambda v: 255 if v else 0)
        n = mask.histogram()[255]
        print(f"{f.name}: {n} pixels differ")
        if n:
            same = False
            mask.save(new / f"diff-{f.name}")
    print("identical" if same else "changed")
    return same


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="contact")
    ap.add_argument("--compare")
    a = ap.parse_args()
    out = (ROOT / a.out).resolve()
    ok = render(out)
    if a.compare:
        ok = compare(out, (ROOT / a.compare).resolve()) and ok
    sys.exit(0 if ok else 1)
