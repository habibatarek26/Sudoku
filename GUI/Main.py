import tkinter as tk
from GameModeSelection import GameModeSelection
from SudokuSolver import SudokuSolver
from PlayerMode import PlayerMode
from level import Level
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku App")
        self.geometry("600x700")
        self.config(bg="#fac8e2")

        self.frames = {}
        self.init_frames()

    def init_frames(self):
        self.frames["GameModeSelection"] = GameModeSelection(self)
        self.frames["SudokuSolver"] = SudokuSolver(self)
        self.frames["PlayerMode"] = PlayerMode(self)  
        self.frames["Level"] = Level(self)  

        self.show_frame("GameModeSelection")


    def show_frame(self, name, *args):
        for frame in self.frames.values():
            frame.pack_forget()
        frame = self.frames[name]
        if args:  
            frame.update_level(*args)
        frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
