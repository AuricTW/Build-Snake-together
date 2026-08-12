"""Supplied Pygame presentation shell for the Snake trio mission.

Students do not need to understand or edit this file during the core mission.
It translates keys, draws the board, and calls the four functions in logic.py.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from .logic import Cell, Direction, advance_body, ate_food, hit_wall, next_head

WIDTH = 640
HEIGHT = 480
CELL = 20
STEP_MS = 130
START_BODY: list[Cell] = [(200, 200), (180, 200), (160, 200)]
START_DIRECTION: Direction = (1, 0)
ASSET_DIR = Path(__file__).with_name("assets")
APPLE_HEIGHT = CELL + CELL // 2
WALL_LENGTH = CELL * 20
WALL_THICKNESS = max(4, CELL // 4)


def _load_sprite(pygame, name: str, size: tuple[int, int]):
    """Load, clean, and scale one blue-on-light-background sprite."""
    sprite = pygame.image.load(ASSET_DIR / name).convert_alpha()
    for y in range(sprite.get_height()):
        for x in range(sprite.get_width()):
            red, green, blue, alpha = sprite.get_at((x, y))
            if red >= 240:
                alpha = 0
            elif red > 160:
                alpha = round((240 - red) * 255 / 80)
            else:
                alpha = 255
            sprite.set_at((x, y), (red, green, blue, alpha))
    return pygame.transform.smoothscale(sprite, size)


def _directional_sprites(pygame, left_facing_sprite):
    """Build rotations for a sprite whose source artwork faces left."""
    return {
        (-1, 0): left_facing_sprite,
        (1, 0): pygame.transform.rotate(left_facing_sprite, 180),
        (0, -1): pygame.transform.rotate(left_facing_sprite, 90),
        (0, 1): pygame.transform.rotate(left_facing_sprite, -90),
    }


def _segment_direction(body: list[Cell], index: int, fallback: Direction) -> Direction:
    """Point a body sprite toward the preceding segment."""
    if index == 0:
        return fallback
    x, y = body[index]
    previous_x, previous_y = body[index - 1]
    direction = ((previous_x - x) // CELL, (previous_y - y) // CELL)
    return direction if direction in {(-1, 0), (1, 0), (0, -1), (0, 1)} else fallback


def _draw_walls(screen, vertical_wall, horizontal_wall) -> None:
    """Tile the twenty-cell wall artwork around the board perimeter."""
    for y in range(0, HEIGHT, WALL_LENGTH):
        screen.blit(vertical_wall, (0, y))
        screen.blit(vertical_wall, (WIDTH - WALL_THICKNESS, y))
    for x in range(0, WIDTH, WALL_LENGTH):
        screen.blit(horizontal_wall, (x, 0))
        screen.blit(horizontal_wall, (x, HEIGHT - WALL_THICKNESS))


def choose_food(body: list[Cell]) -> Cell: # 用來選擇食物位置
    """Choose the first free cell deterministically for reproducible play."""
    for y in range(0, HEIGHT, CELL):
        for x in range(0, WIDTH, CELL):
            if (x, y) not in body:
                return (x, y)
    raise RuntimeError("board is full")


@dataclass
class GameState:
    body: list[Cell]
    direction: Direction
    food: Cell
    score: int = 0
    game_over: bool = False


def new_game() -> GameState:
    body = list(START_BODY)
    return GameState(body=body, direction=START_DIRECTION, food=choose_food(body))


def step(state: GameState) -> None:
    new_head = next_head(state.body[0], state.direction, CELL)
    grow = ate_food(new_head, state.food)
    next_body = advance_body(state.body, new_head, grow)
    self_hit = new_head in next_body[1:]
    if hit_wall(new_head, WIDTH, HEIGHT, CELL) or self_hit:
        state.game_over = True
        return
    state.body = next_body
    if grow:
        state.score += 1
        state.food = choose_food(state.body)


def run_game() -> int:
    try:
        import pygame
    except ImportError:
        print("Pygame is not installed. Run: python -m pip install -e '.[display]' ")
        return 2

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NCKU Snake Trio Studio")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    try:
        head_sprites = _directional_sprites(
            pygame, _load_sprite(pygame, "head.png", (CELL, CELL))
        )
        body_sprites = _directional_sprites(
            pygame, _load_sprite(pygame, "body.png", (CELL, CELL))
        )
        apple_sprite = _load_sprite(pygame, "apple.png", (CELL, APPLE_HEIGHT))
        vertical_wall = _load_sprite(
            pygame, "wall.png", (WALL_THICKNESS, WALL_LENGTH)
        )
        horizontal_wall = pygame.transform.rotate(vertical_wall, 90)
    except (FileNotFoundError, pygame.error) as error:
        print(f"Unable to load game assets: {error}")
        pygame.quit()
        return 2
    state = new_game()
    next_step = pygame.time.get_ticks() + STEP_MS
    running = True

    key_directions = {
        pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
        pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
        pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
        pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = new_game()
                    next_step = pygame.time.get_ticks() + STEP_MS
                elif event.key in key_directions and not state.game_over:
                    candidate = key_directions[event.key]
                    if candidate != (-state.direction[0], -state.direction[1]):
                        state.direction = candidate

        now = pygame.time.get_ticks()
        if not state.game_over and now >= next_step:
            step(state)
            next_step += STEP_MS

        screen.fill((255, 253, 249))
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, (226, 218, 207), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, (226, 218, 207), (0, y), (WIDTH, y))
        fx, fy = state.food
        screen.blit(apple_sprite, (fx, fy - CELL // 2))
        for index, (x, y) in enumerate(state.body):
            if index == 0:
                sprite = head_sprites[state.direction]
            else:
                direction = _segment_direction(state.body, index, state.direction)
                sprite = body_sprites[direction]
            screen.blit(sprite, (x, y))
        _draw_walls(screen, vertical_wall, horizontal_wall)
        message = f"Score {state.score}"
        if state.game_over:
            message += "  |  Game over - press R to restart"
        screen.blit(font.render(message, True, (66, 10, 21)), (12, 10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run one deterministic logic step")
    args = parser.parse_args(argv)
    if args.check:
        state = new_game()
        step(state)
        print({"head": state.body[0], "length": len(state.body), "score": state.score})
        return 0
    return run_game()
