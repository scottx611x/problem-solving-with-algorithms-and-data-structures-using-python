from pprint import pprint


class SudokuGrid:

    def __init__(self):
        self.grid = [
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

    def update_grid(self, coords, value):
        x, y = coords
        self.grid[x][y] = value
        return self.grid

    def display(self):
        pprint(self.grid)

    def _flatten(self):
        return sum(self.grid, [])

    @property
    def is_full(self):
        return not any([i == 0 for i in self._flatten()])

    def get_columns(self):
        columns = [[], [], [], [], [], [], [], [], []]
        for i in range(len(self.grid)):
            for row in self.grid:
                columns[i].append(row[i])
        return columns

    def get_boxes(self):
        rows_a = self.grid[:3]
        rows_b = self.grid[3:6]
        rows_c = self.grid[6:9]

        boxes = [[]] * 9
        boxes[0] = rows_a[0][:3] + rows_a[1][:3] + rows_a[2][:3]
        boxes[1] = rows_a[0][3:6] + rows_a[1][3:6] + rows_a[2][3:6]
        boxes[2] = rows_a[0][6:9] + rows_a[1][6:9] + rows_a[2][6:9]
        boxes[3] = rows_b[0][:3] + rows_b[1][:3] + rows_b[2][:3]
        boxes[4] = rows_b[0][3:6] + rows_b[1][3:6] + rows_b[2][3:6]
        boxes[5] = rows_b[0][6:9] + rows_b[1][6:9] + rows_b[2][6:9]
        boxes[6] = rows_c[0][:3] + rows_c[1][:3] + rows_c[2][:3]
        boxes[7] = rows_c[0][3:6] + rows_c[1][3:6] + rows_c[2][3:6]
        boxes[8] = rows_c[0][6:9] + rows_c[1][6:9] + rows_c[2][6:9]

        return boxes

    def _get_coordinate_list(self):
        grid_length = len(self.grid)
        r = range(grid_length)
        a = [i for i in range(3)] * grid_length
        b = [i for i in range(3, 6)] * grid_length
        c = [i for i in range(6, grid_length)] * grid_length
        x_coords = a + b + c
        y_coords = sorted(list(r) * 3) * 3

        def get_chunks(l, chunk_size=grid_length):
            """Yield successive n-sized chunks from a list."""
            for i in range(0, len(l), chunk_size):
                yield l[i:i + chunk_size]

        return list(get_chunks(list(zip(x_coords, y_coords))))

    def get_box_from_coords(self, coords):
        box_index_to_coords_map = {
            i: coord_list
            for i, coord_list in enumerate(self._get_coordinate_list())
        }

        for box_index, coords_in_box in box_index_to_coords_map.items():
            if coords in coords_in_box:
                return self.get_boxes()[box_index]

    def get_peers(self, coords):
        i, j = coords
        return set(
            self.grid[i] + self.get_columns()[j] +
            self.get_box_from_coords(coords)
        )

    def get_grid_value(self, coords):
        i, j = coords
        return self.grid[i][j]

    def get_possible_entries(self, coords):
        value = self.get_grid_value(coords)

        if not value == 0:
            return []

        possible_entries = list(range(1, 10))

        for square in self.get_peers(coords):
            if square in possible_entries:
                possible_entries.remove(square)

        return possible_entries

    def get_square_with_least_possibilities(self):
        least_possible_entries = None
        coords = None
        for x in range(9):
            for y in range(9):
                possible_entries = self.get_possible_entries((x, y))
                if possible_entries:
                    if least_possible_entries is None:
                        coords = (x, y)
                        least_possible_entries = possible_entries
                    else:
                        if len(possible_entries) < len(least_possible_entries):
                            coords = (x, y)
                            least_possible_entries = possible_entries
        return coords, least_possible_entries


class SudokuSolver(SudokuGrid):

    def solve(self):
        if self.is_solved():
            print("Sudoku Solved!")
            self.display()
            return self.grid

        coords, possible_entries = self.get_square_with_least_possibilities()
        x, y = coords
        if len(possible_entries) == 1:
            self.update_grid((x, y), possible_entries[0])
            return self.solve()
        else:
            for possible_entry in possible_entries:
                self.update_grid((x, y), possible_entry)
                return self.solve()
            self.update_grid((x, y), 0)

    def _check_okay(self, rows_columns_or_boxes):
        for i in rows_columns_or_boxes:
            if sum(i) != 45:
                return False
        else:
            return True

    @property
    def rows_okay(self):
        return self._check_okay(self.grid)

    @property
    def columns_okay(self):
        return self._check_okay(self.get_columns())

    @property
    def boxes_okay(self):
        return self._check_okay(self.get_boxes())

    def is_solved(self):
        return all(
            [self.is_full, self.rows_okay, self.columns_okay, self.boxes_okay]
        )
