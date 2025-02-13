import Connect4Game as Game


class AI_strategy(Game.Connect4GameStrategy): 
    """
    This class inherits from the abstract class Connect4GameStrategy and provides implementaion of the strategy method.
    
    Instance Variables
    ------------------
    self.name: (str) 
              Optional parameter with default value
    
    Methods
    -------
    
    strategy: This method recieves the Connect4Game class or a copy of it and returns the optimal 
               next move based on the current game state.
               
    is_line: This method checks for a line of length(x) in direction(y) for a given value.
    
    is_line_blocked: 
    
    """ 
    def __init__(self, name="Yosef Birnbaum"):
        self.name = name
        
        
    def strategy(self, game_safety_copy):
        """
        This method recieves a Connect4Game class or a copy of it and returns the optimal next
        next move by analyzing the benefits and drawbacks of each move.
        
        Parameters
        ----------
        game_safety_copy (object):
                An instance of the Connect4Game class.
                
        Returns
        -------
        int: a number representing the column of the move to make
        """
        
        # variables to hold the game board and current player, which are retreived from the Connect4Game instance,
        # and a variable for opponent 
        state = game_safety_copy.board
        current_player = game_safety_copy.current_player
        opponent = 3 - current_player
    
    
        # create list of open cols. (I am aware that the instance has a methods for this, but using those methods proved to be more difficult).
        # iterate through each col in board and if the top row (the first sublist indexed at 0) has an open space, indicating
        # additional moves available in that column, append the col to list.
        open_cols = []
        for col in range(7):              
            if state[0][col] == 0:
                open_cols.append(col)
            
                
        # create list of available next moves on the game board by iterating through all cols in open_cols list
        # and through all the rows, starting from the bottom-most row of board(indexed at 5) up to the top.
        # when each empty col/row index is found append them as sublists to the av_moves list. Once index is
        # found, break out of loop since we only want the bottom-most empty space in the col.
        av_moves = []                       
        for col in open_cols:
            for row in range(5, -1, -1):
                if state[row][col] == 0:
                    av_moves.append([row,col])     
                    break 
        
                                      
        # creat a list to hold the scores of each column's move. the list will have sublists each containing a column and a posotive or negative 
        # number. A column isn't limited to one sublist but can have as many as needed based on its impact on the game.
        # iterate through the available moves list to extract the indexes of each row/col combination and make the move 
        # on the gameboard with the number of the current player who represents the AI.
        scores = []  
        for i in av_moves:
            state[i[0]][i[1]] = current_player              
            
            
        # here we evaluate various game states and assign scores accordingly. 
        # By looping throug all direction possibilites and calling the is_line method to check for winning line of four, 
        # we can assign highest number in the scoring for a win.  
            directions = [(1, 1), (-1, 1), (0, 1), (1, 0)]
            if any(self.is_line(state, 4, i[0], i[1], dr, dc, current_player) for dr, dc in directions):
        # append the first element of current available move in av_moves (which is the col) to scores list, and append a score.
                    scores.append([i[1], 200000])
     
            
        # In this section we will check for lines of three and assign scores to moves that create them. we also call the is_line_blocked method
        # to check if a line has no potential to become a winning line of four
        # for a diagnol line (represented by moving in both the row and col directions) give higher score since it is less apparent 
        # than horizontal or vertical lines
            if self.is_line(state, 3, i[0], i[1], 1, 1, current_player) and not self.is_line_blocked(state, i[0], i[1], 1, 1, current_player):
                    scores.append([i[1], 3000])  
            if self.is_line(state, 3, i[0], i[1], -1, 1, current_player) and not self.is_line_blocked(state, i[0], i[1], -1, 1, current_player):
                    scores.append([i[1], 3000]) 
        
                    
        # for horizontal lines
            if self.is_line(state, 3, i[0], i[1], 0, 1, current_player) and not self.is_line_blocked(state, i[0], i[1], 0, 1, current_player): 
        # give slightly higher score to horizontal than vertical since it can be used in a double trap as opposed to vertical
                    scores.append([i[1], 2800])
        
                    
        # for vertical lines
        # if a line of three is only completed on top row, will not lead to win so the row must be greater than the index of the top row
            if self.is_line(state, 3, i[0], i[1], 1, 0, current_player) and i[0] > 0:
                    scores.append([i[1], 2500]) 
        
                
        # here we will check for lines of two.
        # give diagnol higher score than straight since the ai will be told that the middle col is the best, it can get itself
        # caught in a double trap if it favors the vertical line of two in the middle column which would leave the bottom
        # of the borad open for a double trap. But by scoring the diagnol higher it will choose bottom of board.           
            if self.is_line(state, 2, i[0], i[1], 1, 1, current_player) and not self.is_line_blocked(state, i[0], i[1], 1, 1, current_player): 
                    scores.append([i[1], 1000])
            if self.is_line(state, 2, i[0], i[1], -1, 1, current_player) and not self.is_line_blocked(state, i[0], i[1], -1, 1, current_player):
                    scores.append([i[1], 1000]) 
        
                    
        # for vertical line            
        # if line of two is only completed on second to top row it will not lead to a win
        # here the is_line_blocked isn't  called since above the current space cannot be occupied by opponent, and the problem of not 
        # being a potential winning line becauses of being off the board is addressed by the making sure we are past col 1.     
            if self.is_line(state, 2, i[0], i[1], 1, 0, current_player) and i[0] > 1: 
                    scores.append([i[1], 900])                                  
            if self.is_line(state, 2, i[0], i[1], 0, 1, current_player) and not self.is_line_blocked(state, i[0], i[1], 0, 1, current_player):
                    scores.append([i[1], 900])
                    
        
        # assign higher scores to middle col and cols closer to middle since they have more potential. The amounts added are minimal
        # so they will only cause changes if all else is equal
            if i[1] == 3:
                scores.append([i[1], 50] )
            if i[1] == 2 or i[1] == 4:
                    scores.append([i[1], 40])  
            if i[1] < 2 or i[1] > 4:
                    scores.append([i[1], 30])
                    
            
        # continue game one move into the future and test if current chosen move based on the previous scoring (or the scoring outlined 
        # below) will produce a winning opportunity for opponent.            
        # assign negative scores for moves that will result it opponent winning or getting posotive game state
        # make move for opponent in the spot just made available by our previous move by using index for row above 
        # (which is below in list, hence subtract one)
            state[i[0] - 1][i[1]] = opponent 
            if (self.is_line(state, 4, i[0] - 1, i[1], 1, 1, opponent) or self.is_line(state, 4, i[0] -1, i[1], -1, 1, opponent) or
                self.is_line(state, 4, i[0] -1 , i[1], 0, 1, opponent) or self.is_line(state, 4, i[0] - 1, i[1], -1, 0, opponent)):
        # if it sets up a win assign largest negative score in scoring 
                    scores.append([i[1], -150000])
                    
                    
        # check for line of three made available and assign negative score. ABS of Score is less than ai attaining three itself or
        # stoppin opponent from actually getting three.
        # for these potential threats no disticntion is made between diagnol and horizontal
            
            if (self.is_line(state, 3, i[0] - 1, i[1], 1, 1, opponent)  or
                self.is_line(state, 3, i[0] - 1, i[1], -1, 1, opponent) or
                self.is_line(state, 3, i[0] - 1, i[1], 1, 0, opponent)  or
                self.is_line(state, 3, i[0] - 1, i[1], 0, 1, opponent)):
        # assign negative score for potential line of three
                scores.append([i[1], -900])
           

        # check for line of two also
            if (self.is_line(state, 2, i[0] - 1, i[1], 1, 1, opponent) or
                self.is_line(state, 2, i[0] - 1, i[1], -1, 1, opponent) or
                self.is_line(state, 2, i[0] - 1, i[1], 1, 0, opponent)  or
                self.is_line(state, 2, i[0] - 1, i[1], 0, 1, opponent)):
        # negative score for two 
                scores.append([i[1], -600])
          
          
        # restore game state back to how it was to now test what would happen if oppononet would choose the original spot (for each available move)
        # first undo second move and then first move
            state[i[0] - 1][i[1]] = 0     
            state[i[0]][i[1]] = 0
           
        
        # once againg iterate through all availabel moves and have opponent choose it
        for i in av_moves:
            state[i[0]][i[1]] = opponent
            
        
        # if opponent would win assign score second only to winning score            
            if (self.is_line(state, 4, i[0], i[1], 1, 1, opponent) or self.is_line(state, 4, i[0], i[1], -1, 1, opponent) or
                self.is_line(state, 4, i[0], i[1], 0, 1, opponent) or self.is_line(state, 4, i[0], i[1], -1, 0, opponent)): 
                    scores.append([i[1], 100000])
            
            
        # if opponent would get line of three assign score to stop it (score is obviously lower than ai itself getting three)
            if (((self.is_line(state, 3, i[0], i[1], 1, 1, opponent) and not self.is_line_blocked(state, i[0], i[1], 1, 1, opponent))
                or (self.is_line(state, 3, i[0], i[1], -1, 1, opponent) and not self.is_line_blocked(state, i[0], i[1], -1, 1, opponent))
                or  (self.is_line(state, 3, i[0], i[1], 0, 1, opponent) and not self.is_line_blocked(state, i[0], i[1], 0, 1, opponent))
                or  (self.is_line(state, 3, i[0], i[1], 1, 0, opponent)) and not self.is_line_blocked(state, i[0], i[1], 1, 0, opponent))): 
                    scores.append([i[1], 1500])
        
        
        # same for line of two               
            if  (((self.is_line(state, 2, i[0], i[1], 1, 1, opponent) and not self.is_line_blocked(state, i[0], i[1], 1, 1, opponent))
                or (self.is_line(state, 2, i[0], i[1], -1, 1, opponent) and not self.is_line_blocked(state, i[0], i[1], -1, 1, opponent))
                or  (self.is_line(state, 2, i[0], i[1], 0, 1, opponent) and not self.is_line_blocked(state, i[0], i[1], 0, 1, opponent))
                or  (self.is_line(state, 2, i[0], i[1], 1, 0, opponent)) and not self.is_line_blocked(state, i[0], i[1], 1, 0, opponent))): 
                    scores.append([i[1], 500])
        
                    
        # undo move after all tests are completed for a move and a score was assgined to have accurate game state 
        # to test the next possible move       
            state[i[0]][i[1]] = 0
        
        
        # extract all columns of available moves in the scores list. 
        # Since every column that impacted the game as directed by the tests had anohter sublist added to the scores list, we must 
        # get all the unique columns to be able to sum the total score for each column. 
        # we use the set function (which only allows unique values) for the first element of each sublist in the scores list.
        keys = set([x[0] for x in scores])
        
        
        # initialize dictionary to hold each move and its score
        results = {}
        
        
        # populate the dictionary with all available moves and their scores.
        # iterate through all dictionary keys (columns) and sum the second element of the scores sbulists (which are the scores) 
        # if the first element equals the current key. assign the sum as the value of that key  
        for i in keys:
                results [i] = sum([x[1] for x in scores if x[0] == i])
                
        # get the key (col) with the maximum score by passing results.get to the max function as a key instead of the dict keys and return the best move (col)
        move_to_make =    max(results, key=results.get)
        return move_to_make
        
        
                
    def is_line(self, game_state, size, row, col, dr, dc, player_num):
            """
        This method recieves a Connect4Game class or a copy of it and determines weather there is a line of a certain size
        in a specific direction for a given value.
        
        Parameters
        ----------
        game_safety_copy (object):
                An instance of the Connect4Game class.
        size (int):
                length of potential line 
        row (int): 
                row of current index
        col (int) 
                of current index  
        dr  (int):
                direction to move vertically
        dc  (int): 
                direction to move in hoizontally
        player_num (int):
                value to find in a line
              
        Returns
        -------
        (bool): True if line is found and False if not
            """
        # initialize a counter to hold the amount of consecutive values and reassign the values to be offset from their original 
        # positions by one less than their size to be able to complete a line of the desired size. Offsetting enables the fuction 
        # to look in different directions for a line.
            count = 0
            row -= (dr * (size - 1))
            col -= (dc * (size - 1))
            
        # iterate through amount of spaces that can contain the line from the current index which is one less than double it's size.
        # test if these spaces are on the board (since offseting especially from near the edges can be off the board) and if the desired
        # value is found. For each consecutive value found add 1 to the count and if desired size is found return player value.
            for _ in range((size * 2) - 1):
                if 0 <= row < 6 and 0 <= col < 7 and game_state[row][col] == player_num:
                    count += 1
                    if count == size:
                        return True
                
        # if any of the iterations yeild an index out of range or an opponents value, the count reverts back to zero
                else:
                    count = 0
                    
        # each iteration add one (or zero which does nothing) to the row/col index to explore the complete possible winning direction.
        # if no line is found "None" will be returned
                row += dr
                col += dc
                
        # if no line is found return False
            return False
    
    def is_line_blocked(self, game_state, row, col, dr, dc, player_num):
        """
        This method recieves a Connect4Game class or a copy of it and determines if a line of two or three is surrounded by opponents
        peices or edge of the board so that the line cannot be part of a potential line of four. (Although this method correctly determines
        if a line CANNOT be part of a line of four when it returns True , yeilding a False result can sometimes still be part of a blocked
        line due to many possibilites of being blocked.) This method just checks if it will certainly be blocked by checking the edges of 
        a five index length.
        
        Parameters
        ----------
        game_safety_copy (object):
                An instance of the Connect4Game class.
        row (int): 
                row of current index
        col (int) 
                of current index  
        dr  (int):
                direction to move vertically
        dc  (int): 
                direction to move in hoizontally
        player_num (int):
                value to find in a line
              
        Returns
        -------
        (bool): True if both positive and negative spaces on the total five index space is not useable, and False if not. 
        """
        # Check two steps further in the positive direction
        row_pos2 = row + 2 * dr
        col_pos2 = col + 2 * dc

        # Initialize as False as we will test for unusable edges and assign true if blocked
        pos2_blocked = False

        # Check if the spot is off the board or if it's occupied by the opponent's piece. If one of these conditions are met
        # then the edge in the posotive direction is blocked. Since the OR statment returns True if one condition is met, so if
        # either the positive edge isn't on the grid (hence the 'not') or the scpace is occupied by opponent, then pos2 = True
        if not(0 <= row_pos2 < 6 and 0 <= col_pos2 < 7) or game_state[row_pos2][col_pos2] == 3 - player_num:
               pos2_blocked = True


        # Same for edge in the other direction. Check two steps further in the negative direction
        row_neg2 = row - 2 * dr
        col_neg2 = col - 2 * dc

        # Initialize as False
        neg2_blocked = False

        # Same as before. Check if the spot is off the board or if it's occupied by the opponent's piece
        if not (0 <= row_neg2 < 6 and 0 <= col_neg2 < 7) or game_state[row_neg2][col_neg2] == 3 - player_num:
                neg2_blocked = True

        # if both posotive and negative edges of the total five index distance from the current space is not useable return True
        if pos2_blocked and neg2_blocked:
            return True
        else:
            return False
