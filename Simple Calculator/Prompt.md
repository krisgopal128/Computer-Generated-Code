# Input:

Recreate a classic Snake game with a graphical user interface (GUI) using Python and the Tkinter library. The game should include the following features:

# Gameplay:
The game starts with a snake of length 3, moving in a rightward direction.
The snake moves continuously within a square grid.
Food appears randomly on the grid.
The snake grows longer each time it consumes food.
The game ends if the snake collides with the boundaries of the grid or itself.

Controls:
Arrow keys: Control the snake's direction (Up, Down, Left, Right).
Spacebar: Toggle between Start and Pause.

GUI Features:
Game Window: A square grid that displays the snake, food, and boundaries.
Scoreboard: Displays the current score, updating in real-time.
Buttons:
Start/Pause: Starts/pauses the game. The button label dynamically changes to reflect the current state.
Restart: Resets the game to its initial state.
Auto: Activates automatic snake movement. Disables upon user intervention with arrow keys.

Auto Mode:
The snake moves automatically, prioritizing directions that move it closer to the food.
It avoids immediate collisions with the boundaries and itself by analyzing possible directions.
If no clear path to the food exists, it chooses a random direction to avoid getting stuck.

# User Guide:
Requirements: Python 3.10 and the Tkinter library (usually included with Python).

To Play:
Run the Python script.
Click the "Start" button to begin or press any arrow key.
Use the arrow keys to control the snake's direction.
Press the Spacebar key to pause/unpause the game.
Click the "Auto" button to enable automatic snake movement.
Click the "Restart" button to start a new game.

Game Rules:
The snake grows each time it eats food.
The game ends if the snake collides with the boundaries or itself.

# File Generation:

Generate a single Python file named snake_game.py containing the complete code for the Snake game, incorporating all the specified features and functionality.

User Guide:

Include a concise user guide within a comment block at the end of the snake_game.py file. This guide should explain the game's controls, features, and basic rules, as outlined above.

Ensure that the code is well-documented with comments explaining the purpose of each section and function.