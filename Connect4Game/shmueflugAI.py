import Connect4Game as Game
import random


class RandomStrategy(Game.Connect4GameStrategy):
    def __init__(self, name="Shmuel Flug"):
        self.name = name

    @classmethod
    def strategy(cls, game_safety_copy):
        smart_moves = []
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dr, dc in directions:
            #checks in each direction if there are four open spaces or spaces of current players color
            count = 0
            #this variable stores how many of the spaces in the row are filled in with the players color
            winspaces=0
            row = game_safety_copy.row
            col = game_safety_copy.col
            row = row - dr * 3
            col = col - dc * 3
            for _ in range(7):
                if (0 <= row < 6 and 0 <= col < 7 and game_safety_copy.board[row][col] == 0 or 0 <= row < 6 and 0 <= col
                        < 7 and game_safety_copy.board[row][col] == game_safety_copy.current_player):
                    count += 1
                    if 0 <= row < 6 and 0 <= col < 7 and game_safety_copy.board[row][col] == game_safety_copy.current_player:
                        winspaces+=1
                    if count == 4:
                        #adds the space to a list of possible winning spaces with a number epending on how many
                        # are already filled in
                        smart_moves.append((winspaces,col))
                        winspaces = 0
                        count = 0
                    else:
                        winspaces = 0
                        count = 0
                        row += dr
                        col += dc
            #reverses the list so that the move with the least white spaces needed to get four in
            # a row is first and then returns that space
        smart_moves.sort(reverse = True)
        best_move = smart_moves[0][1]
        return best_move

