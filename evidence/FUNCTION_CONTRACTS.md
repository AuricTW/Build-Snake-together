# Four Function Contracts

Write examples before implementation. Do not paste function bodies here.

| Function | Accepted input | Returned result | Invariant / non-goal | Failure or boundary examples |
|---|---|---|---|---|
| `next_head` | Head position `(x, y)`, direction `(-1, 0)`, `(1, 0)`, `(0, -1)`, or `(0, 1)`, and a positive `cell_size` | A new head position `(x, y)` | Does not mutate input. | Normal: head `(200, 200)`, direction `(1, 0)`, cell_size `20` → `(220, 200)`. Boundary: head `(20, 0)`, direction `(0, -1)`, cell_size `20` → `(20, -20)`. |
| `ate_food` | Head position `(x, y)` and food position `(x, y)` | `True` if the head and food are in exactly the same cell, otherwise `False` | Exact cell equality. | Normal: head `(200, 100)`, food `(200, 100)` → `True`. Boundary: head `(200, 100)`, food `(220, 100)` → `False`. |
| `hit_wall` | Head position `(x, y)`, board width, board height, and a positive `cell_size` | `True` if any part of the head is outside the board, otherwise `False` | Board edges are published. | Normal: head `(200, 200)`, width `640`, height `480`, cell_size `20` → `False`. Boundary: head `(20, -20)`, width `640`, height `480`, cell_size `20` → `True`. Head `(620, 460)` → `False` because the whole 20×20 cell is still inside the board. |
| `advance_body` | A list of body cells, a new head position `(x, y)`, and a boolean `grow` | A new list containing the next snake body | Returns a new list. | Normal: body `[(200, 200), (180, 200), (160, 200)]`, new_head `(220, 200)`, grow `False` → `[(220, 200), (200, 200), (180, 200)]`. Boundary: same body, new_head `(220, 200)`, grow `True` → `[(220, 200), (200, 200), (180, 200), (160, 200)]`. |
## Example-to-test bridge

For each function, convert at least one row above into a student-authored test. Write the expected observation before running it.
