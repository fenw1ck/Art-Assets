#!/usr/bin/env python3
"""The research library's map: look things up before researching them again.

Run from the repository folder:
  python3 tools/research.py lookup <name>   what the library knows about <name>, level by level up to its root
  python3 tools/research.py lookup <name> --in <parent>   for something new: show what its parent already covers
  python3 tools/research.py map             the whole tree, with depth, date and gaps
  python3 tools/research.py check           validate every entry's header and parent
  python3 tools/research.py index           rewrite research/index.json (the map, for other tools)

Entries are the Markdown files under research/ (see research/README.md). Needs PyYAML.
"""
import difflib, json, pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "research"
DEPTHS = ["outline", "standard", "deep"]
KINDS = ["subject", "material", "pattern", "technique"]
SECTIONS = ["Parts", "Distinguishing features", "Construction order", "States", "Rendering notes", "Log", "Sources"]


def load():
    entries = {}
    for f in sorted(LIB.rglob("*.md")):
        if f.name == "README.md":
            continue
        text = f.read_text()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            entries[f"!{f}"] = {"file": str(f.relative_to(ROOT)), "error": "no header"}
            continue
        h = yaml.safe_load(m.group(1)) or {}
        body = m.group(2)
        h["file"] = str(f.relative_to(ROOT))
        h["sections"] = [s for s in SECTIONS if re.search(rf"^## {re.escape(s)}", body, re.M)]
        h["sources"] = len(re.findall(r"^- .*https?://", body.split("## Sources", 1)[1], re.M)) if "## Sources" in body else 0
        for k in ("aliases", "gaps", "used_by"):
            h[k] = h.get(k) or []
        h["parent"] = h.get("parent") or "none"
        h["updated"] = str(h.get("updated", ""))
        entries[h.get("id", f"!{f}")] = h
    return entries


def names(e):
    return [e["id"], e.get("title", "")] + list(e["aliases"])


def find(entries, q):
    q = q.lower().strip()
    exact = [e for e in entries.values() if "id" in e and q in (n.lower() for n in names(e))]
    if exact:
        return exact[0], []
    part = [e for e in entries.values() if "id" in e and any(q in n.lower() for n in names(e))]
    if len(part) == 1:
        return part[0], []
    allnames = {n.lower(): e["id"] for e in entries.values() if "id" in e for n in names(e)}
    close = difflib.get_close_matches(q, allnames, n=5, cutoff=0.75)
    return None, sorted({allnames[c] for c in close} | {e["id"] for e in part})


def chain(entries, e):
    out = [e]
    while out[-1]["parent"] != "none":
        p = entries.get(out[-1]["parent"])
        if not p or p in out:
            out.append({"id": out[-1]["parent"], "missing": True})
            break
        out.append(p)
    return out


def describe(e):
    if e.get("missing"):
        return f"  {e['id']:<22} NO ENTRY YET"
    gaps = "; ".join(e["gaps"]) if e["gaps"] else "none listed"
    return (f"  {e['id']:<22} {e['depth']:<9} updated {e['updated']}  {e['sources']} sources  {e['file']}\n"
            f"  {'':<22} sections: {', '.join(e['sections']) or '-'}\n"
            f"  {'':<22} gaps: {gaps}")


def cmd_lookup(entries, q, under=None):
    e, near = find(entries, q)
    if not e and under:
        p, _ = find(entries, under)
        if p:
            print(f"No entry for '{q}' yet. What the library holds above it, from '{p['id']}':\n")
            for level in chain(entries, p):
                print(describe(level))
            print(f"\nNext: research only what sets '{q}' apart, and save it as a new entry with parent: {p['id']}.")
            return
    if not e:
        print(f"No entry for '{q}'.")
        if near:
            print("Close matches: " + ", ".join(near))
        print("Next: research it, starting under the nearest existing parent "
              "(roots: " + ", ".join(sorted(x["id"] for x in entries.values() if x.get("parent") == "none" and x.get("kind") != "technique")) + ").")
        return
    print(f"'{q}' -> {e['id']} ({e.get('title', '')})\n")
    for level in chain(entries, e):
        print(describe(level))
    kids = [x["id"] for x in entries.values() if x.get("parent") == e["id"]]
    if kids:
        print(f"\n  children: {', '.join(kids)}")
    tech = [x["id"] for x in entries.values() if x.get("kind") == "technique"]
    print(f"\n  rendering techniques on file: {', '.join(tech)}")
    print("\nChoices: use as is | fill the listed gaps | run a deeper search")


def cmd_map(entries):
    kids = {}
    for e in entries.values():
        if "id" in e:
            kids.setdefault(e["parent"], []).append(e)

    def walk(pid, indent):
        for e in sorted(kids.get(pid, []), key=lambda x: (x.get("kind", ""), x["id"])):
            gaps = f"  gaps: {len(e['gaps'])}" if e["gaps"] else ""
            print(f"{'  ' * indent}{e['id']}  [{e.get('kind')}, {e.get('depth')}, {e['updated']}]{gaps}")
            walk(e["id"], indent + 1)
    walk("none", 0)
    orphans = [e["id"] for e in entries.values() if "id" in e and e["parent"] != "none" and e["parent"] not in entries]
    if orphans:
        print("\nParent missing for: " + ", ".join(orphans))


def cmd_check(entries):
    bad = 0
    seen = {}
    for key, e in entries.items():
        if "error" in e:
            print(f"{e['file']}: {e['error']}"); bad += 1; continue
        for f in ("id", "title", "kind", "depth", "updated"):
            if not e.get(f):
                print(f"{e['file']}: missing {f}"); bad += 1
        if e.get("kind") not in KINDS:
            print(f"{e['file']}: kind must be one of {KINDS}"); bad += 1
        if e.get("depth") not in DEPTHS:
            print(f"{e['file']}: depth must be one of {DEPTHS}"); bad += 1
        if e["parent"] != "none" and e["parent"] not in entries:
            print(f"{e['file']}: parent '{e['parent']}' has no entry"); bad += 1
        for n in names(e):
            n = n.lower()
            if n and n in seen and seen[n] != e["id"]:
                print(f"{e['file']}: name '{n}' also used by {seen[n]}"); bad += 1
            seen[n] = e["id"]
        if e.get("depth") != "outline" and e["sources"] == 0:
            print(f"{e['file']}: depth {e['depth']} but no sources listed (note it as a gap)")
    print(f"{len(entries)} entries, {bad} problems")
    return bad


def cmd_index(entries):
    keep = ("id", "title", "kind", "parent", "aliases", "depth", "updated", "gaps", "used_by", "file", "sections", "sources")
    data = sorted(({k: e.get(k) for k in keep} for e in entries.values() if "id" in e), key=lambda x: x["file"])
    (LIB / "index.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote research/index.json, {len(data)} entries")


if __name__ == "__main__":
    a = sys.argv[1:]
    E = load()
    if not a or a[0] not in ("lookup", "map", "check", "index"):
        print(__doc__); sys.exit(1)
    if a[0] == "lookup":
        under = None
        if "--in" in a:
            i = a.index("--in"); under = " ".join(a[i + 1:]); a = a[:i]
        cmd_lookup(E, " ".join(a[1:]), under)
    elif a[0] == "map":
        cmd_map(E)
    elif a[0] == "check":
        sys.exit(1 if cmd_check(E) else 0)
    else:
        cmd_index(E)
