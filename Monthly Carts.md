# Monthly Carts

Rules live in [[Collecting Philosophy]]. Budget ~200 EUR, flex +10-20. Orders placed around the 24th.

## How we build a cart (the routine)
Open [[Cart Planner]] (I refresh it with `Tools/refresh.py`), then fill three slots in this order:
1. **Reading slot (at least 1 or 2 Epics, omnibuses count).** Take the lines whose runway (contiguous Epics ready to read) is under 2. Buy the cheapest way to fill that line's first gap. These are the `reading` candidates in the planner.
2. **Security slot.** Books that may vanish or spike: out of print, last copy, ending discount (`security`, urgency high or medium). They sit ahead of a gap, so they don't advance reading yet.
3. **Fit-ins.** Modern palate cleansers, a trophy, or a later classic if there is room. Never at the expense of slots 1 and 2.

Then set `cart: "2026-11"` (etc.) on the chosen books so [[Cart.base|the Cart dashboard]] totals them, add shipping (Walt's about 9 under 150, free above; Cheap-Comics about 20 flat), compare with about 200, and name a fallback for each book that could sell out. Quarterly pre-orders are decided separately and don't count against the 200.

## October 24, 2026: lean plan (updated 2026-09-30)

**Decision 2026-09-30 with the new monthly budget:** October is the **Iron Man (2026) Vol 1 pre-order only**, about 17-20 + about 9 Walt's shipping = about 26-30. It gives 6 issues to read with no singles. [[The Mighty Thor Omnibus Vol 4]] and [[Daredevil Omnibus Vol 3]] are out of the cart for now (their `cart` tag is cleared). They stay on the Buy List as high urgency (last copy, ending discount), so the risk of losing them is accepted.
- Vol 1 is pre-ordered at Walt's before it releases on Oct 27. Decided 2026-10-01: Walt's (careful packing, about 26 with shipping) over Amazon (18, free Prime shipping, risk of a damaged copy and a slow replacement). Walt's charges at order time and holds the order until release.
- Budget context: see [[Collecting Philosophy]] (170 / 220 / 290 depending on the month, plan with 150, quarterly pre-orders inside it).
- Roll-over of unspent money is undecided.

### Earlier, larger plan (2026-09-29), kept for reference

One Walt's order, about **207**, free shipping (above 150). About 7 over, inside the usual flex. Decided 2026-09-29 after Thor Omnibus 4 turned up at Walt's.

| Item | Why | Where | ~Cost |
|---|---|---|---|
| [[The Mighty Thor Omnibus Vol 4]] (#195-228, all of Epic 6, start of Epic 7) | Next-reading anchor: Thor runs dry after Epic 5 | Walt's | 85 |
| [[Daredevil Omnibus Vol 3]] (#75-119, rest of Epic 4, Epic 5, start of Epic 6) | Next reading after Omni 2 (Epic 4 is only half in Omni 2), discounted from 125 | Walt's | 105 |
| [[Iron Man (2026) Vol 1 A New Nightmare]] | Modern palate cleanser, released Oct 27 | Walt's | 17 |
| Shipping (order over 150) | | | 0 |

**Watch until the 24th (decided 2026-09-30: wait, keep an eye on it)**
- Both omnibuses are out of print; Walt's has its last copies. On 2026-09-30 Thor Omnibus 4 showed "1 in stock"; DD Omnibus 3 was in stock with no count.
- The Walt's wishlist shows both as unavailable even though their own pages let you buy them. Trust the product page, not the wishlist.
- Re-check around Oct 15 and Oct 20. If Thor 4 is still the last copy close to the date, consider placing the order early (tag it `cart: "2026-10"` so it counts for October).

**Checklist on the 24th**
1. Thor Omnibus 4 still in stock at 85. Only 1 copy, so this is the item most likely to be gone.
2. DD Omnibus 3 still 105 (discount) and covers #75-119.
3. IM 2026 Vol 1 pre-order still about 17.
4. Total check about 207. If the real total goes past about 215, drop IM 2026 Vol 1 (the modern item), never a classic.
5. Do not add: IM2022 #14-18, the IM 2026 #1-4 cover set, Strange 9, Armor Wars Omni. They are November/December items.

**Fallbacks** (stock is only known on the day)
- Thor Omnibus 4 gone: Thor Epic 6 at Cheap-Comics (50 + 20 shipping) plus DD Omni 3 and Vol 1 at Walt's (122 + about 9 shipping). About 201.
- DD Omnibus 3 gone: Thor Omnibus 4 + Vol 1 = 102 + about 9 shipping = about 111. Don't fill the room with filler. Strange 9 (30 at Cheap-Comics) is the only possible security buy.
- DD Omnibus 3 discount ended (back to 125): it becomes a November item; buy Thor Omnibus 4 + Vol 1 and spend less.

**Looking ahead (Nov/Dec)**
- DD Omnibus 4 (95, just released, discounted) so there's no gap after Omni 3.
- Strange 9 and 10 as one Cheap-Comics bundle; Thor Omnibus 5 (#229-266) when needed.
- IM 2026 #1-4 cover set (trophy, decide after reading Vol 1); IM2022 #14-18, 1-2 at a time.
- December: place the Q1 2027 quarterly pre-order (IM Epic 12, see [[Research Notes]]).

## Pre-order calendar (from Walt's, 2026-10-03)
FOC = final order cutoff. Before it you get the pre-order price; after it the regular price. Walt's charges at order time and holds an order until everything in it is released (and won't mix releases more than about 2 months apart).

| Book | FOC deadline | Pre-order | Regular | Saves | Release |
|---|---|---|---|---|---|
| [[Iron Man by Michelinie Layton and Romita Jr Omnibus]] | **Oct 28, 2026** | 83.99 | 125 | 41.01 (33%) | Apr 13, 2027 |
| [[SM Epic 30 - Maximum Clonage]] | **Nov 25, 2026** | 39.50 | 54.99 | 15.49 (28%) | Feb 9, 2027 |
| [[Iron Man Extremis Premier Collection]] | Jul 29 (passed) | 12.79 (discount, not FOC) | 14.99 | 2.20 | Jan 12, 2027 |
| [[Thor Gorr the God Butcher Premier Collection]] | Sep 23 (passed) | 12.79 (discount, not FOC) | 14.99 | 2.20 | Mar 9, 2027 |
| Iron Man Epic 12 *Iron Monger* | not listed yet | | | | Mar 9, 2027 |
| Daredevil Epic 10 *Redemption* | not listed yet | | | | Mar 9, 2027 |

**Pattern from these dates (inference, check it when the books appear):** Epics have an FOC about 76 days before release (Spider-Man 30: Nov 25 to Feb 9). Omnibuses and Premier Collections have it about 167 days before. If that holds, Iron Man 12 and Daredevil 10 (release Mar 9) would close around **Dec 22-23**, which is just before the December payday. If they appear on Walt's, order a day or two ahead, or in the November cart.

**Which orders can be combined (Walt's holds an order until every item is released):**
- Iron Man 2026 Vol 1 (releases Oct 27) must be its own order, or it would be held until the latest release in it.
- The Michelinie omnibus (Apr 13) is its own order unless combined with items releasing from mid-Feb onward. A separate order costs about 9 shipping under 150.
- Spider-Man 30 (Feb 9), Extremis (Jan 12) and Thor Gorr (Mar 9) all fit in one order, since they are within about 2 months of each other. That order is 12.79 + 39.50 + 12.79 = 65.08, plus about 9 shipping.

**The decisions waiting:**
1. **By Oct 28:** the Michelinie omnibus at 83.99 (saves 41), or skip it and risk paying 125 later or waiting for an Epic 9 that isn't announced. It fits October's 150 allowance only if Vol 1 (26) plus the omnibus (about 93 with shipping) fits what's left after payday; it competes with Thor Omnibus 4 (94 with shipping) for that room.
2. **By Nov 25:** Spider-Man 30 at 39.50 (saves 15.49). It fits the November cart.
3. **No rush:** the two Premier Collections, since their prices aren't tied to a deadline.

## History

### Carts placed
| Date | Items | Notes |
|---|---|---|
| 2026-09-24 | DD Omni 2 (115), IM Epic 15 (39.90), IM2022 TPB 1-2 (17 each), #13 / #19 / #20 (~6-7 each), bags | Heavy month, don't chase extras after it |

### How the October plan was reached (2026-09-29)
**Step 1: pick the genuine next-reading classic.** Which lines actually run out of owned reading?
- Doctor Strange: blocked after Epic 5 (6-7 don't exist). Nothing to buy for reading.
- Iron Man: Epic 7, 8 owned, then a gap at 9 (Apr 2027). Fine for now.
- Spider-Man: Epic 3, 4, Omni 3, 7 owned. Plenty.
- Daredevil: Omni 2 covers #42-74. The next real continuation is #75+ (Omni 3, or Epic 4 which overlaps Omni 2 partly). Not urgent yet.
- **Thor: nothing owned after Epic 5 (Omni 3).** Epic 6 is the line that runs dry first, so it is the natural anchor. Price 50 + ~20 shipping unless bundled.

**Step 2: availability-sensitive classics.** IM Epic 16 (OOP) if a fair copy shows up; IM Epic 19 is easy to find (not urgent).

**Step 3: modern palate cleanser.**
- IM (2026) Vol 1, pre-order ~17. Release is Oct 27, so it has to be decided on the 24th. #1/#2 singles only if the covers are worth it.
- IM2022 #14-18: 1-2 issues from one eBay seller at most.

**Not this month:** IM2026 #7/#8/#12/#13, Strange 9 (security only), Spider-Man 8/9, IM Epic 12 (Q1 2027 pre-order).

**Facts gathered (2026-09-29)**
- Walt's pre-orders charge at order time, so the Q4 157.99 is already paid. October is a clean ~200.
- Thor 6: 50 on Cheap-Comics + flat ~20 shipping = ~70.
- DD Omni 3 (#75-119: rest of Epic 4, all of Epic 5, start of Epic 6): 105 on Walt's, discounted from 125.
- IM Epic 16: still not found. Plan is Armor Wars Omni (released Jan 2026, Walt's 78.99 on sale) + Dragon Seed Saga TPB (~30). See [[Research Notes]]. Not an October item.
- IM 2026: #1 at Walt's 15 (one cover liked). The cartoony covers for #1-#4 form one image and only exist as a set of four on Vinted, 25 + shipping. Vol 1 TPB at Walt's ~17.

**Option A (recommended), ~200**
| Item | Where | ~Cost |
|---|---|---|
| Thor Epic 6 (next-reading anchor) | Cheap-Comics | 50 + 20 |
| DD Omni 3 (discounted, saves 20) | Walt's | 105 |
| IM 2026 Vol 1 pre-order | Walt's | 17 |
| Walt's shipping (order is 122, under the 150 threshold) | | ~9 |
Total about 201. On budget, one classic reading anchor, one availability/discount classic, one modern cleanser.

**Option B, ~130, saves room**
Thor 6 + IM 2026 Vol 1 + the Vinted #1-4 cover set (25 + shipping). Skip DD Omni 3 and accept it may go back to 125 (+20 later). Only worth it if the cover set matters more to you than the discount.

**First decision (2026-09-29): Option A.** Replaced the same day by the final plan above, once Thor Omnibus 4 was found. It leaves 2, almost 3, Epics in the reading queue.

**Recommendation was:** A. The cover set is a pure trophy (Vol 1 already contains #1-6), so it fits November better; if it's gone, no classic was sacrificed. Cart is not final until you confirm.

**Checklist for Option A (superseded)**
1. Walt's: DD Omni 3 still 105? Confirm it covers #75-119 and is in stock. It is the one item with a deadline (the discount).
2. Walt's: IM 2026 Vol 1 pre-order still ~17 and shipping to your country. Bundle it in the same order as DD Omni 3 (122, so ~9 shipping).
3. Cheap-Comics: Thor 6 still 50 and in stock, and check Thor 7 in the same basket (see below).
4. Total check: about 201. If the real total goes past ~215, remove IM 2026 Vol 1 (the modern item), never a classic.
5. Do not add: IM2022 #14-18, cover set, Strange 9, Armor Wars Omni. They are November/December items.
Fallback if something goes wrong: Thor 6 sold out -> buy Thor 7 only if Epic 6 can't be found elsewhere (chronology says wait); DD Omni 3 discount ended -> at 125 it's a November item, put IM 2026 Vol 1 + Thor 6 in October and spend less.
