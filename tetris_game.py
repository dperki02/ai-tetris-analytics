#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 18:02:44 2025

@author: dana-paulette
"""

# tetris_game.py
import pygame
import random
import sys
import math
from typing import List
from db import LeaderboardDB
from ai_agent import TetrisAI

# ---- Optional sounds for confirmation (safe if files are missing) ----
CONFIRM_SOUND = None
CANCEL_SOUND = None

def load_sounds():
    """Try to load optional confirm/cancel sounds; ignore errors if missing."""
    global CONFIRM_SOUND, CANCEL_SOUND
    try:
        CONFIRM_SOUND = pygame.mixer.Sound("confirm.wav")     # or "assets/confirm.wav"
    except Exception:
        CONFIRM_SOUND = None
    try:
        CANCEL_SOUND = pygame.mixer.Sound("cancel.wav")       # or "assets/cancel.wav"
    except Exception:
        CANCEL_SOUND = None



# ==== Game configuration ====
GRID_WIDTH = 12    # was 10
GRID_HEIGHT = 22   # was 20
BLOCK_SIZE = 30
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
FPS = 60

# ==== Colors ====
BLACK = (10, 10, 10)
GRAY = (40, 40, 40)
WHITE = (240, 240, 240)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 0, 240)
GREEN = (0, 255, 0)
RED = (255, 60, 60)
BLUE = (0, 120, 255)
ORANGE = (255, 165, 0)
DARK_BG = (15, 15, 20)

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1],
     [1, 1]],        # O
    [[0, 1, 0],
     [1, 1, 1]],     # T
    [[1, 0, 0],
     [1, 1, 1]],     # J
    [[0, 0, 1],
     [1, 1, 1]],     # L
    [[1, 1, 0],
     [0, 1, 1]],     # S
    [[0, 1, 1],
     [1, 1, 0]],     # Z
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]


def rotate_shape(shape: List[List[int]]) -> List[List[int]]:
    return [list(row) for row in zip(*shape[::-1])]


class TetrisGame:
    def __init__(self, username: str, ai_mode: bool = False, demo_mode: bool = False):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AI-Powered Tetris")
        self.clock = pygame.time.Clock()

        self.username = username
        self.ai_mode = ai_mode
        self.demo_mode = demo_mode
        self.db = LeaderboardDB()
        self.ai_agent = TetrisAI()
        
        # Ensure optional sounds are loaded
        load_sounds()

        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_shape = None
        self.current_color = None
        self.shape_x = 0
        self.shape_y = 0
        self.score = 0
        self.lines_cleared_total = 0
        self.level = 1  # new: starting level
        self.game_over = False
        self.paused = False
        self.confirming_exit = False



        self.ai_target_x = None
        self.ai_target_rotations = 0

        self.font_small = pygame.font.SysFont("Arial", 18)
        self.font_large = pygame.font.SysFont("Arial", 32, bold=True)

        self.spawn_new_piece()

    # ====== Game mechanics ======

    def spawn_new_piece(self):
        idx = random.randint(0, len(SHAPES) - 1)
        self.current_shape = [row[:] for row in SHAPES[idx]]
        self.current_color = SHAPE_COLORS[idx]
        self.shape_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0

        if self.check_collision(self.current_shape, self.shape_x, self.shape_y):
            self.game_over = True

        if self.ai_mode:
            self.plan_ai_move()

    def plan_ai_move(self):
        binary_board = [[1 if cell != 0 else 0 for cell in row] for row in self.board]
        binary_shape = [[1 if cell != 0 else 0 for cell in row] for row in self.current_shape]
        rotations, target_x = self.ai_agent.choose_best_move(
            binary_board, SHAPES, binary_shape
        )
        self.ai_target_x = target_x
        self.ai_target_rotations = rotations

    def check_collision(self, shape, offset_x, offset_y) -> bool:
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    bx = offset_x + x
                    by = offset_y + y
                    if bx < 0 or bx >= GRID_WIDTH or by < 0 or by >= GRID_HEIGHT:
                        return True
                    if self.board[by][bx]:
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.shape_y + y][self.shape_x + x] = self.current_color
        self.clear_lines()
        self.spawn_new_piece()
        
        

    def clear_lines(self):
        new_board = []
        lines_cleared = 0

        for row in self.board:
            if all(row):
                lines_cleared += 1
            else:
                new_board.append(row)

        while len(new_board) < GRID_HEIGHT:
            new_board.insert(0, [0 for _ in range(GRID_WIDTH)])

        self.board = new_board
        if lines_cleared > 0:
            self.lines_cleared_total += lines_cleared
            self.score += lines_cleared * 100
            self.update_level()   # NEW: recalc level when lines increase


    def update_level(self):
        """Update level based on total lines cleared."""
        # Example: every 10 lines increases the level by 1
        self.level = 1 + self.lines_cleared_total // 10


    def move(self, dx: int, dy: int):
        new_x = self.shape_x + dx
        new_y = self.shape_y + dy
        if not self.check_collision(self.current_shape, new_x, new_y):
            self.shape_x = new_x
            self.shape_y = new_y
        elif dy == 1:
            self.lock_piece()

    def rotate(self):
        rotated = rotate_shape(self.current_shape)
        if not self.check_collision(rotated, self.shape_x, self.shape_y):
            self.current_shape = rotated

    def hard_drop(self):
        while not self.check_collision(self.current_shape, self.shape_x, self.shape_y + 1):
            self.shape_y += 1
        self.lock_piece()

    # ====== AI control ======

    def ai_step(self):
        if self.ai_target_rotations > 0:
            rotated = rotate_shape(self.current_shape)
            if not self.check_collision(rotated, self.shape_x, self.shape_y):
                self.current_shape = rotated
            self.ai_target_rotations -= 1
            return

        if self.ai_target_x is not None:
            if self.shape_x < self.ai_target_x:
                if not self.check_collision(self.current_shape, self.shape_x + 1, self.shape_y):
                    self.shape_x += 1
                else:
                    self.hard_drop()
                return
            elif self.shape_x > self.ai_target_x:
                if not self.check_collision(self.current_shape, self.shape_x - 1, self.shape_y):
                    self.shape_x -= 1
                else:
                    self.hard_drop()
                return
            else:
                self.hard_drop()

    # ====== Drawing ======

    def draw_board(self):
        self.screen.fill(DARK_BG)

        # grid lines
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)
                if self.board[y][x]:
                    pygame.draw.rect(self.screen, self.board[y][x], rect)

        # current piece
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (self.shape_x + x) * BLOCK_SIZE,
                        (self.shape_y + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    )
                    pygame.draw.rect(self.screen, self.current_color, rect)

        # HUD (score + lines)
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        lines_text = self.font_small.render(
            f"Lines: {self.lines_cleared_total}", True, WHITE
        )
        level_text = self.font_small.render(f"Level: {self.level}", True, WHITE)
        
        self.screen.blit(score_text, (5, 5))
        self.screen.blit(lines_text, (5, 25))
        self.screen.blit(level_text, (5, 45))

        # Pause overlay
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
        
            # Main pause title
            title = self.font_large.render("PAUSED", True, WHITE)
            self.screen.blit(
                title,
                (
                    SCREEN_WIDTH // 2 - title.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 80,
                ),
            )
        
            subtitle = self.font_small.render("Press P to resume", True, (220, 220, 220))
            self.screen.blit(
                subtitle,
                (
                    SCREEN_WIDTH // 2 - subtitle.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 50,
                ),
            )
        
            # Per-player stats
            stats_lines = [
                f"Player: {self.username}",
                f"Score: {self.score}",
                f"Lines Cleared: {self.lines_cleared_total}",
                f"Level: {self.level}",
            ]
        
            for i, line in enumerate(stats_lines):
                stat_surf = self.font_small.render(line, True, (230, 230, 255))
                self.screen.blit(
                    stat_surf,
                    (
                        SCREEN_WIDTH // 2 - stat_surf.get_width() // 2,
                        SCREEN_HEIGHT // 2 - 10 + i * 22,
                    ),
                )


        
        # Exit confirmation overlay (in-game)
        if self.confirming_exit:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            msg = "Exit game and save score?"
            msg2 = "Press Y/Enter to confirm, N/Esc/Q to cancel"
            msg_surf = self.font_large.render(msg, True, WHITE)
            msg2_surf = self.font_small.render(msg2, True, (220, 220, 220))
            self.screen.blit(
                msg_surf,
                (
                    SCREEN_WIDTH // 2 - msg_surf.get_width() // 2,
                    SCREEN_HEIGHT // 2 - msg_surf.get_height(),
                ),
            )
            self.screen.blit(
                msg2_surf,
                (
                    SCREEN_WIDTH // 2 - msg2_surf.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 10,
                ),
            )

    # ====== Lifecycle ======

    def save_score(self):
        print(f"Game over. Score: {self.score}, Lines: {self.lines_cleared_total}, Level: {self.level}")
        self.db.insert_score(
            self.username,
            self.score,
            self.ai_mode,
            self.lines_cleared_total,
            self.level,
        )

    def run(self):
        fall_time = 0
        # base speed settings (tweak to taste)
        base_speed = 500   # ms at level 1
        speed_step = 40    # speed up 40 ms per level
        min_speed = 120    # never go faster than this

        while True:
            dt = self.clock.tick(FPS)
            fall_time += dt

            for event in pygame.event.get():
                                    
                if event.type == pygame.KEYDOWN:
                    # If we are in exit-confirmation mode, handle only Y/N here
                    if self.confirming_exit:
                        if event.key in (pygame.K_y, pygame.K_RETURN):
                            if CONFIRM_SOUND:
                                CONFIRM_SOUND.play()
                            self.save_score()
                        elif event.key in (pygame.K_n, pygame.K_ESCAPE, pygame.K_q):
                            if CANCEL_SOUND:
                                CANCEL_SOUND.play()
                            self.confirming_exit = False
                        continue  # skip normal key handling while confirming
            
                    # Normal in-game key handling
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        # Ask for confirmation instead of exiting immediately
                        if CANCEL_SOUND:
                            CANCEL_SOUND.play()
                        self.confirming_exit = True
            
                    elif event.key == pygame.K_p:
                        # Toggle pause (but not if we triggered exit)
                        self.paused = not self.paused
            
                    # Player movement only allowed when not paused and not AI
                    if not self.paused and not self.ai_mode:
                        if event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move(0, 1)
                        elif event.key == pygame.K_UP:
                            self.rotate()
                        elif event.key == pygame.K_SPACE:
                            self.hard_drop()



            if self.game_over:
                self.save_score()
                return

            if not self.paused:
                # compute current speed from level
                current_speed = max(min_speed, base_speed - (self.level - 1) * speed_step)
                if fall_time >= current_speed:
                    self.move(0, 1)
                    fall_time = 0

                if self.ai_mode and not self.game_over:
                    self.ai_step()

            self.draw_board()
            pygame.display.flip()


def show_menu():       
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("IT Expert Group 2 Tetris Game")
    clock = pygame.time.Clock()
    
    # Load optional sounds once
    load_sounds()

    # Fonts
    font_title_main = pygame.font.SysFont("Arial", 34, bold=True)
    font_title_sub = pygame.font.SysFont("Arial", 26)
    font_option = pygame.font.SysFont("Arial", 24)
    font_hint = pygame.font.SysFont("Arial", 16)      # bottom instructions
    font_badge = pygame.font.SysFont("Arial", 14)     # top-right badge
    font_confirm = pygame.font.SysFont("Arial", 22, bold=True)

    # Add Exit as fourth option
    options = ["Human Player", "AI Player", "AI Demo Mode", "Exit"]
    selected = 0
    username = "Player"

    # Animation timer for dynamic accent colors
    t = 0

    # Exit confirmation state
    confirming_exit = False

    while True:
        clock.tick(30)
        t += 1

        for event in pygame.event.get():
        
            if event.type == pygame.KEYDOWN:
                # If we're in the exit-confirmation dialog, only handle Y/N here
                if confirming_exit:
                    if event.key in (pygame.K_y, pygame.K_RETURN):
                        if CONFIRM_SOUND:
                            CONFIRM_SOUND.play()
                    elif event.key in (pygame.K_n, pygame.K_ESCAPE, pygame.K_q):
                        if CANCEL_SOUND:
                            CANCEL_SOUND.play()
                        confirming_exit = False
                    continue  # don't process normal menu keys while confirming
        
                # Normal menu key handling
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    # Trigger confirmation dialog instead of exiting immediately
                    if CANCEL_SOUND:
                        CANCEL_SOUND.play()
                    confirming_exit = True
        
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    # Human mode
                    if selected == 0:
                        pygame.display.iconify()
                        username_input = input("Enter human username: ").strip()
                        if username_input:
                            username = username_input
                        if CONFIRM_SOUND:
                            CONFIRM_SOUND.play()
                        return "human", username
        
                    # AI mode
                    elif selected == 1:
                        pygame.display.iconify()
                        username_input = input("Enter AI player name (e.g., AI_BOT): ").strip()
                        if username_input:
                            username = username_input
                        if CONFIRM_SOUND:
                            CONFIRM_SOUND.play()
                        return "ai", username
        
                    # Demo mode
                    elif selected == 2:
                        if CONFIRM_SOUND:
                            CONFIRM_SOUND.play()
                        return "demo", "AI_DEMO"
        
                    # Exit option
                    elif selected == 3:
                        if CANCEL_SOUND:
                            CANCEL_SOUND.play()
                        confirming_exit = True


        # ----- Background with subtle gradient -----
        screen.fill((15, 15, 25))
        for y in range(0, SCREEN_HEIGHT, 4):
            shade = 15 + int(40 * (y / SCREEN_HEIGHT))
            pygame.draw.line(screen, (shade, shade, shade + 10), (0, y), (SCREEN_WIDTH, y))

        # ----- Dynamic accent color for title (soft pulsing) -----
        pulse = (math.sin(t / 30.0) + 1) / 2  # 0..1
        accent_r = int(80 + 120 * pulse)
        accent_g = int(120 + 80 * (1 - pulse))
        accent_b = 255
        accent_color = (accent_r, accent_g, accent_b)

        # ----- Title -----
        title_main = font_title_main.render("IT Expert Group 2", True, accent_color)
        title_sub = font_title_sub.render("Tetris Game", True, (230, 230, 230))

        title_y = 40
        screen.blit(
            title_main,
            (SCREEN_WIDTH // 2 - title_main.get_width() // 2, title_y),
        )
        screen.blit(
            title_sub,
            (SCREEN_WIDTH // 2 - title_sub.get_width() // 2, title_y + 40),
        )

        # ----- Tetris graphic badge under title -----
        badge_block_size = 18
        badge_pattern = [
            [CYAN, None, CYAN, None],
            [None, YELLOW, GREEN, ORANGE],
        ]
        badge_width_px = 4 * badge_block_size
        badge_height_px = 2 * badge_block_size
        badge_start_x = SCREEN_WIDTH // 2 - badge_width_px // 2
        badge_start_y = title_y + 80

        for row_idx, row in enumerate(badge_pattern):
            for col_idx, color in enumerate(row):
                if color is not None:
                    rect = pygame.Rect(
                        badge_start_x + col_idx * badge_block_size,
                        badge_start_y + row_idx * badge_block_size,
                        badge_block_size,
                        badge_block_size,
                    )
                    pygame.draw.rect(screen, color, rect, border_radius=3)
                    pygame.draw.rect(screen, (20, 20, 30), rect, 2, border_radius=3)

        # ----- Menu options -----
        start_y = badge_start_y + badge_height_px + 30
        spacing = 40

        for i, opt in enumerate(options):
            if i == selected:
                highlight_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - 160,
                    start_y + i * spacing - 4,
                    320,
                    32,
                )
                pygame.draw.rect(screen, (40, 40, 70), highlight_rect, border_radius=10)
                color = (255, 255, 255)
            else:
                color = (190, 190, 190)

            opt_surf = font_option.render(opt, True, color)
            screen.blit(
                opt_surf,
                (SCREEN_WIDTH // 2 - opt_surf.get_width() // 2, start_y + i * spacing),
            )

        # ----- Top-right badge: ESC/Q to exit -----
        badge_text = "ESC/Q: Exit"
        badge_surf = font_badge.render(badge_text, True, (255, 255, 255))
        padding_x, padding_y = 8, 4
        badge_rect = pygame.Rect(
            SCREEN_WIDTH - badge_surf.get_width() - padding_x * 2 - 10,
            10,
            badge_surf.get_width() + padding_x * 2,
            badge_surf.get_height() + padding_y * 2,
        )
        pygame.draw.rect(screen, (30, 30, 50), badge_rect, border_radius=8)
        pygame.draw.rect(screen, (80, 80, 120), badge_rect, 1, border_radius=8)
        screen.blit(
            badge_surf,
            (badge_rect.x + padding_x, badge_rect.y + padding_y),
        )

        # ----- Bottom instructions (two lines) -----
        instructions_lines = [
            "Use ↑ / ↓ to choose • ENTER to start",
            "Select 'Exit' or press ESC/Q to quit • P pauses in game",
        ]

        overlay_height = 70
        overlay = pygame.Surface((SCREEN_WIDTH, overlay_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, SCREEN_HEIGHT - overlay_height))

        for i, line in enumerate(instructions_lines):
            hint_surf = font_hint.render(line, True, (255, 255, 255))
            y = SCREEN_HEIGHT - overlay_height + 10 + i * (font_hint.get_height() + 4)
            screen.blit(
                hint_surf,
                (SCREEN_WIDTH // 2 - hint_surf.get_width() // 2, y),
            )

        # ----- Exit confirmation overlay (menu-level) -----

        if confirming_exit:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))
        
            msg = "Exit IT Expert Group 2 Tetris Game?"
            msg2 = "Y or Enter = Yes   •   N / Esc / Q = No"
        
            msg_surf = font_confirm.render(msg, True, (255, 255, 255))
            msg2_surf = font_hint.render(msg2, True, (200, 220, 255))
        
            screen.blit(
                msg_surf,
                (
                    SCREEN_WIDTH // 2 - msg_surf.get_width() // 2,
                    SCREEN_HEIGHT // 2 - msg_surf.get_height(),
                ),
            )
            screen.blit(
                msg2_surf,
                (
                    SCREEN_WIDTH // 2 - msg2_surf.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 12,
                ),
            )


        pygame.display.flip()



if __name__ == "__main__":
    while True:
        mode, username = show_menu()

        if mode == "human":
            game = TetrisGame(username=username, ai_mode=False, demo_mode=False)
        elif mode == "ai":
            game = TetrisGame(username=username, ai_mode=True, demo_mode=False)
        else:  # demo
            game = TetrisGame(username="AI_DEMO", ai_mode=True, demo_mode=True)

        game.run()  # returns after saving score

        # Ask if the user wants to play again
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer not in ("y", "yes"):
            break

    pygame.quit()
    sys.exit()

