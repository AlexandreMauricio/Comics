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
| `budget` | `monthly` or `quarterly` (quarterly pre-orders are outside the 200 EUR) |
| `price_paid` / `price_seen` / `store` / `price_note` | what I paid, what I saw, and where |
| `seq` | position on the line's timeline, so every list follows the first comic. Computed, don't edit |
| `purpose` | reading, security, preorder, future, modern, event. Computed |
| `missing_before` | wanted books only: unowned Epics between your reading position and this book. 0 means it is a contiguous next-reading buy. Computed |
| `urgency`, `urgency_reason` | high/medium/low with why (discount ending, last copy, out of print). Set by hand or by Claude |
| `cart` | e.g. `"2026-10"`: the book is in that month's cart. The Cart dashboard totals it |
| `covered_by` / `covers` | links between an Epic and the omnibus/TPB that contains it |
| `tier`, `story_rating`, `rating_reason` | ChatGPT/Gemini ranking, unverified |
| `my_rating` | your own rating after reading |
| `verified` | set to true once you have checked the book's info |

## Statuses
- `owned`: I have the Epic itself.
- `covered`: I own the content via an omnibus (e.g. IM Epic 2-5). It still appears in the Reading Queue because the roadmap is Epic-numbered.
- `incoming`: ordered or pre-ordered, not arrived.
- `planned`: decided, not ordered yet (next cart or pre-order).
- `wanted`: on the shopping list.
- `oop`: wanted but hard to find/out of print.
- `unreleased`: not published yet.
- `parked`: deliberately ignored for now (e.g. modern Daredevil).

## Keeping derived data fresh
After orders, arrivals or finished books, ask Claude to run `Tools/refresh.py`. It recomputes `seq`, `purpose`, `missing_before` and rewrites [[Cart Planner]]. It only touches those properties and the planner note.

## Routine
- Book arrives: change `status` to `owned` (or `covered`), keep `price_paid`.
- Finish a book: set `read: true`, add `my_rating`, set the next book's `next_read: true`, and add a line to [[Reading Log]].
- Place an order: set `status: incoming`, `price_paid`, `store`, `budget`.
- Ask me (Claude) to do these for you if you'd rather just tell me.

If a dashboard shows an error or looks empty, tell me: I couldn't open Obsidian to test the `.base` files, so the first look is the real test.
