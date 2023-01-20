"""
Tic Tac Toe Player
"""

from copy import deepcopy
from ctypes import util
import math
from re import I

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Sum over all X's and O's
    Xsum = 0
    Osum = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                Xsum += 1
            elif board[i][j] == O:
                Osum += 1
    # Subtracting Osum from Xsum should give you the right player
    # even in starting board.
    if (Xsum - Osum == 0):
        return X
    else:
        return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibles = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possibles.add((i, j))
    return possibles
                
    
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #print(action)
    i = action[0]
    j = action[1]
    deepboard = deepcopy(board)
    
    if deepboard[i][j] != EMPTY:
        raise NameError("Whoops! Invalid action!")
    else:
        deepboard[i][j] = player(board) 
    
    return deepboard
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # i -> rows j -> columns

    # Undoubtedly not the most efficient way
    # but I think you can do the horizontal en vertical in one loop
    for i in range(len(board)):
        Xcountx = 0
        Ocountx = 0
        Xcounty = 0
        Ocounty = 0
        for j in range(len(board[i])):
            if board[i][j] == X:
                Xcountx += 1
            elif board[i][j] == O:
                Ocountx += 1
            
            if board[j][i] == X:
                Xcounty += 1
            elif board[j][i] == O:
                Ocounty += 1
            
        #print(Xcountx, Ocountx, Xcounty, Ocounty)
        if (Xcountx == 3) or (Xcounty == 3):
            return X
        elif (Ocountx == 3) or (Ocounty == 3):
            return O

    # Reset counters, maybe a more elegant option is possible? Ugly
    Xcountx = 0
    Ocountx = 0
    Xcounty = 0
    Ocounty = 0

    # Is there a way to not hardcode the diagonal wins?
    # When i = j, top left to bottorm right diagonal
    # When i + j = n of an n x n matrix, bottom left to top right
    for i in range(len(board)):    
        for j in range(len(board[i])):
            if i == j and board[i][j] == X:
                Xcountx += 1
            elif i == j and board[i][j] == O:
                Ocountx += 1
            
            if i + j == (len(board)-1) and board[i][j] == X:
                Xcounty += 1
            elif i + j == (len(board)-1) and board[i][j] == O:
                Ocounty += 1

    if (Xcountx == len(board)) or (Xcounty == len(board)):
        return X
    elif (Ocountx == len(board)) or (Ocounty == len(board)):
        return O

    return None
        


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    elif actions(board) == set():
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        v = -math.inf
        for action in actions(board):
            score = min_value(result(board,action))
            if score > v:
                v = score
                best_action = action
        return best_action

    elif player(board) == O:
        v = math.inf
        for action in actions(board):
            score = max_value(result(board, action))
            if score < v:
                v = score
                best_action = action
        return best_action
    

def max_value(board):
    """
    Returns the utility of a board for the maximizing player.
    """
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    
    return v


def min_value(board):
    """
    Returns the utility of a board for the minimizing player
    """
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    
    return v