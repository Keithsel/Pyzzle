import time
from cv_main import *
class SudokuSolver:
    def __init__(self, board):
        self.board = [[0] * 9 for _ in range(9)]
        self.rows = [set(range(1, 10)) for _ in range(9)]
        self.columns = [set(range(1, 10)) for _ in range(9)]
        self.blocks = [set(range(1, 10)) for _ in range(9)]
        self.empty_cells = []  # Stack for backtracking
        self.valid = self.initialize_board(board)  # Valid flag

    def validate_character(self, char):
        return char in '1234567890.-_'

    def validate_and_parse_board(self, board):
        if len(board) != 81 or not all(self.validate_character(char) for char in board):
            return False
        for i in range(81):
            row, col = divmod(i, 9)
            char = board[i]
            if char in '123456789':
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
        self.board[row][col] = num

    def remove_number(self, num, row, col):
        block_index = (row // 3) * 3 + col // 3
        self.rows[row].add(num)
        self.columns[col].add(num)
        self.blocks[block_index].add(num)
        self.board[row][col] = 0

    def is_safe(self, num, row, col):
        block_index = (row // 3) * 3 + col // 3
        return (num in self.rows[row] and num in self.columns[col] and num in self.blocks[block_index])

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return -1, -1

    def solve(self):
        if not self.valid:
            return False  # Invalid board configuration

        row, col = self.find_empty_cell()
        if row == -1:  # No empty cell found, puzzle solved
            return True

        for num in sorted(self.rows[row] & self.columns[col] & self.blocks[(row // 3) * 3 + col // 3]):
                self.place_number(num, row, col)
                if self.solve():
                    return True
                self.remove_number(num, row, col)  # Backtrack

        return False

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else '.' for num in row))

def solve_sudoku(puzzle_string):
    solver = SudokuSolver(puzzle_string)
    if solver.solve():
        solver.print_board()
    else:
        print("No solution exists or invalid puzzle.")


start = time.time()
if __name__ == "__main__":
    start = time.time()
    # Construct an argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--img_fpath", default="sudoku_images\8.jpg", type=str, help="Path to sudoku image file")
    ap.add_argument("--model_fpath", default="models\model.keras", type=str, help="Path to saved Keras CNN model")
    args = vars(ap.parse_args())
    sudoku_string = solve_sudoku_puzzle(args)
    solve_sudoku(sudoku_string)
    end = time.time()
    print(f"Execution time: {end - start:.5f} seconds.")
    plt.show()
