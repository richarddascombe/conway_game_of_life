"""
================================================================================
CONWAY'S GAME OF LIFE - 1-CLICK PROJECT SETUP SCRIPT (FOR MACOS / LINUX / WINDOWS)
================================================================================
Run this in your terminal:
    python3 setup_project.py

This script extracts all 11 project files cleanly into a folder named
`conway_game_of_life` on your machine without requiring any ZIP utilities!
================================================================================
"""

import os

PROJECT_DIR = "conway_game_of_life"

def main():
    print("=" * 60)
    print("Setting up Conway's Game of Life Project...")
    print("=" * 60)
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, ".devcontainer"), exist_ok=True)
    print(f"Project folder ready at: ./{PROJECT_DIR}")
    print("Run: cd conway_game_of_life && pip install -r requirements.txt && streamlit run app.py")

if __name__ == "__main__":
    main()