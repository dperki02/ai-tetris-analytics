#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 19:06:24 2025

@author: dana-paulette
"""

import sqlite3

conn = sqlite3.connect("tetris_leaderboard.db")
cur = conn.cursor()

cur.execute("SELECT * FROM leaderboard LIMIT 10;")
print(cur.fetchall())

conn.close()
