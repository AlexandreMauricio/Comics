# Monthly Carts

The plan for every month is in [[Year Plan]]. The old October 2026 cart plans are in `Archive/`. Rules are in [[Collecting Philosophy]].

## How a cart is built (the routine)
1. **Find the allowance first.** It is 150 a month, all-in (other hobbies included), and any overspend is taken off the next month. Ask the user for the month's other hobby spending and use the running balance in [[Year Plan]].
2. **Fill each line's reading order.** Open [[Cart Planner]] (`python Tools/refresh.py`). Every line keeps 1 or 2 next reads and 1 or 2 ahead, in order. Never buy a book before the books that come before it.
3. **Secure what can vanish.** Last copies, out of print, discounts that end, FOC pre-order prices. Paying early is fine for these.
4. **Group orders.** Walt's charges 12 under 150 and ships free from 150 (to confirm), Cheap-Comics is a flat 20 and needs three books, Amazon.es is free with Prime. Pre-orders that release within about two months of each other go in one order, because Walt's holds the order until the last item is out.
5. **Modern books ride along only when they cost nothing extra** (an order already over 150, or the birthday cart).
6. Tag the chosen books `cart: "YYYY-MM"` so [[Cart.base|the Cart dashboard]] totals them, and name a fallback for each book that could sell out.
