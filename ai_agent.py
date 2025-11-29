#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 18:00:10 2025

@author: dana-paulette
"""

# ai_agent.py
from typing import List, Tuple, Optional
import os
import pickle

WEIGHTS_FILE = "ai_weights.pkl"


class TetrisAI:
    def __init__(
        self,
        w_lines: float = 1.0,
        w_height: float = -0.5,
        w_holes: float = -0.8,
        w_bumpiness: float = -0.3,
        load_from_file: bool = True,
    ):
        # Default weights
        self.w_lines = w_lines
        self.w_height = w_height
        self.w_holes = w_holes
        self.w_bumpiness = w_bumpiness

        # Optionally load learned weights
        if load_from_file and os.path.exists(WEIGHTS_FILE):
            try:
                with open(WEIGHTS_FILE, "rb") as f:
                    weights = pickle.load(f)
                (
                    self.w_lines,
                    self.w_height,
                    self.w_holes,
                    self.w_bumpiness,
                ) = weights
                print("[TetrisAI] Loaded learned weights:", weights)
            except Exception as e:
                print("[TetrisAI] Failed to load weights, using defaults:", e)

    def get_weights(self):
        return (self.w_lines, self.w_height, self.w_holes, self.w_bumpiness)

    def set_weights(self, w_lines, w_height, w_holes, w_bumpiness):
        self.w_lines = w_lines
        self.w_height = w_height
        self.w_holes = w_holes
        self.w_bumpiness = w_bumpiness

    def choose_best_move(
        self,
        board: List[List[int]],
        shapes: List[List[List[int]]],
        current_shape: List[List[int]],
    ) -> Tuple[int, int]:
        """
        Returns (best_rotation_count, best_x_position)
        rotation_count: 0-3
        x_position: column index where the shape's leftmost block will be placed.
        """
        best_score = None
        best_rotation = 0
        best_x = 0

        rotated_shape = current_shape
        for rot in range(4):
            shape_w = len(rotated_shape[0])
            for x in range(0, len(board[0]) - shape_w + 1):
                test_board, lines_cleared = self.simulate_drop(board, rotated_shape, x)
                if test_board is None:
                    continue

                score = self.evaluate_board(test_board, lines_cleared)
                if best_score is None or score > best_score:
                    best_score = score
                    best_rotation = rot
                    best_x = x

            rotated_shape = self.rotate_shape(rotated_shape)

        return best_rotation, best_x

    def rotate_shape(self, shape: List[List[int]]) -> List[List[int]]:
        # Rotate 90 degrees clockwise
        return [list(row) for row in zip(*shape[::-1])]

    def simulate_drop(
        self,
        board: List[List[int]],
        shape: List[List[int]],
        x_pos: int,
    ) -> Tuple[Optional[List[List[int]]], int]:
        height = len(board)
        shape_h = len(shape)
        shape_w = len(shape[0])

        y_pos = 0
        while True:
            if self.check_collision(board, shape, x_pos, y_pos):
                y_pos -= 1
                break
            y_pos += 1
            if y_pos + shape_h > height:
                y_pos -= 1
                break

        if y_pos < 0 or self.check_collision(board, shape, x_pos, y_pos):
            return None, 0

        new_board = [row[:] for row in board]
        for y in range(shape_h):
            for x in range(shape_w):
                if shape[y][x]:
                    new_board[y_pos + y][x_pos + x] = 1

        new_board, lines_cleared = self.clear_lines(new_board)
        return new_board, lines_cleared

    def check_collision(
        self,
        board: List[List[int]],
        shape: List[List[int]],
        x_pos: int,
        y_pos: int,
    ) -> bool:
        height = len(board)
        width = len(board[0])
        shape_h = len(shape)
        shape_w = len(shape[0])

        for y in range(shape_h):
            for x in range(shape_w):
                if shape[y][x]:
                    bx = x_pos + x
                    by = y_pos + y
                    if bx < 0 or bx >= width or by < 0 or by >= height:
                        return True
                    if board[by][bx]:
                        return True
        return False

    def clear_lines(self, board: List[List[int]]):
        height = len(board)
        width = len(board[0])
        new_board = []
        lines_cleared = 0

        for y in range(height):
            if all(board[y][x] != 0 for x in range(width)):
                lines_cleared += 1
            else:
                new_board.append(board[y])

        while len(new_board) < height:
            new_board.insert(0, [0] * width)

        return new_board, lines_cleared

    def evaluate_board(self, board: List[List[int]], lines_cleared: int) -> float:
        agg_height = self.aggregate_height(board)
        holes = self.count_holes(board)
        bumpiness = self.bumpiness(board)

        score = (
            self.w_lines * lines_cleared
            + self.w_height * agg_height
            + self.w_holes * holes
            + self.w_bumpiness * bumpiness
        )
        return score

    def column_heights(self, board: List[List[int]]) -> List[int]:
        height = len(board)
        width = len(board[0])
        heights = [0] * width
        for x in range(width):
            for y in range(height):
                if board[y][x]:
                    heights[x] = height - y
                    break
        return heights

    def aggregate_height(self, board: List[List[int]]) -> int:
        return sum(self.column_heights(board))

    def count_holes(self, board: List[List[int]]) -> int:
        height = len(board)
        width = len(board[0])
        holes = 0
        for x in range(width):
            block_seen = False
            for y in range(height):
                if board[y][x]:
                    block_seen = True
                elif block_seen and not board[y][x]:
                    holes += 1
        return holes

    def bumpiness(self, board: List[List[int]]) -> int:
        heights = self.column_heights(board)
        return sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))
