"""Supplied Pygame presentation shell for the Snake trio mission.

Students do not need to understand or edit this file during the core mission.
It translates keys, draws the board, and calls the four functions in logic.py.
"""

# 讓型別註記可以更彈性地使用，例如可以先寫還沒定義的類別名稱
from __future__ import annotations

# argparse：處理執行程式時輸入的參數，例如 --check
import argparse

# random：用來隨機產生食物位置
import random

# dataclass：方便建立用來儲存遊戲狀態的類別
from dataclasses import dataclass

# Path：處理檔案路徑，例如圖片素材所在位置
from pathlib import Path

# 從 logic.py 匯入遊戲核心邏輯
from .logic import Cell, Direction, advance_body, ate_food, hit_wall, next_head


# =========================
# 遊戲基本設定
# =========================

WIDTH = 640          # 遊戲視窗寬度，640 pixels
HEIGHT = 480         # 遊戲視窗高度，480 pixels

CELL = 20            # 每一格的大小為 20 × 20 pixels

STEP_MS = 130        # 蛇每移動一步的時間間隔，單位毫秒


# 蛇一開始的位置
# 第一個 tuple 是蛇頭，後面依序是蛇身
START_BODY: list[Cell] = [
    (200, 200),
    (180, 200),
    (160, 200)
]

# 蛇一開始往右走
# (1, 0)：
# x 方向 +1
# y 方向不變
START_DIRECTION: Direction = (1, 0)


# assets 資料夾的位置
# __file__ 代表目前這個 Python 檔案的位置
ASSET_DIR = Path(__file__).with_name("assets")


# 蘋果圖片高度
# CELL = 20
# 所以 APPLE_HEIGHT = 20 + 10 = 30
APPLE_HEIGHT = CELL + CELL // 2


# 每一段牆壁圖片的長度
# 20 格 × 每格 20 pixels = 400 pixels
WALL_LENGTH = CELL * 20


# 牆壁厚度
# max(4, 20 // 4) = max(4, 5) = 5 pixels
WALL_THICKNESS = max(4, CELL // 4)


# 建立獨立的亂數產生器
# 用來決定食物出現的位置
RNG = random.Random()


# =========================
# 圖片處理
# =========================

def _load_sprite(pygame, name: str, size: tuple[int, int]):
    """Load, clean, and scale one blue-on-light-background sprite."""

    # 從 assets 資料夾讀入圖片
    # convert_alpha() 保留圖片透明度
    sprite = pygame.image.load(ASSET_DIR / name).convert_alpha()

    # 一個 pixel 一個 pixel 掃描圖片
    for y in range(sprite.get_height()):
        for x in range(sprite.get_width()):

            # 取得該 pixel 的 RGBA
            red, green, blue, alpha = sprite.get_at((x, y))

            # 如果紅色值非常高，表示接近白色背景
            # 將它設為完全透明
            if red >= 240:
                alpha = 0

            # 如果是介於背景與圖案之間的顏色
            # 計算半透明效果，讓邊緣比較平滑
            elif red > 160:
                alpha = round((240 - red) * 255 / 80)

            # 其他顏色視為圖案本體
            # 設為完全不透明
            else:
                alpha = 255

            # 把新的透明度寫回圖片
            sprite.set_at((x, y), (red, green, blue, alpha))

    # 將圖片縮放成指定大小後回傳
    return pygame.transform.smoothscale(sprite, size)


def _directional_sprites(pygame, left_facing_sprite):
    """Build rotations for a sprite whose source artwork faces left."""

    # 原始圖片預設朝左
    # 透過旋轉建立四個方向的圖片
    return {
        (-1, 0): left_facing_sprite,                       # 左
        (1, 0): pygame.transform.rotate(left_facing_sprite, 180),  # 右
        (0, -1): pygame.transform.rotate(left_facing_sprite, 90),  # 上
        (0, 1): pygame.transform.rotate(left_facing_sprite, -90),  # 下
    }


def _segment_direction(
    body: list[Cell],
    index: int,
    fallback: Direction
) -> Direction:
    """Point a body sprite toward the preceding segment."""

    # 如果 index = 0，代表這是蛇頭
    # 直接使用目前蛇的移動方向
    if index == 0:
        return fallback

    # 取得目前這一節蛇身的位置
    x, y = body[index]

    # 取得前一節蛇身的位置
    previous_x, previous_y = body[index - 1]

    # 計算目前蛇身應該朝向哪一個方向
    #
    # 例如：
    # 前一節在 (200, 200)
    # 目前這節在 (180, 200)
    #
    # x 差 = 20
    # 20 // CELL = 1
    #
    # direction = (1, 0)
    # 表示這一節應該朝右
    direction = (
        (previous_x - x) // CELL,
        (previous_y - y) // CELL
    )

    # 確認計算出來的方向是合法方向
    # 如果不是，就使用 fallback
    return (
        direction
        if direction in {(-1, 0), (1, 0), (0, -1), (0, 1)}
        else fallback
    )


def _draw_walls(screen, vertical_wall, horizontal_wall) -> None:
    """Tile the twenty-cell wall artwork around the board perimeter."""

    # 畫左右兩側的垂直牆壁
    for y in range(0, HEIGHT, WALL_LENGTH):

        # 左牆
        screen.blit(vertical_wall, (0, y))

        # 右牆
        screen.blit(
            vertical_wall,
            (WIDTH - WALL_THICKNESS, y)
        )

    # 畫上下兩側的水平牆壁
    for x in range(0, WIDTH, WALL_LENGTH):

        # 上牆
        screen.blit(horizontal_wall, (x, 0))

        # 下牆
        screen.blit(
            horizontal_wall,
            (x, HEIGHT - WALL_THICKNESS)
        )


# =========================
# 食物位置
# =========================

def choose_food(body: list[Cell]) -> Cell:
    """Choose a random free cell inside the visible wall boundary."""

    # 用來存放所有「可以放食物」的位置
    free_cells = []

    # 從 y = CELL 開始
    # 到 HEIGHT - CELL 前停止
    #
    # 也就是避開最外圍牆壁
    for y in range(CELL, HEIGHT - CELL, CELL):

        # 同樣避開左右兩側的牆壁
        for x in range(CELL, WIDTH - CELL, CELL):

            # 如果這個位置目前沒有蛇身
            if (x, y) not in body:

                # 就把這個位置加入可用位置
                free_cells.append((x, y))

    # 從所有可用的位置中隨機選一個
    # 當作新的食物位置
    return RNG.choice(free_cells)


# =========================
# 遊戲狀態
# =========================

@dataclass
class GameState:
    # 蛇身的位置
    # body[0] 為蛇頭
    body: list[Cell]

    # 蛇目前移動方向
    direction: Direction

    # 食物目前的位置
    food: Cell

    # 玩家目前分數
    # 預設為 0
    score: int = 0

    # 遊戲是否結束
    # 預設為 False
    game_over: bool = False


def new_game() -> GameState:
    """建立一個全新的遊戲狀態。"""

    # 複製 START_BODY
    #
    # 不直接使用 START_BODY，
    # 避免遊戲過程修改到原本的起始資料
    body = list(START_BODY)

    # 建立 GameState
    return GameState(
        body=body,
        direction=START_DIRECTION,
        food=choose_food(body)
    )


# =========================
# 遊戲每一步的邏輯
# =========================

def step(state: GameState) -> None:
    """讓遊戲狀態往前執行一步。"""

    # 根據目前蛇頭位置、方向與 CELL 大小
    # 計算下一步蛇頭的位置
    new_head = next_head(
        state.body[0],
        state.direction,
        CELL
    )

    # 判斷新的蛇頭位置是否碰到食物
    #
    # True  = 吃到
    # False = 沒吃到
    grow = ate_food(
        new_head,
        state.food
    )

    # 根據新的蛇頭與 grow
    # 計算下一步完整的蛇身
    #
    # grow = True：
    # 蛇會增加一節
    #
    # grow = False：
    # 蛇維持原本長度
    next_body = advance_body(
        state.body,
        new_head,
        grow
    )

    # 判斷蛇頭有沒有撞到自己的身體
    #
    # next_body[1:]：
    # 排除第一格蛇頭，只檢查後面的蛇身
    self_hit = new_head in next_body[1:]

    # 判斷：
    # 1. 是否撞到牆壁
    # 2. 是否撞到自己的身體
    #
    # 只要其中一項成立，遊戲就結束
    if hit_wall(
        new_head,
        WIDTH,
        HEIGHT,
        CELL
    ) or self_hit:

        state.game_over = True
        return

    # 沒有撞牆也沒有撞自己
    # 正式更新蛇身
    state.body = next_body

    # 如果這一步有吃到食物
    if grow:

        # 分數 +1
        state.score += 1

        # 再隨機產生新的食物
        state.food = choose_food(state.body)


# =========================
# Pygame 主程式
# =========================

def run_game() -> int:
    """啟動 Pygame 遊戲。"""

    # 嘗試載入 pygame
    try:
        import pygame

    # 如果電腦沒有安裝 pygame
    except ImportError:
        print(
            "Pygame is not installed. "
            "Run: python -m pip install -e '.[display]' "
        )
        return 2

    # 初始化 pygame
    pygame.init()

    # 建立 640 × 480 的遊戲視窗
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # 設定視窗標題
    pygame.display.set_caption("NCKU Snake Trio Studio")

    # 建立 Clock
    # 用來控制畫面更新速度
    clock = pygame.time.Clock()

    # 建立字型
    # None 表示使用 pygame 預設字型
    # 字體大小 32
    font = pygame.font.Font(None, 32)

    # =========================
    # 載入遊戲圖片
    # =========================

    try:
        # 載入蛇頭圖片
        # 並建立上下左右四個方向
        head_sprites = _directional_sprites(
            pygame,
            _load_sprite(
                pygame,
                "head.png",
                (CELL, CELL)
            )
        )

        # 載入蛇身圖片
        # 並建立上下左右四個方向
        body_sprites = _directional_sprites(
            pygame,
            _load_sprite(
                pygame,
                "body.png",
                (CELL, CELL)
            )
        )

        # 載入蘋果圖片
        apple_sprite = _load_sprite(
            pygame,
            "apple.png",
            (CELL, APPLE_HEIGHT)
        )

        # 載入垂直牆壁圖片
        vertical_wall = _load_sprite(
            pygame,
            "wall.png",
            (WALL_THICKNESS, WALL_LENGTH)
        )

        # 將垂直牆旋轉 90 度
        # 得到水平牆
        horizontal_wall = pygame.transform.rotate(
            vertical_wall,
            90
        )

    # 如果圖片不存在或 pygame 無法讀取
    except (FileNotFoundError, pygame.error) as error:

        print(f"Unable to load game assets: {error}")

        # 關閉 pygame
        pygame.quit()

        return 2


    # 建立新遊戲
    state = new_game()

    # 設定下一次蛇移動的時間
    next_step = pygame.time.get_ticks() + STEP_MS

    # 控制主迴圈是否繼續執行
    running = True


    # =========================
    # 鍵盤控制
    # =========================

    key_directions = {

        # ← 或 A：向左
        pygame.K_LEFT: (-1, 0),
        pygame.K_a: (-1, 0),

        # → 或 D：向右
        pygame.K_RIGHT: (1, 0),
        pygame.K_d: (1, 0),

        # ↑ 或 W：向上
        pygame.K_UP: (0, -1),
        pygame.K_w: (0, -1),

        # ↓ 或 S：向下
        pygame.K_DOWN: (0, 1),
        pygame.K_s: (0, 1),
    }


    # =========================
    # 遊戲主迴圈
    # =========================

    while running:

        # -------------------------
        # 處理玩家輸入
        # -------------------------

        for event in pygame.event.get():

            # 玩家按視窗右上角 X
            if event.type == pygame.QUIT:
                running = False

            # 玩家按下鍵盤
            elif event.type == pygame.KEYDOWN:

                # 按 R 重新開始遊戲
                if event.key == pygame.K_r:

                    state = new_game()

                    # 重新計算下一次移動時間
                    next_step = (
                        pygame.time.get_ticks()
                        + STEP_MS
                    )

                # 如果按的是方向鍵
                # 而且遊戲還沒有結束
                elif (
                    event.key in key_directions
                    and not state.game_over
                ):

                    # 取得玩家想要轉向的方向
                    candidate = key_directions[event.key]

                    # 禁止蛇直接 180 度反方向移動
                    #
                    # 例如：
                    # 現在 direction = (1, 0) 向右
                    #
                    # 反方向就是：
                    # (-1, 0) 向左
                    #
                    # 因此向右走時不能立刻按左
                    if candidate != (
                        -state.direction[0],
                        -state.direction[1]
                    ):
                        state.direction = candidate


        # -------------------------
        # 更新遊戲狀態
        # -------------------------

        # 取得 pygame 啟動到現在經過多少毫秒
        now = pygame.time.get_ticks()

        # 如果遊戲沒有結束
        # 而且已經到下一次移動的時間
        if (
            not state.game_over
            and now >= next_step
        ):

            # 讓蛇往前移動一步
            step(state)

            # 下一次再過 STEP_MS 毫秒移動
            next_step += STEP_MS


        # =========================
        # 畫面繪製
        # =========================

        # 將背景填成接近白色
        screen.fill((255, 253, 249))


        # -------------------------
        # 畫垂直格線
        # -------------------------

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(
                screen,
                (226, 218, 207),
                (x, 0),
                (x, HEIGHT)
            )


        # -------------------------
        # 畫水平格線
        # -------------------------

        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(
                screen,
                (226, 218, 207),
                (0, y),
                (WIDTH, y)
            )


        # -------------------------
        # 畫食物
        # -------------------------

        # 取得食物座標
        fx, fy = state.food

        # 蘋果圖片高度比 CELL 高
        # 所以 y 往上移 CELL // 2
        # 讓蘋果視覺上對準格子
        screen.blit(
            apple_sprite,
            (fx, fy - CELL // 2)
        )


        # -------------------------
        # 畫蛇
        # -------------------------

        # enumerate 可以同時取得：
        # index = 第幾節
        # (x, y) = 該節的位置
        for index, (x, y) in enumerate(state.body):

            # index = 0 代表蛇頭
            if index == 0:

                # 根據蛇目前方向選擇蛇頭圖片
                sprite = head_sprites[state.direction]

            # 其他 index 是蛇身
            else:

                # 計算這節蛇身應該朝哪一個方向
                direction = _segment_direction(
                    state.body,
                    index,
                    state.direction
                )

                # 選擇相對應的蛇身圖片
                sprite = body_sprites[direction]

            # 把蛇的這一節畫到畫面
            screen.blit(sprite, (x, y))


        # -------------------------
        # 畫牆壁
        # -------------------------

        _draw_walls(
            screen,
            vertical_wall,
            horizontal_wall
        )


        # -------------------------
        # 顯示分數
        # -------------------------

        # 基本顯示文字
        message = f"Score {state.score}"

        # 如果遊戲結束
        # 額外顯示提示文字
        if state.game_over:
            message += (
                "  |  Game over - "
                "press R to restart"
            )

        # 將文字畫到左上角
        screen.blit(
            font.render(
                message,
                True,
                (66, 10, 21)
            ),
            (12, 10)
        )


        # 將這一幀真正顯示到螢幕
        pygame.display.flip()

        # 限制畫面更新最高為 60 FPS
        clock.tick(60)


    # 離開主迴圈後關閉 pygame
    pygame.quit()

    # 正常結束程式
    return 0


# =========================
# 程式進入點
# =========================

def main(argv: list[str] | None = None) -> int:

    # 建立命令列參數解析器
    parser = argparse.ArgumentParser()

    # 加入 --check 選項
    #
    # 執行：
    # python ... --check
    #
    # 時不會開啟完整遊戲，
    # 只會執行一次固定的邏輯測試
    parser.add_argument(
        "--check",
        action="store_true",
        help="run one deterministic logic step"
    )

    # 解析使用者輸入的參數
    args = parser.parse_args(argv)


    # 如果有輸入 --check
    if args.check:

        # 固定亂數種子
        # 讓每次測試產生相同結果
        RNG.seed(0)

        # 建立新遊戲
        state = new_game()

        # 執行一步
        step(state)

        # 顯示結果
        print({
            "head": state.body[0],
            "length": len(state.body),
            "score": state.score
        })

        return 0


    # 沒有 --check 的話
    # 正常啟動 Pygame 遊戲
    return run_game()