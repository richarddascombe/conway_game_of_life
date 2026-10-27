"""
================================================================================
UNIT TESTS FOR CONWAY'S GAME OF LIFE ENGINE
================================================================================
Run with:
    python3 -m unittest test_game.py -v
================================================================================
"""

import unittest
from game_engine import GameOfLife

class TestGameOfLife(unittest.TestCase):
    def test_initialization_24x24(self):
        game = GameOfLife(rows=24, cols=24, seed=123)
        self.assertEqual(len(game.grid), 24)
        self.assertEqual(len(game.grid[0]), 24)
        self.assertEqual(game.generation, 0)
        self.assertGreater(sum(sum(row) for row in game.grid), 0)

    def test_static_still_life_block(self):
        game = GameOfLife(rows=24, cols=24)
        game.load_pattern('block', start_r=10, start_c=10)
        result = game.step()
        self.assertTrue(result['is_terminated'])
        self.assertEqual(result['reason'], 'static')
        self.assertEqual(result['period'], 1)

    def test_flip_flop_blinker_oscillator(self):
        game = GameOfLife(rows=24, cols=24)
        game.load_pattern('blinker', start_r=10, start_c=10)
        result1 = game.step()
        self.assertFalse(result1['is_terminated'])
        result2 = game.step()
        self.assertTrue(result2['is_terminated'])
        self.assertEqual(result2['reason'], 'oscillator')
        self.assertEqual(result2['period'], 2)

if __name__ == '__main__':
    unittest.main()