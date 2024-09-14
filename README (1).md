
# Tetris Autoplayer

This assignment involved brainstorming strategies and implementing them in the form of code to build an autoplayer for the given version of game Tetris and to score as much as possible.

## Contents And Running The Program

We were provided the code of the game with a RandomPlayer class that used to place the tiles randomly. I developed the JashsPlayer class that selects the best possible action for the tile by analysing all the possible combinations of the positions of the current tile and the next tile. It takes into account all the possible scores and then picks the action that will result in the maximum score. I developed strategies depending on the specific rules of this version of the game which were different from the nomral version of Tteris.

To run the program, use the terminal while in the same directory and enter 'python3 visual.py' for a visual representation of the game or else enter 'python3 cmdline.py' for a terminal representation.