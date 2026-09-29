# How this vault works

## One note per book
Every Epic, omnibus, TPB and important single is a note in `Books/<line>/`. The properties at the top of the note are the data. The dashboards (`*.base` files) are live tables built from those properties.

## Key properties
| Property | Meaning |
|---|---|
| `line` | Iron Man, Doctor Strange, Spider-Man, Daredevil, Thor, or an event/other series |
| `type` | Epic Collection, Omnibus, TPB, Single, Graphic Novel |
| `number` | Epic number (roadmap is Epic-numbered) |
| `status` | see below |
| `read` | true/false |
| `next_read` | true on the one book to read next in that line |
| `my_rating` | your own rating after reading, 1-10. Your impressions go in the note's "My impressions" section and in [[Reading Log]] |
| `budget` | `monthly` or `quarterly` (quarterly pre-orders are outside the 200 EUR) |
| `price_paid` / `price_seen` / `store` / `price_note` | what I paid, what I saw, and where |
| `ordered` | date the order was placed (e.g. `2026-09-24`). Puts the book in the right month on the Spending dashboard |
| `cart` | e.g. `"2026-10"`: the book is in that month's cart. The Cart dashboard totals it |
| `covers` / `covers_partial` | on an omnibus/TPB: the Epics it contains completely / only in part |
| `covered_by` | on an Epic: every omnibus/TPB that contains any of it |
| `coverage_gaps` | on an Epic: issues that none of the listed omnibuses contain (e.g. IM Epic 16: `#267-269, #276-277`) |
| `order` | position for books that aren't an Epic and don't cover one (modern runs, events). Set by hand; higher sorts later |
| `urgency`, `urgency_reason` | high/medium/low with why (discount ending, last copy, out of print). Set by hand or by Claude |
| `ai_tier`, `ai_stars`, `ai_score`, `ai_reason`, `ai_highlight`, `ai_acquisition`, `ai_source` | the old ChatGPT/Gemini ranking from `Epics.xlsx`. Unverified opinions, kept for comparison |
| `goodreads_rating`, `goodreads_votes` | reader averages pulled from Goodreads |
| `verified` | true once the book's issues/pages/editions were checked against Wikipedia (see [[Sources and Verification]]) |

**Computed by `Tools/refresh.py`, don't edit:** `seq` (timeline position), `purpose` (reading, security, preorder, future, modern, event), `missing_before` (unowned Epics between your reading position and this book; 0 = a contiguous next-reading buy), `covered_via`, `order_month`, and the status of Epics you get through an omnibus (below).

## Statuses
- `owned`: I have the Epic itself (or the omnibus/TPB/single itself).
- `covered`: I own the whole content via omnibuses (e.g. IM Epic 2-5). It still appears in the Reading Queue because the roadmap is Epic-numbered.
- `incoming`: ordered or pre-ordered, not arrived (or, for an Epic, the omnibus that contains it is on its way).
- `partial`: only part of the Epic is owned or on its way through an omnibus; the rest still has to be bought (e.g. DD Epic 4: first half in Omni 2, second half in Omni 3). It counts as a gap in the reading runway and shows on the Buy List.
- `planned`: decided, not ordered yet (next cart or pre-order).
- `wanted`: on the shopping list.
- `oop`: wanted but hard to find/out of print.
- `unreleased`: not published yet.
- `parked`: deliberately ignored for now (e.g. modern Daredevil).

You only set statuses on the books you buy. An Epic you get through omnibuses follows them: when the omnibus is `incoming` the Epic becomes `incoming`, when it's `owned` the Epic becomes `covered`, and if an omnibus holds only part of it the Epic is `partial` until every part is in hand. The `covered_via` property shows which omnibus it came from.

## Keeping derived data fresh
After orders, arrivals or finished books, ask Claude to run `Tools/refresh.py`. It:
- recomputes the properties above,
- rewrites [[Cart Planner]] (the cart shown is the one for the next 24th; `--cart 2026-11` picks another month),
- rewrites the Lines table in [[Comics Hub]] and the tables in [[Ratings Overview]] (only the parts between the `%% generated %%` markers),
- runs the checks: two next-reads in one line, one-way `covers`/`covered_by` links, `covered` Epics with no omnibus in hand, paid books still marked wanted, read Epics whose omnibus only had part of them, and similar. `refresh.py check` runs only the checks.

## Routine
- Book arrives: tell me, or change its `status` to `owned`. Epics inside an omnibus update themselves on the next refresh.
- Finish a book: set `read: true`, add `my_rating`, move `next_read: true` to the next book, and add a line to [[Reading Log]].
- Place an order: set `status: incoming`, `price_paid`, `ordered`, `store`, `budget`.
- Ask me (Claude) to do these for you if you'd rather just tell me.

If a dashboard shows an error or looks empty, tell me: I couldn't open Obsidian to test the `.base` files, so the first look is the real test.
