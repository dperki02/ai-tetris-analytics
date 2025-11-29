#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 18:00:52 2025

@author: dana-paulette
"""

# train_ai.py
import random
import pickle
from typing import List
import numpy as np
from sklearn.linear_model import LinearRegression

from ai_agent import TetrisAI, WEIGHTS_FILE

GRID_WIDTH = 12   # match tetris_game.py
GRID_HEIGHT = 22


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


class HeadlessTetrisEnv:
    """
    Simple, non-graphical Tetris environment for training.
    Uses TetrisAI to decide moves given weights.
    """

    def __init__(self, ai: TetrisAI, max_steps: int = 500):
        self.ai = ai
        self.max_steps = max_steps
        self.reset()

    def reset(self):
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.steps = 0
        self.spawn_new_piece()

    def spawn_new_piece(self):
        idx = random.randint(0, len(SHAPES) - 1)
        self.current_shape = [row[:] for row in SHAPES[idx]]
        self.shape_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        if self.check_collision(self.current_shape, self.shape_x, self.shape_y):
            self.game_over = True

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
                    self.board[self.shape_y + y][self.shape_x + x] = 1
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
        self.score += lines_cleared * 100

    def _board_to_binary(self) -> List[List[int]]:
        return [[1 if cell != 0 else 0 for cell in row] for row in self.board]

    def _shape_to_binary(self, shape) -> List[List[int]]:
        return [[1 if cell != 0 else 0 for cell in row] for row in shape]

    def step(self):
        """
        One AI decision + piece drop until lock.
        """
        if self.game_over or self.steps > self.max_steps:
            self.game_over = True
            return

        binary_board = self._board_to_binary()
        binary_shape = self._shape_to_binary(self.current_shape)

        rotation, target_x = self.ai.choose_best_move(
            binary_board, SHAPES, binary_shape
        )

        # Apply rotation
        for _ in range(rotation):
            self.current_shape = self.ai.rotate_shape(self.current_shape)

        # Move horizontally
        while self.shape_x < target_x and not self.check_collision(self.current_shape, self.shape_x + 1, self.shape_y):
            self.shape_x += 1
        while self.shape_x > target_x and not self.check_collision(self.current_shape, self.shape_x - 1, self.shape_y):
            self.shape_x -= 1

        # Drop
        while not self.check_collision(self.current_shape, self.shape_x, self.shape_y + 1):
            self.shape_y += 1
        self.lock_piece()
        self.steps += 1

    def run_episode(self) -> int:
        self.reset()
        while not self.game_over:
            self.step()
        return self.score


def random_weights(base=(1.0, -0.5, -0.8, -0.3), scale=0.5):
    return tuple(
        b + random.uniform(-scale, scale) for b in base
    )


def train(num_trials: int = 40, episodes_per_trial: int = 2):
    """
    Simple ML-style loop:
    - Try many random weight vectors.
    - Evaluate their average score in the headless env.
    - Fit LinearRegression: weights -> expected score.
    - Use model to pick a promising candidate.
    - Save best weights to ai_weights.pkl.
    """
    print("[TRAIN] Starting training...")

    X = []
    y = []

    base = (1.0, -0.5, -0.8, -0.3)

    for trial in range(num_trials):
        w = random_weights(base, scale=1.0)
        ai = TetrisAI(
            w_lines=w[0],
            w_height=w[1],
            w_holes=w[2],
            w_bumpiness=w[3],
            load_from_file=False,
        )
        env = HeadlessTetrisEnv(ai, max_steps=400)

        scores = []
        for _ in range(episodes_per_trial):
            score = env.run_episode()
            scores.append(score)

        avg_score = sum(scores) / len(scores)
        X.append(list(w))
        y.append(avg_score)
        print(f"[TRIAL {trial+1}/{num_trials}] weights={w}, avg_score={avg_score}")

    X = np.array(X)
    y = np.array(y)

    model = LinearRegression()
    model.fit(X, y)
    print("[TRAIN] Regression coefficients:", model.coef_, "intercept:", model.intercept_)

    candidate_weights = []
    for _ in range(50):
        candidate_weights.append(random_weights(base, scale=1.5))
    candidate_weights = np.array(candidate_weights)
    preds = model.predict(candidate_weights)
    best_idx = int(np.argmax(preds))
    best_w = tuple(candidate_weights[best_idx])
    print("[TRAIN] Best predicted weights from model:", best_w, "predicted score:", preds[best_idx])

    # Verify best
    ai_best = TetrisAI(
        w_lines=best_w[0],
        w_height=best_w[1],
        w_holes=best_w[2],
        w_bumpiness=best_w[3],
        load_from_file=False,
    )
    env_best = HeadlessTetrisEnv(ai_best, max_steps=500)
    verify_scores = [env_best.run_episode() for _ in range(3)]
    verify_avg = sum(verify_scores) / len(verify_scores)
    print("[TRAIN] Verified avg score with best weights:", verify_avg)

    with open(WEIGHTS_FILE, "wb") as f:
        pickle.dump(best_w, f)
    print(f"[TRAIN] Saved best weights to {WEIGHTS_FILE}: {best_w}")


if __name__ == "__main__":
    train()
