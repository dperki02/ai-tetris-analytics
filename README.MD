🎮 AI-Powered Tetris Game with Intelligent Agent + Live Analytics Dashboard

Created by: Dana Paulette (dperki02)
Senior IT & Digital Transformation Leader • AI-Driven Engineer • Founder of DeoNexa

████████╗███████╗████████╗████████╗██╗███████╗███████╗
╚══██╔══╝██╔════╝╚══██╔══╝╚══██╔══╝██║██╔════╝██╔════╝
   ██║   █████╗     ██║      ██║   ██║█████╗  ███████╗
   ██║   ██╔══╝     ██║      ██║   ██║██╔══╝  ╚════██║
   ██║   ███████╗   ██║      ██║   ██║███████╗███████║
   ╚═╝   ╚══════╝   ╚═╝      ╚═╝   ╚═╝╚══════╝╚══════╝

             AI Tetris • Analytics • Reinforcement Logic

🚀 Live Demo (Streamlit Dashboard)

🔗 Live Dashboard:
👉 https://ai-tetris-analytics-dperki02.streamlit.app

🏷️ Badges
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Dashboard-FF4B4B.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub stars](https://img.shields.io/github/stars/dperki02/ai-tetris-analytics?style=social)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)
![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)
![Made With Love](https://img.shields.io/badge/Made%20With-%E2%9D%A4%EF%B8%8F-red.svg)

📸 Screenshots

(Replace placeholders with your own screenshots from the game + dashboard)

Game Menu

Gameplay

Dashboard – Session Summary

🧠 Project Summary

This repository contains a full AI-enhanced Tetris ecosystem:

🎮 1. Modern, Polished Tetris Game

Human mode

AI Player mode

AI Demo mode

Animated menu screen

Pause screen with player stats

Clean UI / UX

Sound effects

Leveling system

Play-again loop

🤖 2. Intelligent AI Agent

Heuristic-based move scoring

Linear Regression reinforcement cycle

Weight training via train_ai.py

AI gets smarter over time

🗃 3. SQLite Leaderboard

Tracks:

Username

Score

Lines cleared

Level reached

Timestamp

Human vs AI

📊 4. Live Streamlit Analytics Dashboard

Session Summary (KPI metrics)

Player dropdown filter

AI vs Human performance

Trend charts

Scatter plots

Lines cleared patterns

Level-based analytics

🏗 Architecture Overview
                  +-----------------------------+
                  |      AI Agent (Heuristics)  |
                  |  ai_agent.py                |
                  +-------------+---------------+
                                |
                                v
+-------------+      +----------------------+      +------------------+
|  Game Loop  | ---> |  SQLite Leaderboard  | ---> | Streamlit Charts |
| tetris_game |      | tetris_leaderboard.db|      | dashboard.py     |
+------+------+      +----------------------+      +---------+--------+
        ^                                                      |
        |                                                      |
        +--------------- train_ai.py <-------------------------+

🛠 Installation & Setup
Clone the Repo
git clone https://github.com/dperki02/ai-tetris-analytics.git
cd ai-tetris-analytics

🧪 Local Environment Setup
Using Conda (recommended)
conda create -n ai_tetris python=3.10
conda activate ai_tetris
pip install -r requirements.txt

Optional: Install pygame locally
pip install pygame

▶️ Run the Tetris Game
python tetris_game.py


Controls

Key	Action
↑	Rotate piece
←/→	Move left/right
↓	Soft drop
Space	Hard drop
P	Pause
ESC/Q	Exit with confirmation
🧠 Train AI
python train_ai.py


Produces updated ai_weights.pkl.

📈 Run Analytics Dashboard
streamlit run dashboard.py


Go to:

http://localhost:8501

🌐 Hosting on Streamlit Cloud

Push code to GitHub

Go to: https://streamlit.io/cloud

Create new app

Choose:

Repo: dperki02/ai-tetris-analytics

Branch: main

File: dashboard.py

Deploy 🎉

🎤 Demo Script (For Presentations, Employers & Clients)

Use this script to present your project in 3–5 minutes.

1. Open with Problem + Vision

“I built an AI-powered Tetris ecosystem to demonstrate integration across AI, Python game development, database engineering, and real-time analytics.”

2. Launch the Game

Show menu

Start AI play mode

Show pause screen stats

Play one quick human round

Quit to trigger score save

3. Open the Dashboard

Filter by player

Show session summary

Show score trends

Highlight AI vs Human results

Show level analytics

4. Wrap Up

“This project demonstrates seamless integration of agent-based AI, UX design, analytics engineering, and full-stack Python development.”

👥 Contributing
1. Fork repo  
2. Create feature branch (git checkout -b feature/new-idea)  
3. Commit changes  
4. Push branch  
5. Open a pull request  


PRs welcome!

📜 License

MIT License — use it freely.

❤️ Connect

Created by: Dana Paulette (dperki02)
Founder of DeoNexa Digital Solutions
AI • Engineering • Leadership • Analytics

⭐ If you enjoyed this project, please star the repo!

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
