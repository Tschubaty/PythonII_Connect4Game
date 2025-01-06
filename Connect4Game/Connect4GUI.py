import tkinter as tk
from tkinter import messagebox
import Connect4Game as game
import DanielBatyrevAI as DanielAI
import copy
random_choice = DanielAI.RandomStrategy()
yosef_choice = YosefAI.AI_strategy()
shmuli_choice = ShmulyAI.NotRandomStrategy()

class Connect4GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect 4")
        self.game = game.Connect4Game()

        self.buttons = []
        for col in range(7):
            button = tk.Button(master, text=str(col + 1), command=lambda c=col: self.make_move(c))
            button.grid(row=0, column=col)
            self.buttons.append(button)

        self.canvas = tk.Canvas(master, width=7 * 60, height=6 * 60)
        self.canvas.grid(row=1, column=0, columnspan=7)
        self.draw_board()



    def make_move(self, column):
        self.game.make_move(column)
        self.draw_board()
        if self.game.winner is not None:
            winner_text = f"Player {self.game.winner} wins!"
            messagebox.showinfo("Game Over", winner_text)
            self.master.destroy()
        else:
            game_copy = copy.deepcopy(self.game)
            self.game.make_move(shmuli_choice.strategy(game_copy))
            self.draw_board()
            if self.game.winner is not None:
                winner_text = f"Player {self.game.winner} wins!"
                messagebox.showinfo("Game Over", winner_text)
                self.master.destroy()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(6):
            for col in range(7):
                x0, y0 = col * 60, row * 60
                x1, y1 = x0 + 60, y0 + 60
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

                if self.game.board[row][col] == 1:
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="red", outline="red")
                elif self.game.board[row][col] == 2:
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="yellow", outline="yellow")

        for col in range(7):
            if self.game.board[0][col] == 0:
                self.buttons[col]["state"] = tk.NORMAL
            else:
                self.buttons[col]["state"] = tk.DISABLED


if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()
