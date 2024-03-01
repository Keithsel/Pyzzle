from flask import Flask, request, jsonify
from sudoku_solver.cv_main import detect_sudoku_board
from sudoku_solver.sudoku_solver import solve_sudoku

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'path/to/puzzles/sudoku_images'

@app.route('/upload', methods=['POST'])
def upload_file():
    # Uploaded image will be saved in the 'puzzles/sudoku_images' directory and will be passed to the cv_main.py script, which will return the solved sudoku puzzle as a string
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            img_fpath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            sudoku_string = detect_sudoku_board(img_fpath)
            return jsonify(sudoku_string)
        else:
            return jsonify({"error": "No file uploaded"})
    else:
        return jsonify({"error": "Invalid request method"})
    
@app.route('/confirm', methods=['POST'])
    # User will check if the board recognized by the model is correct. If not, they can manually edit the board then confirm the changes.
    # Only return unsolved sudoku puzzle string in this case
def confirm_board():
    if request.method == 'POST':
        sudoku_string = request.json['sudoku_string']
        return jsonify(sudoku_string)
    else:
        return jsonify({"error": "Invalid request method"})
    
@app.route('/solve', methods=['POST'])
    # The string of the unsolved sudoku puzzle will be passed to the sudoku_solver.py script, which will return the solved sudoku puzzle as a string, which will be displayed to the frontend as board with the solution
def solve():
    if request.method == 'POST':
        sudoku_string = request.json['sudoku_string']
        solved_sudoku_string = solve_sudoku(sudoku_string)
        return jsonify(solved_sudoku_string)
    else:
        return jsonify({"error": "Invalid request method"})
    
if __name__ == "__main__":
    app.run(debug=True)

