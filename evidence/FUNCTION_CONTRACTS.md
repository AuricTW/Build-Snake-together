# Four Function Contracts

Write examples before implementation. Do not paste function bodies here.

| Function | Accepted input | Returned result | Invariant / non-goal | Failure or boundary examples |
|---|---|---|---|---|
| `next_head` | head position and direction as (x, y) coordinates | the new head position | does not mutate input. | head at (19, 0), direction (1, 0), go to (20, 0) |
| `ate_food` | head position and apple position | boolean | Exact cell equality. | apple and head position both at (20, -20)|
| `hit_wall` | | | Board edges are published. | |
| `advance_body` | | | Returns a new list. | |

## Example-to-test bridge

For each function, convert at least one row above into a student-authored test. Write the expected observation before running it.
