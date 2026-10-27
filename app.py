"""
================================================================================
CONWAY'S GAME OF LIFE - STREAMLIT WEB APP
================================================================================
Project: Conway's Game of Life Educational Learning Lab
Framework: Streamlit (Pure Python - No HTML, CSS, or JavaScript required)
Grid: 24 x 24 Cells
Interval: 0.5 seconds between generations
Termination: Automatic when static still-life, flip-flop oscillator, or extinction occurs.

HOW TO RUN:
    1. In your terminal (VS Code or GitHub Codespaces):
       pip install streamlit
    2. Run the application:
       streamlit run app.py
    3. Streamlit will launch a local web server (typically at http://localhost:8501)
       and open it in your default browser.
================================================================================
"""

import time
import random
import streamlit as st
from game_engine import GameOfLife

# 1. Page Configuration & Header
st.set_page_config(
    page_title="Conway's Game of Life (24x24)",
    page_icon="🧬",
    layout="centered"
)

st.title("Conway's Game of Life")
st.write(
    """
    **Welcome to Conway's Game of Life!**  
    This is a 24 by 24 cellular automaton governed by 4 pure mathematical rules:
    1. **Underpopulation:** Any live cell with fewer than 2 live neighbors dies.
    2. **Survival:** Any live cell with 2 or 3 live neighbors lives to the next generation.
    3. **Overpopulation:** Any live cell with more than 3 live neighbors dies.
    4. **Reproduction:** Any dead cell with exactly 3 live neighbors becomes a live cell.
    
    Click **Start** to generate a random seed and watch the world evolve!  
    The simulation advances every **0.5s** and will **automatically end** when the grid reaches
    a static state (no changes), a flip-flop / oscillator cycle, or extinction.
    """
)

# 2. Session State Initialization
if "game" not in st.session_state:
    st.session_state.game = GameOfLife(rows=24, cols=24, seed=None, initial_density=0.22)

if "is_running" not in st.session_state:
    st.session_state.is_running = False

if "last_status" not in st.session_state:
    st.session_state.last_status = "Ready to start. Click the button below to generate a new world!"

# 3. User Interface Controls
col1, col2 = st.columns([1, 1])

with col1:
    start_clicked = st.button("▶ Start New Game (Random Seed)", type="primary", use_container_width=True)

with col2:
    stop_clicked = st.button("⏹ Stop Simulation", use_container_width=True)

if start_clicked:
    new_seed = random.randint(1, 999999)
    st.session_state.game.randomize(seed=new_seed, density=0.22)
    st.session_state.is_running = True
    st.session_state.last_status = f"Simulation started with random seed #{new_seed}."

if stop_clicked:
    st.session_state.is_running = False
    st.session_state.last_status = "Simulation paused by user."

# 4. Display Placeholders
grid_placeholder = st.empty()
stats_placeholder = st.empty()
status_placeholder = st.empty()

def render_board(game: GameOfLife) -> str:
    # Render using Unicode square emojis (high contrast without CSS/HTML)
    return game.render_emojis(live_emoji="🟩", dead_emoji="⬛")

# 5. Simulation Loop (0.5s per generation, with auto-stop)
if st.session_state.is_running:
    grid_placeholder.text(render_board(st.session_state.game))
    stats_placeholder.metric(
        label="Current Generation",
        value=st.session_state.game.generation,
        delta=f"{sum(sum(r) for r in st.session_state.game.grid)} live cells"
    )
    status_placeholder.info(st.session_state.last_status)

    while st.session_state.is_running:
        time.sleep(0.5)

        step_result = st.session_state.game.step()
        current_gen = step_result["generation"]
        live_count = step_result["live_cells"]

        grid_placeholder.text(render_board(st.session_state.game))

        stats_placeholder.metric(
            label="Current Generation",
            value=current_gen,
            delta=f"{live_count} live cells (Changed: {step_result['changes']})"
        )

        if step_result["is_terminated"]:
            st.session_state.is_running = False
            reason = step_result["reason"]
            msg = step_result["message"]
            st.session_state.last_status = msg

            if reason == "static":
                status_placeholder.success(f"🏁 **Simulation Completed:** {msg}")
            elif reason == "oscillator":
                status_placeholder.warning(f"🔄 **Simulation Completed:** {msg}")
            elif reason == "extinct":
                status_placeholder.error(f"💀 **Simulation Completed:** {msg}")
            break
        else:
            status_placeholder.caption(f"Simulating generation {current_gen}... (0.5s per step)")

else:
    grid_placeholder.text(render_board(st.session_state.game))
    stats_placeholder.metric(
        label="Current Generation",
        value=st.session_state.game.generation,
        delta=f"{sum(sum(r) for r in st.session_state.game.grid)} live cells"
    )
    status_placeholder.info(st.session_state.last_status)

st.divider()
st.caption("100% Pure Python Streamlit Learning Project · 24x24 Toroidal Grid · Automatic Equilibrium & Flip-Flop Detection")