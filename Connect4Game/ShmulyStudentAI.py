"""Creates an AI that can use a random minimax strategy and a non-random minimax strategy"""
#Imports the rules of the game from Connect4Game.py
import Connect4Game as Game
#Imports random
import random

#Use inheritance to inherit the functions from Connect4GameStrategy
class RandomStrategy(Game.Connect4GameStrategy):
    """Creates an AI that uses a random strategy"""
    #Default the name to Shmuly Student
    def __init__(self, name="Shmuly Student"):
        #Call the __init__ from the base class
        super().__init__()
        #Set the name
        self.name = name
    #Use classmethod to create an instance of the class
    @classmethod
    #Take in the copy of the rules
    def strategy(cls, game_safety_copy):
        #Create a list
        valid_moves = list()
        #Loop 7 times
        for col in range(7):
            #If the move is valid
            if game_safety_copy.is_valid_move(col):
                #Append the move
                valid_moves.append(col)
        #Return a random choice out of the valid moves
        return random.choice(valid_moves)

#Use inheritance to inherit the functions from Connect4GameStrategy
class NotRandomStrategy(Game.Connect4GameStrategy):
    """Creates an AI that uses a non-random strategy"""
    #Default the name to Shmuly Student
    def __init__(self, name="Shmuly Student"):
        #Call the __init__ from the base class
        super().__init__()
        #Set the name
        self.name = name
    def strategy(self, game_safety_copy):
        """Takes in the copy of the rules to make the strategy for finding the best move"""
        #Set alpha to -inf so it can get better
        alpha = float('-inf')
        #Set beta to inf so it can get worse
        beta = float('inf')
        #Set depth to 4 because 5 goes too slowly
        depth = 4
        #Initialize best move to be any move, like the first available move
        best_move = self.get_available_moves(game_safety_copy)[0]
        #Set best value to -inf so it can get better
        best_value = float('-inf')
        #Call the minimax function to get the best move
        #Loop through every move
        for available_move in self.get_available_moves(game_safety_copy):
            #Do the move using the rules from game_safety_copy
            #and using the column of the available move
            self.try_move(available_move, game_safety_copy)
            #Call minimax
            value = self.minimax_strategy(alpha, beta, depth - 1, False, game_safety_copy, available_move)
            #Reset the board
            self.undo_move(available_move, game_safety_copy)
            #Get the best value and best move
            if value > best_value:
                best_value = value
                best_move = available_move
        #Return the best move
        return best_move

    def minimax_strategy(self, alpha, beta, depth, maximizing_player, game_safety_copy, available_move):
        """Does the minimax calculation to find the best and worst moves for the maximizing player
        and does alpha-beta pruning by taking in alpha, beta, the current depth, whether the current
        player is the maximizing player, the copy of the rules, and the current column of the move
        that we're trying"""
        #First check if there's a win
        #Set the row to 0
        available_move_row = 0
        #Go through all of the rows in the column of the move that was just done
        for row in range(6):
            #The first row to be filled is where our move just went
            if game_safety_copy.board[row][available_move] != 0:
                #Get the row
                available_move_row = row
                #Break the loop
                break
        #Check if there was a win in the move that was just done using the row and column
        if game_safety_copy.check_winner(available_move_row, available_move):
            #If there was
            #If maximizing player is True, then the opponent just went. Therefore, return -inf
            if(maximizing_player):
                return float('-inf')
            #If maximizing player is False, then the player just went. Therefore, return inf           
            else:
                return float('inf')
        #Now check if the depth is 0
        if depth == 0:
            #If it is, get the score and end the loop
            return self.evaluate_board(maximizing_player, game_safety_copy)
     
        #Set up the variable of the possible moves to loop through
        possible_moves = self.get_available_moves(game_safety_copy)
        #If it's the maximizing player's turn
        if maximizing_player:
            #Set the max value to -inf so it can get better
            max_value = float('-inf')
            #Loop through the possible moves
            for move in possible_moves:
                #Switch current player from opponent to player
                game_safety_copy.current_player = 3 - game_safety_copy.current_player
                #Try the move using the rules from game_safety_copy
                self.try_move(move, game_safety_copy)
                #Get the score by recursively calling the minimax function with depth minus
                #1 and with maximizing player being False to go to the opponent's move
                value = self.minimax_strategy(alpha, beta, depth - 1, not maximizing_player, game_safety_copy, move)
                #Undo the move that was tried
                self.undo_move(move, game_safety_copy)
                #Switch back to the original player
                game_safety_copy.current_player = 3 - game_safety_copy.current_player
                #Return the larger of the values and assign it to max_value
                max_value = max(max_value, value)
                #Return the larger of the values and assign it to alpha
                alpha = max(alpha, max_value)
                #If beta is less than alpha, it won't be chosen
                if beta <= alpha:
                    #Therefore, break
                    break
            #Return the max value
            return max_value
        #If it's the minimizing player's turn
        else:
            #Set the min value to inf so it can get worse
            min_value = float('inf')
            #Loop through the possible moves
            for move in possible_moves:
                #Switch current player from player to opponent
                game_safety_copy.current_player = 3 - game_safety_copy.current_player
                #Try the move using the rules from game_safety_copy
                self.try_move(move, game_safety_copy)
                #Get the score by recursively calling the minimax function with depth minus
                #1 and with maximizing player being True to go to the player's move
                value = self.minimax_strategy(alpha, beta, depth - 1, not maximizing_player, game_safety_copy, move)
                #Undo the move that was tried
                self.undo_move(move, game_safety_copy)
                #Switch back to the original player
                game_safety_copy.current_player = 3 - game_safety_copy.current_player
                #Return the smaller of the values and assign it to min_value
                min_value = min(min_value, value)
                #Return the smaller of the values and assign it to beta
                beta = min(beta, min_value)
                #If beta is less than alpha, it won't be chosen
                if beta <= alpha:
                    #Therefore, break
                    break
            #Return the min value
            return min_value
     
    def try_move(self, column, game_safety_copy):
        """Does a move for the minimax by taking in the column 
        of the move and the rules from game_safety_copy"""
        #Loop through the rows from the bottom up in the column to do the move
        for row in range(5, -1, -1):
            #The first row to be empty
            if game_safety_copy.board[row][column] == 0:
                #Set it to your number
                game_safety_copy.board[row][column] = game_safety_copy.current_player
                #Break out of the loop
                break

    def undo_move(self, column, game_safety_copy):
        """Undo the move that was just done by taking in the column
        of the move and the rules from game_safety_copy"""
        #Loop through the rows from the top down in the column to undo the move
        for row in range(6):
            #The first row to be filled
            if game_safety_copy.board[row][column] != 0:
                #Change to 0 to unfill it
                game_safety_copy.board[row][column] = 0
                #Break the loop
                break

    def get_available_moves(self, game_safety_copy):
        """Get the available moves using the rules from game_safety_copy"""
        #Create a list
        valid_moves = list()
        #Loop through the columns
        for col in range(7):
            #If the move is valid
            if game_safety_copy.is_valid_move(col):
                #Append the move
                valid_moves.append(col)
        #Return the list of valid moves
        return valid_moves
    
    def evaluate_board(self, is_maximizing, game_safety_copy):
        """Evaluate the desirability of the current board state by taking in whether
        the current player is maximizing and the rules from game_safety_copy"""
        #Set the score to 0
        score = 0
        #Check each position on the board for potential winning lines
        for row in range(6):
            for col in range(7):
                #If the position is empty
                if game_safety_copy.board[row][col] == 0:
                    #Check the desirability of the empty position
                    score += self.evaluate_position(row, col, is_maximizing, game_safety_copy)

        return score

    def evaluate_position(self, row, col, is_maximizing, game_safety_copy):
        """Evaluate the desirability of a specific position by taking in the row and column of
        the move and whether the current player is maximizing and the rules from game_safety_copy"""
        #Set the score to 0
        score = 0
        #Set the player to the current player
        player = game_safety_copy.current_player
        #Set the opponent to the opponent
        opponent = 3 - game_safety_copy.current_player
        #Set up the four directional components
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        #Loop through each direction
        for dr, dc in directions:
            #Check lines for a win
            #Set the player count to 0
            count_player = 0
            #Set the opponent count to 0
            count_opponent = 0
            #Set up the temporary row and column
            temp_row, temp_col = row - dr * 3, col - dc * 3
            #Loop seven times to cover all spots that could be part of a win, including the current move
            for _ in range(7):
                #If the move is good
                if 0 <= temp_row < 6 and 0 <= temp_col < 7:
                    #If the position belongs to the player
                    if game_safety_copy.board[temp_row][temp_col] == player:
                        #Add 1
                        count_player += 1
                    #If the position belongs to the opponent
                    elif game_safety_copy.board[temp_row][temp_col] == opponent:
                        #Add 1
                        count_opponent += 1
                    #Adjust the score based on the count
                    score += self.score_for_count(count_player, count_opponent)
                #Change the temporary row and column
                temp_row += dr
                temp_col += dc
        #If is maximizing is True, we're analyzing the opponent's move
        if is_maximizing:
            #Therefore, return -score
            return -score
        #If is maximizing is False, we're analyzing the player's move
        else:
            #Therefore, return score
            return score

    def score_for_count(self, count_player, count_opponent):
        """Assign a score based on the count of discs in a
        line by taking in the count of player and opponent"""
        #Potential winning move in the next turn
        if count_player == 3:
            #Return 100
            return 100
        #Good position
        if count_player == 2:
            #Return 10
            return 10
        #Basic position
        if count_player == 1:
            #Return 1
            return 1
        #Potential winning move in the next turn
        if count_opponent == 3:
            #Return -100
            return -100
        #Good position
        if count_opponent == 2:
            #Return -10
            return -10
        #Basic position
        if count_opponent == 1:
            #Return -1
            return -1
        #If none of these, return 0
        return 0
