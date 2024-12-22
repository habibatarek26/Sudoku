import tkinter as tk
from tkinter import messagebox
import random
from algorithm import CSP
import math 

class PlayerMode(tk.Frame):  
    def __init__(self, parent, level=None):
        super().__init__(parent) 
        self.parent = parent  
        self.level = level 
        self.config(bg="#fac8e2") 
        self.grid = [[0] * 9 for _ in range(9)]  # Initialize all elements to 0

        # Initialize one random element

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
        

    def initialize_random_element(self):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        self.grid[row][col] = random.randint(1, 9)

    def process_board_state(self):
        board_state = {}
        self.grid = self.read_grid()
        self.initialize_random_element()

        for row in range(1, 10):
            for col in range(1, 10):
                var = f"V{row}{col}"
                value = self.grid[row - 1][col - 1]
                if value != 0:
                    board_state[var] = value

        self.states = self.my_fun(board_state)
        
        # Ensure self.states is not None before proceeding
        if self.states is None:
            messagebox.showinfo("Error", "No valid solution found!")
            return

        # Proceed with state-based logic depending on the level
        if self.level == "Hard":
            num = 20 if len(self.states) - 1 >= 70 else math.floor(len(self.states) * 1 / 2)
            self.update_grid_from_state(self.states[num])
        elif self.level == "Easy":
            num = 40 if len(self.states) - 1 >= 70 else math.floor(len(self.states) * 3 / 4)
            self.update_grid_from_state(self.states[num])
        else:
            num = 30 if len(self.states) - 1 >= 70 else math.floor(len(self.states) * 2 / 3)
            self.update_grid_from_state(self.states[num])


    def update_level(self, level):
        self.level = level 
        self.clear2()
        self.process_board_state()

    def validate_input(self, value):
        if value == "" or (value.isdigit() and 1 <= int(value) <= 9):
            return True
        return False

    def solve(self):
        self.grid = self.read_grid()
        board_state = string = ''.join(str(item) for row in self.grid for item in row)

        if(not self.states):
            messagebox.showinfo("Puzzle Solving Failed", "Oops! Try a different Solution")
        elif not (board_state == self.states[-1]):
            messagebox.showinfo("Puzzle Solving Failed", "Oops! Try a different Solution")
            return
        else:
            messagebox.showinfo("Congratulations !!", "Congratulations")

    
    def my_fun(self, board_state):
        sud = CSP(board_state)
        return sud.Solve()

    def go_back_to_menu(self):
        self.clear2()  
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
                    self.entries[row][col].insert(0, str(value))  
                else:
                    self.entries[row][col].insert(0, "")  

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
             if not self.entries[row][col].cget("state") == "disabled":  # Only clear disabled entries
                self.entries[row][col].config(state="normal")
                self.entries[row][col].delete(0, tk.END)
        self.grid = [[0] * 9 for _ in range(9)]
        self.states = []
    def clear2(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].config(state="normal")
                self.entries[row][col].delete(0, tk.END)
        self.grid = [[0] * 9 for _ in range(9)]
        self.states = []



##Easy: 30-40 clues
##Medium: 25-30 clues
##Hard: 17-24 clues