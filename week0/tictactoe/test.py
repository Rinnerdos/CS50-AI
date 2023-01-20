import math

from tictactoe import initial_state, max_value, minimax, player, actions, result, utility, winner


X = "X"
O = "O"
EMPTY = None

BOARD = [[X, O, X],
         [X, O, X],
         [EMPTY, EMPTY, X]]
print(player(BOARD))
#print(actions(BOARD))
#print(winner(BOARD))
#print(result(BOARD, minimax(BOARD)))
print(utility(BOARD))