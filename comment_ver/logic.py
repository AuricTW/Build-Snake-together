"""Four small, testable rules used by the supplied Pygame shell.

Your trio edits only this file for the core mission. Keep every function pure:
do not import Pygame, open a window, read the keyboard, or change the supplied
`body` list in place.
"""

# 讓型別註記的使用方式更彈性
from __future__ import annotations


# Cell 代表遊戲棋盤上的一個位置
# 格式為 (x, y)
# 例如：(200, 200)
Cell = tuple[int, int]

# Direction 代表蛇移動的方向
#
# (-1, 0) = 左
# (1, 0)  = 右
# (0, -1) = 上
# (0, 1)  = 下
Direction = tuple[int, int]


# ==================================================
# 1. 計算蛇頭下一步的位置
# ==================================================

def next_head(
    head: Cell,
    direction: Direction,
    cell_size: int
) -> Cell:
    """Return the next head cell.

    Interface:
        head: current (x, y) grid position.
        direction: one of (-1, 0), (1, 0), (0, -1), (0, 1).
        cell_size: positive number of pixels moved in one step.
        return: a new (x, y) tuple.

    Hint: calculate x and y separately. Do not mutate any input.
    """

    # head[0] 是目前蛇頭的 x 座標
    # head[1] 是目前蛇頭的 y 座標
    #
    # direction[0] 是 x 方向
    # direction[1] 是 y 方向
    #
    # cell_size 是每次移動的距離
    #
    # 新位置 =
    # 原本位置 + 移動方向 × 每格大小

    return (
        head[0] + direction[0] * cell_size,
        head[1] + direction[1] * cell_size,
    )


# ==================================================
# 2. 判斷蛇有沒有吃到食物
# ==================================================

def ate_food(head: Cell, food: Cell) -> bool:
    """Return True exactly when the snake head occupies the food cell."""

    # 如果蛇頭座標和食物座標完全相同
    # 就代表蛇吃到食物
    #
    # 例如：
    # head = (200, 100)
    # food = (200, 100)
    #
    # head == food → True

    return head == food


# ==================================================
# 3. 判斷蛇頭有沒有撞牆
# ==================================================

def hit_wall(
    head: Cell,
    width: int,
    height: int,
    cell_size: int
) -> bool:
    """Return True when any part of the head is outside the board.

    Legal x values begin at 0 and stop before width.
    Legal y values begin at 0 and stop before height.
    The head is aligned to the grid, so its top-left coordinate is enough.
    """

    # 把蛇頭座標拆成 x 和 y
    x, y = head

    # 判斷四個方向是否超出遊戲範圍
    #
    # x < 0
    # → 超出左邊界
    #
    # x + cell_size > width
    # → 蛇頭右側超出右邊界
    #
    # y < 0
    # → 超出上邊界
    #
    # y + cell_size > height
    # → 蛇頭下側超出下邊界

    return (
        x < 0
        or x + cell_size > width
        or y < 0
        or y + cell_size > height
    )


# ==================================================
# 4. 更新蛇身
# ==================================================

def advance_body(
    body: list[Cell],
    new_head: Cell,
    grow: bool
) -> list[Cell]:
    """Return the next snake body without changing `body`.

    The returned list always begins with `new_head`.

    When `grow` is True:
        keep every old segment.

    Otherwise:
        remove only the old tail.
    """

    # 如果 grow == True：
    # 代表蛇吃到食物，要變長
    # 所以保留全部舊蛇身
    #
    # 如果 grow == False：
    # 代表只是正常移動
    # body[:-1] 會拿掉最後一節蛇尾
    #
    # 注意：
    # body[:-1] 會建立一個新的 list，
    # 不會修改原本傳進來的 body

    old_segments = body if grow else body[:-1]

    # 建立新的蛇身
    #
    # 第一格一定是新的蛇頭 new_head
    # 後面再接上原本需要保留的蛇身
    #
    # *old_segments 代表把 list 裡面的元素展開
    #
    # 例如：
    #
    # new_head = (220, 200)
    #
    # old_segments =
    # [(200, 200), (180, 200)]
    #
    # 最後得到：
    #
    # [
    #   (220, 200),
    #   (200, 200),
    #   (180, 200)
    # ]

    return [new_head, *old_segments]