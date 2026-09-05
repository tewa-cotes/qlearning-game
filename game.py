from piece import Board,Piece
from player import Player
import random
import copy
# 手札から置く
# [0, size, row, col]
# 盤面から移動
# [1, from_row, from_col, size, to_row, to_col]
class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = Player(0)
        self.player2 = Player(1)
        self.players=[self.player1,self.player2]
        self.current_player_color = self.player1.color
        self.display_map = {0:"🔹", 1:"🔷", 2:"🟦", 3:"🔸", 4:"🔶", 5:"🟧"}

    def reset(self):
        self.board = Board()
        self.player1 = Player(0)
        self.player2 = Player(1)
        self.players=[self.player1,self.player2]
        self.current_player_color = self.player1.color
    def change_turn(self):
        self.current_player_color = 1-self.current_player_color

    def change_n_to_pic(self,piece,):
        pass
    def print_board(self):
        for i,cell in enumerate(cell for row in self.board.board for cell in row):
            if cell:
                key = cell[-1].color * 3 + cell[-1].size
                print(self.display_map[key], end=" ")
            else:
                print("  ", end=" ")
            if(i+1)%3==0:
                print()

    def get_hand_box(self):
        for i in range(3):
            print(f"{self.display_map[3*self.current_player_color+i]}: {self.players[self.current_player_color].players_piece[i]}")
        choiced_size = int(input("サイズを選んで0~2:"))
        choiced_row = int(input("行を入力:"))
        choiced_col = int(input("列を入力:"))
        hand_box = [0,choiced_size,choiced_row,choiced_col]
        return hand_box 
    def placed_from_hand(self,hand_box):
        piece = Piece(self.current_player_color,hand_box[1])
        self.board.place_piece(hand_box[2],hand_box[3],piece)
        self.players[self.current_player_color].players_piece[hand_box[1]]-=1

    def get_board_box(self):
        choiced_row_from_board = int(input("取りたい駒の行を選択:"))
        choiced_col_from_board = int(input("取りたい駒の行を選択:"))
        choiced_row_to_board = int(input("動かす先の行を選択:"))
        choiced_col_to_board = int(input("動かす先の列を選択:"))
        size = self.board.board[choiced_row_from_board][choiced_col_from_board][-1].size
        board_box = [1,choiced_row_from_board,choiced_col_from_board,choiced_row_to_board,choiced_col_to_board,size]
        return board_box
    
    def placed_from_board(self,board_box):
        piece = self.board.board[board_box[1]][board_box[2]][-1]
        self.board.board[board_box[1]][board_box[2]].pop()
        self.board.place_piece(board_box[3],board_box[4],piece)


    def human_move(self):
        print("あんたの番です")
        self.print_board()
        hand_or_board = int(input("手から出す場合0,盤面から動かす場合1:"))
        if hand_or_board:
            return self.get_board_box()

        else:
            return self.get_hand_box()

    def check_winner(self):
        check_board = []
        for row in self.board.board:
            new_row = []
            for cell in row:
                if cell:
                    new_row.append(cell[-1].color)
                else:
                    new_row.append(None)
            check_board.append(new_row)
        lines = []
        for i in range(3):
            lines.append(check_board[i])
            lines.append([row[i] for row in check_board])
        lines.append([check_board[i][i] for i in range(3)])
        lines.append([check_board[i][2-i] for i in range(3)])
        blue_win = [0,0,0] in lines
        orange_win = [1,1,1] in lines
        if blue_win:
            if orange_win:
                return 1-self.current_player_color
            else:
                return 0
        else:
            if orange_win:
                return 1
            else: 
                return None
    def get_reboard_for_legal_moves(self):
        self.reboard_for_legal_moves = []
        for row in self.board.board:
            new_row = []
            for cell in row:
                new_cell=-1
                if cell:
                    if cell[-1].color == self.current_player_color:
                        new_cell = 5
                    else:
                        new_cell = cell[-1].size
                new_row.append(new_cell)
            self.reboard_for_legal_moves.append(new_row)
    def get_board_piece_positions(self):
        self.board_piece_positions = []
        for row_i, row in enumerate(self.board.board):
            for col_i, cell in enumerate(row):
                if cell and cell[-1].color == self.current_player_color:
                    self.board_piece_positions.append([row_i, col_i])
    def get_board_moves(self):
        self.get_board_piece_positions()
        self.board_moves=[]
        for position in self.board_piece_positions:
            for row_i, row in enumerate(self.reboard_for_legal_moves):
                for col_i, cell in enumerate(row):
                    if self.board.board[position[0]][position[1]][-1].size > cell:
                        size = self.board.board[position[0]][position[1]][-1].size
                        self.board_moves.append([1,position[0],position[1],row_i,col_i, size])

    def get_hand_piece_size(self):
        self.hand_piece_size=[]
        for i in range(3):
            if self.players[self.current_player_color].players_piece[i] >= 1:
                self.hand_piece_size.append(i)

    def get_hand_moves(self):
        self.get_hand_piece_size()
        self.hand_moves=[]
        for size in self.hand_piece_size:
            for row_i, row in enumerate(self.reboard_for_legal_moves):
                for col_i, cell in enumerate(row):
                    if size > cell:
                        self.hand_moves.append([0,size,row_i, col_i])
    def get_legal_moves(self):
        self.get_reboard_for_legal_moves()
        self.get_board_moves()
        self.get_hand_moves()
        self.legal_moves = self.hand_moves + self.board_moves
        return self.legal_moves

    def get_random_moves(self):
        self.get_legal_moves()
        return random.choice(self.legal_moves)
    def apply_move(self,move):
        
        if move[0]:

            self.placed_from_board(move)
        else:

            self.placed_from_hand(move)

# class State:
#     def __init__(self,game):
#         self.state = [
#             [-1,-1,-1],#0が青、1がオレンジ
#             [-1,-1,-1],
#             [-1,-1,-1],
#             [-1,-1,-1],
#             [-1,-1,-1],
#             [-1,-1,-1],
#             [-1,-1,-1],
#             [-1,-1,-1],
#             [-1,-1,-1]
#         ]
#         self.players_hands=[[2,2,2],[2,2,2]]
#         self.game = game
#         self.full_state = [
#             self.state,
#             self.players_hands,
#             self.game.current_player_color
#         ]

#     def hand(self, move):
#         player = self.game.current_player_color
#         self.players_hands[player][move[1]]-=1
#         self.state[3 * move[2] + move[3]][move[1]] = player

#     def board(self, move):
#         player = self.game.current_player_color
#         size = move[5]
#         self.state[3 * move[1] + move[2]][size] = -1
#         self.state[3 * move[3] + move[4]][size] = player

#     def update_state(self,move):
#         if move[0] :
#             self.board(move)
#         else:
#             self.hand(move)

#     def copy_state(self):
#         return copy.deepcopy(self.full_state)
