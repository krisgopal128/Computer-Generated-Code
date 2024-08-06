## Input:

Recreate a classic Ping Pong game with a graphical user interface (GUI) using Python and the Tkinter library. The game should feature two paddles, a ball, and a scoreboard.

## Gameplay:

The game involves two paddles, one controlled by the player (right side) and the other controlled by an AI (left side).

The ball bounces between the paddles and the top/bottom walls of the window.

Points are awarded to the player or AI if the ball passes beyond the opponent's paddle.

The player's paddle moves vertically using the Up and Down arrow keys.

The AI paddle moves automatically to track the ball's vertical position.

## GUI Features:

Game Window: A rectangular canvas displaying the paddles, ball, and boundaries.

Scoreboard: Displays the current score for the player and AI, updating in real-time.

Buttons:

Start/Pause: Toggles between starting and pausing the game. The button label should dynamically change to reflect the current state.

Restart: Resets the game to its initial state, including the score.

Auto Mode: Activates an "auto" mode for the player's paddle, mirroring the AI's movements. This allows for a two-player mode where both paddles are controlled automatically.

AI Paddle Behavior:

The AI paddle should attempt to keep its center aligned with the ball's vertical position.

The AI paddle's speed should be moderate, allowing the player a chance to score.

Auto Mode:

In auto mode, the player's paddle will mimic the AI's movement, effectively making it a two-player game where both paddles are controlled automatically.

## User Guide:

Requirements: Python 3.x and the Tkinter library (usually included with Python).

To Play:

Run the Python script.

Click the "Start" button or press any arrow key to begin.

Use the Up and Down arrow keys to control the player's paddle.

Click the "Auto Mode" button to activate auto mode for the player's paddle.

Click the "Restart" button to start a new game.

## File Generation:

Generate a single Python file named ping_pong.py containing the complete code for the Ping Pong game, incorporating all the specified features and functionality.

## User Guide:

Include a concise user guide within a comment block at the end of the ping_pong.py file. This guide should explain the game's controls, features, and basic rules, as outlined above.

Ensure the code is well-documented with comments explaining the purpose of each section and function.