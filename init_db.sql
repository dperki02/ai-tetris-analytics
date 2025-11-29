CREATE TABLE IF NOT EXISTS leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    score INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    is_ai INTEGER NOT NULL CHECK (is_ai IN (0, 1))
);

-- Sample data (10+ rows, mix AI & human)
INSERT INTO leaderboard (username, score, timestamp, is_ai) VALUES
('Dana',         1200, '2025-11-20T10:01:00', 0),
('PlayerOne',     800, '2025-11-20T11:30:00', 0),
('AI_BOT_1',     1500, '2025-11-20T12:15:00', 1),
('PlayerTwo',     500, '2025-11-20T13:05:00', 0),
('AI_BOT_2',     1700, '2025-11-20T14:45:00', 1),
('GamerGirl',    1300, '2025-11-21T09:10:00', 0),
('AI_BOT_1',     1900, '2025-11-21T10:40:00', 1),
('CasualJoe',     600, '2025-11-21T11:20:00', 0),
('AI_BOT_3',     1100, '2025-11-21T12:55:00', 1),
('SpeedRunner',  2000, '2025-11-21T14:30:00', 0),
('AI_BOT_2',     2100, '2025-11-21T15:05:00', 1);
