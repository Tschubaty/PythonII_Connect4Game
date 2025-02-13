import random
from copy import deepcopy
import Connect4Game

class BasyaRosenthalAI(Connect4Game.Connect4GameStrategy):
    """
    Strategy: 
    This AI uses a combination of immediate win detection and the Minimax algorithm 
    with Alpha-Beta pruning to determine the best move in Connect4.
    
    Strengths:
    - Immediate Win Detection: Before running minimax, it checks for immediate winning move saving time and ensuring it wont miss definate win.
    - Minimax: Uses an optimized minimax search to evaluate board states efficiently
    - Alpha beta pruning: Uses alpha beta pruning to save time and processing power
    - Board Evaluation: Evaluates board positions based strategic importance (ex center column advantage, possible losses) 
    
    Weaknesses:
    -Not Unbeatable: Not all possiblities are coved- a good player can still beat the game (I beat it a bunch of times)
     sometimes will fall for more complex traps.
    """
   
    # initialize AI with name and search depth (for minimax)(default depth 4)
    def __init__(self, name="Basya Rosenthal", search_depth=4):
        self.name = name                    # AI name
        self.search_depth = search_depth    # max depth for minimax search


    def strategy(self, gameState):
        """
        Uses immediate win check and minimax with alpha-beta pruning to choose best move in conect4 game
       
        Args:
            gameState (Connect4Game): A copy of current game state.
       
        Returns:
            int: Column index (0-6) for the next move.
        """

        AIplayer = gameState.current_player

        # loop through each col to see if winning move available
        for col in range(7):
            #  if column is not full
            if gameState.is_valid_move(col):    
                newState = deepcopy(gameState)  # deep copy of current game state wont effect actual game
                newState.make_move(col)          # try move in that column
                if newState.winner == AIplayer: # check if player wins after this move made
                    # return winning col
                    return col

        # if no immediate win use minimax
        bestScore = float('-inf') #defaults to -infinity
        bestMove = None

        # loop through each column to evaluating moves using minimax
        for col in range(7):
            #  if column is not full
            if gameState.is_valid_move(col):
                newState = deepcopy(gameState)  # copy of the game state for testing moves
                newState.make_move(col)     # try move

                # get minimax value for current col
                score = self.minimax(newState, self.search_depth - 1, float('-inf'), float('inf'), False, AIplayer)
               
                # if this move's score is better than the best score so far update best score and best move
                if score > bestScore:
                    bestScore = score
                    bestMove = col

       
        # if no move selected with minimax choose a random valid move
        # avoids errors - especially at end of game when might not be optimal move
        if bestMove is None:
            validMoves = [col for col in range(7) if gameState.is_valid_move(col)]
            bestMove = random.choice(validMoves)
       
        return bestMove

    # recursive minimax function with alpha-beta pruning
    def minimax(self, gameState, depth, alpha, beta, maximizingPlayer, currentPlayer):
        """
        Minimax search with alpha-beta pruning.
       
        Args:
            gameState: The current game state to evaluate
            depth: Current depth 
            alpha: best value for maximizer
            beta: best value for minimizer
            maximizingPlayer: Boolean flag; True if AI turn, False for opponent
            currentPlayer: player number (1 or 2)
           
        Returns:
            int: minimax score
        """
        # return immediaetly if depth is 0 or the game state will end (win /loss /tie)
        if depth == 0 or self.isOver(gameState):
            return self.evaluateBoard(gameState, currentPlayer)

        # if maximizing player's turn
        if maximizingPlayer:
            maxEval = float('-inf')  #  defaults to -infinity.
            # loop over all columns to try possible moves
            for col in range(7):
                if gameState.is_valid_move(col):
                    newState = deepcopy(gameState)
                    newState.make_move(col)
                    # recursively call minimax for minimizing player
                    eval = self.minimax(newState, depth - 1, alpha, beta, False, currentPlayer)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    # if beta is less than or equal to alpha prune branch
                    if beta <= alpha:
                        break  
            return maxEval
        else:
            # opponent's turn (minimizing player)
            minEval = float('inf')  # defaults infinity.
            for col in range(7):
                if gameState.is_valid_move(col):
                    newState = deepcopy(gameState)
                    newState.make_move(col)
                    # recursively call minimax for maximizing player
                    eval = self.minimax(newState, depth - 1, alpha, beta, True, currentPlayer)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    # if beta is less than or equal to alpha- prune branch
                    if beta <= alpha:
                        break
            return minEval

    # checks if the current game state is over
    def isOver(self, gameState):
        """
        Checks if game is over (someone won or no moves left)
       
        Args:
            gameState (Connect4Game): current game state
       
        Returns:
            bool: True if the game is over False if not
        """

        # if there is a winner
        if gameState.winner is not None:
            return True
        # if any valid move exists, possible moves left
        for col in range(7):
            if gameState.is_valid_move(col):
                return False
        # if no valid moves return True
        return True
   
    def evaluateBoard(self, gameState, AIplayer):
        """
        Evaluates the board score based on potential wins.
       
        Args:
            gameState: game state to evaluate.
            AIplayer: AI's player number.
       
        Returns:
            int: score
        """
        # determine opponents player number (1 or 2) by doing opponent minus ai will have result 1 or 2
        #  easily switch between player 1 and player 2
        opponent = 3 - AIplayer

        # if the game state is a win for ai player return a very high score (100000)
        if gameState.winner == AIplayer:
            return 100000
        # if the opponent has won return a very low score (-100000)
        elif gameState.winner == opponent:
            return -100000
        # If the game over and no one wins return 0.
        elif self.isOver(gameState):
            return 0

        board = gameState.board 
        score = 0

        # adding points to score depending on the col
        # center column is usually more valuable in Connect4 because pieces there is more potential

        centerCol = [board[r][3] for r in range(6)]  # middle column (column index 3)
        centerCount = centerCol.count(AIplayer)      # how many of our pieces are in the center
        score += centerCount * 3                     # higher score for pieces in center

        # ----- evaluate horizontal groups -----
        # group of 4 cells along each row
        for r in range(6):
            for c in range(7 - 3):  # 7-3 ensure group of 4 cells
                group = [board[r][c+i] for i in range(4)]
                score += self.evaluateGroup(group, AIplayer)

        # ----- evaluate vertical groups -----
        # group of 4 cells along each col
        for r in range(6 - 3):  #  group is within bounds
            for c in range(7):
                group = [board[r+i][c] for i in range(4)]
                score += self.evaluateGroup(group, AIplayer)

        # ----- evaluate down diagonals (\\) -----
        for r in range(6 - 3):
            for c in range(7 - 3):
                group = [board[r+i][c+i] for i in range(4)]
                score += self.evaluateGroup(group, AIplayer)

        # ----- evaluate up diagonals (/) -----
        for r in range(3, 6):  # start at row 3 up to last row
            for c in range(7 - 3):
                group = [board[r-i][c+i] for i in range(4)]
                score += self.evaluateGroup(group, AIplayer)

        # return final score 
        return score

    # evaluates a single group (4 cells) returns a score
    def evaluateGroup(self, group, AIplayer):
        """
        Scores a group of 4 cells
       
        Args:
            group (list): A list of 4 cells from the board.
            AIplayer (int): The AI's player number.
       
        Returns:
            int: Score of group
        """
        score = 0
        opponent = 3 - AIplayer

        # if all 4 cells belong to ai player
        if group.count(AIplayer) == 4:
            score += 100
        # if there are 3 of our pieces and one empty space, it is pretty good
        elif group.count(AIplayer) == 3 and group.count(0) == 1:
            score += 5
        # If there are 2 of our pieces and two empty spaces it is ok not bad
        elif group.count(AIplayer) == 2 and group.count(0) == 2:
            score += 2

        # if opponent is close to winning (3 opponent pieces and 1 empty),
        # subtract points
        if group.count(opponent) == 3 and group.count(0) == 1:
            score -= 4

        # return  score for group
        return score
