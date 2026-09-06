from game import Game
from controller import Controll, Randomcontroller
from qlearning import Qlearningcontroller


game = Game()

q_player = Qlearningcontroller(game, 0,"q_table1.pkl")  # 0 = 新規学習
random_player = Randomcontroller(game)

controller = Controll(
    q_player,
    random_player,
    game
)

controller.main(1000000,100000)

