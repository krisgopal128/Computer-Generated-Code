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

        self.canvas = tk.Canvas(self.window, width=self.game_width, height=self.game_height, bg="black")
        self.canvas.pack()

        self.score = 0
        self.score_label = tk.Label(self.window, text="Score: 0", font=("Helvetica", 16))
        self.score_label.pack()

        self.start_button = tk.Button(self.window, text="Start", command=self.start_game)
        self.start_button.pack()

        self.restart_button = tk.Button(self.window, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        self.auto_button = tk.Button(self.window, text="Auto", command=self.toggle_auto)
        self.auto_button.pack()

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
        for x, y in self.snake:
            self.canvas.create_rectangle(x * self.game_width / self.grid_size, y * self.game_height / self.grid_size,
                                       (x + 1) * self.game_width / self.grid_size,
                                       (y + 1) * self.game_height / self.grid_size, fill="green", tags="snake")

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(x * self.game_width / self.grid_size, y * self.game_height / self.grid_size,
                               (x + 1) * self.game_width / self.grid_size,
                               (y + 1) * self.game_height / self.grid_size, fill="red", tags="food")

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

        # Lookahead and Backtracking with Depth-First Search (DFS)
        best_direction = None
        max_depth = 5  # Adjust this value for more/less lookahead

        def dfs(x, y, depth, visited, direction):
            nonlocal best_direction
            if depth == 0:
                return
            visited.add((x, y))
            if (x, y) == self.food:
                best_direction = direction
                return

            possible_moves = [(x, y - 1, "Up"), (x, y + 1, "Down"), (x - 1, y, "Left"), (x + 1, y, "Right")]
            for new_x, new_y, new_direction in possible_moves:
                if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size and (new_x, new_y) not in visited and (new_x, new_y) not in self.snake:
                    dfs(new_x, new_y, depth - 1, visited.copy(), direction or new_direction)

        dfs(head_x, head_y, max_depth, set(), None)

        if best_direction:
            self.direction = best_direction
        else:
            # If no safe path found with lookahead, try to avoid immediate collision
            possible_directions = ["Up", "Down", "Left", "Right"]
            for direction in possible_directions:
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
            else:
                # If no clear path, choose a random direction
                self.direction = random.choice(possible_directions)

    def game_loop(self):
        if not self.game_over and not self.paused:
            if self.auto_mode:
                self.auto_move()
            self.move_snake()
            if self.check_collision():
                self.game_over = True
                self.start_button.config(text="Game Over")
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