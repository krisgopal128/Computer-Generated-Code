import tkinter as tk
import random

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.grid_size = 20
        self.game_width = 400
        self.game_height = 400
        self.delay = 100
        self.auto_mode = False
        self.auto_restart = False

        self.canvas = tk.Canvas(self.window, width=self.game_width, height=self.game_height, bg="black")
        self.canvas.pack()

        self.score = 0
        self.highest_score = 0
        self.restart_count = 0

        self.score_label = tk.Label(self.window, text="Score: 0", font=("Helvetica", 16))
        self.score_label.pack()

        self.highest_score_label = tk.Label(self.window, text="Highest Score: 0", font=("Helvetica", 16))
        self.highest_score_label.pack()

        self.restart_count_label = tk.Label(self.window, text="Restarts: 0", font=("Helvetica", 16))
        self.restart_count_label.pack()

        # Button Frame for Horizontal Placement
        button_frame = tk.Frame(self.window)
        button_frame.pack()

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)

        self.restart_button = tk.Button(button_frame, text="Restart", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT)

        self.auto_button = tk.Button(button_frame, text="Auto", command=self.toggle_auto)
        self.auto_button.pack(side=tk.LEFT)

        self.auto_restart_var = tk.BooleanVar()
        self.auto_restart_checkbox = tk.Checkbutton(self.window, text="Auto Restart", variable=self.auto_restart_var, command=self.toggle_auto_restart)
        self.auto_restart_checkbox.pack()

        self.direction = "Right"
        self.snake = [(self.grid_size // 2, self.grid_size // 2), (self.grid_size // 2 - 1, self.grid_size // 2),
                      (self.grid_size // 2 - 2, self.grid_size // 2)]
        self.food = self.generate_food()

        self.window.bind("<Up>", self.change_direction)
        self.window.bind("<Down>", self.change_direction)
        self.window.bind("<Left>", self.change_direction)
        self.window.bind("<Right>", self.change_direction)
        self.window.bind("<space>", self.toggle_pause)

        self.game_over = False
        self.paused = True

    def start_game(self):
        if self.paused:
            self.paused = False
            self.start_button.config(text="Pause")
            self.game_loop()

    def restart_game(self):
        if self.score > self.highest_score:
            self.highest_score = self.score
            self.highest_score_label.config(text="Highest Score: {}".format(self.highest_score))

        self.game_over = False
        self.paused = True
        self.start_button.config(text="Start")
        self.direction = "Right"
        self.snake = [(self.grid_size // 2, self.grid_size // 2), (self.grid_size // 2 - 1, self.grid_size // 2),
                      (self.grid_size // 2 - 2, self.grid_size // 2)]
        self.food = self.generate_food()
        self.score = 0
        self.score_label.config(text="Score: 0")
        self.canvas.delete("all")
        self.draw_snake()
        self.draw_food()

    def toggle_auto(self):
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            self.auto_button.config(bg="green")
        else:
            self.auto_button.config(bg="SystemButtonFace")  # Default button color
            # Reset the restart count when auto mode is turned off
            self.restart_count = 0
            self.restart_count_label.config(text="Restarts: 0")

    def toggle_auto_restart(self):
        self.auto_restart = self.auto_restart_var.get()

    def toggle_pause(self, event=None):
        if not self.game_over:
            self.paused = not self.paused
            if self.paused:
                self.start_button.config(text="Resume")
            else:
                self.start_button.config(text="Pause")
                self.game_loop()

    def change_direction(self, event):
        new_direction = event.keysym
        if (new_direction == "Up" and self.direction != "Down") or \
           (new_direction == "Down" and self.direction != "Up") or \
           (new_direction == "Left" and self.direction != "Right") or \
           (new_direction == "Right" and self.direction != "Left"):
            self.direction = new_direction
            self.auto_mode = False  # Disable auto mode on user input

    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                return x, y

    def draw_snake(self):
        self.canvas.delete("snake")
        for i, (x, y) in enumerate(self.snake):
            color = "green" if i == 0 else "lightgreen"  # Different color for head
            self.canvas.create_rectangle(x * self.game_width / self.grid_size, y * self.game_height / self.grid_size,
                                       (x + 1) * self.game_width / self.grid_size,
                                       (y + 1) * self.game_height / self.grid_size, fill=color, outline="darkgreen", tags="snake")

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(x * self.game_width / self.grid_size + 2, y * self.game_height / self.grid_size + 2,
                               (x + 1) * self.game_width / self.grid_size - 2,
                               (y + 1) * self.game_height / self.grid_size - 2, fill="red", outline="darkred", tags="food")

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.score_label.config(text="Score: {}".format(self.score))
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def check_collision(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= self.grid_size or head_y < 0 or head_y >= self.grid_size or self.snake[0] in self.snake[1:]:
            return True
        return False

    def auto_move(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food

        # --- Rule-Based System ---

        # Rule: If food is to the left and body is on the left, try to turn right & around the body
        if food_x < head_x and (head_x - 1, head_y) in self.snake:
            if head_y > 0 and (head_x, head_y - 1) not in self.snake:  # Try to go up
                self.direction = "Up"
            elif head_y < self.grid_size - 1 and (head_x, head_y + 1) not in self.snake:  # Try to go down
                self.direction = "Down"
            # ... (Add more rules as needed)

        # --- Manhattan Distance Heuristic with Collision Avoidance and Hamiltonian Path Fallback ---

        else:  # If no rule-based decision is made
            # 1. Manhattan Distance Calculation
            distances = {
                "Up": abs(head_x - food_x) + abs((head_y - 1) - food_y),
                "Down": abs(head_x - food_x) + abs((head_y + 1) - food_y),
                "Left": abs((head_x - 1) - food_x) + abs(head_y - food_y),
                "Right": abs((head_x + 1) - food_x) + abs(head_y - food_y)
            }

            # 2. Sort Possible Directions by Closest Manhattan Distance
            sorted_directions = sorted(distances, key=distances.get)

            # 3. Avoid Immediate Collisions
            for direction in sorted_directions:
                if direction == "Up" and (head_x, head_y - 1) not in self.snake and head_y - 1 >= 0:
                    self.direction = direction
                    break
                elif direction == "Down" and (head_x, head_y + 1) not in self.snake and head_y + 1 < self.grid_size:
                    self.direction = direction
                    break
                elif direction == "Left" and (head_x - 1, head_y) not in self.snake and head_x - 1 >= 0:
                    self.direction = direction
                    break
                elif direction == "Right" and (head_x + 1, head_y) not in self.snake and head_x + 1 < self.grid_size:
                    self.direction = direction
                    break

            # 4. Hamiltonian Path Fallback (if no safe direction based on distance)
            else:
                # Define a simple Hamiltonian cycle as a fallback strategy
                if head_y == 0 and head_x < self.grid_size - 1:
                    self.direction = "Right"
                elif head_x == self.grid_size - 1 and head_y < self.grid_size - 1:
                    self.direction = "Down"
                elif head_y == self.grid_size - 1 and head_x > 0:
                    self.direction = "Left"
                elif head_x == 0 and head_y > 0:
                    self.direction = "Up"

    def game_loop(self):
        if not self.game_over and not self.paused:
            if self.auto_mode:
                self.auto_move()
            self.move_snake()
            if self.check_collision():
                self.game_over = True
                self.start_button.config(text="Game Over")
                if self.auto_mode and self.auto_restart:
                    self.restart_count += 1
                    self.restart_count_label.config(text="Restarts: {}".format(self.restart_count))
                    self.restart_game()
                    self.start_game()
            else:
                self.canvas.delete("all")
                self.draw_snake()
                self.draw_food()
                self.window.after(self.delay, self.game_loop)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
