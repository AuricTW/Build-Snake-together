# Snake Trio Log

## Members and first roles

- Driver:李韋宏
- Navigator:周芯妤
- Tester / Recorder:洪子由

Rotate roles after each completed TODO.

## Gate record

| Gate | Driver | Navigator | Tester / Recorder | Observed result | Next action |
|---|---|---|---|---|---|
| Baseline | | | | | |
| TODO 1 - next head | | | | | |
| TODO 2 - food | | | | | |
| TODO 3 - wall | | | | | |
| TODO 4 - body | | | | | |
| Playable run | | | | | |

## Explain-back

1. Which function was easiest to test, and why?
我們團隊認為hit_wall是最容易測試的功能
2. Which failing test gave the clearest clue?

===================================================== FAILURES ======================================================
_______________________________________ test_next_head_moves_exactly_one_cell _______________________________________

    def test_next_head_moves_exactly_one_cell() -> None:
>       assert next_head((40, 60), (1, 0), 20) == (60, 60)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests_public\test_snake_contract.py:11: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

head = (40, 60), direction = (1, 0), cell_size = 20

    def next_head(head: Cell, direction: Direction, cell_size: int) -> Cell: # 計算下一個蛇頭位置
        """Return the next head cell.
    
        Interface:
            head: current ``(x, y)`` grid position.
            direction: one of ``(-1, 0)``, ``(1, 0)``, ``(0, -1)``, ``(0, 1)``.
            cell_size: positive number of pixels moved in one step.
            return: a new ``(x, y)`` tuple.
    
        Hint: calculate x and y separately.  Do not mutate any input.
        """
        # TODO 1: replace this line with one return statement.
>       raise NotImplementedError("TODO 1: compute the next head")
E       NotImplementedError: TODO 1: compute the next head

src\snake_trio\logic.py:26: NotImplementedError
______________________________________ test_ate_food_uses_exact_cell_equality _______________________________________

    def test_ate_food_uses_exact_cell_equality() -> None:
>       assert ate_food((20, 20), (20, 20)) is True
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests_public\test_snake_contract.py:16: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

head = (20, 20), food = (20, 20)

    def ate_food(head: Cell, food: Cell) -> bool:
        """Return True exactly when the snake head occupies the food cell.
    
        Hint: both values use the same ``(x, y)`` tuple format.
        """
        # TODO 2: replace this line with one boolean return statement.
>       raise NotImplementedError("TODO 2: compare head and food")
E       NotImplementedError: TODO 2: compare head and food

src\snake_trio\logic.py:35: NotImplementedError
________________________________________ test_hit_wall_checks_all_four_edges ________________________________________

    def test_hit_wall_checks_all_four_edges() -> None:
>       assert hit_wall((0, 0), 640, 480, 20) is False
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests_public\test_snake_contract.py:21: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

head = (0, 0), width = 640, height = 480, cell_size = 20

    def hit_wall(head: Cell, width: int, height: int, cell_size: int) -> bool:
        """Return True when any part of the head is outside the board.
    
        Legal x values begin at 0 and stop before ``width``.
        Legal y values begin at 0 and stop before ``height``.
        The head is aligned to the grid, so its top-left coordinate is enough.
        """
        # TODO 3: check left, right, top, and bottom boundaries.
>       raise NotImplementedError("TODO 3: check four wall boundaries")
E       NotImplementedError: TODO 3: check four wall boundaries

src\snake_trio\logic.py:46: NotImplementedError
_______________________________ test_advance_body_returns_a_new_list_and_obeys_growth _______________________________

    def test_advance_body_returns_a_new_list_and_obeys_growth() -> None:
        original = [(40, 20), (20, 20), (0, 20)]
>       moved = advance_body(original, (60, 20), grow=False)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests_public\test_snake_contract.py:31: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

body = [(40, 20), (20, 20), (0, 20)], new_head = (60, 20), grow = False

    def advance_body(body: list[Cell], new_head: Cell, grow: bool) -> list[Cell]:
        """Return the next snake body without changing ``body``.
    
        The returned list always begins with ``new_head``.  When ``grow`` is True,
        keep every old segment.  Otherwise remove only the old tail.
        """
        # TODO 4: build and return a new list.  Never call body.insert/pop/remove.
>       raise NotImplementedError("TODO 4: create the next body")
E       NotImplementedError: TODO 4: create the next body

src\snake_trio\logic.py:56: NotImplementedError
============================================== short test summary info ==============================================
FAILED tests_public/test_snake_contract.py::test_next_head_moves_exactly_one_cell - NotImplementedError: TODO 1: compute the next head
FAILED tests_public/test_snake_contract.py::test_ate_food_uses_exact_cell_equality - NotImplementedError: TODO 2: compare head and food
FAILED tests_public/test_snake_contract.py::test_hit_wall_checks_all_four_edges - NotImplementedError: TODO 3: check four wall boundaries
FAILED tests_public/test_snake_contract.py::test_advance_body_returns_a_new_list_and_obeys_growth - NotImplementedError: TODO 4: create the next body


3. What did your trio ask AI at L1, and what decision remained human-owned?
請給我們一個 Arrange-Act-Assert 的測試架構範例，用來說明如何測試『串列長度是否增加』？