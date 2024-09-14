from board import Direction, Rotation, Action
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
                

            

    def choose_action(self, board):
        self.print_board(board)
        #time.sleep(0.5)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])

class JashsPlayer(Player):
    def __init__(self, seed=None):
        pass

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
                
    def heights(self, board):
        column_heights = [0] * board.width
        for x,y in board.cells:
            column_heights[x] =  max(column_heights[x], board.height - y)
        return column_heights
        
    def count_holes(self, board):
        holes = 0
        heights = self.heights(board)
        for x in range(board.width):
            for y in range(heights[x] - 1, -1, -1):
                if (x, board.height - y - 1) not in board.cells:
                    holes += 1            
        return holes
        
    def bumpiness(self, board):
        heights = self.heights(board)
        bumpiness_penalty = 0
        for i in range(board.width - 1):
            bumpiness_penalty -= abs(heights[i] - heights[i + 1])
        return bumpiness_penalty 
    
    def line_clearnig(self):
        cell_difference = self.newcells - self.oldcells

        if cell_difference == -32:
            return 101
        elif cell_difference == -2:
            return -76
        elif cell_difference == -12:
            return -61
        elif cell_difference == -22:
            return -31
        elif cell_difference == -42:
            return 121
        elif cell_difference == -52:
            return 141
        elif cell_difference == -62:
            return 161
        elif cell_difference == -72:
            return 201
        else:
            return 0



        
    def score(self, board):
        weight_of_height = 12.5
        weight_of_bumpiness = 20
        weight_of_holes = 100

        heights = self.heights(board)
        height_penalty= max(heights) * weight_of_height

        holes_penalty = self.count_holes(board) * weight_of_holes

        bumpiness_penalty = self.bumpiness(board) * weight_of_bumpiness

        line_clear_penalty = self.line_clearnig() 

        score = - height_penalty + bumpiness_penalty - holes_penalty + line_clear_penalty

        return score


    def move_to_target(self, board, target_position, target_rotation):
        list_of_moves = []
        has_landed = False
        while not has_landed and target_rotation != 0:
            if target_rotation == 3:
                list_of_moves.append(Rotation.Anticlockwise)
                has_landed = board.rotate(Rotation.Anticlockwise)
                break
            list_of_moves.append(Rotation.Clockwise)
            has_landed = board.rotate(Rotation.Clockwise)
            target_rotation -= 1 

        while not has_landed and target_position > board.falling.left:
            list_of_moves.append(Direction.Right)
            has_landed = board.move(Direction.Right)
        while not has_landed and target_position < board.falling.left:
            list_of_moves.append(Direction.Left)
            has_landed = board.move(Direction.Left)
        
        if not has_landed:
            list_of_moves.append(Direction.Drop)
            board.move(Direction.Drop)

        return list_of_moves
        
           

    def choose_action(self, board):
        diff_possibilities = []
        for r in range(4):
            for x in range(board.width - (board.falling.right - board.falling.left)):
                c_b = board.clone()
                self.oldcells = len(c_b.cells)
                list_of_moves = self.move_to_target(c_b, x, r)                
                for r2 in range(4):
                    for x2 in range(board.width - (c_b.falling.right - c_b.falling.left)):
                        c_b2 = c_b.clone()
                        list_of_moves += self.move_to_target(c_b2,x2,r2)
                        self.newcells = len(c_b2.cells)
                        diff_possibilities.append((self.score(c_b2), list_of_moves))
        _, list_of_moves = max(diff_possibilities, key=lambda x: x[0])
        return list_of_moves

SelectedPlayer = JashsPlayer
