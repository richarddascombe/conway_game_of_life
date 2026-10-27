# Conway's Game of Life — 24x24 Educational Simulation

An educational, 100% pure Python implementation of John Horton Conway's Game of Life (1970).
Designed for students and developers learning cellular automata, modular software architecture,
and Streamlit, with turnkey support for VS Code, GitHub Codespaces, Docker, and Google Colab.

## The Four Transition Rules
1. Underpopulation: Live cell with < 2 live neighbors dies.
2. Survival: Live cell with 2 or 3 live neighbors lives on.
3. Overpopulation: Live cell with > 3 live neighbors dies.
4. Reproduction: Dead cell with == 3 live neighbors becomes alive.

## How to Run in VS Code
1. pip install -r requirements.txt
2. streamlit run app.py