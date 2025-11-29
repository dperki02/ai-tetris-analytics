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
Play again? (y/n):
`
The game immediately returns to the menu without restarting the script.

### 🎵 **6. Optional Sound Effects**
- confirm.wav  
- cancel.wav  

---

## 🛠 Installation & Setup

### **Clone the Repo**
bash git clone https://github.com/dperki02/ai-tetris-analytics.git cd ai-tetris-analytics
`

### **Set Up Environment**

Using conda (recommended):
bash conda create -n ai_tetris python=3.10 conda activate ai_tetris
### **Install Dependencies**
bash pip install -r requirements.txt
### **Initialize the Database (if needed)**
bash sqlite3 tetris_leaderboard.db < init_db.sql
or run the game once — it will create the DB automatically.

---

## ▶️ Run the Tetris Game
bash python tetris_game.py
### Controls:

| Key     | Action                   |
| ------- | ------------------------ |
| ↑       | Rotate piece             |
| ← / →   | Move piece left/right    |
| ↓       | Soft drop                |
| Space   | Hard drop                |
| P       | Pause / Resume           |
| ESC / Q | Exit (with confirmation) |

On game over or exit, the session is stored in the SQLite database.

---

## 🧠 Train the AI Agent
bash python train_ai.py
Outputs:

* Best predicted weights
* Validation performance
* Saves new weights to **ai_weights.pkl**

The game automatically loads this file on startup.

---

## 📈 Launch the Analytics Dashboard
bash streamlit run dashboard.py
Visit the local URL (typically):
http://localhost:8501
Features:

* Session summary
* Username filtering
* Multiple performance charts
* AI vs Human comparisons

---

## 🌐 Hosting (Streamlit Cloud)

You can deploy the dashboard online by connecting this repo to:

[https://streamlit.io/cloud](https://streamlit.io/cloud)

Select:

* Repo: `dperki02/ai-tetris-analytics`
* Branch: `main`
* File: `dashboard.py`

Your dashboard will be instantly available at a public URL.

---

## 🧩 Project Structure
text ai_tetris_project/ ├── ai_agent.py ├── dashboard.py ├── db.py ├── tetris_game.py ├── train_ai.py ├── requirements.txt ├── init_db.sql ├── tetris_leaderboard.db (optional) ├── confirm.wav (optional) ├── cancel.wav (optional) └── README.md
---

## 🏗 Future Enhancements (Roadmap)

* Deploy the full system as a web application using WebAssembly or Pyodide
* Add multiplayer modes or challenges
* Add next-piece predictor visual
* Add per-session analytics and heatmaps
* Integrate cloud database (PostgreSQL)
* Add authentication for user profiles
* Add achievement badges on the dashboard

---

## ❤️ Author

**Dana Paulette (dperki02)**
Senior IT & Digital Transformation Leader
Founder – DeoNexa Digital Solutions
AI | Engineering | Product Analytics | Innovation

---

## 📜 License

MIT License — free to use, modify, and share.

---

# 🎉 Thank you for checking out the AI Tetris Project!

If you enjoyed it, feel free to star ⭐ the repo.

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
