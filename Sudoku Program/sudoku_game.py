import tkinter as tk
from tkinter import messagebox
import random
import time

class Sudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.grid = [[0] * 9 for _ in range(9)]
        self.selected_cell = None
        self.timer_label = None
        self.timer_seconds = 0
        self.timer_running = False
        self.difficulty = "easy"
        self.create_widgets()

    def create_widgets(self):
        # Create Sudoku grid
        self.buttons = []
        for row in range(9):
            row_buttons = []
            for col in range(9):
                btn = tk.Button(self.root, width=3, height=1, font=('Arial', 18),
                                command=lambda r=row, c=col: self.select_cell(r, c))
                btn.grid(row=row, column=col, padx=1, pady=1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Create control buttons
        tk.Button(self.root, text="Start", command=self.start_game).grid(row=9, column=0, columnspan=3, pady=5)
        tk.Button(self.root, text="Reset", command=self.reset_game).grid(row=9, column=3, columnspan=3, pady=5)
        tk.Button(self.root, text="Check", command=self.check_solution).grid(row=9, column=6, columnspan=3, pady=5)

        # Create difficulty selection
        tk.Label(self.root, text="Difficulty:").grid(row=10, column=0, columnspan=3, pady=5)
        self.difficulty_var = tk.StringVar(value="easy")
        tk.Radiobutton(self.root, text="Easy", variable=self.difficulty_var, value="easy").grid(row=10, column=3, pady=5)
        tk.Radiobutton(self.root, text="Med", variable=self.difficulty_var, value="medium").grid(row=10, column=4, pady=5)
        tk.Radiobutton(self.root, text="Hard", variable=self.difficulty_var, value="hard").grid(row=10, column=5, pady=5)

        # Create timer display
        self.timer_label = tk.Label(self.root, text="Time: 00:00", font=('Arial', 14))
        self.timer_label.grid(row=11, column=0, columnspan=9, pady=5)

        # Bind key events
        self.root.bind("<Key>", self.handle_key)

    def start_game(self):
        self.reset_game()
        self.generate_puzzle()
        self.start_timer()

    def reset_game(self):
        self.grid = [[0] * 9 for _ in range(9)]
        for row in self.buttons:
            for btn in row:
                btn.config(text="", state=tk.NORMAL, bg="SystemButtonFace")
        self.selected_cell = None
        self.timer_seconds = 0
        self.timer_running = False
        self.update_timer()

    def generate_puzzle(self):
        # Generate a full Sudoku grid using a simple backtracking algorithm
        def is_valid(grid, row, col, num):
            for i in range(9):
                if grid[row][i] == num or grid[i][col] == num:
                    return False
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if grid[i][j] == num:
                        return False
            return True

        def solve(grid):
            for row in range(9):
                for col in range(9):
                    if grid[row][col] == 0:
                        for num in range(1, 10):
                            if is_valid(grid, row, col, num):
                                grid[row][col] = num
                                if solve(grid):
                                    return True
                                grid[row][col] = 0
                        return False
            return True

        def remove_numbers(grid, level):
            if level == "easy":
                attempts = 5
            elif level == "medium":
                attempts = 25
            else:
                attempts = 45

            while attempts > 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                while grid[row][col] == 0:
                    row = random.randint(0, 8)
                    col = random.randint(0, 8)
                backup = grid[row][col]
                grid[row][col] = 0

                grid_copy = [row[:] for row in grid]
                attempts -= 1
                if not solve(grid_copy):
                    grid[row][col] = backup
                    attempts += 1

        base_grid = [[0] * 9 for _ in range(9)]
        solve(base_grid)
        remove_numbers(base_grid, self.difficulty_var.get())
        self.grid = base_grid

        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    self.buttons[row][col].config(text=str(self.grid[row][col]), state=tk.DISABLED, bg="light grey")

    def select_cell(self, row, col):
        if self.selected_cell:
            self.buttons[self.selected_cell[0]][self.selected_cell[1]].config(bg="SystemButtonFace")
        self.selected_cell = (row, col)
        self.buttons[row][col].config(bg="light blue")

    def handle_key(self, event):
        if self.selected_cell:
            row, col = self.selected_cell
            if event.char in '123456789':
                self.grid[row][col] = int(event.char)
                self.buttons[row][col].config(text=event.char)
            elif event.char == '0' or event.keysym == 'BackSpace':
                self.grid[row][col] = 0
                self.buttons[row][col].config(text="")

    def start_timer(self):
        self.timer_running = True
        if self.difficulty_var.get() == "easy":
            self.timer_seconds = 15 * 60
        elif self.difficulty_var.get() == "medium":
            self.timer_seconds = 25 * 60
        else:
            self.timer_seconds = 45 * 60
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            minutes, seconds = divmod(self.timer_seconds, 60)
            self.timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                messagebox.showinfo("Time's up!", "Time's up! You lost the game.")

    def check_solution(self):
        if all(self.is_valid(self.grid, row, col, self.grid[row][col]) for row in range(9) for col in range(9)):
            messagebox.showinfo("Congratulations!", "You won the game!")
        else:
            messagebox.showerror("Error", "The solution is incorrect.")

    def is_valid(self, grid, row, col, num):
        for i in range(9):
            if grid[row][i] == num and col != i:
                return False
            if grid[i][col] == num and row != i:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num and (i != row or j != col):
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = Sudoku(root)
    root.mainloop()
