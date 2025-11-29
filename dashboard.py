#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 18:04:57 2025

@author: dana-paulette
"""

# dashboard.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

DB_PATH = "tetris_leaderboard.db"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT id, username, score, timestamp, is_ai, lines_cleared, level FROM leaderboard",
        conn,
    )
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["player_type"] = df["is_ai"].apply(lambda x: "AI" if x == 1 else "Human")
    
    def max_level_per_player_chart(df):
        max_levels = df.groupby("username")["level"].max().sort_values(ascending=False)
        fig, ax = plt.subplots()
        ax.bar(max_levels.index, max_levels.values)
        ax.set_title("Max Level Reached per Player")
        ax.set_ylabel("Level")
        ax.set_xticklabels(max_levels.index, rotation=45, ha="right")
        st.pyplot(fig)
        
    def avg_level_by_type_chart(df):
        avg_levels = df.groupby("player_type")["level"].mean()
        fig, ax = plt.subplots()
        ax.bar(avg_levels.index, avg_levels.values)
        ax.set_title("Average Level by Player Type")
        ax.set_ylabel("Average Level")
        st.pyplot(fig)

    return df


def top_scores_chart(df):
    top_df = df.sort_values("score", ascending=False).head(10)
    fig, ax = plt.subplots()
    ax.bar(top_df["username"], top_df["score"])
    ax.set_title("Top 10 Player Scores")
    ax.set_ylabel("Score")
    ax.set_xticklabels(top_df["username"], rotation=45, ha="right")
    st.pyplot(fig)


def score_over_time_chart(df):
    df_sorted = df.sort_values("timestamp")
    fig, ax = plt.subplots()
    for ptype, group in df_sorted.groupby("player_type"):
        ax.plot(group["timestamp"], group["score"], marker="o", label=ptype)
    ax.set_title("Score Progression Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Score")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)


def ai_vs_human_chart(df):
    avg_scores = df.groupby("player_type")["score"].mean()
    fig, ax = plt.subplots()
    ax.pie(avg_scores, labels=avg_scores.index, autopct="%1.1f%%")
    ax.set_title("AI vs Human Average Score Share")
    st.pyplot(fig)


def avg_lines_per_player_chart(df):
    avg_lines = df.groupby("username")["lines_cleared"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.bar(avg_lines.index, avg_lines.values)
    ax.set_title("Average Lines Cleared per Player")
    ax.set_ylabel("Lines Cleared")
    ax.set_xticklabels(avg_lines.index, rotation=45, ha="right")
    st.pyplot(fig)


def score_vs_lines_scatter(df):
    fig, ax = plt.subplots()
    scatter = ax.scatter(df["lines_cleared"], df["score"], c=df["is_ai"].map({0: 0, 1: 1}))
    ax.set_title("Score vs Lines Cleared")
    ax.set_xlabel("Lines Cleared")
    ax.set_ylabel("Score")
    st.pyplot(fig)
    
    
def max_level_per_player_chart(df):
    """Shows highest level reached by each player."""
    max_levels = df.groupby("username")["level"].max().sort_values(ascending=False)
    
    fig, ax = plt.subplots()
    ax.bar(max_levels.index, max_levels.values)
    ax.set_title("Max Level Reached per Player")
    ax.set_ylabel("Level")
    ax.set_xticklabels(max_levels.index, rotation=45, ha="right")
    
    st.pyplot(fig)

def avg_level_by_type_chart(df):
    """Shows average achieved level for Human vs AI."""
    avg_levels = df.groupby("player_type")["level"].mean()
    
    fig, ax = plt.subplots()
    ax.bar(avg_levels.index, avg_levels.values)
    ax.set_title("Average Level by Player Type (AI vs Human)")
    ax.set_ylabel("Average Level")
    
    st.pyplot(fig)


def main():
    st.title("Tetris Leaderboard Analytics Dashboard")

    # ---- Load & filter data ----
    df = load_data()

    st.sidebar.header("Filters")
    usernames = sorted(df["username"].unique())
    username_options = ["All players"] + usernames

    selected_username = st.sidebar.selectbox(
        "Select player",
        options=username_options,
        index=0,
    )

    if selected_username != "All players":
        df_filtered = df[df["username"] == selected_username]
    else:
        df_filtered = df

    # Guard: no records
    if df_filtered.empty:
        st.warning("No records found for this selection.")
        return

    # Context caption
    if selected_username == "All players":
        st.caption("Showing data for **all players**.")
    else:
        st.caption(f"Showing data for **{selected_username}**.")

    # ---- Session Summary ----
    st.markdown("### Session Summary")

    games_played = len(df_filtered)
    best_score = int(df_filtered["score"].max())
    avg_score = float(df_filtered["score"].mean())
    total_lines = int(df_filtered["lines_cleared"].sum())
    max_level = int(df_filtered["level"].max())
    avg_level = float(df_filtered["level"].mean())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Games Played", games_played)
    with col2:
        st.metric("Best Score", best_score)
    with col3:
        st.metric("Average Score", f"{avg_score:.1f}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Total Lines Cleared", total_lines)
    with col5:
        st.metric("Max Level Reached", max_level)
    with col6:
        st.metric("Average Level", f"{avg_level:.1f}")

    # ---- Raw data ----
    st.markdown("---")
    st.subheader("Raw Leaderboard Data")
    st.dataframe(df_filtered.sort_values("score", ascending=False))

    # ---- Charts using df_filtered ----
    st.markdown("---")
    st.subheader("Top Player Scores")
    top_scores_chart(df_filtered)

    st.markdown("---")
    st.subheader("Score Progression Over Time")
    score_over_time_chart(df_filtered)

    st.markdown("---")
    st.subheader("AI vs Human Performance")
    ai_vs_human_chart(df_filtered)

    st.markdown("---")
    st.subheader("Average Lines Cleared per Player")
    avg_lines_per_player_chart(df_filtered)

    st.markdown("---")
    st.subheader("Score vs Lines Cleared")
    score_vs_lines_scatter(df_filtered)

    st.markdown("---")
    st.subheader("Max Level Reached per Player")
    max_level_per_player_chart(df_filtered)

    st.markdown("---")
    st.subheader("Average Level by Player Type (AI vs Human)")
    avg_level_by_type_chart(df_filtered)


if __name__ == "__main__":
    main()
