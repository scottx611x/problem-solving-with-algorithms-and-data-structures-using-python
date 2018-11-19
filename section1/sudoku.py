
class SudokuGrid:
    BLANK = "X"

    def __init__(self):
        self.grid = [
            [
                [6, self.BLANK, 7],
                [self.BLANK, 1, self.BLANK],
                [self.BLANK, 9, self.BLANK]
            ],
            [
                [4, 1, self.BLANK],
                [3, 9, self.BLANK],
                [6, 2, self.BLANK]
            ],
            [
                [self.BLANK, 9, self.BLANK],
                [6, self.BLANK, self.BLANK],
                [self.BLANK, self.BLANK, 5]
            ],
            [
                [2, self.BLANK, self.BLANK],
                [7, self.BLANK, self.BLANK],
                [self.BLANK, 8, 3]
            ],
            [
                [7, 5, 1],
                [8, 3, 9],
                [2, self.BLANK, self.BLANK]
            ],
            [
                [self.BLANK, 8, 3],
                [self.BLANK, 6, 4],
                [self.BLANK, 5, 1]
            ],
            [
                [1, 7, self.BLANK],
                [self.BLANK, 4, self.BLANK],
                [8, 3, 9]
            ],
            [
                [5, 4, 2],
                [9, 8, self.BLANK],
                [self.BLANK, 7, 6]
            ],
            [
                [self.BLANK, 3, 9],
                [1, 7, self.BLANK],
                [5, 4, self.BLANK]
            ]
        ]

    def get_rows(self):
        rows = [[], [], [], [], [], [], [], [], []]
        offset = 0
        count = 0

        for i in range(len(self.grid)):
            for index, row in enumerate(self.grid[i]):
                rows[index + offset].extend(row)
                count += 1
                if count == 9:
                    count = 0
                    offset += 3
        return rows

    def get_columns(self):
        columns = [[], [], [], [], [], [], [], [], []]
        for i in range(len(self.grid)):
            for row in self.get_rows():
                columns[i].append(row[i])
        return columns

    def get_nonets(self):
        return [sum(nonets, []) for nonets in self.grid[0:9]]


class SudokuSolver(SudokuGrid):
    def solve(self):
        pass

    def _check_okay(self, rows_columns_or_nonets):
        for cleaned in [
            [i for i in j if isinstance(i, int)]
            for j in rows_columns_or_nonets
        ]:
            if sum(cleaned) != 9:
                return False
        else:
            return True

    @property
    def rows_okay(self):
        return self._check_okay(self.get_rows())

    @property
    def columns_okay(self):
        return self._check_okay(self.get_columns())

    @property
    def nonets_okay(self):
        return self._check_okay(self.get_nonets())
