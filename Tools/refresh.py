"""Vault refresh for the comics Obsidian vault.

Run from anywhere:  python refresh.py            (recompute derived properties + Cart Planner.md)
                    python refresh.py set "<note name>" key value   (set/replace one property; value is YAML, e.g. 'true', '"2026-10"', 85)

Derived properties written to every book note (do not edit by hand):
  seq            position on its line's timeline. Epics use their Epic number; an omnibus/TPB uses the
                 lowest Epic number it covers + 0.5, so it sorts right after the Epic where it starts.
                 Modern runs and events use 1000+ / small manual values. Every list sorts by seq.
  missing_before for wanted/planned/oop books: how many Epics between the reading position and this book
                 are not owned/covered/incoming (0 means buying it is contiguous with what you can read).
  purpose        reading | security | preorder | future | modern | event
Managed by hand or with `set`: urgency, urgency_reason, cart (e.g. "2026-10").
"""
import glob
import os
import re
import sys
import yaml

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
READY = ("owned", "covered", "incoming")
NEEDS = ("wanted", "oop", "planned")
DERIVED = ("seq", "missing_before", "purpose")
MAIN = ["Iron Man", "Doctor Strange", "Spider-Man", "Thor", "Daredevil"]
CURRENT_CART = "2026-10"


def load(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return text, m, yaml.safe_load(m.group(1))


def write_props(path, updates, remove=()):
    """Replace/insert single-line properties in the frontmatter, leaving everything else untouched."""
    text, m, _ = load(path)
    lines = m.group(1).split("\n")
    keys = set(updates) | set(remove)
    lines = [l for l in lines if not any(l.startswith(k + ":") for k in keys)]
    new = [f"{k}: {v}" for k, v in updates.items() if v is not None]
    at = next((i for i, l in enumerate(lines) if l.startswith("source:")), len(lines))
    lines[at:at] = new
    open(path, "w", encoding="utf-8").write("---\n" + "\n".join(lines) + "\n---\n" + text[m.end():])


def scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    return '"' + str(v).replace('"', "'") + '"'


def manual_seq(fm, name):
    t = fm.get("title", "") + " " + name
    m = re.search(r"\(2022\) #(\d+)", t)
    if m:
        return 1000 + int(m.group(1)) + 0.5
    if "IM2022" in t or "Gerry Duggan" in t:
        for k, v in (("Vol 1", 1001), ("Vol 2", 1007), ("Vol 3", 1013)):
            if k in t:
                return v
    if "(2026)" in t or "IM2026" in t:
        if "cartoony" in t.lower() or "#1-4" in t:
            return 2001.6
        if "liked cover" in t or "#1 " in t and "Vol" not in t:
            return 2001.5
        if "Vol 2" in t:
            return 2007
        return 2001
    table = {"Strange Season One": 1.5, "Aaron": 1001, "Absolute Carnage": 2, "First Host": 1, "King in Black": 3, "Venom War": 4, "Secret Wars": 1}
    for k, v in table.items():
        if k in t:
            return v
    return 9999


def main():
    files = glob.glob(VAULT + "Books/**/*.md", recursive=True)
    notes = {}
    for f in files:
        _, _, fm = load(f)
        notes[os.path.basename(f)[:-3]] = (f, fm)
    epic_num = {n: fm["number"] for n, (f, fm) in notes.items() if fm.get("type") == "Epic Collection" and not fm.get("modern") and isinstance(fm.get("number"), int)}
    seq = {}
    for n, (f, fm) in notes.items():
        if fm.get("type") == "Epic Collection" and isinstance(fm.get("number"), int):
            seq[n] = (100 + fm["number"]) if fm.get("modern") else fm["number"]
        elif fm.get("covers"):
            nums = [epic_num[l[2:-2]] for l in fm["covers"] if l[2:-2] in epic_num]
            seq[n] = (min(nums) + 0.5) if nums else manual_seq(fm, n)
        else:
            seq[n] = manual_seq(fm, n)
    # per-line epic timeline
    line_epics = {}
    for n, (f, fm) in notes.items():
        if n in epic_num:
            line_epics.setdefault(fm["line"], []).append((fm["number"], n, fm))
    pos = {}
    runway = {}
    gap = {}
    for line, eps in line_epics.items():
        eps.sort()
        position = next((e[0] for e in eps if not e[2].get("read")), None)
        pos[line] = position
        if position is None:
            continue
        r = 0
        first_gap = None
        for num, n, fm in eps:
            if num < position:
                continue
            if fm["status"] in READY:
                if first_gap is None:
                    r += 1
            elif first_gap is None:
                first_gap = (num, n)
        runway[line] = r
        gap[line] = first_gap
    # derived per note
    out = {}
    for n, (f, fm) in notes.items():
        upd = {"seq": scalar(seq[n])}
        st = fm.get("status")
        line = fm["line"]
        if st in NEEDS:
            if seq[n] >= 1000 or fm.get("modern"):
                purpose = "modern"
                mb = None
            elif line not in line_epics or line in ("Venom", "Secret Wars"):
                purpose = "event"
                mb = None
            else:
                own_epics = {epic_num[l[2:-2]] for l in fm.get("covers", []) if l[2:-2] in epic_num}
                if n in epic_num:
                    own_epics.add(fm["number"])
                start = min(own_epics) if own_epics else None
                position = pos.get(line)
                mb = 0
                if start is not None and position is not None:
                    for num, en, efm in line_epics[line]:
                        if position <= num < start and num not in own_epics and efm["status"] not in READY:
                            mb += 1
                if fm.get("budget") == "quarterly" and st == "planned":
                    purpose = "preorder"
                elif mb == 0:
                    purpose = "reading"
                elif st == "oop" or fm.get("urgency") in ("high", "medium"):
                    purpose = "security"
                else:
                    purpose = "future"
            upd["purpose"] = scalar(purpose)
            if mb is not None:
                upd["missing_before"] = mb
            out[n] = (purpose, mb)
        write_props(f, upd, remove=[k for k in DERIVED if k not in upd])
    make_planner(notes, seq, pos, runway, gap, line_epics)
    print("refreshed", len(files), "notes")


def money(fm):
    v = fm.get("price_paid") or fm.get("price_seen")
    return v


def make_planner(notes, seq, pos, runway, gap, line_epics):
    # reload (frontmatter changed)
    data = {}
    for n, (f, _) in notes.items():
        _, _, fm = load(f)
        data[n] = fm
    L = ["# Cart Planner", "",
         "Generated by `Tools/refresh.py` from the book notes. Do not edit by hand; ask Claude to refresh it after orders, arrivals or finished books.", "",
         "## 1. Reading runway (the one-or-two-Epics-a-month rule)", "",
         "| Line | Reading position | Epics ready to read (contiguous) | First gap | Ways to fill the gap |", "|---|---|---|---|---|"]
    for line in MAIN:
        if line not in pos or pos[line] is None:
            continue
        eps = {e[0]: e for e in line_epics[line]}
        p = pos[line]
        g = gap.get(line)
        gtxt, fill = "none", ""
        if g:
            gnum = g[0]
            gtxt = f"Epic {gnum}"
            opts = []
            for n, fm in data.items():
                if fm["line"] != line or fm.get("status") not in NEEDS + ("unreleased",):
                    continue
                covers = {data[l[2:-2]]["number"] for l in fm.get("covers", []) if l[2:-2] in data and isinstance(data[l[2:-2]].get("number"), int) and data[l[2:-2]].get("type") == "Epic Collection"}
                if n == g[1] or gnum in covers:
                    price = fm.get("price_seen")
                    opts.append(f"[[{n}]]" + (f" ({price} {fm.get('store', '')})".replace(" )", ")") if price else "") + f" - {fm['status']}")
            fill = "; ".join(opts) if opts else "no route found"
        L.append(f"| {line} | Epic {p} | {runway.get(line, 0)} | {gtxt} | {fill} |")
    L += ["", "A line whose runway is under 2 needs its next contiguous book in the cart. Strange is blocked when the first gap is an unreleased Epic.", ""]
    cand = [(fm["line"], seq[n], n, fm) for n, fm in data.items() if fm.get("status") in NEEDS]
    cand = [c for c in cand if c[3].get("purpose") != "future" or c[3].get("price_seen") or (c[3].get("missing_before") or 0) <= 2]
    order = {"reading": 0, "security": 1, "preorder": 2, "future": 3, "modern": 4, "event": 5}
    cand.sort(key=lambda x: (order.get(x[3].get("purpose", "future"), 9), runway.get(x[0], 99), x[0], x[1]))
    L += ["## 2. Candidates by purpose", "",
          "Sorted by purpose, then by how short the line's runway is, then by the first comic. Far-future books with no price and many missing Epics before them are left out (see the Buy List dashboard for everything).", "",
          "| Purpose | Line | Line runway | Book | Status | Price seen | Store | Missing Epics before it | Urgency |", "|---|---|---|---|---|---|---|---|---|"]
    for line, s, n, fm in cand:
        L.append(f"| {fm.get('purpose', '')} | {line} | {runway.get(line, '')} | [[{n}]] | {fm['status']} | {fm.get('price_seen', '')} | {fm.get('store', '')} | {fm.get('missing_before', '')} | {fm.get('urgency', '')}{(' - ' + fm['urgency_reason']) if fm.get('urgency_reason') else ''} |")
    L += ["", "- **reading**: nothing unowned sits between your reading position and this book. This is the 'next Epic' slot.",
          "- **security**: out of print, or a deadline (discount, last copy). Ahead of a gap, so it doesn't advance reading yet.",
          "- **preorder**: quarterly pre-order, outside the 200 EUR.", "- **future**: not urgent, far from your position.",
          "- **modern / event**: palate cleansers.", ""]
    cart = [(fm["line"], seq[n], n, fm) for n, fm in data.items() if fm.get("cart") == CURRENT_CART]
    cart.sort(key=lambda x: (x[0], x[1]))
    total = 0
    L += [f"## 3. Current cart ({CURRENT_CART})", "", "| Book | Store | Price | Purpose |", "|---|---|---|---|"]
    for line, s, n, fm in cart:
        p = money(fm) or 0
        total += p
        L.append(f"| [[{n}]] | {fm.get('store', '')} | {p} | {fm.get('purpose', '')} |")
    L += ["", f"Subtotal of listed books: **{round(total, 2)} EUR**. Add shipping by store (Walt's about 9 below 150, free above; Cheap-Comics about 20 flat). Budget about 200, flexible, no rollover; quarterly pre-orders are outside it.", ""]
    open(VAULT + "Cart Planner.md", "w", encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    if len(sys.argv) >= 5 and sys.argv[1] == "set":
        name, key, value = sys.argv[2], sys.argv[3], sys.argv[4]
        hits = [f for f in glob.glob(VAULT + "Books/**/*.md", recursive=True) if os.path.basename(f)[:-3] == name]
        assert len(hits) == 1, hits
        write_props(hits[0], {key: value})
        print("set", key, "on", name)
    else:
        main()
