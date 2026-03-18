from easyAI import TwoPlayerGame
import random

# Convert D7 to (3,6) and back...
to_string = lambda move: " ".join(
    ["ABCDEFGHIJ"[move[i][0]] + str(move[i][1] + 1) for i in (0, 1)]
)
to_tuple = lambda s: ("ABCDEFGHIJ".index(s[0]), int(s[1:]) - 1)


class Hexapawn(TwoPlayerGame):
    """
    A nice game whose rules are explained here:
    http://fr.wikipedia.org/wiki/Hexapawn
    """

    def __init__(self, players, size=(4, 4), probabilistic=True):
        self.size = M, N = size
        self.probabilistic = probabilistic 
        self.respawn_probability = 0.1 if probabilistic else 0.0
        p = [[(i, j) for j in range(N)] for i in [0, M - 1]]

        for i, d, goal, pawns in [(0, 1, M - 1, p[0]), (1, -1, 0, p[1])]:
            players[i].direction = d
            players[i].goal_line = goal
            players[i].pawns = pawns
            players[i].captured = []  # Lista zdobytych pionków

        self.players = players
        self.current_player = 1

    def possible_moves(self):
        moves = []
        opponent_pawns = self.opponent.pawns
        d = self.player.direction
        for i, j in self.player.pawns:
            if (i + d, j) not in opponent_pawns:
                moves.append(((i, j), (i + d, j)))
            if (i + d, j + 1) in opponent_pawns:
                moves.append(((i, j), (i + d, j + 1)))
            if (i + d, j - 1) in opponent_pawns:
                moves.append(((i, j), (i + d, j - 1)))

        return list(map(to_string, [(i, j) for i, j in moves]))

    def make_move(self, move):
        self.make_move_deterministic(move)
        
        if self.probabilistic and self.player.captured:
            respawning = []
            for i in range(len(self.player.captured)):
                if random.random() < self.respawn_probability:
                    respawning.append(i)
            
            for i in sorted(respawning, reverse=True):
                self._respawn_pawn(i)
    
    def make_move_deterministic(self, move):
        move = list(map(to_tuple, move.split(" ")))
        ind = self.player.pawns.index(move[0])
        self.player.pawns[ind] = move[1]


        if move[1] in self.opponent.pawns:
            self.opponent.pawns.remove(move[1])
            _, captured_column = move[1]
            self.player.captured.append(captured_column)
    
    def _respawn_pawn(self, pawn_index):
        if pawn_index >= len(self.player.captured):
            return
        column = self.player.captured[pawn_index]
        self.player.captured.pop(pawn_index)
        start_line = self.size[0] - 1 if self.player.direction == -1 else 0
        if (start_line, column) not in self.player.pawns and (start_line, column) not in self.opponent.pawns:
            self.player.pawns.append((start_line, column))
    
    def get_chance_outcomes(self):
        if not self.probabilistic or not self.player.captured:
            return [(1.0, ())]
        
        num_captured = len(self.player.captured)
        
        outcomes = []
        for mask in range(2 ** num_captured):
            respawning_pawns = []
            probability = 1.0
            
            for i in range(num_captured):
                if mask & (1 << i):  # i-ty bit jest ustawiony
                    respawning_pawns.append(i)
                    probability *= self.respawn_probability  # 10%
                else:
                    probability *= (1.0 - self.respawn_probability)  # 90%
            
            outcomes.append((probability, tuple(respawning_pawns)))
        
        return outcomes
    
    def apply_chance_outcome(self, outcome):
        for pawn_index in sorted(outcome, reverse=True):
            if pawn_index < len(self.player.captured):
                self._respawn_pawn(pawn_index)

    def lose(self):
        return any([i == self.opponent.goal_line for i, j in self.opponent.pawns]) or (
            self.possible_moves() == []
        )

    def is_over(self):
        return self.lose()

    def show(self):
        f = (
            lambda x: "1"
            if x in self.players[0].pawns
            else ("2" if x in self.players[1].pawns else ".")
        )
        print(
            "\n".join(
                [
                    " ".join([f((i, j)) for j in range(self.size[1])])
                    for i in range(self.size[0])
                ]
            )
        )


class NegamaxNoAB:
    def __init__(self, depth, scoring=None):
        self.depth = depth
        self.scoring = scoring
    
    def __call__(self, game):

        scoring = self.scoring if self.scoring else (lambda g: g.scoring())
        
        def negamax_no_ab(game, depth):

            if depth == 0 or game.is_over():
                return scoring(game) * (1 + 0.001 * depth)
            
            possible_moves = game.possible_moves()
            best_value = float('-inf')
            
            for move in possible_moves:
                game_copy = game.copy()
                game_copy.make_move(move)
                game_copy.switch_player()
                
                move_value = -negamax_no_ab(game_copy, depth - 1)
                
                if move_value > best_value:
                    best_value = move_value
                    if depth == self.depth:
                        game.ai_move = move
            
            return best_value
        
        negamax_no_ab(game, self.depth)
        return game.ai_move


if __name__ == "__main__":
    from easyAI import AI_Player, Human_Player, Negamax

    scoring = lambda game: -100 if game.lose() else 0
    ai = Negamax(10, scoring)
    game = Hexapawn([AI_Player(ai), AI_Player(ai)])
    game.play()
    print("player %d wins after %d turns " % (game.opponent_index, game.nmove))
