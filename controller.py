from qlearning import Qlearningcontroller
class Humancontroller:
    def __init__(self,game):
        self.game = game
        self.is_qlearning = False #qlearningかどうか
    def select_move(self):
        return self.game.human_move()
class Randomcontroller:
    def __init__(self,game):
        self.game = game
        self.is_qlearning = False #qlearningかどうか
    def select_move(self):
        return self.game.get_random_moves()




class Controll:
    def __init__(self,p1,p2,game):
        self.game = game
        self.players = [p1,p2]
        self.check = p1.is_qlearning or p2.is_qlearning
        self.controller = self.players[self.game.current_player_color]
        self.notcontroller = self.players[1-self.game.current_player_color]
    def change_controller(self):
        self.controller,self.notcontroller = self.notcontroller,self.controller
    def reset(self):
        self.game.reset()

        self.controller = self.players[self.game.current_player_color]
        self.notcontroller = self.players[1-self.game.current_player_color]

        for player in self.players:
            if player.is_qlearning:
                player.reset()
    def one_play(self):
        while True:
            if self.controller.is_qlearning:
                self.controller.qlearning()
            move = self.controller.select_move()
            self.game.apply_move(move)
            if self.controller.is_qlearning:
                self.controller.keep_qm(move)
                self.controller.update_state(move)
            if self.notcontroller.is_qlearning:
                self.notcontroller.update_state(move)
            win = self.game.check_winner()
            if win is None:
                self.change_controller()
                self.game.change_turn()

                if self.controller.is_qlearning:
                    self.controller.state[33] = 1 - self.controller.state[33]
                if self.notcontroller.is_qlearning:
                    self.notcontroller.state[33] = 1 - self.notcontroller.state[33]

            elif win == self.game.current_player_color:
                if self.controller.is_qlearning:
                    self.controller.update_q(1)
                if self.notcontroller.is_qlearning:
                    self.notcontroller.update_q(-1)
                break
            elif win == 1-self.game.current_player_color:
                if self.controller.is_qlearning:
                    self.controller.update_q(-1)
                if self.notcontroller.is_qlearning:
                    self.notcontroller.update_q(1)
                break

    def main(self, n, save_interval=10000):
        for i in range(n):
            if i:
                self.reset()
            self.one_play()
            for player in self.players:
                if player.is_qlearning:
                    player.trained_games += 1
            if (i + 1) % save_interval == 0:
                print(f"{i+1}回処理済み")
                for player in self.players:
                    if player.is_qlearning:
                        player.save()
        # save_intervalの途中で終了した場合
        if n % save_interval != 0:
            for player in self.players:
                if player.is_qlearning:
                    player.save()











    
