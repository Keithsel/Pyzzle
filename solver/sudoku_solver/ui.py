import tkinter as tk
from tkinter import filedialog
import argparse
import cv_main as cv
import sudoku_solver as solver

class UploadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Upload Sudoku Image")
        label.pack(pady=10, padx=10)

        upload_button = tk.Button(self, text="Upload Image",
                                  command=self.upload_image)
        upload_button.pack()

    def upload_image(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                              title = "Select an Image",
                                              filetypes = (("JPG Files", "*.jpg"),
                                                           ("PNG Files", "*.png"),
                                                           ("All Files", "*.*")))
        
        ap = argparse.ArgumentParser()
        ap.add_argument("--img_fpath", default=filename, type=str, help="Path to sudoku image file")
        ap.add_argument("--model_fpath", default="solver/sudoku_solver/models/model.keras", type=str, help="Path to saved Keras CNN model")
        args = vars(ap.parse_args())
        sudoku_string = cv.detect_sudoku_board(args)

        return sudoku_string

        self.controller.process_image_and_show(filename, ConfirmationPage)

class ConfirmationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Confirm Sudoku Board")
        label.pack(pady=10, padx=10)

    def display_board(self, board_string):
        self.board_frame = tk.Frame(self)
        self.board_frame.pack(pady=10, padx=10)

        for row in range(9):
            for col in range(9):
                cell_value = board_string[row * 9 + col]
                cell = tk.Label(self.board_frame, text=cell_value, 
                                width=2, height=1, borderwidth=1, relief="groove")
                cell.grid(row=row, column=col)  

        confirm_button = tk.Button(self, text="Solve",
                                   command=self.solve_sudoku)
        confirm_button.pack()

    def display_board(self, board_string):
        # ... (Previous code for creating the board_frame) ...

        self.cells = []  # Store references to the cells
        for row in range(9):
            row_cells = []
            for col in range(9):
                cell_value = board_string[row * 9 + col]
                cell = tk.Entry(self.board_frame, text=cell_value, 
                                width=2, justify="center")  # Using Entry for editing
                cell.grid(row=row, column=col)
                row_cells.append(cell)
            self.cells.append(row_cells)

        edit_button = tk.Button(self, text="Edit", command=self.toggle_edit_mode)  
        edit_button.pack()

    def toggle_edit_mode(self):
        for row in self.cells:
            for cell in row:
                cell.config(state="normal" if cell.cget('state') == "disabled" else "disabled")

    def get_board_string(self):
        board_string = ""
        for row in self.cells:
            for cell in row:
                board_string += cell.get() or '0'  # Handle empty cells
        return board_string

    def solve_sudoku(self):
        # Get board string from display
        # Call your Sudoku solver
        # Pass the solved board to the SolvedPage
        self.controller.process_image_and_show(None, SolvedPage)

class SolvedPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Solved Sudoku")
        label.pack(pady=10, padx=10)

        # Add display for the solved board here

class SudokuSolverApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sudoku Solver")

        self.container = tk.Frame(self.window)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (UploadPage, ConfirmationPage, SolvedPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(UploadPage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

    def process_image_and_show(self, filename, next_page):
        if filename:
            # Process the image and get the board string
            board_string = "000300000004000285081002000800000592000000700006009003040730009090800000020905107"
            # Show the next page with the board string
            

        self.show_frame(next_page)

if __name__ == "__main__":
    app = SudokuSolverApp()
    app.window.mainloop()
