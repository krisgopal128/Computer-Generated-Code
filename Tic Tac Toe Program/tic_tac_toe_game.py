import tkinter as tk
from random import randint

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.geometry("365x485")

        self.player_turn = True
        self.game_mode = "computer"
        self.game_over_flag = False  # <--- Add this flag to track game over status
        self.player_score = 0
        self.computer_score = 0

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.window, command=lambda row=i, column=j: self.click(row, column), height=8, width=16)
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset)
        self.reset_button.grid(row=3, column=1)

        self.play_with_friends_button = tk.Button(self.window, text="Play with Friend", command=self.play_with_friends, wraplength=100)
        self.play_with_friends_button.grid(row=4, column=1)

        self.scoreboard = tk.Label(self.window, text="Player: 0 - Computer: 0", font=('Helvetica', 24))
        self.scoreboard.grid(row=5, column=0, columnspan=3)  # <--- Overlay the scoreboard

    def play_with_friends(self):
        self.game_mode = "friends"
        self.reset()

    def click(self, row, column):
        if self.buttons[row][column]['text'] == "" and not self.game_over_flag:  # <--- Check game over flag
            if self.game_mode == "computer":
                self.buttons[row][column]['text'] = "X"
                self.check_win()
                if not self.game_over_flag:  # <--- Check game over flag before computer move
                    self.computer_move()
            elif self.game_mode == "friends":
                if self.player_turn:
                    self.buttons[row][column]['text'] = "X"
                else:
                    self.buttons[row][column]['text'] = "O"
                self.player_turn = not self.player_turn  # switch turns
                self.check_win()

    def computer_move(self):
        possible_moves = []
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]['text'] == "":
                    possible_moves.append((i, j))
        if possible_moves:
            move = self.minimax(possible_moves)
            self.buttons[move[0]][move[1]]['text'] = "O"
            self.check_win()

    def minimax(self, possible_moves):
        best_move = None
        best_score = -float('inf')
        for move in possible_moves:
            self.buttons[move[0]][move[1]]['text'] = "O"
            score = self.evaluate_board()
            self.buttons[move[0]][move[1]]['text'] = ""
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def evaluate_board(self):
        score = 0
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]['text'] == "O":
                    score += 1
                elif self.buttons[i][j]['text'] == "X":
                    score -= 1
        return score

    def check_win(self):
        for i in range(3):
            if self.buttons[i][0]['text'] == self.buttons[i][1]['text'] == self.buttons[i][2]['text'] != "":
                self.game_over(self.buttons[i][0]['text'])
                return
            if self.buttons[0][i]['text'] == self.buttons[1][i]['text'] == self.buttons[2][i]['text'] != "":
                self.game_over(self.buttons[0][i]['text'])
                return
        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != "":
            self.game_over(self.buttons[0][0]['text'])
            return
        if self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != "":
            self.game_over(self.buttons[0][2]['text'])
            return

    def game_over(self, winner):
        self.game_over_flag = True  # <--- Set game over flag
        for row in self.buttons:
            for button in row:
                button['state'] = 'disabled'
        if winner == "X":
            self.player_score += 1
            self.scoreboard['text'] = f"Player: {self.player_score} - Computer: {self.computer_score}"
            print("Player wins!")
            return  # <--- Add this line to prevent multiple prints
        else:
            self.computer_score += 1
            self.scoreboard['text'] = f"Player: {self.player_score} - Computer: {self.computer_score}"
            print("Computer wins!")

    def reset(self):
        self.game_over_flag = False  # <--- Reset game over flag
        for row in self.buttons:
            for button in row:
                button['text'] = ""
                button['state'] = 'normal'
        self.player_turn = True

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
