import numpy as np
import time

class SudokuSolver:
    def __init__(self, board):
        self.board = np.zeros((9, 9), dtype=int)
        self.rows = [set(range(1, 10)) for _ in range(9)]
        self.columns = [set(range(1, 10)) for _ in range(9)]
        self.blocks = [set(range(1, 10)) for _ in range(9)]
        self.valid = self.initialize_board(board)

    def validate_character(self, char):
        return char in "1234567890.-_"

    def validate_and_parse_board(self, board):
        if len(board) != 81 or not all(self.validate_character(char) for char in board):
            return False
        for i in range(81):
            row, col = divmod(i, 9)
            char = board[i]
            if char in "123456789":
                num = int(char)
                if not self.is_safe(num, row, col):
                    return False
                self.place_number(num, row, col)
        return True

    def initialize_board(self, board):
        return self.validate_and_parse_board(board)

    def place_number(self, num, row, col):
        block_index = (row // 3) * 3 + col // 3
        self.rows[row].remove(num)
        self.columns[col].remove(num)
        self.blocks[block_index].remove(num)
        self.board[row, col] = num

    def remove_number(self, num, row, col):
        block_index = (row // 3) * 3 + col // 3
        self.rows[row].add(num)
        self.columns[col].add(num)
        self.blocks[block_index].add(num)
        self.board[row, col] = 0

    def is_safe(self, num, row, col):
        block_index = (row // 3) * 3 + col // 3
        return (num in self.rows[row] and num in self.columns[col] and num in self.blocks[block_index])

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i, j] == 0:
                    return i, j
        return -1, -1

    def solve(self):
        if not self.valid:
            return False
        row, col = self.find_empty_cell()
        if row == -1:
            return True
        possible_numbers = self.get_possible_numbers(row, col)
        sorted_numbers = sorted(possible_numbers, key=lambda num: self.get_remaining_values(num, row, col))
        for num in sorted_numbers:
            self.place_number(num, row, col)
            if self.solve():
                return True
            self.remove_number(num, row, col)
        return False

    def get_possible_numbers(self, row, col):
        block_index = (row // 3) * 3 + col // 3
        return list(self.rows[row] & self.columns[col] & self.blocks[block_index])

    def get_remaining_values(self, num, row, col):
        remaining_values = 0
        if num not in self.rows[row] or num not in self.columns[col]:
            return remaining_values
        for i in range(9):
            if i != col and num in self.columns[i]:
                remaining_values += 1
        for j in range(9):
            if j != row and num in self.rows[j]:
                remaining_values += 1
        block_start_row = (row // 3) * 3
        block_start_col = (col // 3) * 3
        for i in range(block_start_row, block_start_row + 3):
            for j in range(block_start_col, block_start_col + 3):
                if i != row and j != col and num in self.rows[i] and num in self.columns[j]:
                    remaining_values += 1
        return remaining_values

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else "." for num in row))


def solve_sudoku(puzzle_string):
    solver = SudokuSolver(puzzle_string)
    if solver.solve():
        solver.print_board()
    else:
        print("No solution exists or invalid puzzle.")


start = time.time()
puzzle_string = "700000400020070080003008009000500300060020090001007006000300900030040060009001035"
solve_sudoku(puzzle_string)
end = time.time()
print(f"Time taken: {end - start:.5f} seconds")
