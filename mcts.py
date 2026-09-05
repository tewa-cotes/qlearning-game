import math
import copy
from game import Game
class Node:
    def __init__(self,parent=None, move=None):
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
        children_node = Node(parent = node, move = move)
        node.children.append(children_node)
        return children_node
    def uct(self, node, child):
        C=1
        uct = child.wins / child.visits + C*math.sqrt(math.log(node.visits) / child.visits)
        return uct
    def select(self, node):
        ucts = []
        for child in node.children:
            ucts.append(self.uct(node, child))
        index =ucts.index(max(ucts))
        children_node = node.children[index]
        return children_node
    def action(self,node):
        
        if node.untried_moves:
            children_node = self.expand(node)
            expanded = True
        else:
            children_node = self.select(node)
            expanded = False
        return children_node, expanded 
    def get_depth(self, node):
        depth = 0
        while node.parent is not None:
            depth += 1
            node = node.parent
        return depth
    def backpropagate(self, node, winner):#このnodeは最終のーど
        current_node = node
        while current_node is not None:
            current_node.visits += 1
            current_node = current_node.parent
        current_node = node
        depth = self.get_depth(node)
        if winner:
            if depth % 2:
                for _ in range(depth // 2 + 1):
                    current_node.wins += 1
                    current_node = current_node.parent.parent
            else:
                for _ in range(depth // 2):
                    current_node.parent.wins += 1
                    current_node = current_node.parent.parent
        else:
            if depth % 2:
                for _ in range(depth // 2):
                    current_node.parent.wins += 1
                    current_node = current_node.parent.parent
            else:
                for _ in range(depth // 2 + 1):
                    current_node.wins += 1
                    current_node = current_node.parent.parent    
            
        



    def simlation_by_finish(self,game,root_node):
        sim_game = copy.deepcopy(game)
        sim_root_node = root_node
        while True:
            sim_root_node, expanded = self.action(sim_root_node)
            sim_game.apply_move(sim_root_node.move)
            winner = sim_game.check_winner()
            if winner is not None:
                self.backpropagate(sim_root_node,winner)
                break
            sim_game.change_turn()

            if expanded:
                sim_game.get_legal_moves()
                sim_root_node.untried_moves = sim_game.legal_moves.copy()

        

    def simulation(self,game,root_node):
        game.get_legal_moves()
        root_node.untried_moves = game.legal_moves.copy()
        for _ in range(1000):
            self.simlation_by_finish(game,root_node)
        
