import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sv_ttk
import threading
from PIL import Image
import os
import time

from sudoku_solver import SudokuSolver
from cv_main import detect_sudoku_board

# Base class for all pages
class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

# Page for uploading and recognizing Sudoku image
class UploadPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # UI setup
        tk.Label(self, text="Upload Sudoku Image", font=('Helvetica', 20)).pack(pady=20)
        self.upload_status = tk.Label(self, text="", font=('Helvetica', 16))
        self.upload_status.pack()
        self.upload_button = tk.Button(self, text="Upload Image", font=('Helvetica', 16), command=self.upload_image)
        self.upload_button.pack()
        self.recognize_button = tk.Button(self, text="Recognize Board", font=('Helvetica', 16), state=tk.DISABLED, command=self.recognize_board)
        self.recognize_button.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                with Image.open(file_path) as img:
                    if img.width < 100 or img.height < 100 or img.width > 5000 or img.height > 5000:
                        raise ValueError("Image size must be between 100x100 and 5000x5000 pixels.")

                target_directory = "puzzles/sudoku_images"
                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)
                target_path = os.path.join(target_directory, os.path.basename(file_path))

                with Image.open(file_path) as img:
                    img.save(target_path)
                self.upload_status.config(text=f"Image saved to {os.path.normpath(target_path)}")

            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
                self.upload_image()
            except Exception as e:
                messagebox.showerror("Error", "Failed to upload image. Please try again.")
                print(f"Error uploading image: {e}")
                self.upload_image()

            self.uploaded_image_path = file_path
            messagebox.showinfo("Success", "Image uploaded successfully. You can now recognize the board.")
            self.recognize_button['state'] = tk.NORMAL

    def recognize_board(self):
        board, board_string = detect_sudoku_board(self.uploaded_image_path, 'solver\sudoku_solver\models\model.keras')
        self.controller.show_frame(EditPage, board_string, board)
        print(board)

# Page for editing and solving Sudoku board
class EditPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # UI setup
        tk.Label(self, text="Edit Sudoku Board", font=('Helvetica', 20)).pack(pady=20)
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(pady=20)
        self.progress_label = tk.Label(self, text="", font=('Helvetica', 16))
        self.progress_label.pack()
        self.edit_mode = False
        self.toggle_edit_button = tk.Button(self, text="Edit mode: Off", font=('Helvetica', 16), command=self.toggle_edit_mode)
        self.toggle_edit_button.pack(pady=20)
        tk.Button(self, text="Solve", font=('Helvetica', 16), command=self.solve_board).pack()

        self.board_string = ""
        self.entries = []

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.update_editability()
        self.toggle_edit_button.config(text=f"Edit mode: {'On' if self.edit_mode else 'Off'}")

    def display_board(self, board_array):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.entries = []

        for i, row in enumerate(board_array):
            row_entries = []
            for j, num in enumerate(row):
                entry = tk.Entry(self.grid_frame, width=2, font=('Helvetica', 20), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, num if num != 0 else "")
                entry.config(state=tk.NORMAL if self.edit_mode else tk.DISABLED)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def update_editability(self):
        for row in self.entries:
            for entry in row:
                entry.config(state=tk.NORMAL if self.edit_mode else tk.DISABLED)

    def set_board(self, board_string, board_array):
        self.board_string = board_string
        self.display_board(board_array)
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # UI setup
        tk.Label(self, text="Upload Sudoku Image").pack(pady=10)
        self.upload_status = tk.Label(self, text="")
        self.upload_status.pack()
        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()
        self.recognize_button = tk.Button(self, text="Recognize Board", state=tk.DISABLED, command=self.recognize_board)
        self.recognize_button.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                with Image.open(file_path) as img:
                    if img.width < 100 or img.height < 100 or img.width > 5000 or img.height > 5000:
                        raise ValueError("Image size must be between 100x100 and 5000x5000 pixels.")

                target_directory = "puzzles/sudoku_images"
                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)
                target_path = os.path.join(target_directory, os.path.basename(file_path))

                with Image.open(file_path) as img:
                    img.save(target_path)
                self.upload_status.config(text=f"Image saved to {os.path.normpath(target_path)}")

            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
                self.upload_image()
            except Exception as e:
                messagebox.showerror("Error", "Failed to upload image. Please try again.")
                print(f"Error uploading image: {e}")
                self.upload_image()

            self.uploaded_image_path = file_path
            messagebox.showinfo("Success", "Image uploaded successfully. You can now recognize the board.")
            self.recognize_button['state'] = tk.NORMAL

    def recognize_board(self):
        board, board_string = detect_sudoku_board(self.uploaded_image_path, 'solver\sudoku_solver\models\model.keras')
        self.controller.show_frame(EditPage, board_string, board)
        print(board)

# Page for editing and solving Sudoku board
class EditPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # UI setup
        tk.Label(self, text="Edit Sudoku Board").pack(pady=10)
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(pady=10)
        self.progress_label = tk.Label(self, text="")
        self.progress_label.pack()
        self.edit_mode = False
        self.toggle_edit_button = tk.Button(self, text="Edit mode: Off", command=self.toggle_edit_mode)
        self.toggle_edit_button.pack(pady=10)
        tk.Button(self, text="Solve", command=self.solve_board).pack()

        self.board_string = ""
        self.entries = []

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.update_editability()
        self.toggle_edit_button.config(text=f"Edit mode: {'On' if self.edit_mode else 'Off'}")

    def display_board(self, board_array):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.entries = []

        for i, row in enumerate(board_array):
            row_entries = []
            for j, num in enumerate(row):
                entry = tk.Entry(self.grid_frame, width=2, font=('Helvetica', 20), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, num if num != 0 else "")
                entry.config(state=tk.NORMAL if self.edit_mode else tk.DISABLED)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def update_editability(self):
        for row in self.entries:
            for entry in row:
                entry.config(state=tk.NORMAL if self.edit_mode else tk.DISABLED)

    def set_board(self, board_string, board_array):
        self.board_string = board_string
        self.display_board(board_array)

    def solve_board(self):
        self.progress_label.config(text="Solving, please wait...")
        solve_thread = threading.Thread(target=self.run_solve)
        solve_thread.start()

    def run_solve(self):
        start_time = time.time()
        self.update_board_string_from_entries()

        solver = SudokuSolver(self.board_string)
        if solver.solve():
            end_time = time.time()
            solve_time = end_time - start_time
            solved_board = solver.print_board()

            self.controller.after(0, self.show_solved_board, solved_board, solve_time)
        else:
            self.controller.after(0, self.progress_label.config, {"text": "Solve failed."})

    def update_board_string_from_entries(self):
        updated_string = ""
        for row in self.entries:
            for entry in row:
                num = entry.get()
                updated_string += num if num.isdigit() else '0'
        self.board_string = updated_string

    # Function to show solved Sudoku board
    def show_solved_board(self, solved_board, solve_time):
        self.controller.show_frame(SolvePage, solved_board, solve_time)

# Page for displaying solved Sudoku board
class SolvePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # UI setup
        tk.Label(self, text="Solved Sudoku Board").pack(pady=10)
        self.solved_board_frame = tk.Frame(self)
        self.solved_board_frame.pack(pady=10)
        self.solve_time_label = tk.Label(self, text="")
        self.solve_time_label.pack()

    def set_solved_board(self, solved_board, solve_time=None):
        for widget in self.solved_board_frame.winfo_children():
            widget.destroy()

        for i, row in enumerate(solved_board):
            for j, num in enumerate(row):
                entry_text = str(num) if num != 0 else ""
                entry = tk.Entry(self.solved_board_frame, width=2, font=('Helvetica', 20), justify='center', readonlybackground='lightgray', borderwidth=1, relief="solid")
                entry.grid(row=i, column=j, padx=1, pady=1)
                entry.insert(0, entry_text)
                entry.config(state='readonly')

        if solve_time is not None:
            self.solve_time_label.config(text=f"Solve time: {solve_time:.2f} seconds")

# Main application
class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.frames = {}
        for F in (UploadPage, EditPage, SolvePage):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(UploadPage)

        self.geometry('1000x800')
        self.resizable(True, True)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width, window_height = 500, 800
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}") # Center window

    # Frame switcher
    def show_frame(self, page_class, *args, **kwargs):
        frame = self.frames[page_class.__name__]

        if hasattr(frame, 'set_solved_board') and (args or kwargs):
            frame.set_solved_board(*args, **kwargs)
        elif hasattr(frame, 'set_board') and (args or kwargs):
            frame.set_board(*args, **kwargs)
        
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
