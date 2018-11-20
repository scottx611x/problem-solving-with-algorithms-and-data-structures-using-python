from unittest import TestCase

from section1.sudoku import SudokuGrid, SudokuSolver
from section1.utils import captured_output


class SudokuGridTests(TestCase):
    def setUp(self):
        self.sudoku_grid = SudokuGrid()

    def test_get_columns(self):
        self.assertEqual(
            self.sudoku_grid.get_columns(),
            [
                [6, 0, 0, 2, 7, 0, 1, 0, 8],
                [0, 1, 9, 0, 0, 8, 7, 4, 3],
                [7, 0, 0, 0, 0, 3, 0, 0, 9],
                [4, 3, 6, 7, 8, 2, 5, 9, 0],
                [1, 9, 2, 5, 3, 0, 4, 8, 7],
                [0, 0, 0, 1, 9, 0, 2, 0, 6],
                [0, 6, 0, 0, 0, 0, 0, 1, 5],
                [9, 0, 0, 8, 6, 5, 3, 7, 4],
                [0, 0, 5, 3, 4, 1, 9, 0, 0]
            ]
        )

    def test_get_grid(self):
        self.assertEqual(
            self.sudoku_grid.grid,
            [
                [6, 0, 7, 4, 1, 0, 0, 9, 0],
                [0, 1, 0, 3, 9, 0, 6, 0, 0],
                [0, 9, 0, 6, 2, 0, 0, 0, 5],
                [2, 0, 0, 7, 5, 1, 0, 8, 3],
                [7, 0, 0, 8, 3, 9, 0, 6, 4],
                [0, 8, 3, 2, 0, 0, 0, 5, 1],
                [1, 7, 0, 5, 4, 2, 0, 3, 9],
                [0, 4, 0, 9, 8, 0, 1, 7, 0],
                [8, 3, 9, 0, 7, 6, 5, 4, 0]
            ]
        )

    def test_get_boxes(self):
        self.assertEqual(
            self.sudoku_grid.get_boxes(),
            [
                [6, 0, 7, 0, 1, 0, 0, 9, 0],
                [4, 1, 0, 3, 9, 0, 6, 2, 0],
                [0, 9, 0, 6, 0, 0, 0, 0, 5],
                [2, 0, 0, 7, 0, 0, 0, 8, 3],
                [7, 5, 1, 8, 3, 9, 2, 0, 0],
                [0, 8, 3, 0, 6, 4, 0, 5, 1],
                [1, 7, 0, 0, 4, 0, 8, 3, 9],
                [5, 4, 2, 9, 8, 0, 0, 7, 6],
                [0, 3, 9, 1, 7, 0, 5, 4, 0]
            ]
        )

    def test_get_box_from_coords(self):
        self.assertEqual(
            self.sudoku_grid.get_box_from_coords((1, 1)),
            self.sudoku_grid.get_boxes()[0]
        )
        self.assertEqual(
            self.sudoku_grid.get_box_from_coords((1, 4)),
            self.sudoku_grid.get_boxes()[1]
        )
        self.assertEqual(
            self.sudoku_grid.get_box_from_coords((1, 7)),
            self.sudoku_grid.get_boxes()[2]
        )
        self.assertEqual(
            self.sudoku_grid.get_box_from_coords((4, 1)),
            self.sudoku_grid.get_boxes()[3]
        )
        self.assertEqual(
            self.sudoku_grid.get_box_from_coords((4, 4)),
            self.sudoku_grid.get_boxes()[4]
        )
        self.assertEqual(
            self.sudoku_grid.get_box_from_coords((4, 7)),
            self.sudoku_grid.get_boxes()[5]
        )
        self.assertEqual(
            self.sudoku_grid.get_box_from_coords((7, 1)),
            self.sudoku_grid.get_boxes()[6]
        )
        self.assertEqual(
            self.sudoku_grid.get_box_from_coords((7, 4)),
            self.sudoku_grid.get_boxes()[7]
        )
        self.assertEqual(
            self.sudoku_grid.get_box_from_coords((7, 7)),
            self.sudoku_grid.get_boxes()[8]
        )

    def test_is_full(self):
        self.assertFalse(self.sudoku_grid.is_full)

    def test_get_possible_entries(self):
        self.assertEqual(
            self.sudoku_grid.get_possible_entries((0, 1)),
            [2, 5]
        )
        self.assertEqual(
            self.sudoku_grid.get_possible_entries((3, 1)),
            [6]
        )
        self.assertEqual(
            self.sudoku_grid.get_possible_entries((0, 8)),
            [2, 8]
        )

    def test_display_grid(self):
        with captured_output() as output:
            self.sudoku_grid.display()
        self.assertEqual("""[[6, 0, 7, 4, 1, 0, 0, 9, 0],
 [0, 1, 0, 3, 9, 0, 6, 0, 0],
 [0, 9, 0, 6, 2, 0, 0, 0, 5],
 [2, 0, 0, 7, 5, 1, 0, 8, 3],
 [7, 0, 0, 8, 3, 9, 0, 6, 4],
 [0, 8, 3, 2, 0, 0, 0, 5, 1],
 [1, 7, 0, 5, 4, 2, 0, 3, 9],
 [0, 4, 0, 9, 8, 0, 1, 7, 0],
 [8, 3, 9, 0, 7, 6, 5, 4, 0]]
""", output.getvalue())


class SudokuSolverTests(TestCase):
    def setUp(self):
        self.sudoku_solver = SudokuSolver()

    def test_rows_okay(self):
        self.assertFalse(self.sudoku_solver.rows_okay)

    def test_columns_okay(self):
        self.assertFalse(self.sudoku_solver.columns_okay)

    def test_boxes_okay(self):
        self.assertFalse(self.sudoku_solver.boxes_okay)

    def test_solve(self):
        with captured_output() as output:
            self.sudoku_solver.solve()
        self.assertEqual("""Sudoku Solved!
[[6, 2, 7, 4, 1, 5, 3, 9, 8],
 [4, 1, 5, 3, 9, 8, 6, 2, 7],
 [3, 9, 8, 6, 2, 7, 4, 1, 5],
 [2, 6, 4, 7, 5, 1, 9, 8, 3],
 [7, 5, 1, 8, 3, 9, 2, 6, 4],
 [9, 8, 3, 2, 6, 4, 7, 5, 1],
 [1, 7, 6, 5, 4, 2, 8, 3, 9],
 [5, 4, 2, 9, 8, 3, 1, 7, 6],
 [8, 3, 9, 1, 7, 6, 5, 4, 2]]
""", output.getvalue())