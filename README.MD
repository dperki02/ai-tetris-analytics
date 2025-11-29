#!/usr/bin/env python3
# 🎮 AI-Powered Tetris Game with Intelligent Agent, Leaderboard, and Analytics Dashboard  
**Created by: Dana Paulette (dperki02)**

This project is a full-stack, AI-driven Tetris implementation demonstrating modern software engineering across:

- **Python game development (pygame)**
- **AI/ML heuristic agent + training loop (scikit-learn)**
- **SQLite-backed leaderboard tracking**
- **Streamlit analytics dashboard**
- **Visual polish, UX interactions, sound feedback, and gameplay progression**

It is built as a **showcase project** for technical interviews, AI engineering discussions, and demos of AI + Analytics integration.

---

## 🚀 Features Overview

### 🎮 **1. Playable Tetris Game (with polished UI)**
- Human mode  
- AI Player mode (uses learned heuristics)  
- AI Demo mode  
- Clean animated menu interface  
- Tetris logo badge + ESC/Q exit badge  
- Pause screen with per-player stats (Score, Lines, Level)  
- Smooth gameplay, rotation, gravity, hard drop, collision detection  

### 🤖 **2. AI Gameplay Agent**
- Heuristic evaluation of:
  - Lines cleared
  - Holes
  - Bumpiness
  - Aggregate height  
- AI Training Loop (`train_ai.py`) uses:
  - Random weight exploration
  - LinearRegression (scikit-learn)
  - Saves learned weights to `ai_weights.pkl`
- Game loads trained weights automatically

### 🗃 **3. Leaderboard & Database**
- Tracks:
  - Username  
  - Score  
  - Lines cleared  
  - Level reached  
  - Timestamp  
  - AI vs Human flag  
- Stored in local SQLite (`tetris_leaderboard.db`)

### 📊 **4. Full Analytics Dashboard (Streamlit)**
Live or hosted on Streamlit Cloud.

Includes:
- Session Summary (games played, best score, avg score, lines, levels)
- Per-player filters  
- Top 10 scores  
- Score progression over time  
- AI vs Human performance  
- Lines cleared per player  
- Score vs lines scatter  
- Max Level per player  
- Average level (AI vs Human)

### 🔁 **5. Play Again Loop**
After each game:


This project showcases a full pipeline:

- Pygame-based Tetris game (human or AI)
- Heuristic AI agent with a training loop using scikit-learn
- SQLite leaderboard backend
- Streamlit dashboard with visual analytics

See the code files for details:
- `tetris_game.py` – Game + menu UI
- `ai_agent.py` – AI logic and weight loading
- `train_ai.py` – Training loop that evolves heuristic weights
- `db.py` – Leaderboard database helper
- `dashboard.py` – Analytics dashboard
- `init_db.sql` – DB schema + sample data
- `requirements.txt` – Python dependencies
