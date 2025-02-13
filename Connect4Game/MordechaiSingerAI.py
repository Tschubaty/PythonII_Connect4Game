# I had actually started working on this last monday, when I thought that the first entry had been graded
# So I had a few days of work before I emailed about it last wednesday. When you said it hadn't been graded
# I resubmitted the original work. You are of course correct that it hadn't been tested. For some reason,
# I was unable to get my original copy of your program to work with my ai. I should have contacted you about that
# instead of submitting untested code. Anyway, this code has been tested and works fairly well.


import Connect4Game as Game
import copy

class MinimaxStrategy(Game.Connect4GameStrategy):
    """
    Class contains methods to employ the minimax strategy, and alpha beta pruning
    to plan several moves ahead and select the best one.

    Attributes
    ----------
    name : str
        name of strategy

    Methods
    -------
    strategy(cls, game_safety_copy):
        Code for strategy, receives and outputs best possible move.

    _minimax(cls, game_state, depth, alpha, beta, maximizing_player):
        Code that does main minimax loop for each potential move.

    _evaluate_board(cls, game_state):
        evaluates board state and returns heuristic score
    """

    def __init__(self, name="Mordechai Singer"):
        """
        Initializes Strategy instance with a given name.
        
        Args:
            name (str): The name of the strategy or its creator. Defaults to "Mordechai Singer".
        """
        self.name = name  # Store the name of the strategy

    @classmethod
    def strategy(cls, game_safety_copy):
        """
        Code for strategy, receives and outputs best possible move.

        Args:
            game_safety_copy (Connect4Game): safe copy of current game state

        Returns:
            int: The column of the best move
        """
        depth = 6  # maximum search depth
        alpha = float('-inf')  # initializes alpha as negative infinity
        beta = float('inf')  # initializes beta as positive infinity
        
        valid_moves = list()  # list to store all columns where move is valid
        for col in range(7):  # iterate over all columns in Connect4 board
            if game_safety_copy.is_valid_move(col):  # check if column is valid 
                valid_moves.append(col)  # add valid columns to list

        # check in case of next move being a winning move for ai or player
        for col in valid_moves:
            # check for ai win in next move
            game_copy = copy.deepcopy(game_safety_copy)
            game_copy.make_move(col)
            if game_copy.winner == game_copy.current_player:
                return col  # do winning move
            
            # check if player wins in  next move
            game_copy = copy.deepcopy(game_safety_copy)
            opponent = 3 - game_copy.current_player  # calculate opponent's player number
            game_copy.current_player = opponent  # temporarily switch to opponent
            game_copy.make_move(col)
            if game_copy.winner == opponent:
                return col  # block opponent's winning move

        best_score = float('-inf')  # initialize best score as negative infinity
        best_move = valid_moves[0]  # ensure we always have a valid move to return

        # evaluate all possible moves
        for col in valid_moves:  # iterate through all valid moves
            game_copy = copy.deepcopy(game_safety_copy)  # create copy of game state
            game_copy.make_move(col)  # simulate making move
            
            score = cls._minimax(game_copy, depth - 1, alpha, beta, False)  # evaluate move
            
            if score > best_score:  # update best score and move if current move is better
                best_score = score
                best_move = col
            
            alpha = max(alpha, best_score)  # update alpha value for pruning
            if beta <= alpha:  # prune search tree if beta is less than or equal to alpha
                break

        return best_move  # return best move

    @classmethod
    def _minimax(cls, game_state, depth, alpha, beta, maximizing_player):
        """
        Code that does main minimax loop for each potential move

        Args:
            game_state (Connect4Game): current state of the game
            depth (int): amount of depth left to search through options
            alpha (float): best explored option along path to root for maximizer
            beta (float): best explored option along path to root for minimizer
            maximizing_player (bool): whether current move is for maximizing player

        Returns:
            int: evaluated score of board state
        """
        if depth == 0 or game_state.winner is not None:  # if depth limit reached or game is won
            return cls._evaluate_board(game_state)  # return heuristic evaluation
        
        valid_moves = list()  # list to store all columns where move is valid
        for col in range(7):  # iterate over all columns in Connect4 board
            if game_state.is_valid_move(col):  # check if column is valid 
                valid_moves.append(col)  # add valid columns to list
        
        if not valid_moves:  # handle case where board is full
            return 0

        if maximizing_player:  # if maximizing player's turn
            best_score = float('-inf')  # initialize best score as negative infinity
            for col in valid_moves:  # iterate through all valid moves
                game_copy = copy.deepcopy(game_state)  # create copy of game state
                game_copy.make_move(col)  # simulate making a move
                score = cls._minimax(game_copy, depth - 1, alpha, beta, False)  # recursively evaluate the move
                best_score = max(best_score, score)  # update best score
                alpha = max(alpha, best_score)  # update alpha value for pruning
                if beta <= alpha:  # prune search tree if beta is less than or equal to alpha
                    break
            return best_score  # return best score
        else:  # if minimizing player's turn
            best_score = float('inf')  # initialize best score as positive infinity
            for col in valid_moves:  # iterate through all valid moves
                game_copy = copy.deepcopy(game_state)  # create copy of game state
                game_copy.make_move(col)  # simulate making a move
                score = cls._minimax(game_copy, depth - 1, alpha, beta, True)  # recursively evaluate the move
                best_score = min(best_score, score)  # update best score
                beta = min(beta, best_score)  # update beta value for pruning
                if beta <= alpha:  # prune search tree if beta is less than or equal to alpha
                    break
            return best_score  # return best score

    @classmethod
    def _evaluate_board(cls, game_state):
        """
        evaluates board state and returns heuristic score

        Args:
            game_state (Connect4Game): current state game
        
        Returns:
            int: heuristic score of board state
        """
        # Handle game-ending states
        if game_state.winner is not None:
            if game_state.winner == game_state.current_player:
                return float('inf')  # Current player wins
            else:
                return float('-inf')  # Opponent wins

        score = 0  # initialize score for board evaluation
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # horizontal, vertical, diagonal directions
        
        # evaluate every position
        for row in range(6):
            for col in range(7):
                if game_state.board[row][col] == 0:  # skip empty positions
                    continue
                    
                # check all possible winning directions from current position
                for dr, dc in directions:
                    sequence = []  # store sequence of 4 positions
                    # build sequence of 4 consecutive positions
                    for i in range(4):
                        r, c = row + dr * i, col + dc * i
                        if 0 <= r < 6 and 0 <= c < 7:  # ensure position is within board
                            sequence.append(game_state.board[r][c])
                        else:
                            break
                            
                    # evaluate sequence if it contains 4 positions
                    if len(sequence) == 4:
                        player_count = sequence.count(game_state.current_player)  # count current player's pieces
                        opponent_count = sequence.count(3 - game_state.current_player)  # count opponent's pieces
                        empty_count = sequence.count(0)  # count empty spaces
                        
                        # score 
                        if empty_count == 0:  
                            if player_count == 4:
                                score += 100 
                            elif opponent_count == 4:
                                score -= 100  
                        elif empty_count == 1:  
                            if player_count == 3:
                                score += 5  
                            elif opponent_count == 3:
                                score -= 5  
                        elif empty_count == 2:  
                            if player_count == 2:
                                score += 2 
                            elif opponent_count == 2:
                                score -= 2  

        return score  # return final evaluated score