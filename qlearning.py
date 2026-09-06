import pickle
import random
import  json
from pathlib import Path
class Qlearningcontroller:

    def __init__(self,game, mode, filename):#aが1→引き続き学習, 0なら新規学習
        self.alfa = 0.1 #学習率
        self.ganma = 0.95 #将来の価値の重み
        self.epsilon = 0.2 #ランダムに参照する確率
        self.game = game
        self.q_table = {}
        self.state = self.get_state()
        
        self.filename = Path(filename).with_suffix(".pkl")
        self.history_dir = self.filename.parent / f"{self.filename.stem}_history"
        self.meta_filename = self.filename.with_name(self.filename.stem + "history")
        self.trained_games = 0
        if mode:
            self.get_q_tabel()
            self.load_meta()
        self.check_state()
        self.is_qlearning=True
        self.prev_state = None
        self.prev_move = None
    def reset(self):
        self.state = self.get_state()
        self.prev_move = None
        self.prev_state = None
    def get_q_tabel(self):
        with open(self.filename, "rb") as file:
            self.q_table = pickle.load(file)

    def check_state(self):# board、stateを更新してからじゃないとだめ
        legal_moves = self.game.get_legal_moves()
        if tuple(self.state) not in self.q_table:
            self.q_table[tuple(self.state)] = {}
            for a in legal_moves:
                self.q_table[tuple(self.state)][tuple(a)] = 0


    def get_state(self):
        state=[-1] * 34
        board = self.game.board.board
        for row_index,row in enumerate(board):
            for col_index,cell in enumerate(row):
                if cell is not None:
                    for piece in cell:
                        index = 9 * row_index + 3 * col_index + piece.size
                        state[index] = piece.color
        state[27:33] = [2] * 6
        state[33] = self.game.current_player_color
        return state
    def keep_qm(self,move):
        self.prev_move = move
        self.prev_state = self.state.copy()
    def select_move(self):
        self.check_state()
        if random.random() > self.epsilon:
            moves = self.q_table[tuple(self.state)]
            max_q = max(moves.values())

            best_moves = [move for move, q in moves.items() if q == max_q]
            return random.choice(best_moves)

            
        else:
            return self.game.get_random_moves()

    def write_csv(self, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename, "wb") as file:
            pickle.dump(self.q_table, file)
    def save_meta(self):
        with open(self.meta_filename, "w", encoding="utf-8") as file:
            json.dump({"trained_games": self.trained_games}, file)
    def load_meta(self):
        if not self.meta_filename.exists():
            return
        with open(self.meta_filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.trained_games = data["trained_games"]
    def save(self):
        # 最新版
        self.write_csv()
        # 履歴フォルダ
        self.history_dir.mkdir(parents=True, exist_ok=True)

        history_file = (self.history_dir / f"{self.filename.stem}_{self.trained_games}.pkl")
        self.write_csv(history_file)

        self.save_meta()
    def update_state(self,move):
        cpc = self.game.current_player_color
        if move[0]:
            
            self.state[9 * move[1] + 3 * move[2] + move[5]] = -1
            self.state[9 * move[3] + 3 * move[4] + move[5]] = cpc
        else:
            self.state[9 * move[2] + 3 * move[3] + move[1]] = cpc
            self.state[27 + 3 * cpc + move[1]] -= 1
    def update_q(self,r):
        prev_q = self.q_table[tuple(self.prev_state)][tuple(self.prev_move)]
        if r:
            maxq = 0
        else:
            maxq = max(self.q_table[tuple(self.state)].values())
        q = prev_q + self.alfa * (r + self.ganma * maxq - prev_q)
        self.q_table[tuple(self.prev_state)][tuple(self.prev_move)] = q
         
    def qlearning(self):
        self.check_state()
        if self.prev_state is not None and self.prev_move is not None:
            self.update_q(0)
        
        









        




