import time

from game import Game
from controller import Humancontroller, Randomcontroller, Controll
from qlearning import Qlearningcontroller


game = Game()

# 例：Q-learning AI vs Random
p1 = Qlearningcontroller(game, 1, "q_table1.csv")
p2 = Randomcontroller(game)

controller = Controll(p1, p2, game)


start = time.perf_counter()

controller.main(10000)

end = time.perf_counter()


elapsed = end - start

print(f"10000ゲーム: {elapsed:.3f} 秒")
print(f"1ゲーム平均: {elapsed / 10000:.6f} 秒")
print(f"1秒あたり: {10000 / elapsed:.2f} ゲーム")
print(f"1時間あたり: {10000 / elapsed * 3600:.0f} ゲーム")
print(f"24時間あたり: {10000 / elapsed * 86400:.0f} ゲーム")