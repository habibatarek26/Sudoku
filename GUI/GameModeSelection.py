import tkinter as tk

class GameModeSelection(tk.Frame):  # Inherit from tk.Frame
    def __init__(self, parent):
        super().__init__(parent)  # Initialize as a Frame widget
        self.parent = parent
        self.config(bg="#fac8e2")  # Set background color

        self.title_label = tk.Label(
            self,  # Use self, which is now the Frame
            text="Game Mode Menu",
            font=("Mali", 36, "bold", "italic"),
            bg="#fac8e2",
            fg="black",
        )
        self.title_label.pack(pady=50)
        

        self.sudoku_button = tk.Button(
            self,  # Use self, which is now the Frame
            text="Sudoku Solver",
            command=self.open_sudoku_solver,
            font=("Mali", 18, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=20,
        )
        self.sudoku_button.pack(pady=20)

        self.sudoku_button = tk.Button(
            self,  # Use self, which is now the Frame
            text="Play",
            command=self.play_user_mode,
            font=("Mali", 18, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=20,
        )
        self.sudoku_button.pack(pady=20)

    def open_sudoku_solver(self):
        self.parent.show_frame("SudokuSolver")
    def play_user_mode(self):
        self.parent.show_frame("Level")
    
