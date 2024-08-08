import tkinter as tk
import random
import copy

class Game2048:
    def __init__(self, master):
        self.master = master
        master.title("2048")

        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.high_score = 0  # Not implemented in this version
        self.previous_grid = None
        self.previous_score = 0

        self.create_widgets()
        self.add_new_tile()
        self.add_new_tile()

    def create_widgets(self):
        """Creates the GUI elements: score label, grid, and buttons."""
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()

        self.score_label = tk.Label(self.main_frame, text="Score: 0")
        self.score_label.pack()

        self.grid_frame = tk.Frame(self.main_frame)
        self.grid_frame.pack()

        self.cells = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                cell_frame = tk.Frame(self.grid_frame, width=60, height=60, borderwidth=1, relief="solid")
                cell_frame.grid(row=i, column=j)
                cell_number = tk.Label(cell_frame, text="", font=("Arial", 24))
                cell_number.place(relx=0.5, rely=0.5, anchor="center")
                row.append({"frame": cell_frame, "number": cell_number})
            self.cells.append(row)

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack()

        self.new_game_button = tk.Button(self.button_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(side="left")

        self.undo_button = tk.Button(self.button_frame, text="Undo", command=self.undo)
        self.undo_button.pack(side="left")

        self.restart_button = tk.Button(self.button_frame, text="Restart", command=self.restart)
        self.restart_button.pack(side="left")

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

    def add_new_tile(self):
        """Adds a new tile (2 or 4) to a random empty cell."""
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
            self.update_grid()

    def update_grid(self):
        """Updates the visual representation of the grid based on the grid data."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                if value == 0:
                    self.cells[i][j]["frame"].config(bg="lightgray")
                    self.cells[i][j]["number"].config(text="")
                else:
                    self.cells[i][j]["frame"].config(bg=self.get_tile_color(value))
                    self.cells[i][j]["number"].config(text=str(value))

    def get_tile_color(self, value):
        """Returns the color associated with a tile value."""
        colors = {
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e"
        }
        return colors.get(value, "#cdc1b4")

    def stack(self):
        """Stacks tiles towards the left, removing empty spaces between them."""
        new_grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            fill_position = 0
            for j in range(self.grid_size):
                if self.grid[i][j] != 0:
                    new_grid[i][fill_position] = self.grid[i][j]
                    fill_position += 1
        self.grid = new_grid

    def combine(self):
        """Combines adjacent tiles of the same value, moving towards the left."""
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i][j + 1]:
                    self.grid[i][j] *= 2
                    self.grid[i][j + 1] = 0
                    self.score += self.grid[i][j]
                    self.score_label.config(text="Score: " + str(self.score))

    def reverse(self):
        """Reverses the order of tiles in each row."""
        new_grid = []
        for i in range(self.grid_size):
            new_grid.append(self.grid[i][::-1])
        self.grid = new_grid

    def transpose(self):
        """Transposes the grid (rows become columns and vice versa)."""
        new_grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                new_grid[i][j] = self.grid[j][i]
        self.grid = new_grid

    def left(self, event):
        """Handles the left arrow key press."""
        self.previous_grid = copy.deepcopy(self.grid)
        self.previous_score = self.score
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_grid()

    def right(self, event):
        """Handles the right arrow key press."""
        self.previous_grid = copy.deepcopy(self.grid)
        self.previous_score = self.score
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_grid()

    def up(self, event):
        """Handles the up arrow key press."""
        self.previous_grid = copy.deepcopy(self.grid)
        self.previous_score = self.score
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_grid()

    def down(self, event):
        """Handles the down arrow key press."""
        self.previous_grid = copy.deepcopy(self.grid)
        self.previous_score = self.score
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_grid()

    def new_game(self):
        """Starts a new game."""
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.score_label.config(text="Score: 0")
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()

    def undo(self):
        """Undoes the last move."""
        if self.previous_grid:
            self.grid = copy.deepcopy(self.previous_grid)
            self.score = self.previous_score
            self.score_label.config(text="Score: " + str(self.score))
            self.update_grid()
            self.previous_grid = None

    def restart(self):
        """Restarts the current game."""
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()

root = tk.Tk()
game = Game2048(root)
root.mainloop()