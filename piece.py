class Piece:
    def __init__(self, color, size):
        self.color = color #01
        self.size = size  #0,1,2
        

class Board:
    def __init__(self):
        self.board = [[[] for _ in range(3)]for _ in range(3)]

    def place_check(self, row, col, piece):
        cell = self.board[row][col]
        if cell:
            max_size = cell[-1].size
            if piece.size > max_size:
                return True
            else:
                return False
        else:
            return True
        
    def place_piece(self, row, col, piece):
        self.board[row][col].append(piece)



    