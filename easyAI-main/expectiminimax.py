"""
Expectiminimax z odcięciem alfa-beta dla gier probabilistycznych.

Algorytm dla gier dwuosobowych z elementem losowym (chance nodes).
Rozszerzenie Negamax, które uwzględnia prawdopodobieństwa różnych wyników losowych.
"""

inf = float("infinity")


def expectiminimax(game, depth, origDepth, scoring, alpha=-inf, beta=+inf):
    """
    Expectiminimax z alfa-beta pruning.
    
    Algorytm przeszukuje drzewo gry uwzględniając:
    - Węzły decyzyjne graczy (max/min)
    - Węzły losowe (chance) - oblicza wartość oczekiwaną
    
    Args:
        game: obiekt gry (musi mieć metody get_chance_outcomes i apply_chance_outcome)
        depth: pozostała głębokość rekurencji
        origDepth: oryginalna głębokość (do zapisania najlepszego ruchu)
        scoring: funkcja oceny pozycji
        alpha: dolne ograniczenie (alfa)
        beta: górne ograniczenie (beta)
    
    Returns:
        wartość pozycji dla bieżącego gracza
    """
    
    # Warunek końcowy: osiągnięto maksymalną głębokość lub gra się skończyła
    if depth == 0 or game.is_over():
        # Bonus za szybsze zwycięstwa / późniejsze porażki
        return scoring(game) * (1 + 0.001 * depth)
    
    possible_moves = game.possible_moves()
    
    if depth == origDepth:
        game.ai_move = possible_moves[0]
    
    best_value = -inf
    
    for move in possible_moves:
        # Wykonaj deterministyczną część ruchu
        game_copy = game.copy()
        game_copy.make_move_deterministic(move)
        
        # Teraz następuje węzeł CHANCE - oblicz wartość oczekiwaną
        # NIE negujemy wartości tutaj, bo już jest zanegowana w expectation_node
        move_value = expectation_node(game_copy, depth, origDepth, scoring, alpha, beta)
        
        if move_value > best_value:
            best_value = move_value
            if depth == origDepth:
                game.ai_move = move
        
        # Alfa-beta pruning
        alpha = max(alpha, best_value)
        if alpha >= beta:
            break
    
    return best_value


def expectation_node(game, depth, origDepth, scoring, alpha, beta):
    """
    Węzeł losowy (chance node) - oblicza wartość oczekiwaną.
    
    Po wykonaniu ruchu mogą wystąpić różne losowe zdarzenia.
    Obliczamy średnią ważoną wartości wszystkich możliwych wyników.
    
    Args:
        game: stan gry po wykonaniu deterministycznego ruchu
        depth, origDepth, scoring, alpha, beta: parametry jak w expectiminimax
    
    Returns:
        wartość oczekiwana pozycji
    """
    
    # Pobierz możliwe losowe zdarzenia i ich prawdopodobieństwa
    if hasattr(game, 'get_chance_outcomes'):
        chance_outcomes = game.get_chance_outcomes()
    else:
        # Jeśli gra nie ma probabilistyki, traktuj jak normalny Negamax
        chance_outcomes = [(1.0, ())]
    
    expected_value = 0.0
    
    for probability, outcome in chance_outcomes:
        # Stwórz kopię gry i zastosuj losowe zdarzenie
        game_after_chance = game.copy()
        
        if hasattr(game_after_chance, 'apply_chance_outcome'):
            game_after_chance.apply_chance_outcome(outcome)
        
        # Zmień gracza i kontynuuj rekurencję
        game_after_chance.switch_player()
        
        # Rekurencyjne wywołanie dla przeciwnika (negujemy bounds i wartość - Negamax style)
        value = -expectiminimax(
            game_after_chance,
            depth - 1,
            origDepth,
            scoring,
            -beta,
            -alpha
        )
        
        # Dodaj do wartości oczekiwanej
        expected_value += probability * value
    
    return expected_value


class ExpectimaxAB:
    """
    Klasa opakowująca algorytm Expectiminimax z alfa-beta.
    
    Używa się podobnie jak Negamax z easyAI:
    
    Example:
        >>> from expectiminimax import ExpectimaxAB
        >>> from lab01 import Hexapawn
        >>> from easyAI import AI_Player
        >>> 
        >>> scoring = lambda game: -100 if game.lose() else 0
        >>> ai = ExpectimaxAB(depth=8, scoring=scoring)
        >>> game = Hexapawn([AI_Player(ai), AI_Player(ai)], probabilistic=True)
        >>> game.play()
    
    Parameters:
        depth: Głębokość przeszukiwania (liczba ruchów do przodu)
        scoring: Funkcja oceny pozycji f(game) -> score
        win_score: Wartość powyżej której uznajemy wygraną (przydatne do optymalizacji)
    """
    
    def __init__(self, depth, scoring=None, win_score=+inf):
        self.depth = depth
        self.scoring = scoring
        self.win_score = win_score
    
    def __call__(self, game):
        """
        Zwraca najlepszy ruch dla bieżącego stanu gry.
        
        Args:
            game: obiekt gry
        
        Returns:
            najlepszy ruch (string lub inny typ zgodny z game.possible_moves())
        """
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


# Dodatkowa klasa: Expectiminimax BEZ alfa-beta (dla porównania wydajności)
class ExpectimaxNoAB:
    """
    Expectiminimax BEZ odcięcia alfa-beta.
    Sprawdza wszystkie możliwe węzły - wolniejszy, ale kompletny.
    Przydatny do porównania wydajności z wersją z alfa-beta.
    """
    
    def __init__(self, depth, scoring=None):
        self.depth = depth
        self.scoring = scoring
    
    def __call__(self, game):
        scoring = self.scoring if self.scoring else (lambda g: g.scoring())
        
        def expectimax_no_ab(game, depth):
            """Expectiminimax bez alfa-beta odcięć."""
            if depth == 0 or game.is_over():
                return scoring(game) * (1 + 0.001 * depth)
            
            possible_moves = game.possible_moves()
            best_value = -inf
            
            for move in possible_moves:
                game_copy = game.copy()
                game_copy.make_move_deterministic(move)
                
                # Węzeł chance
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
                    
                    # Negacja wartości dla przeciwnika (Negamax)
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
