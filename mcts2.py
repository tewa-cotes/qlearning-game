import math
import copy
import csv


class Node:
    def __init__(self, parent=None, move=None):
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = []


class MCTS:
    def __init__(self):
        self.root_node = Node()

    def expand(self, node):
        move = node.untried_moves.pop()

        child_node = Node(
            parent=node,
            move=move
        )

        node.children.append(child_node)

        return child_node

    def uct(self, node, child):
        C = 1

        uct = (
            child.wins / child.visits
            + C * math.sqrt(
                math.log(node.visits) / child.visits
            )
        )

        return uct

    def select(self, node):
        ucts = []

        for child in node.children:
            ucts.append(
                self.uct(node, child)
            )

        index = ucts.index(max(ucts))

        return node.children[index]

    def get_depth(self, node):
        depth = 0

        while node.parent is not None:
            depth += 1
            node = node.parent

        return depth

    def backpropagate(self, node, winner, root_player):
        current_node = node

        while current_node is not None:
            current_node.visits += 1

            depth = self.get_depth(current_node)

            if depth > 0:
                if depth % 2 == 1:
                    move_player = root_player
                else:
                    move_player = 1 - root_player

                if move_player == winner:
                    current_node.wins += 1

            current_node = current_node.parent

    def rollout(self, game):
        while True:
            move = game.random_move()

            game.apply_move(move)

            winner = game.check_winner()

            if winner is not None:
                return winner

            game.change_turn()

    def simulation_by_finish(self, game, root_node):
        sim_game = copy.deepcopy(game)
        sim_node = root_node

        root_player = game.current_player_color

        # Selection
        while not sim_node.untried_moves:

            sim_node = self.select(sim_node)

            sim_game.apply_move(sim_node.move)

            winner = sim_game.check_winner()

            if winner is not None:
                self.backpropagate(
                    sim_node,
                    winner,
                    root_player
                )
                return

            sim_game.change_turn()

        # Expansion
        sim_node = self.expand(sim_node)

        sim_game.apply_move(sim_node.move)

        winner = sim_game.check_winner()

        if winner is not None:
            self.backpropagate(
                sim_node,
                winner,
                root_player
            )
            return

        sim_game.change_turn()

        # 新Nodeの合法手を保存
        sim_game.get_legal_moves()
        sim_node.untried_moves = sim_game.legal_moves.copy()

        # Rollout
        winner = self.rollout(sim_game)

        # Backpropagation
        self.backpropagate(
            sim_node,
            winner,
            root_player
        )

    def simulation(self, game, root_node, count=1000):
        game.get_legal_moves()

        root_node.untried_moves = game.legal_moves.copy()

        for _ in range(count):
            self.simulation_by_finish(
                game,
                root_node
            )

    def get_best_move(self, root_node):
        best_child = max(
            root_node.children,
            key=lambda child: child.visits
        )

        return best_child.move

    def save_tree_csv(
        self,
        root_node,
        filename="mcts_tree.csv"
    ):
        rows = []

        def walk(node):
            depth = self.get_depth(node)

            if node.visits > 0:
                win_rate = node.wins / node.visits
            else:
                win_rate = 0

            rows.append([
                depth,
                node.move,
                node.visits,
                node.wins,
                win_rate,
                len(node.children),
                len(node.untried_moves)
            ])

            for child in node.children:
                walk(child)

        walk(root_node)

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "depth",
                "move",
                "visits",
                "wins",
                "win_rate",
                "children_count",
                "untried_moves_count"
            ])

            writer.writerows(rows)