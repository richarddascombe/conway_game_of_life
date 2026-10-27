"""
CONWAY'S GAME OF LIFE - GOOGLE COLAB STANDALONE RUNNER
Paste this entire script into a single Google Colab cell and press Shift+Enter!
"""

import time
import random
from IPython.display import clear_output

class GameOfLife:
    def __init__(self, rows=24, cols=24, seed=None, density=0.22):
        self.rows, self.cols, self.generation = rows, cols, 0
        self.history = []
        if seed: random.seed(seed)
        self.grid = [[1 if random.random() < density else 0 for _ in range(cols)] for _ in range(rows)]
        self.history.append(tuple(tuple(r) for r in self.grid))

    def count_neighbors(self, r, c):
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0: continue
                count += self.grid[(r + dr) % self.rows][(c + dc) % self.cols]
        return count

    def step(self):
        nxt = [[0]*self.cols for _ in range(self.rows)]
        changes, live = 0, 0
        for r in range(self.rows):
            for c in range(self.cols):
                n = self.count_neighbors(r, c)
                curr = self.grid[r][c]
                val = 1 if (curr == 1 and n in (2,3)) or (curr == 0 and n == 3) else 0
                nxt[r][c] = val
                if val: live += 1
                if val != curr: changes += 1
        self.grid, self.generation = nxt, self.generation + 1
        snap = tuple(tuple(r) for r in self.grid)
        if live == 0: return {'term': True, 'msg': 'Extinction (all dead)'}
        if changes == 0: return {'term': True, 'msg': 'Static Equilibrium (still-life)'}
        for i in range(len(self.history)-1, -1, -1):
            if snap == self.history[i]:
                return {'term': True, 'msg': f'Flip-Flop / Oscillator (Period {len(self.history)-i})'}
        self.history.append(snap)
        if len(self.history) > 16: self.history.pop(0)
        return {'term': False, 'live': live}

    def render(self):
        return "\n".join("".join("🟩" if c else "⬛" for c in row) for row in self.grid)

seed = random.randint(1000, 999999)
game = GameOfLife(24, 24, seed=seed)
while True:
    clear_output(wait=True)
    print(f"=== CONWAY'S GAME OF LIFE (24x24) | Seed: {seed} ===")
    print(game.render())
    print(f"\nCurrent Generation: {game.generation}")
    time.sleep(0.5)
    res = game.step()
    if res['term']:
        clear_output(wait=True)
        print(f"=== SIMULATION FINISHED ===")
        print(game.render())
        print(f"\nCurrent Generation: {game.generation}")
        print(f"Reason: {res['msg']}")
        break