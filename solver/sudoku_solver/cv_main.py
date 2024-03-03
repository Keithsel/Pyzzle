import cv2
import os
import tensorflow as tf
import sys
sys.path.append('solver/sudoku_solver/sudoku_utils')
import sudoku_utils as sutils

def detect_sudoku_board(img_fpath='puzzles/sudoku_images/1.jpg', model_fpath='solver\sudoku_solver\models\model.keras'):
    if not os.path.exists(img_fpath):
        raise FileNotFoundError(f"File not found: '{img_fpath}'")
    
    img = cv2.imread(img_fpath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = sutils.resize_and_maintain_aspect_ratio(input_image=img, new_width=1000)

    # Load the trained model
    loaded_model = tf.keras.models.load_model(model_fpath)

    # Locate grid cells in the image and predict the Sudoku grid
    cells, M, board_image = sutils.get_valid_cells_from_image(img)
    grid_array = sutils.get_predicted_sudoku_grid(loaded_model, cells)

    # Convert the 2D array of the puzzle grid to a string
    sudoku_string = ''.join(''.join(map(str, row)) for row in grid_array)
    return grid_array, sudoku_string

if __name__ == "__main__":
    print(detect_sudoku_board())