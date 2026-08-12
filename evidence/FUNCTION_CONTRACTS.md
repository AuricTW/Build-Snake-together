# Four Function Contracts

Write examples before implementation. Do not paste function bodies here.

| Function | Accepted input | Returned result | Invariant / non-goal | Failure or boundary examples |
|---|---|---|---|---|
| `next_head` | Head position `(x, y)`, direction, and a positive `cell_size` | A new head position `(x, y)` | Does not mutate input. | Normal: head `(2, 3)`, direction `(1, 0)`, cell_size `1` → `(3, 3)`. Boundary: head `(0, 0)`, direction `(-1, 0)`, cell_size `1` → `(-1, 0)`. |
| `ate_food` | Head position and food position as `(x, y)` cells | `True` if head and food are in the same cell, otherwise `False` | Exact cell equality. | Normal: head `(3, 3)`, food `(3, 3)` → `True`. Boundary: head `(3, 3)`, food `(3, 4)` → `False`. |
| `hit_wall` | Head position `(x, y)`, board `width`, `height`, and positive `cell_size` | `True` if any part of the head is outside the board, otherwise `False` | Board edges are published. | Normal: head `(10, 10)`, width `100`, height `100`, cell_size `10` → `False`. Boundary: head `(90, 90)`, width `100`, height `100`, cell_size `10` → `False`; head `(100, 90)` → `True`. |
| `advance_body` | A list of body cells, a new head cell, and boolean `grow` | A new list representing the next snake body | Returns a new list. | Normal: body `[(2,2),(1,2)]`, new_head `(3,2)`, grow `False` → `[(3,2),(2,2)]`. Boundary: same body with grow `True` → `[(3,2),(2,2),(1,2)]`. |

## Example-to-test bridge

For each function, convert at least one row above into a student-authored test. Write the expected observation before running it.
