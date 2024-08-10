import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random

class JigsawPuzzleApp:
    """
    Main application class for the jigsaw puzzle game.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Jigsaw Puzzle Game")
        self.canvas_size = 1024  # Size of the canvas for the puzzle
        self.grid_size = 4  # Default grid size (4x4)
        self.pieces = []  # List to store puzzle piece objects
        self.showing_image = False  # Flag to track if the full image is being shown
        self.hint_active = False  # Flag to track if hints are active
        self.image = None  # Variable to store the loaded image
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges the UI widgets for the application.
        """
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white", highlightthickness=2, highlightbackground="black")
        self.canvas.pack()

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT)

        self.check_button = tk.Button(self.root, text="Check", command=self.check_completion)
        self.check_button.pack(side=tk.LEFT)

        self.hint_button = tk.Button(self.root, text="Hint On", command=self.toggle_hint)
        self.hint_button.pack(side=tk.LEFT)

        self.show_button = tk.Button(self.root, text="Show", command=self.show_image)
        self.show_button.pack(side=tk.LEFT)

        self.level_var = tk.StringVar(value="Medium")
        self.level_menu = tk.OptionMenu(self.root, self.level_var, "Easy", "Medium", "Hard", command=self.set_difficulty)
        self.level_menu.pack(side=tk.RIGHT)

    def set_difficulty(self, level):
        """
        Sets the difficulty of the puzzle by changing the grid size and regenerating the puzzle.
        """
        if level == "Easy":
            self.grid_size = 3
        elif level == "Medium":
            self.grid_size = 4
        elif level == "Hard":
            self.grid_size = 5

        # Automatically regenerate the puzzle with the new difficulty
        if self.image:
            self.create_puzzle()

    def load_image(self):
        """
        Opens a file dialog for the user to select an image and loads it.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                image = Image.open(file_path)
                self.image = self.resize_image(image)
                self.create_puzzle()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def resize_image(self, image):
        """
        Resizes the image to fit within the canvas while maintaining aspect ratio.
        """
        image.thumbnail((self.canvas_size, self.canvas_size))
        return image

    def create_puzzle(self):
        """
        Creates the puzzle pieces from the loaded image.
        """
        piece_width = self.image.width // self.grid_size
        piece_height = self.image.height // self.grid_size
        self.pieces.clear()
        self.canvas.delete("all")

        # Draw the grid lines
        self.draw_grid_lines()

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                box = (j * piece_width, i * piece_height, (j + 1) * piece_width, (i + 1) * piece_height)
                piece_image = self.image.crop(box)
                piece = PuzzlePiece(self, self.canvas, piece_image, j, i, piece_width, piece_height, i * self.grid_size + j + 1)
                self.pieces.append(piece)

        random.shuffle(self.pieces)
        self.display_pieces()

    def draw_grid_lines(self):
        """
        Draws the grid lines on the canvas based on the current grid size.
        """
        piece_width = self.image.width // self.grid_size
        piece_height = self.image.height // self.grid_size
        for i in range(self.grid_size + 1):
            # Vertical lines
            self.canvas.create_line(i * piece_width, 0, i * piece_width, piece_height * self.grid_size, fill="green", width=2, tags="grid_line")
            # Horizontal lines
            self.canvas.create_line(0, i * piece_height, piece_width * self.grid_size, i * piece_height, fill="green", width=2, tags="grid_line")

    def display_pieces(self):
        """
        Displays the puzzle pieces on the canvas.
        """
        self.canvas.delete("piece")  # Clear any old pieces
        for piece in self.pieces:
            piece.display()

    def reset_game(self):
        """
        Resets the puzzle by shuffling the pieces and re-displaying them based on the current difficulty level.
        """
        if self.image:
            # Regenerate the puzzle based on the current difficulty
            self.create_puzzle()

    def check_completion(self):
        """
        Checks if the puzzle is completed.
        """
        for piece in self.pieces:
            if not piece.is_in_correct_position():
                return False
        messagebox.showinfo("Congratulations", "You completed the puzzle!")
        return True

    def toggle_hint(self):
        """
        Toggles the display of hints on the puzzle pieces.
        """
        self.hint_active = not self.hint_active
        if self.hint_active:
            self.hint_button.config(text="Hint Off")
        else:
            self.hint_button.config(text="Hint On")
        for piece in self.pieces:
            piece.toggle_hint(self.hint_active)

    def show_image(self):
        """
        Toggles between showing the complete image and the puzzle pieces.
        """
        if not self.showing_image:
            if self.image:  # Only show if an image is loaded
                self.canvas.delete("piece")  # Clear puzzle pieces
                self.canvas.delete("grid_line")  # Clear grid lines (if any)
                self.original_image = ImageTk.PhotoImage(self.image)  # Store the PhotoImage
                self.canvas.create_image(0, 0, image=self.original_image, anchor=tk.NW)
                self.showing_image = True
                self.show_button.config(text="Show Puzzle")
        else:
            self.canvas.delete("all")  # Clear everything
            self.create_puzzle()  # Recreate the puzzle
            self.showing_image = False
            self.show_button.config(text="Show Image")


class PuzzlePiece:
    """
    Represents a single puzzle piece.
    """
    def __init__(self, app, canvas, image, x, y, width, height, piece_number):
        self.app = app
        self.canvas = canvas
        self.image = ImageTk.PhotoImage(image)
        self.correct_x = x  # Correct x-coordinate on the grid
        self.correct_y = y  # Correct y-coordinate on the grid
        self.width = width
        self.height = height
        self.piece_number = piece_number
        self.current_position = (random.randint(0, self.canvas.winfo_width() - width),
                                 random.randint(0, self.canvas.winfo_height() - height))
        self.canvas_id = None  # ID of the canvas image item
        self.text_id = None  # ID of the hint text item

    def display(self):
        """
        Displays the piece on the canvas.
        """
        self.canvas_id = self.canvas.create_image(self.current_position, image=self.image, anchor=tk.NW, tags="piece")
        self.canvas.tag_bind(self.canvas_id, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.canvas_id, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.canvas_id, '<ButtonRelease-1>', self.on_release)

    def on_press(self, event):
        """
        Handles the mouse press event.
        """
        self.drag_data = {"x": event.x, "y": event.y}

    def on_drag(self, event):
        """
        Handles the mouse drag event.
        """
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.canvas.move(self.canvas_id, dx, dy)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_release(self, event):
        """
        Handles the mouse release event.
        """
        self.snap_to_grid()
        if self.app.check_completion():
            messagebox.showinfo("Winner!", "You have successfully completed the puzzle!")

    def snap_to_grid(self):
        """
        Snaps the piece to the nearest grid position.
        """
        x0, y0 = self.canvas.coords(self.canvas_id)
        snapped_x = round(x0 / self.width) * self.width
        snapped_y = round(y0 / self.height) * self.height
        self.canvas.coords(self.canvas_id, snapped_x, snapped_y)

        # Check if the piece is in the correct position after snapping
        if self.is_in_correct_position():
            self.join_correct_position()

    def is_in_correct_position(self):
        """
        Checks if the piece is in its correct position on the grid.
        """
        x0, y0 = self.canvas.coords(self.canvas_id)
        return int(x0) == self.correct_x * self.width and int(y0) == self.correct_y * self.height

    def join_correct_position(self):
        """
        Snaps the piece to its exact correct position if it's close enough.
        This provides a visual cue that the piece is in the right place.
        """
        self.canvas.coords(self.canvas_id, self.correct_x * self.width, self.correct_y * self.height)

    def toggle_hint(self, show):
        """
        Toggles the display of the hint (piece number) on the piece.
        """
        x0, y0 = self.canvas.coords(self.canvas_id)
        if show:
            if self.text_id is None:
                self.text_id = self.canvas.create_text(x0 + self.width // 2,
                                                       y0 + self.height // 2,
                                                       text=str(self.piece_number),
                                                       font=("Arial", 24), fill="red")
        else:
            if self.text_id is not None:
                self.canvas.delete(self.text_id)
                self.text_id = None


def main():
    root = tk.Tk()
    app = JigsawPuzzleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()