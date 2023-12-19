# Connect4-AI
This Python implementation features a Game Tree Search AI designed to play the game Connect4. You can play a match against the AI and customize the difficulty level by adjusting the lookahead value. A higher lookahead distance increases the difficulty by allowing the AI to look more into the future. The implementation incorporates Alpha-Beta pruning to significantly enhance search speed by almost 10 times in this case.

## Running the code
### Prerequisites
Ensure that Python 3 is installed on your system.<br>

### Instructions
Download both FourConnectAI.py and FourConnect.py into a folder.
Open a Terminal in that folder and run "python3 FourConnectAI.py"

## How the code works
This FourConnectAI.py has the complete code for the AI player. It encompasses the implementation of tree search, heuristic function and alpha-beta pruning. The main function is also present in this function.<br>
The FourConnect.py file has the class describing the board and helper functions to play the moves that the AI and player specify. It ensures that a move is valid and prints the board after a move.
