"""
Test Expectiminimax - sprawdza czy algorytm działa poprawnie
"""

from lab01 import Hexapawn
from expectiminimax import ExpectimaxAB
from easyAI import AI_Player, Negamax


def test_single_game():
    """Test pojedynczej gry z Expectimax."""
    print("Test pojedynczej gry z ExpectimaxAB...")
    
    scoring = lambda game: -100 if game.lose() else 0
    
    # Gra probabilistyczna z Expectimax
    ai_expectimax = ExpectimaxAB(depth=6, scoring=scoring)
    game = Hexapawn([AI_Player(ai_expectimax), AI_Player(ai_expectimax)], 
                    size=(4, 4), probabilistic=True)
    
    print("Rozgrywka Expectimax vs Expectimax (probabilistic)...")
    game.play()
    print(f"Zwycięzca: gracz {game.opponent_index} po {game.nmove} ruchach\n")


def test_expectimax_vs_negamax():
    """Porównanie Expectimax vs Negamax."""
    print("Test: ExpectimaxAB vs Negamax (probabilistic)...")
    
    scoring = lambda game: -100 if game.lose() else 0
    
    ai_expectimax = ExpectimaxAB(depth=6, scoring=scoring)
    ai_negamax = Negamax(6, scoring)
    
    game = Hexapawn([AI_Player(ai_expectimax), AI_Player(ai_negamax)], 
                    size=(4, 4), probabilistic=True)
    
    print("Rozgrywka ExpectimaxAB vs Negamax (probabilistic)...")
    game.play()
    print(f"Zwycięzca: gracz {game.opponent_index} po {game.nmove} ruchach")
    print(f"(gracz 1 = ExpectimaxAB, gracz 2 = Negamax)\n")


if __name__ == "__main__":
    print("=" * 60)
    print("TESTY EXPECTIMINIMAX")
    print("=" * 60 + "\n")
    
    test_single_game()
    test_expectimax_vs_negamax()
    
    print("=" * 60)
    print("Testy zakończone!")
    print("=" * 60)
