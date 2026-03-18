inf = float("infinity")


def expectiminimax(game, depth, origDepth, scoring, alpha=-inf, beta=+inf):
    if depth == 0 or game.is_over():
        return scoring(game) * (1 + 0.001 * depth)
    
    possible_moves = game.possible_moves()
    
    if depth == origDepth:
        game.ai_move = possible_moves[0]
    
    best_value = -inf
    
    for move in possible_moves:
        game_copy = game.copy()
        game_copy.make_move_deterministic(move)
        
        move_value = expectation_node(game_copy, depth, origDepth, scoring, alpha, beta)
        
        if move_value > best_value:
            best_value = move_value
            if depth == origDepth:
                game.ai_move = move
        
        alpha = max(alpha, best_value)
        if alpha >= beta:
            break
    
    return best_value


def expectation_node(game, depth, origDepth, scoring, alpha, beta):
    if hasattr(game, 'get_chance_outcomes'):
        chance_outcomes = game.get_chance_outcomes()
    else:
        chance_outcomes = [(1.0, ())]
    
    expected_value = 0.0
    
    for probability, outcome in chance_outcomes:
        game_after_chance = game.copy()
        
        if hasattr(game_after_chance, 'apply_chance_outcome'):
            game_after_chance.apply_chance_outcome(outcome)
        
        game_after_chance.switch_player()
        
        value = -expectiminimax(
            game_after_chance,
            depth - 1,
            origDepth,
            scoring,
            -beta,
            -alpha
        )
        
        expected_value += probability * value
    
    return expected_value


class ExpectimaxAB:
    def __init__(self, depth, scoring=None, win_score=+inf):
        self.depth = depth
        self.scoring = scoring
        self.win_score = win_score
    
    def __call__(self, game):
        scoring = self.scoring if self.scoring else (lambda g: g.scoring())
        
        self.alpha = expectiminimax(
            game,
            self.depth,
            self.depth,
            scoring,
            -self.win_score,
            +self.win_score
        )
        
        return game.ai_move

class ExpectimaxNoAB:
    def __init__(self, depth, scoring=None):
        self.depth = depth
        self.scoring = scoring
    
    def __call__(self, game):
        scoring = self.scoring if self.scoring else (lambda g: g.scoring())
        
        def expectimax_no_ab(game, depth):
            if depth == 0 or game.is_over():
                return scoring(game) * (1 + 0.001 * depth)
            
            possible_moves = game.possible_moves()
            best_value = -inf
            
            for move in possible_moves:
                game_copy = game.copy()
                game_copy.make_move_deterministic(move)
                
                if hasattr(game_copy, 'get_chance_outcomes'):
                    chance_outcomes = game_copy.get_chance_outcomes()
                else:
                    chance_outcomes = [(1.0, ())]
                
                expected_value = 0.0
                for probability, outcome in chance_outcomes:
                    game_after = game_copy.copy()
                    if hasattr(game_after, 'apply_chance_outcome'):
                        game_after.apply_chance_outcome(outcome)
                    game_after.switch_player()
                    
                    value = -expectimax_no_ab(game_after, depth - 1)
                    expected_value += probability * value
                
                move_value = expected_value
                
                if move_value > best_value:
                    best_value = move_value
                    if depth == self.depth:
                        game.ai_move = move
            
            return best_value
        
        expectimax_no_ab(game, self.depth)
        return game.ai_move
