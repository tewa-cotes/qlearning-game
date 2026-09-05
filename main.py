from game import Game
from controller import Controll, Randomcontroller
from qlearning import Qlearningcontroller


game = Game()

q_player = Qlearningcontroller(game, 1,"q_table1.csv")  # 0 = 新規学習
random_player = Randomcontroller(game)

controller = Controll(
    q_player,
    random_player,
    game
)

controller.main(100000,50000)

