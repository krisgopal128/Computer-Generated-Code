import tkinter as tk
import random

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.canvas = tk.Canvas(self.window, width=400, height=400, bg="black")
        self.canvas.pack()

        self.snake = [(10, 10), (10, 11), (10, 12)]
        self.food = self.generate_food()
        self.direction = "right"
        self.score = 0
        self.game_running = False
        self.auto_mode = False

        self.create_buttons()
        self.create_scoreboard()
        self.bind_keys()
        self.draw_snake()
        self.draw_food()

        self.window.mainloop()

    def generate_food(self):
        while True:
            x = random.randint(0, 19)
            y = random.randint(0, 19)
            if (x, y) not in self.snake:
                return x, y

    def draw_snake(self):
        self.canvas.delete("snake")
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                # Head
                self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill="dark green",
                                            outline="black", tags="snake")
            else:
                # Body
                self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill="green", outline="black",
                                            tags="snake")

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(x * 20 + 2, y * 20 + 2, (x + 1) * 20 - 2, (y + 1) * 20 - 2, fill="red",
                                outline="black", tags="food")

    def move_snake(self):
        if not self.game_running:
            return

        head_x, head_y = self.snake[0]
        if self.direction == "up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "right":
            new_head = (head_x + 1, head_y)

        self.snake.insert(0, new_head)

        if self.check_collision():
            self.game_over()
            return

        if self.snake[0] == self.food:
            self.score += 1
            self.update_scoreboard()
            self.food = self.generate_food()
            self.draw_food()
        else:
            self.snake.pop()

        self.draw_snake()
        if self.auto_mode:
            self.window.after(125, self.auto_move)  # Move every 1/8 second in auto mode
        else:
            self.window.after(100, self.move_snake)

    def check_collision(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= 20 or head_y < 0 or head_y >= 20:
            return True
        if self.snake[0] in self.snake[1:]:
            return True
        return False

    def game_over(self):
        self.game_running = False
        self.auto_mode = False
        self.start_pause_button.config(text="Start")
        self.canvas.create_text(200, 200, text="Game Over", font=("Arial", 30), fill="white")

    def bind_keys(self):
        self.window.bind("<Up>", lambda event: self.start_or_change_direction("up"))
        self.window.bind("<Down>", lambda event: self.start_or_change_direction("down"))
        self.window.bind("<Left>", lambda event: self.start_or_change_direction("left"))
        self.window.bind("<Right>", lambda event: self.start_or_change_direction("right"))
        self.window.bind("<space>", lambda event: self.toggle_start_pause())

    def start_or_change_direction(self, new_direction):
        if not self.game_running:
            self.game_running = True
            self.move_snake()
        # User interaction pauses auto mode
        self.auto_mode = False
        self.change_direction(new_direction)

    def change_direction(self, new_direction):
        if new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction
        elif new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction

    def create_buttons(self):
        button_frame = tk.Frame(self.window)
        button_frame.pack()

        self.start_pause_button = tk.Button(button_frame, text="Start", command=self.toggle_start_pause)
        self.start_pause_button.pack(side="left")

        restart_button = tk.Button(button_frame, text="Restart", command=self.restart_game)
        restart_button.pack(side="left")

        auto_button = tk.Button(button_frame, text="Auto", command=self.toggle_auto)
        auto_button.pack(side="left")

    def create_scoreboard(self):
        self.scoreboard = self.canvas.create_text(
            350, 20, text=f"Score: {self.score}", font=("Arial", 14), fill="white"
        )
        self.canvas.itemconfig(self.scoreboard, stipple="gray50")  # Make it translucent

    def update_scoreboard(self):
        self.canvas.itemconfig(self.scoreboard, text=f"Score: {self.score}")

    def toggle_start_pause(self):
        if self.game_running:
            self.game_running = False
            self.start_pause_button.config(text="Start")
        else:
            self.game_running = True
            self.start_pause_button.config(text="Pause")
            self.move_snake()

    def restart_game(self):
        self.game_running = False
        self.auto_mode = False
        self.start_pause_button.config(text="Start")
        self.snake = [(10, 10), (10, 11), (10, 12)]
        self.food = self.generate_food()
        self.direction = "right"
        self.score = 0
        self.update_scoreboard()
        self.canvas.delete("all")  # Clear the canvas
        self.draw_snake()
        self.draw_food()

    def toggle_auto(self):
        if not self.game_running:
            self.game_running = True
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            self.auto_move()

    def auto_move(self):
        if self.auto_mode and self.game_running:
            head_x, head_y = self.snake[0]
            food_x, food_y = self.food

            possible_directions = ["up", "down", "left", "right"]

            # Remove directions that would lead to immediate collision
            if head_x == 0 or (head_x - 1, head_y) in self.snake:
                possible_directions.remove("left")
            if head_x == 19 or (head_x + 1, head_y) in self.snake:
                possible_directions.remove("right")
            if head_y == 0 or (head_x, head_y - 1) in self.snake:
                possible_directions.remove("up")
            if head_y == 19 or (head_x, head_y + 1) in self.snake:
                possible_directions.remove("down")

            # Remove directions that would lead to coiling and hitting itself
            if len(self.snake) > 3:
                second_segment = self.snake[1]
                if (head_x, head_y - 1) == second_segment and "up" in possible_directions:
                    possible_directions.remove("up")
                if (head_x, head_y + 1) == second_segment and "down" in possible_directions:
                    possible_directions.remove("down")
                if (head_x - 1, head_y) == second_segment and "left" in possible_directions:
                    possible_directions.remove("left")
                if (head_x + 1, head_y) == second_segment and "right" in possible_directions:
                    possible_directions.remove("right")

            # Prioritize directions that move closer to the food
            if "left" in possible_directions and head_x > food_x:
                new_direction = "left"
            elif "right" in possible_directions and head_x < food_x:
                new_direction = "right"
            elif "up" in possible_directions and head_y > food_y:
                new_direction = "up"
            elif "down" in possible_directions and head_y < food_y:
                new_direction = "down"
            else:
                # If no good direction, choose a random one
                if possible_directions:
                    new_direction = random.choice(possible_directions)
                else:
                    # No possible moves, game over
                    self.game_over()
                    return

            self.change_direction(new_direction)
            self.move_snake()

if __name__ == "__main__":
    SnakeGame()