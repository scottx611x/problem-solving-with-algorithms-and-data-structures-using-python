from unittest import TestCase

from section1.sudoku import SudokuGrid, SudokuSolver


class SudokuGridTests(TestCase):
    def setUp(self):
        self.sudoku_grid = SudokuGrid()

    def test_get_columns(self):
        self.assertEqual(
            self.sudoku_grid.get_columns(),
            [
                [6, 'X', 'X', 2, 7, 'X', 1, 'X', 8],
                ['X', 1, 9, 'X', 'X', 8, 7, 4, 3],
                [7, 'X', 'X', 'X', 'X', 3, 'X', 'X', 9],
                [4, 3, 6, 7, 8, 2, 5, 9, 'X'],
                [1, 9, 2, 5, 3, 'X', 4, 8, 7],
                ['X', 'X', 'X', 1, 9, 'X', 2, 'X', 6],
                ['X', 6, 'X', 'X', 'X', 'X', 'X', 1, 5],
                [9, 'X', 'X', 8, 6, 5, 3, 7, 4],
                ['X', 'X', 5, 3, 4, 1, 9, 'X', 'X']
            ]
        )

    def test_get_rows(self):
        self.assertEqual(
            self.sudoku_grid.get_rows(),
            [
                [6, 'X', 7, 4, 1, 'X', 'X', 9, 'X'],
                ['X', 1, 'X', 3, 9, 'X', 6, 'X', 'X'],
                ['X', 9, 'X', 6, 2, 'X', 'X', 'X', 5],
                [2, 'X', 'X', 7, 5, 1, 'X', 8, 3],
                [7, 'X', 'X', 8, 3, 9, 'X', 6, 4],
                ['X', 8, 3, 2, 'X', 'X', 'X', 5, 1],
                [1, 7, 'X', 5, 4, 2, 'X', 3, 9],
                ['X', 4, 'X', 9, 8, 'X', 1, 7, 'X'],
                [8, 3, 9, 'X', 7, 6, 5, 4, 'X']
            ]
        )

    def test_get_nonets(self):
        self.assertEqual(
            self.sudoku_grid.get_nonets(),
            [
                [6, 'X', 7, 'X', 1, 'X', 'X', 9, 'X'],
                [4, 1, 'X', 3, 9, 'X', 6, 2, 'X'],
                ['X', 9, 'X', 6, 'X', 'X', 'X', 'X', 5],
                [2, 'X', 'X', 7, 'X', 'X', 'X', 8, 3],
                [7, 5, 1, 8, 3, 9, 2, 'X', 'X'],
                ['X', 8, 3, 'X', 6, 4, 'X', 5, 1],
                [1, 7, 'X', 'X', 4, 'X', 8, 3, 9],
                [5, 4, 2, 9, 8, 'X', 'X', 7, 6],
                ['X', 3, 9, 1, 7, 'X', 5, 4, 'X']
            ]
        )

class SudokuSolverTests(TestCase):
    def setUp(self):
        self.sudoku_solver = SudokuSolver()

    def test_rows_okay(self):
        self.assertFalse(self.sudoku_solver.rows_okay)

    def test_columns_okay(self):
        self.assertFalse(self.sudoku_solver.columns_okay)

    def test_nonets_okay(self):
        self.assertFalse(self.sudoku_solver.nonets_okay)

    def test_solve(self):
        self.assertEqual(
            self.sudoku_solver.solve(),
            "IMPLEMENT THE EXACT COVER/ DANCING LINKS ALGORITHM"
            "https://en.wikipedia.org/wiki/Exact_cover#Detailed_example"
        )