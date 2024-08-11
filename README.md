# 🔴 Checkers Champion ⚫️

## How To Play
___
### Turns
* The darker color moves first. In this case, the player is Black and the AI opponent is Red.
This means the player moves first.
* Moving a piece one square diagonally (referred to as adjacent movement) constitutes a turn and the other player would then make a move
* A single jump counts as a turn---multiple consecutive jumps also count as a single turn and are a vital part in winning.

### Movement
* Pieces can only move diagonally (either adjacent or jump)
* Regular (non-king) pieces can only move towards the opponent (towards the opposite side of the board)
* Kings are achieved by getting your piece to the other side of the board. They can move in any diagonal direction.
* If a jump exists on the board, you MUST take it. If multiple jumps exist, you can choose which piece to jump.

### Ending the Game
The game is over when Black or Red has no pieces left. Draws have not been implemented since they involve one player asking the other to prove he can win (or get closer to winning) in the next 40 moves or the game ends in a draw.


## 🧠 Minimax - The Brain Behind the Algorithm
___
### What is Minimax?
Minimax is an decision-making adversarial search algorithm best suited for 2 player turn-based games, such as Tic-Tac-Toe, Chess, or in this case, Checkers.

### How Does it Work?
* It works by choosing the best move assuming that the opponent is playing optimally. This is similar to the end game of Tic-Tac-Toe, where if a human player is trying to win, they would think about their move and what the opponent can do if a move was made.
* Minimax has 2 players, a min player and a max player. The min player tries to minimize the score and the max player tries to maximize the score. In Tic-Tac-Toe, the min player could be X and the max player O, or vice versa. In this implementation, Black is the max player and Red the min player.
* The algorithm looks through all possible moves that can be made, alternating between whose turn it is, min or max, making the respective move for each player until it reaches a terminal, or game over, state. Doing this guarantees that the optimal move is made. For Checkers, playing through every possible move is impractical since it would take so much time for a move to be made, so 2 methods were implemented to speed it up: Alpha-Beta Pruning and Depth-Limited Minimax.

### Alpha-Beta Pruning
* Alpha-Beta Pruning is a way to speed up Minimax by eliminating branches of the game tree that are worse than ones we have seen so far since there is no need to consider branches that will lead to less favorable position like losing, when we can get a better position like having a draw.
* Doing this still allows the algorithm to make the optimal move

### Depth-Limited Minimax
* Depth-Limited Minimax limits how many moves ahead the algorithm looks at. Instead of playing to a terminal state where the game is over, the algorithm will stop at say, 5 moves ahead and look at the game state. This is where the evaulation function comes in.
* The evalution function takes in a game state and returns a number based on who the board favors, a positive number favoring the max player and a negative number favoring the min player. This determines how good the minimax algorithm is. For this implementation, a basic evaulation function was used, summing the pieces on the board, giving extra weight to those that are kings; however, a more complex evaluation function can be used to consider the position of the pieces on the board since center control is better.
* Depth-Limited Minimax, since it does not search to the end of the game, is not guaranteed to make the most optimal move. 
___
