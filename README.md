# nqueens
This program will solve the problem of placing 8 queens on a chess board such that none of them attack each other. There will also be a boulder placed in the board which blocks the queens' attack and occupies a place on the board.

It makes use of hill-climbing with random restart algorithm:
  Defining neighborhood:\n
    - Goal state: queens are not attacking each other and are placed in valid positions (multiple queens are not in the same position or in the same position as the boulder)
    - Neighbor state: from the current state, move ONE queen to a valid position along its column
    - Heuristic value: the number of queens being attacked (the lower the value, the better the state)
  Algorithm:
    - Move each the queens from the right-most respectively to the position with the lowest heuristic value
    - Stop if the goal state is reached
    - If the goal state is not reached after all queens are moved, restart by placing each queen on a column randomly
