import tkinter as tk
import random

class BrickBreaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Brick Breaker")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()

        # Game Variables
        self.lives = 3
        self.score = 0
        self.is_paused = False
        self.ball_speed_x = 3
        self.ball_speed_y = -3

        # Paddle
        self.paddle = self.canvas.create_rectangle(250, 360, 350, 375, fill="white")
        self.canvas.bind_all("<Left>", self.move_left)
        self.canvas.bind_all("<Right>", self.move_right)

        # Ball
        self.ball = self.canvas.create_oval(290, 340, 310, 360, fill="white")

        # Bricks
        self.bricks = []
        self.create_bricks()

        # Scoreboard
        self.score_text = self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 14))
        self.lives_text = self.canvas.create_text(550, 20, text=f"Lives: {self.lives}", fill="white", font=("Arial", 14))

        # Buttons
        self.start_pause_button = tk.Button(root, text="Start", command=self.toggle_pause)
        self.start_pause_button.pack(side="left", padx=10)

        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack(side="right", padx=10)

        # Start the game loop
        self.game_loop()

    def create_bricks(self):
        colors = ["red", "orange", "yellow", "green", "blue"]
        for row in range(5):
            brick_color = random.choice(colors)
            for col in range(10):
                x1 = col * 60 + 5
                y1 = row * 30 + 5
                x2 = x1 + 50
                y2 = y1 + 20
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=brick_color)
                self.bricks.append(brick)

    def move_left(self, event):
        if not self.is_paused:
            self.canvas.move(self.paddle, -20, 0)

    def move_right(self, event):
        if not self.is_paused:
            self.canvas.move(self.paddle, 20, 0)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.start_pause_button.config(text="Resume")
        else:
            self.start_pause_button.config(text="Pause")

    def restart_game(self):
        self.canvas.delete("all")
        self.lives = 3
        self.score = 0
        self.is_paused = False
        self.ball_speed_x = 3
        self.ball_speed_y = -3
        self.paddle = self.canvas.create_rectangle(250, 360, 350, 375, fill="white")
        self.ball = self.canvas.create_oval(290, 340, 310, 360, fill="white")
        self.bricks = []
        self.create_bricks()
        self.score_text = self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 14))
        self.lives_text = self.canvas.create_text(550, 20, text=f"Lives: {self.lives}", fill="white", font=("Arial", 14))
        self.start_pause_button.config(text="Pause")

    def game_loop(self):
        if not self.is_paused:
            self.move_ball()
            self.check_collisions()
            self.update_scoreboard()

        self.root.after(20, self.game_loop)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
        ball_pos = self.canvas.coords(self.ball)
        
        if ball_pos[0] <= 0 or ball_pos[2] >= 600:  # Left or Right wall
            self.ball_speed_x = -self.ball_speed_x
        if ball_pos[1] <= 0:  # Top wall
            self.ball_speed_y = -self.ball_speed_y
        if ball_pos[3] >= 400:  # Bottom wall
            self.lives -= 1
            if self.lives > 0:
                self.reset_ball()
            else:
                self.game_over()

    def reset_ball(self):
        self.canvas.coords(self.ball, 290, 340, 310, 360)
        self.ball_speed_x = 3
        self.ball_speed_y = -3

    def check_collisions(self):
        ball_pos = self.canvas.coords(self.ball)
        items = self.canvas.find_overlapping(ball_pos[0], ball_pos[1], ball_pos[2], ball_pos[3])

        for item in items:
            if item == self.paddle:
                self.ball_speed_y = -self.ball_speed_y
            elif item in self.bricks:
                self.bricks.remove(item)
                self.canvas.delete(item)
                self.ball_speed_y = -self.ball_speed_y
                self.score += 10

    def update_scoreboard(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")

    def game_over(self):
        self.canvas.create_text(300, 200, text="Game Over", fill="white", font=("Arial", 24))
        self.is_paused = True
        self.start_pause_button.config(text="Start")

if __name__ == "__main__":
    root = tk.Tk()
    game = BrickBreaker(root)
    root.mainloop()
