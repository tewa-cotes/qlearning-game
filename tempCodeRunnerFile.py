from game import Game
game = Game()

while True:
    move = game.random_move()
    game.apply_move(move)
    winner = game.check_winner()
    if winner is not None:
        game.print_board()
        print(f"player{winner}win")
        break
    game.change_turn()