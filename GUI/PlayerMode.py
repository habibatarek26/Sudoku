import tkinter as tk
from tkinter import messagebox
import random

class PlayerMode(tk.Frame):  
    def __init__(self, parent, level=None):
        super().__init__(parent) 
        self.parent = parent  
        self.level = level 
        self.config(bg="#fac8e2") 
        self.grid = [[0] * 9 for _ in range(9)]  # Initialize all elements to 0

        # Initialize one random element
        self.initialize_random_element()

        self.title_label = tk.Label(
            self,
            text="Sudoku Solver",
            font=("Water Brush", 45, "bold", "italic"),
            bg="#fac8e2",
            fg="black",
        )
        self.title_label.pack(pady=20)

        self.grid_frame = tk.Frame(self, bg="#000000", bd=3, relief="solid")
        self.grid_frame.pack(pady=10)

        self.entries = [[None] * 9 for _ in range(9)]
        for row in range(9):
            for col in range(9):
                top = 2 if row % 3 == 0 else 1
                left = 2 if col % 3 == 0 else 1
                bottom = 2 if row == 8 else 1
                right = 2 if col == 8 else 1

                validate_command = (self.register(self.validate_input), "%P")

                entry = tk.Entry(
                    self.grid_frame,
                    width=2,
                    font=("Mali", 18),
                    justify="center",
                    bd=0,
                    bg="#fcfcf7",
                    fg="black",
                    validate="key",
                    validatecommand=validate_command,
                )
                entry.grid(row=row, column=col, padx=(left, right), pady=(top, bottom), ipadx=10, ipady=10)
                self.entries[row][col] = entry

        self.states = []
        self.current_state_index = -1

        self.button_frame = tk.Frame(self, bg="#fac8e2")
        self.button_frame.pack(pady=20)

        self.solve_button = tk.Button(
            self.button_frame,
            text="Submit",
            command=self.solve,
            font=("Mali", 16, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=10,
        )
        self.solve_button.grid(row=0, column=0, padx=10)

        self.clear_button = tk.Button(
            self.button_frame,
            text="Clear Board",
            command=self.clear,
            font=("Mali", 16, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=10,
        )
        self.clear_button.grid(row=0, column=1, padx=10)

        self.slide_frame = tk.Frame(self, bg="#fac8e2")
        self.slide_frame.pack(pady=10)

        self.back_button = tk.Button(
            self,
            text="← Back to Menu",
            command=self.go_back_to_menu,
            font=("Mali", 16, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=15,
        )
        self.back_button.pack(pady=20)

        self.process_board_state()

    def initialize_random_element(self):
        """ Initialize one random element with a value between 1 and 9 """
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        self.grid[row][col] = random.randint(1, 9)

    def process_board_state(self):
        """ Process the board by calling myFun and displaying the first state """
        board_state = ''.join(str(cell) for row in self.grid for cell in row)
        self.states = self.my_fun(board_state)

        # Display the first state from the list returned by myFun
        self.update_grid_from_state("010101010010101010010101010010101010010101010010101010010101010010101010010101010")

    def update_level(self, level):
        self.level = level 

    def validate_input(self, value):
        if value == "" or (value.isdigit() and 1 <= int(value) <= 9):
            return True
        return False

    def solve(self):
        self.grid = self.read_grid()
        board_state = "".join(str(cell) for row in self.grid for cell in row)

        self.states = self.my_fun(board_state)
        if not board_state == self.states.pop():
            messagebox.showinfo("Puzzle Solving Failed", "Oops! Try a different Solution")
            return
        else:
            messagebox.showinfo("Congratulations !!")

    
    def my_fun(self, board_state):
        """ Returns a list of possible board states (as strings) """
        return [board_state, board_state.replace("0", "1"), board_state.replace("0", "2")]

    def go_back_to_menu(self):
        self.parent.show_frame("GameModeSelection")

    def read_grid(self):
        return [[int(self.entries[row][col].get()) if self.entries[row][col].get().isdigit() else 0 for col in range(9)] for row in range(9)]

    def update_grid_from_state(self, state):
        for row in range(9):
            for col in range(9):
                value = int(state[row * 9 + col])
                
                if value == 0:
                    self.entries[row][col].config(state="normal")
                else:
                    self.entries[row][col].insert(0, state[row * 9 + col])
                    self.entries[row][col].config(state="disabled")
                    
                self.entries[row][col].delete(0, tk.END)
                if value != 0:
                    self.entries[row][col].insert(0, str(value))  # Insert the value if not 0
                else:
                    self.entries[row][col].insert(0, "")  # Insert an empty string for 0

                self.entries[row][col].config(
                    disabledbackground="#ececec",  
                    disabledforeground="black",   
                    font=("Mali", 18, "italic"),  
                    highlightbackground="#cccccc",  
                    highlightthickness=1
                )


    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].config(state="normal")
                self.entries[row][col].delete(0, tk.END)
        self.grid = [[0] * 9 for _ in range(9)]
        self.states = []
        self.current_state_index = -1
