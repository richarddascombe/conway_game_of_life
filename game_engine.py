"""
================================================================================
CONWAY'S GAME OF LIFE - CORE ENGINE MODULE
================================================================================
Author: Educational Project for Conway's Game of Life
Language: 100% Pure Python (Standard Library Only - No C extensions required)
Grid Size: 24 x 24 Toroidal Cellular Automaton
================================================================================
"""

import random
from typing import List, Tuple, Optional, Dict

class GameOfLife:
    def __init__(self, rows: int = 24, cols: int = 24, seed: Optional[int] = None, initial_density: float = 0.20):
        self.rows: int = rows
        self.cols: int = cols
        self.generation: int = 0
        self.max_history: int = 16
        self.history: List[Tuple[Tuple[int, ...], ...]] = []
        self.grid: List[List[int]] = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.randomize(seed=seed, density=initial_density)

    def randomize(self, seed: Optional[int] = None, density: float = 0.20) -> None:
        if seed is not None:
            random.seed(seed)
        self.generation = 0
        self.history.clear()
        self.grid = [
            [1 if random.random() < density else 0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]
        self.history.append(self.get_state_tuple())

    def clear(self) -> None:
        self.generation = 0
        self.history.clear()
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_state_tuple(self) -> Tuple[Tuple[int, ...], ...]:
        return tuple(tuple(row) for row in self.grid)

    def count_neighbors(self, r: int, c: int, wrap: bool = True) -> int:
        count = 0
        offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)
        ]
        for dr, dc in offsets:
            nr = r + dr
            nc = c + dc
            if wrap:
                nr = nr % self.rows
                nc = nc % self.cols
                count += self.grid[nr][nc]
            else:
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    count += self.grid[nr][nc]
        return count

    def step(self) -> Dict[str, any]:
        next_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        changes = 0
        live_count = 0

        for r in range(self.rows):
            for c in range(self.cols):
                current_state = self.grid[r][c]
                neighbors = self.count_neighbors(r, c, wrap=True)

                if current_state == 1:
                    next_state = 1 if neighbors in (2, 3) else 0
                else:
                    next_state = 1 if neighbors == 3 else 0

                next_grid[r][c] = next_state
                if next_state == 1:
                    live_count += 1
                if next_state != current_state:
                    changes += 1

        self.grid = next_grid
        self.generation += 1

        current_snapshot = self.get_state_tuple()
        termination_info = self._check_termination(current_snapshot, live_count, changes)

        self.history.append(current_snapshot)
        if len(self.history) > self.max_history:
            self.history.pop(0)

        return {
            'generation': self.generation,
            'live_cells': live_count,
            'changes': changes,
            'is_terminated': termination_info['is_terminated'],
            'reason': termination_info['reason'],
            'period': termination_info['period'],
            'message': termination_info['message']
        }

    def _check_termination(self, current_snapshot, live_count: int, changes: int) -> Dict[str, any]:
        if live_count == 0:
            return {'is_terminated': True, 'reason': 'extinct', 'period': 0, 'message': f"Extinction: All cells died at Gen {self.generation}."}
        if changes == 0:
            return {'is_terminated': True, 'reason': 'static', 'period': 1, 'message': f"Static Equilibrium: No cells changed at Gen {self.generation}."}
        for i in range(len(self.history) - 1, -1, -1):
            if current_snapshot == self.history[i]:
                period = len(self.history) - i
                reason_label = "Flip-Flop (Period 2)" if period == 2 else f"Oscillator (Period {period})"
                return {'is_terminated': True, 'reason': 'oscillator', 'period': period, 'message': f"{reason_label} detected from {period} gens ago."}
        return {'is_terminated': False, 'reason': 'running', 'period': None, 'message': f"Generation {self.generation} running."}

    def render_emojis(self, live_emoji: str = "🟩", dead_emoji: str = "⬛") -> str:
        return "\n".join("".join(live_emoji if cell == 1 else dead_emoji for cell in row) for row in self.grid)

    def load_pattern(self, pattern_name: str, start_r: int = 10, start_c: int = 10) -> None:
        self.clear()
        patterns = {
            'blinker': [(0, 0), (0, 1), (0, 2)],
            'toad': [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)],
            'beacon': [(0, 0), (0, 1), (1, 0), (2, 3), (3, 2), (3, 3)],
            'block': [(0, 0), (0, 1), (1, 0), (1, 1)],
            'beehive': [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)],
            'glider': [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        }
        pattern = patterns.get(pattern_name.lower())
        if pattern:
            for dr, dc in pattern:
                r = (start_r + dr) % self.rows
                c = (start_c + dc) % self.cols
                self.grid[r][c] = 1
        self.history.append(self.get_state_tuple())