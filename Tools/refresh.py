"""Vault refresh for the comics Obsidian vault.

Usage (run from anywhere):
  python refresh.py                  recompute derived data, rewrite the generated notes, then run the checks
  python refresh.py --cart 2026-11   same, but show that month's cart in the planner (default: the cart for the next 24th)
  python refresh.py check            only run the checks, change nothing
  python refresh.py set "<note name>" key value   set one property (value is YAML: true, "2026-10", 85)

Derived properties (written here, don't edit by hand):
  seq            position on the line's timeline. Epics use their number (modern Epics 100+); an omnibus/TPB uses
                 the lowest Epic it covers + 0.5; anything else uses its hand-set `order` property.
  status         only for Epics you don't own yourself: covered / incoming / partial, worked out from the omnibuses
                 that contain them (`covers` = whole Epic, `covers_partial` = part of it). Owned or read Epics are
                 never touched.
  covered_via    the owned/incoming omnibuses that derived status came from.
  missing_before books you still need: unowned Epics between the reading position and this book (0 = contiguous).
  purpose        reading | security | preorder | future | modern | event
  order_month    "YYYY-MM" from the hand-set `ordered` date, for the Spending dashboard.
Generated notes: Cart Planner.md, and the %% generated %% blocks in Comics Hub.md and Ratings Overview.md.
"""
import datetime
import glob
import os
import re
import sys
import yaml

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
READY = ("owned", "covered", "incoming")
NEEDS = ("wanted", "oop", "planned", "partial")
STATUSES = READY + NEEDS + ("unreleased", "parked")
RANK = {"owned": 5, "covered": 4, "incoming": 3, "partial": 2}
DERIVED = ("seq", "missing_before", "purpose", "covered_via", "order_month")
MAIN = ["Iron Man", "Doctor Strange", "Spider-Man", "Thor", "Daredevil"]
PRIORITY = {"Iron Man": 1, "Doctor Strange": 2}


# ---------- files ----------

def load(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return text, m, yaml.safe_load(m.group(1))


def save(path, text):
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if text != old:
        open(path, "w", encoding="utf-8", newline="\n").write(text)


def write_props(path, updates, remove=()):
    """Set single-line properties in place (new ones go before `source:`); drop the keys in `remove`."""
    text, m, _ = load(path)
    out, done, skipping = [], set(), False
    for l in m.group(1).split("\n"):
        km = re.match(r"^([A-Za-z_][\w-]*):", l)
        if not km:
            if not skipping:
                out.append(l)
            continue
        k = km.group(1)
        skipping = False
        if k in updates:
            if updates[k] is not None:
                out.append(f"{k}: {updates[k]}")
            done.add(k)
            skipping = True
        elif k in remove:
            skipping = True
        else:
            out.append(l)
    new = [f"{k}: {v}" for k, v in updates.items() if k not in done and v is not None]
    at = next((i for i, l in enumerate(out) if l.startswith("source:")), len(out))
    out[at:at] = new
    save(path, "---\n" + "\n".join(out) + "\n---\n" + text[m.end():])


def replace_block(path, name, body):
    """Rewrite the text between `%% begin generated: name %%` and `%% end generated: name %%`."""
    text = open(path, encoding="utf-8").read()
    start, end = f"%% begin generated: {name} %%", f"%% end generated: {name} %%"
    i, j = text.index(start) + len(start), text.index(end)
    save(path, text[:i] + "\n" + body.strip("\n") + "\n" + text[j:])


def scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, list):
        return "[" + ", ".join(scalar(x) for x in v) + "]"
    return '"' + str(v).replace('"', "'") + '"'


def target(link):
    return link.strip("[]").split("|")[0]


def links(fm, key):
    v = fm.get(key) or []
    return [target(x) for x in ([v] if isinstance(v, str) else v)]


def load_notes():
    notes = {}
    for f in glob.glob(VAULT + "Books/**/*.md", recursive=True):
        notes[os.path.basename(f)[:-3]] = (f, load(f)[2])
    return notes


def default_cart(today=None):
    """Orders go in around the 24th: until then it's this month's cart, after it next month's."""
    t = today or datetime.date.today()
    if t.day > 24:
        t = (t.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
    return t.strftime("%Y-%m")


# ---------- model ----------

def is_epic(fm):
    return fm.get("type") == "Epic Collection" and isinstance(fm.get("number"), int)


def coverage(notes):
    """epic name -> (full coverers, partial coverers)."""
    cov = {}
    for n, (f, fm) in notes.items():
        for e in links(fm, "covers"):
            cov.setdefault(e, ([], []))[0].append(n)
        for e in links(fm, "covers_partial"):
            cov.setdefault(e, ([], []))[1].append(n)
    return cov


def derive_status(fm, full, part, notes):
    """(status, via) from the omnibuses in hand, or None. `complete` says whether the Epic is fully in hand."""
    st = lambda n: notes[n][1].get("status") if n in notes else None
    rf = [c for c in full if st(c) in ("owned", "incoming")]
    rp = [c for c in part if st(c) in ("owned", "incoming")]
    if rf:
        return ("covered" if any(st(c) == "owned" for c in rf) else "incoming"), rf
    if rp:
        complete = len(part) >= 2 and len(rp) == len(part) and not fm.get("coverage_gaps")
        if complete:
            return ("covered" if all(st(c) == "owned" for c in rp) else "incoming"), rp
        return "partial", rp
    return None


def build(notes):
    """Compute everything derived. Returns a dict of per-note updates plus line summaries."""
    cov = coverage(notes)
    upd = {n: {} for n in notes}
    # 1. Epic status from omnibuses
    for n, (f, fm) in notes.items():
        if not is_epic(fm) or fm.get("read") or fm.get("status") == "owned" or n not in cov:
            if fm.get("covered_via"):
                upd[n]["covered_via"] = None
            continue
        d = derive_status(fm, *cov[n], notes)
        derived_before = bool(fm.get("covered_via"))
        # a hand-set status wins unless the omnibuses give a better one; once derived, it keeps following them
        if d and (derived_before or RANK.get(d[0], 0) > RANK.get(fm.get("status"), 0)):
            upd[n]["status"] = scalar(d[0])
            upd[n]["covered_via"] = scalar([f"[[{c}]]" for c in d[1]])
            fm["status"], fm["covered_via"] = d[0], d[1]
        elif derived_before:
            # the omnibus it came from is no longer owned or incoming
            upd[n]["status"] = scalar("wanted")
            upd[n]["covered_via"] = None
            fm["status"] = "wanted"
            fm.pop("covered_via")
    # 2. seq
    epic_num = {n: fm["number"] for n, (f, fm) in notes.items() if is_epic(fm) and not fm.get("modern")}
    seq = {}
    for n, (f, fm) in notes.items():
        covered = [epic_num[e] for e in links(fm, "covers") + links(fm, "covers_partial") if e in epic_num]
        if is_epic(fm):
            seq[n] = (100 + fm["number"]) if fm.get("modern") else fm["number"]
        elif covered:
            seq[n] = min(covered) + 0.5
        else:
            seq[n] = fm.get("order", 9999)
        upd[n]["seq"] = scalar(seq[n])
    # 3. per-line timeline
    line_epics = {}
    for n in epic_num:
        fm = notes[n][1]
        line_epics.setdefault(fm["line"], []).append((fm["number"], n, fm))
    pos, runway, gap = {}, {}, {}
    for line, eps in line_epics.items():
        eps.sort()
        pos[line] = next((e[0] for e in eps if not e[2].get("read")), None)
        if pos[line] is None:
            continue
        r, first_gap = 0, None
        for num, n, fm in eps:
            if num < pos[line] or first_gap:
                continue
            if fm["status"] in READY:
                r += 1
            else:
                first_gap = (num, n)
        runway[line], gap[line] = r, first_gap
    # 4. purpose / missing_before / order_month
    for n, (f, fm) in notes.items():
        st, line = fm.get("status"), fm["line"]
        if st in NEEDS:
            mb = None
            if seq[n] >= 1000 or fm.get("modern"):
                purpose = "modern"
            elif line not in line_epics or line in ("Venom", "Secret Wars"):
                purpose = "event"
            else:
                own = {epic_num[e] for e in links(fm, "covers") + links(fm, "covers_partial") if e in epic_num}
                if n in epic_num:
                    own.add(fm["number"])
                mb = 0
                if own and pos.get(line) is not None:
                    mb = sum(1 for num, en, efm in line_epics[line]
                             if pos[line] <= num < min(own) and num not in own and efm["status"] not in READY)
                if fm.get("budget") == "quarterly" and st == "planned":
                    purpose = "preorder"
                elif mb == 0:
                    purpose = "reading"
                elif st == "oop" or fm.get("urgency") in ("high", "medium"):
                    purpose = "security"
                else:
                    purpose = "future"
            upd[n]["purpose"] = scalar(purpose)
            upd[n]["missing_before"] = mb
            fm["purpose"], fm["missing_before"] = purpose, mb
        else:
            upd[n]["purpose"] = upd[n]["missing_before"] = None
            fm.pop("purpose", None), fm.pop("missing_before", None)
        upd[n]["order_month"] = scalar(str(fm["ordered"])[:7]) if fm.get("ordered") else None
    return upd, seq, pos, runway, gap, line_epics


# ---------- generated notes ----------

def label(n, fm):
    if is_epic(fm):
        return f"[[{n}\\|Epic {fm['number']}]]"  # escaped pipe: it sits inside a table
    return f"[[{n}]]"


def make_planner(notes, seq, pos, runway, gap, cart_month):
    data = {n: fm for n, (f, fm) in notes.items()}
    L = ["# Cart Planner", "",
         "Generated by `Tools/refresh.py` from the book notes. Do not edit by hand; ask Claude to refresh it after orders, arrivals or finished books.", "",
         "## 1. Reading runway (the one-or-two-Epics-a-month rule)", "",
         "| Line | Reading position | Epics ready to read (contiguous) | First gap | Ways to fill the gap |", "|---|---|---|---|---|"]
    for line in MAIN:
        if pos.get(line) is None:
            continue
        g = gap.get(line)
        gtxt, fill = "none", ""
        if g:
            gnum, gname = g
            gtxt = f"Epic {gnum}" + (f" ({data[gname]['status']})" if data[gname]["status"] == "partial" else "")
            opts = []
            for n, fm in data.items():
                if fm["line"] != line or fm.get("status") not in NEEDS + ("unreleased",):
                    continue
                full = {data[e]["number"] for e in links(fm, "covers") if e in data and is_epic(data[e])}
                part = {data[e]["number"] for e in links(fm, "covers_partial") if e in data and is_epic(data[e])}
                if n == gname or gnum in full | part:
                    price = fm.get("price_seen")
                    opts.append(f"[[{n}]]" + (f" ({price} {fm.get('store', '')})".replace(" )", ")") if price else "")
                                + f" - {fm['status']}" + (" (part of it)" if gnum in part and gnum not in full else ""))
            fill = "; ".join(opts) if opts else "no route found"
        L.append(f"| {line} | Epic {pos[line]} | {runway.get(line, 0)} | {gtxt} | {fill} |")
    L += ["", "A line whose runway is under 2 needs its next contiguous book in the cart. Strange is blocked when the first gap is an unreleased Epic. `partial` means an omnibus you have holds only part of that Epic.", ""]
    cand = [(fm["line"], seq[n], n, fm) for n, fm in data.items() if fm.get("status") in NEEDS]
    cand = [c for c in cand if c[3].get("purpose") != "future" or c[3].get("price_seen") or (c[3].get("missing_before") or 0) <= 2]
    order = {"reading": 0, "security": 1, "preorder": 2, "future": 3, "modern": 4, "event": 5}
    cand.sort(key=lambda x: (order.get(x[3].get("purpose", "future"), 9), runway.get(x[0], 99), x[0], x[1]))
    L += ["## 2. Candidates by purpose", "",
          "Sorted by purpose, then by how short the line's runway is, then by the first comic. Far-future books with no price and many missing Epics before them are left out (see the Buy List dashboard for everything).", "",
          "| Purpose | Line | Line runway | Book | Status | Price seen | Store | Missing Epics before it | Urgency |", "|---|---|---|---|---|---|---|---|---|"]
    for line, s, n, fm in cand:
        mb = fm.get("missing_before")
        L.append(f"| {fm.get('purpose', '')} | {line} | {runway.get(line, '')} | [[{n}]] | {fm['status']} | {fm.get('price_seen', '')} | {fm.get('store', '')} | {'' if mb is None else mb} | {fm.get('urgency', '')}{(' - ' + fm['urgency_reason']) if fm.get('urgency_reason') else ''} |")
    L += ["", "- **reading**: nothing unowned sits between your reading position and this book. This is the 'next Epic' slot.",
          "- **security**: out of print, or a deadline (discount, last copy). Ahead of a gap, so it doesn't advance reading yet.",
          "- **preorder**: quarterly pre-order, outside the 200 EUR.", "- **future**: not urgent, far from your position.",
          "- **modern / event**: palate cleansers.", ""]
    cart = sorted(((fm["line"], seq[n], n, fm) for n, fm in data.items() if fm.get("cart") == cart_month), key=lambda x: (x[0], x[1]))
    total = 0
    L += [f"## 3. Current cart ({cart_month})", "", "| Book | Store | Price | Purpose |", "|---|---|---|---|"]
    for line, s, n, fm in cart:
        p = fm.get("price_paid") or fm.get("price_seen") or 0
        total += p
        L.append(f"| [[{n}]] | {fm.get('store', '')} | {p} | {fm.get('purpose', '')} |")
    if not cart:
        L.append("| (nothing has `cart: \"" + cart_month + "\"` yet) | | | |")
    L += ["", f"Subtotal of listed books: **{round(total, 2)} EUR**. Add shipping by store (Walt's about 9 below 150, free above; Cheap-Comics about 20 flat). Budget about 200, flexible, no rollover; quarterly pre-orders are outside it.", ""]
    save(VAULT + "Cart Planner.md", "\n".join(L))


def make_hub_lines(notes, pos, runway, gap, line_epics):
    L = ["| Line | Read up to | Next read | Ready to read after it | First gap |", "|---|---|---|---|---|"]
    for line in MAIN:
        eps = line_epics.get(line, [])
        done = [num for num, n, fm in eps if fm.get("read")]
        nxt = [label(n, fm) for n, (f, fm) in sorted(notes.items(), key=lambda x: x[1][1].get("seq", 0))
               if fm.get("line") == line and fm.get("next_read")]
        g = gap.get(line)
        gtxt = "none"
        if g:
            st = notes[g[1]][1]["status"]
            gtxt = f"Epic {g[0]} ({st})" + (": blocked" if st == "unreleased" else "")
        name = f"[[{line}]]" + (f" (#{PRIORITY[line]})" if line in PRIORITY else "")
        L.append(f"| {name} | {'Epic ' + str(max(done)) if done else '-'} | {', '.join(nxt) or '-'} | {max(runway.get(line, 0) - 1, 0)} | {gtxt} |")
    L.append("| [[Other Series]] | tried, mostly dropped | | | |")
    replace_block(VAULT + "Comics Hub.md", "lines", "\n".join(L))


def make_ratings(notes):
    out = []
    for line in MAIN:
        eps = sorted(((fm["number"], n, fm) for n, (f, fm) in notes.items()
                      if fm.get("line") == line and is_epic(fm) and not fm.get("modern") and fm.get("goodreads_rating")))
        out += [f"## {line}", "", "| Epic | Book | Goodreads | Ratings | Mine | AI tier | Status | Read |", "|---|---|---|---|---|---|---|---|"]
        for num, n, fm in eps:
            title = fm.get("title") or n
            warn = " ⚠" if (fm.get("goodreads_votes") or 0) < 30 else ""
            out.append(f"| {num} | [[{n}\\|{title}]] | {fm['goodreads_rating']}{warn} | {fm.get('goodreads_votes', '')} | {fm.get('my_rating', '')} | {fm.get('ai_tier', '')} | {fm['status']} | {'yes' if fm.get('read') else ''} |")
        out.append("")
    out.append("⚠ = fewer than 30 ratings. Mine = your `my_rating` (1-10).")
    replace_block(VAULT + "Ratings Overview.md", "ratings", "\n".join(out))


# ---------- checks ----------

def checks(notes):
    """Things that look wrong in the book notes. Returns (problems, info)."""
    P, I = [], []
    cov = coverage(notes)
    by_line = {}
    for n, (f, fm) in notes.items():
        for k in ("line", "type", "status"):
            if not fm.get(k):
                P.append(f"{n}: missing `{k}`")
        if fm.get("status") not in STATUSES:
            P.append(f"{n}: unknown status {fm.get('status')!r}")
        if fm.get("next_read"):
            by_line.setdefault(fm["line"], []).append(n)
            if fm.get("read"):
                P.append(f"{n}: marked read and next_read")
        for key in ("covers", "covers_partial", "covered_by", "covered_via"):
            for t in links(fm, key):
                if t not in notes:
                    P.append(f"{n}: `{key}` links to missing note [[{t}]]")
        for t in links(fm, "covers") + links(fm, "covers_partial"):
            if t in notes and n not in links(notes[t][1], "covered_by"):
                P.append(f"{t}: `covered_by` should include [[{n}]]")
        for t in links(fm, "covered_by"):
            if t in notes and n not in links(notes[t][1], "covers") + links(notes[t][1], "covers_partial"):
                P.append(f"{t}: `covers` or `covers_partial` should include [[{n}]]")
        st = fm.get("status")
        if st in ("covered", "partial") and is_epic(fm):
            d = derive_status(fm, *cov.get(n, ([], [])), notes)
            if not d:
                P.append(f"{n}: status {st} but no omnibus containing it is owned or incoming")
            elif fm.get("read") and d[0] == "partial":
                gaps = fm.get("coverage_gaps")
                P.append(f"{n}: read, but the omnibus you read it in has only part of it" + (f" (not in it: {gaps})" if gaps else ""))
        if fm.get("price_paid") and st in ("wanted", "planned", "oop"):
            P.append(f"{n}: has price_paid but status is {st}")
        if fm.get("price_paid") and not fm.get("ordered"):
            I.append(f"{n}: paid but no `ordered` date, so it has no month in Spending")
        if st == "incoming" and not fm.get("price_paid") and not fm.get("covered_via"):
            I.append(f"{n}: incoming but no price_paid")
        if not is_epic(fm) and not (links(fm, "covers") + links(fm, "covers_partial")) and "order" not in fm:
            P.append(f"{n}: no `order` property, so it sorts last")
    for line, ns in by_line.items():
        if len(ns) > 1:
            P.append(f"{line}: {len(ns)} books have next_read ({', '.join(ns)})")
    for line in MAIN:
        if line not in by_line:
            P.append(f"{line}: no book has next_read")
    unrated = sorted(n for n, (f, fm) in notes.items() if fm.get("read") and not fm.get("my_rating"))
    if unrated:
        I.append(f"{len(unrated)} read books have no my_rating yet (Ratings dashboard, 'Read, not rated yet')")
    return P, I


def report(notes):
    P, I = checks(notes)
    print(f"checks: {len(P)} problem(s)")
    for p in P:
        print("  !", p)
    for i in I:
        print("  -", i)
    return P


# ---------- main ----------

def main(cart_month):
    notes = load_notes()
    upd, seq, pos, runway, gap, line_epics = build(notes)
    for n, u in upd.items():
        sets = {k: v for k, v in u.items() if v is not None}
        write_props(notes[n][0], sets, remove=[k for k, v in u.items() if v is None])
    notes = load_notes()
    make_planner(notes, seq, pos, runway, gap, cart_month)
    make_hub_lines(notes, pos, runway, gap, line_epics)
    make_ratings(notes)
    print(f"refreshed {len(notes)} notes, cart {cart_month}")
    report(notes)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["set"] and len(args) >= 4:
        name, key, value = args[1], args[2], args[3]
        hits = [f for f in glob.glob(VAULT + "Books/**/*.md", recursive=True) if os.path.basename(f)[:-3] == name]
        assert len(hits) == 1, hits
        write_props(hits[0], {key: value})
        print("set", key, "on", name)
    elif args[:1] == ["check"]:
        sys.exit(1 if report(load_notes()) else 0)
    else:
        cart = args[args.index("--cart") + 1] if "--cart" in args else default_cart()
        main(cart)
