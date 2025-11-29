#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 17:59:23 2025

@author: dana-paulette
"""

# db.py
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

DB_PATH = "tetris_leaderboard.db"


class LeaderboardDB:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._create_table_if_not_exists()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table_if_not_exists(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                score INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                is_ai INTEGER NOT NULL CHECK (is_ai IN (0, 1)),
                lines_cleared INTEGER NOT NULL DEFAULT 0,
                level INTEGER NOT NULL DEFAULT 1
            );
            """
        )

        conn.commit()
        conn.close()

    def insert_score(self, username: str, score: int, is_ai: bool, lines_cleared: int, level: int):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO leaderboard (username, score, timestamp, is_ai, lines_cleared, level)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                score,
                datetime.now().isoformat(timespec="seconds"),
                1 if is_ai else 0,
                lines_cleared,
                level,
            ),
        )
        conn.commit()
        conn.close()


    def get_all_scores(self) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, score, timestamp, is_ai, lines_cleared FROM leaderboard"
        )
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "username": r[1],
                "score": r[2],
                "timestamp": r[3],
                "is_ai": bool(r[4]),
                "lines_cleared": r[5],
                "level": r[6],
            }
            for r in rows
        ]
