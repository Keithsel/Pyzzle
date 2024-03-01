from nicegui import ui
from sudoku_solver.cv_main import detect_sudoku_board
from sudoku_solver import solve_sudoku
import sys
sys.path.append('backend/sudoku_solver/sudoku_utils')

def handle_upload(file_info):
    file_path = file_info['path']
    unsolved_sudoku = detect_sudoku_board(file_path)
    unsolved_board.label = f'Unsolved Board:\n{unsolved_sudoku}'
    solve_button.set_disabled(False)

def handle_solve():
    solved_sudoku = solve_sudoku(unsolved_board.label.split('\n', 1)[1])
    solved_board.label = f'Solved Board:\n{solved_sudoku}'

with ui.row():
    ui.upload(on_upload=handle_upload)
    solve_button = ui.button('Solve Sudoku', on_click=handle_solve).set_disabled(True)

unsolved_board = ui.label('Unsolved Board:\n')
solved_board = ui.label('Solved Board:\n')

ui.run()
