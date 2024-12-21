import tkinter as tk
from tkinter import messagebox


class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("500x600")
        self.root.config(bg="#fac8e2")

        self.grid = [[0] * 9 for _ in range(9)]

        self.title_label = tk.Label(
            self.root,
            text="Sudoku Solver",
            font=("Water Brush", 45, "bold", "italic"),
            bg="#fac8e2",
            fg="black",
        )
        self.title_label.pack(pady=20)

        self.grid_frame = tk.Frame(self.root, bg="#000000", bd=3, relief="solid")
        self.grid_frame.pack(pady=10)

        self.entries = [[None] * 9 for _ in range(9)]
        for row in range(9):
            for col in range(9):
                top = 2 if row % 3 == 0 else 1
                left = 2 if col % 3 == 0 else 1
                bottom = 2 if row == 8 else 1
                right = 2 if col == 8 else 1

                validate_command = (self.root.register(self.validate_input), "%P")

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
        self.movie_running = False

        self.button_frame = tk.Frame(self.root, bg="#fac8e2")
        self.button_frame.pack(pady=20)

        self.solve_button = tk.Button(
            self.button_frame,
            text="Solve",
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

        self.final_button = tk.Button(
            self.button_frame,
            text="Final State",
            command=self.show_final_result,
            font=("Mali", 16, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=10,
        )
        self.final_button.grid(row=1, column=0, padx=10)

        self.movie_button = tk.Button(
            self.button_frame,
            text="Animation",
            command=self.movie_show,
            font=("Mali", 16, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=10,
        )
        self.movie_button.grid(row=1, column=1, padx=10)

        self.slide_frame = tk.Frame(self.root, bg="#fac8e2")
        self.slide_frame.pack(pady=10)

        self.prev_button = tk.Button(
            self.slide_frame,
            text="←",
            command=self.previous_state,
            font=("Mali", 18),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            state=tk.DISABLED,
            width=5,
        )
        self.prev_button.grid(row=0, column=0, padx=10)

        self.next_button = tk.Button(
            self.slide_frame,
            text="→",
            command=self.next_state,
            font=("Mali", 18),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            state=tk.DISABLED,
            width=5,
        )
        self.next_button.grid(row=0, column=1, padx=10)

    def validate_input(self, value):
        """
        Validates that the input is either empty or a digit between 1 and 9.
        """
        if value == "" or (value.isdigit() and 1 <= int(value) <= 9):
            return True
        return False

    def solve(self):
        self.grid = self.read_grid()
        board_state = "".join(str(cell) for row in self.grid for cell in row)

        self.states = self.my_fun(board_state)
        if not self.states:
            messagebox.showinfo("No Solution", "No solution exists for this Sudoku puzzle.")
            return

        self.current_state_index = 0
        self.update_grid_from_state(self.states[self.current_state_index])

        self.prev_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        self.movie_button.config(state=tk.NORMAL)
        self.final_button.config(state=tk.NORMAL)
        
###################################################################
    def my_fun(self, board_state):
        # Example: Generate dummy states
        return [board_state, board_state.replace("0", "1"), board_state.replace("0", "2")]
###################################################################


    def previous_state(self):
        if self.current_state_index > 0:
            self.current_state_index -= 1
        self.update_grid_from_state(self.states[self.current_state_index])

    def next_state(self):
        if self.current_state_index < len(self.states) - 1:
            self.current_state_index += 1
        self.update_grid_from_state(self.states[self.current_state_index])

    def movie_show(self):
        if self.states and not self.movie_running:
            self.movie_running = True
            self.run_movie()

    def run_movie(self):
        if self.movie_running and self.current_state_index < len(self.states):
            self.update_grid_from_state(self.states[self.current_state_index])
            self.current_state_index += 1
            self.root.after(750, self.run_movie)  # Adjust delay (in milliseconds) as needed
        else:
            self.movie_running = False
            self.current_state_index = 0

    def show_final_result(self):
        if self.states:
            self.update_grid_from_state(self.states[-1])

    def read_grid(self):
        return [[int(self.entries[row][col].get()) if self.entries[row][col].get().isdigit() else 0 for col in range(9)] for row in range(9)]

    def update_grid_from_state(self, state):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, state[row * 9 + col])

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
        self.grid = [[0] * 9 for _ in range(9)]
        self.states = []
        self.current_state_index = -1
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.movie_button.config(state=tk.DISABLED)
        self.final_button.config(state=tk.DISABLED)
        self.movie_running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
