import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("500x600")
        self.root.config(bg="#F4B8D7")  # Soft pink background
        
        self.grid = [[0]*9 for _ in range(9)]  # Initialize a 9x9 grid
        
        # Title
        self.title_label = tk.Label(self.root, text="Sudoku Solver", font=("Mali", 30, "bold"), bg="#F4B8D7", fg="#FF3366")
        self.title_label.pack(pady=20)
        
        # Frame for the Sudoku grid
        self.grid_frame = tk.Frame(self.root, bg="#000000", bd=3, relief="solid")  # Bold outer border
        self.grid_frame.pack(pady=10)

        # Create the 9x9 grid of Entry widgets
        self.entries = [[None]*9 for _ in range(9)]
        for row in range(9):
            for col in range(9):
                # Determine the border thickness for 3x3 subgrid boxes
                top = 2 if row % 3 == 0 else 1
                left = 2 if col % 3 == 0 else 1
                bottom = 2 if row == 8 else 1
                right = 2 if col == 8 else 1

                # Entry widget for each cell
                entry = tk.Entry(self.grid_frame, width=2, font=('Mali', 18), justify='center', bd=0, bg="#F9E4E5", fg="black", validate="key")
                entry.grid(row=row, column=col, sticky="nsew", ipadx=10, ipady=10)

                # Configure validation to accept only numbers 1-9
                validate_command = (self.root.register(self.validate_input), "%P")
                entry.config(validatecommand=validate_command)
                
                # Apply borders for 3x3 subgrids
                entry.grid(row=row, column=col, padx=(left, right), pady=(top, bottom))
                self.entries[row][col] = entry

        # Solve and Clear buttons
        self.button_frame = tk.Frame(self.root, bg="#F4B8D7")
        self.button_frame.pack(pady=20)

        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve, font=("Mali", 16), bg="#D99FB4", fg="white", relief="solid", width=10)
        self.solve_button.grid(row=0, column=0, padx=10)

        self.clear_button = tk.Button(self.button_frame, text="Clear Board", command=self.clear, font=("Mali", 16), bg="#D99FB4", fg="white", relief="solid", width=10)
        self.clear_button.grid(row=0, column=1, padx=10)

    def validate_input(self, value):
        if value == "" or (value.isdigit() and 1 <= int(value) <= 9):
            return True
        return False

    def solve(self):
              
        if self.solve_sudoku():
            self.update_grid()
        else:
            messagebox.showinfo("No Solution", "No solution exists for this Sudoku puzzle.")
    
    def solve_sudoku(self):
        
        return True

    def is_safe(self, row, col, num):
        # Check row
        if num in self.grid[row]:
            return False
        
        # Check column
        if num in [self.grid[i][col] for i in range(9)]:
            return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False
        
        return True

    def update_grid(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(self.grid[row][col]))

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
        self.grid = [[0]*9 for _ in range(9)]


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
