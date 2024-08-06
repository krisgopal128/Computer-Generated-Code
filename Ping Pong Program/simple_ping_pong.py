import tkinter as tk
import random

# Window setup
window = tk.Tk()
window.title("Ping Pong")

# Constants
WIDTH = 800
HEIGHT = 600
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 10
BALL_SIZE = 10
BASE_PADDLE_SPEED = 10
PADDLE_SPEED_INCREMENT = 2
MAX_PADDLE_SPEED = 18
BALL_SPEED_X = 5
BALL_SPEED_Y = 5


# Game variables
player_score = 0
ai_score = 0
ball_x = WIDTH / 2
ball_y = HEIGHT / 2
ball_x_direction = random.choice([-1, 1])
ball_y_direction = random.choice([-1, 1])
player_paddle_y = HEIGHT / 2 - PADDLE_HEIGHT / 2
ai_paddle_y = HEIGHT / 2 - PADDLE_HEIGHT / 2
game_paused = True
auto_mode = False
player_paddle_speed = BASE_PADDLE_SPEED

# Canvas creation
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Paddle and ball creation
player_paddle = canvas.create_rectangle(
    WIDTH - PADDLE_WIDTH - 10,
    player_paddle_y,
    WIDTH - 10,
    player_paddle_y + PADDLE_HEIGHT,
    fill="white",
)
ai_paddle = canvas.create_rectangle(
    10, ai_paddle_y, 10 + PADDLE_WIDTH, ai_paddle_y + PADDLE_HEIGHT, fill="white"
)
ball = canvas.create_oval(
    ball_x - BALL_SIZE,
    ball_y - BALL_SIZE,
    ball_x + BALL_SIZE,
    ball_y + BALL_SIZE,
    fill="white",
)

# Scoreboard creation
scoreboard = canvas.create_text(
    WIDTH / 2, 20, text=f"{player_score} - {ai_score}", fill="white", font=("Arial", 24)
)


# Function to update the scoreboard
def update_scoreboard():
    canvas.itemconfig(scoreboard, text=f"{player_score} - {ai_score}")


# Function to move the player paddle
def move_player_paddle(event):
    global player_paddle_y, player_paddle_speed
    if event.keysym == "Up" and player_paddle_y > 0:
        player_paddle_y -= player_paddle_speed
        player_paddle_speed = min(
            player_paddle_speed + PADDLE_SPEED_INCREMENT, MAX_PADDLE_SPEED
        )
    elif event.keysym == "Down" and player_paddle_y < HEIGHT - PADDLE_HEIGHT:
        player_paddle_y += player_paddle_speed
        player_paddle_speed = min(
            player_paddle_speed + PADDLE_SPEED_INCREMENT, MAX_PADDLE_SPEED
        )
    canvas.coords(
        player_paddle,
        WIDTH - PADDLE_WIDTH - 10,
        player_paddle_y,
        WIDTH - 10,
        player_paddle_y + PADDLE_HEIGHT,
    )

    # Reset speed only when the ball hits the paddle
    if (
        ball_x + BALL_SIZE >= WIDTH - PADDLE_WIDTH - 10
        and player_paddle_y <= ball_y <= player_paddle_y + PADDLE_HEIGHT
    ):
        player_paddle_speed = BASE_PADDLE_SPEED


# Function to move the AI paddle
def move_ai_paddle():
    global ai_paddle_y
    if ball_y > ai_paddle_y + PADDLE_HEIGHT / 2 and ai_paddle_y < HEIGHT - PADDLE_HEIGHT:
        ai_paddle_y += BASE_PADDLE_SPEED / 2
    elif ball_y < ai_paddle_y + PADDLE_HEIGHT / 2 and ai_paddle_y > 0:
        ai_paddle_y -= BASE_PADDLE_SPEED / 2
    canvas.coords(ai_paddle, 10, ai_paddle_y, 10 + PADDLE_WIDTH, ai_paddle_y + PADDLE_HEIGHT)


# Function to move the ball
def move_ball():
    global ball_x, ball_y, ball_x_direction, ball_y_direction, player_score, ai_score
    ball_x += BALL_SPEED_X * ball_x_direction
    ball_y += BALL_SPEED_Y * ball_y_direction

    # Bounce off top and bottom walls
    if ball_y <= BALL_SIZE or ball_y >= HEIGHT - BALL_SIZE:
        ball_y_direction *= -1

    # Bounce off paddles
    if (
        ball_x - BALL_SIZE <= 10 + PADDLE_WIDTH
        and ai_paddle_y <= ball_y <= ai_paddle_y + PADDLE_HEIGHT
    ):
        ball_x_direction *= -1
        # Ensure ball doesn't get stuck inside the paddle
        ball_x = 10 + PADDLE_WIDTH + BALL_SIZE

    if (
        ball_x + BALL_SIZE >= WIDTH - PADDLE_WIDTH - 10
        and player_paddle_y <= ball_y <= player_paddle_y + PADDLE_HEIGHT
    ):
        ball_x_direction *= -1
        # Ensure ball doesn't get stuck inside the paddle
        ball_x = WIDTH - PADDLE_WIDTH - 10 - BALL_SIZE

    # Score points
    if ball_x < 0:
        player_score += 1
        reset_ball()
    elif ball_x > WIDTH:
        ai_score += 1
        reset_ball()

    canvas.coords(
        ball, ball_x - BALL_SIZE, ball_y - BALL_SIZE, ball_x + BALL_SIZE, ball_y + BALL_SIZE
    )


# Function to reset the ball
def reset_ball():
    global ball_x, ball_y, ball_x_direction, ball_y_direction
    ball_x = WIDTH / 2
    ball_y = HEIGHT / 2
    ball_x_direction = random.choice([-1, 1])
    ball_y_direction = random.choice([-1, 1])
    update_scoreboard()


# Function to start/pause the game
def toggle_pause():
    global game_paused
    game_paused = not game_paused
    if not game_paused:
        game_loop()


# Function to restart the game
def restart_game():
    global player_score, ai_score, ball_x, ball_y, ball_x_direction, ball_y_direction, player_paddle_y, ai_paddle_y, game_paused
    player_score = 0
    ai_score = 0
    ball_x = WIDTH / 2
    ball_y = HEIGHT / 2
    ball_x_direction = random.choice([-1, 1])
    ball_y_direction = random.choice([-1, 1])
    player_paddle_y = HEIGHT / 2 - PADDLE_HEIGHT / 2
    ai_paddle_y = HEIGHT / 2 - PADDLE_HEIGHT / 2
    game_paused = True
    canvas.coords(
        player_paddle,
        WIDTH - PADDLE_WIDTH - 10,
        player_paddle_y,
        WIDTH - 10,
        player_paddle_y + PADDLE_HEIGHT,
    )
    canvas.coords(ai_paddle, 10, ai_paddle_y, 10 + PADDLE_WIDTH, ai_paddle_y + PADDLE_HEIGHT)
    canvas.coords(
        ball, ball_x - BALL_SIZE, ball_y - BALL_SIZE, ball_x + BALL_SIZE, ball_y + BALL_SIZE
    )
    update_scoreboard()


# Function to toggle auto mode
def toggle_auto_mode():
    global auto_mode
    auto_mode = not auto_mode
    if auto_mode:
        auto_mode_button.config(bg="green")
    else:
        auto_mode_button.config(bg="SystemButtonFace")


# Main game loop
def game_loop():
    if not game_paused:
        move_ball()
        if not auto_mode:
            move_ai_paddle()
        else:
            # Auto mode - Always move paddles in sync with the ball
            global ai_paddle_y
            if ball_y > ai_paddle_y + PADDLE_HEIGHT / 2 and ai_paddle_y < HEIGHT - PADDLE_HEIGHT:
                ai_paddle_y += BASE_PADDLE_SPEED
            elif ball_y < ai_paddle_y + PADDLE_HEIGHT / 2 and ai_paddle_y > 0:
                ai_paddle_y -= BASE_PADDLE_SPEED
            canvas.coords(ai_paddle, 10, ai_paddle_y, 10 + PADDLE_WIDTH, ai_paddle_y + PADDLE_HEIGHT)
            canvas.coords(player_paddle, WIDTH - PADDLE_WIDTH - 10, ai_paddle_y, WIDTH - 10, ai_paddle_y + PADDLE_HEIGHT)

        window.after(10, game_loop)


# Button creation
button_frame = tk.Frame(window)
button_frame.pack()

start_pause_button = tk.Button(button_frame, text="Start/Pause", command=toggle_pause)
start_pause_button.pack(side="left")

restart_button = tk.Button(button_frame, text="Restart", command=restart_game)
restart_button.pack(side="left")

auto_mode_button = tk.Button(button_frame, text="Auto Mode", command=toggle_auto_mode)
auto_mode_button.pack(side="left")

# Bind keys for player movement
window.bind("<KeyPress-Up>", move_player_paddle)
window.bind("<KeyPress-Down>", move_player_paddle)
window.bind("<KeyRelease-Up>", move_player_paddle)
window.bind("<KeyRelease-Down>", move_player_paddle)

# Start the GUI
window.mainloop()