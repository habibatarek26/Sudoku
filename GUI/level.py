import tkinter as tk

class Level(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)  
        self.parent = parent
        self.config(bg="#fac8e2")

        self.title_label = tk.Label(
            self, 
            text="Level",
            font=("Mali", 36, "bold", "italic"),
            bg="#fac8e2",
            fg="black",
        )
        self.title_label.pack(pady=50)

        self.sudoku_button_easy = tk.Button(
            self, 
            text="Easy",
            command=lambda: self.play_user_mode("Easy"),  
            font=("Mali", 18, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=20,
        )
        self.sudoku_button_easy.pack(pady=20)

        self.sudoku_button_medium = tk.Button(
            self,  
            text="Medium",
            command=lambda: self.play_user_mode("Medium"), 
            font=("Mali", 18, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=20,
        )
        self.sudoku_button_medium.pack(pady=20)

        self.sudoku_button_hard = tk.Button(
            self, 
            text="Hard",
            command=lambda: self.play_user_mode("Hard"),  
            font=("Mali", 18, "italic"),
            bg="#D99FB4",
            fg="white",
            relief="solid",
            width=20,
        )
        self.sudoku_button_hard.pack(pady=20)

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

    def play_user_mode(self, level):
        self.parent.show_frame("PlayerMode", level)  
        
    def go_back_to_menu(self):
        self.parent.show_frame("GameModeSelection")