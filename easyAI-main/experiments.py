from lab01 import Hexapawn, NegamaxNoAB
from easyAI import AI_Player, Negamax
from expectiminimax import ExpectimaxAB, ExpectimaxNoAB
import time


def run_single_experiment(num_games, ai1, ai2, name1, name2, probabilistic):
    wins = {name1: 0, name2: 0}
    times = {name1: [], name2: []}
    total_moves = 0
    
    print(f"\n{name1} vs {name2} ({num_games} gier, {'prob' if probabilistic else 'det'})")
    
    for i in range(num_games):
        if i % 2 == 0:
            players = [AI_Player(ai1), AI_Player(ai2)]
            current_ai = [name1, name2]
        else:
            players = [AI_Player(ai2), AI_Player(ai1)]
            current_ai = [name2, name1]
        
        game = Hexapawn(players, size=(4, 4), probabilistic=probabilistic)
        moves = 0
        
        while not game.is_over():
            player_idx = (moves % 2)
            ai_name = current_ai[player_idx]
            
            start = time.time()
            move = game.get_move()
            elapsed = time.time() - start
            
            times[ai_name].append(elapsed)
            game.make_move(move)
            game.switch_player()
            moves += 1
        
        total_moves += moves
        winner_idx = game.opponent_index
        winner_name = current_ai[0] if winner_idx == 1 else current_ai[1]
        wins[winner_name] += 1
    
    avg_time1 = sum(times[name1]) / len(times[name1]) * 1000 if times[name1] else 0
    avg_time2 = sum(times[name2]) / len(times[name2]) * 1000 if times[name2] else 0
    
    print(f"  {name1}: {wins[name1]} wygranych, {avg_time1:.2f}ms/ruch")
    print(f"  {name2}: {wins[name2]} wygranych, {avg_time2:.2f}ms/ruch")
    print(f"  Srednia ruchow: {total_moves/num_games:.1f}")
    
    return wins, times, total_moves / num_games


def main_6pt():
    scoring = lambda game: -100 if game.lose() else 0
    num_games = 20
    
    print("=" * 60)
    print("ZADANIE NA 6 PUNKTÓW - NEGAMAX")
    print("=" * 60)
    
    ai_list = [
        (Negamax(5, scoring), "Negamax-5-AB"),
        (Negamax(10, scoring), "Negamax-10-AB"),
        (NegamaxNoAB(5, scoring), "Negamax-5"),
    ]
    
    print("\n### DETERMINISTYCZNE ###")
    for i in range(len(ai_list)):
        for j in range(i+1, len(ai_list)):
            run_single_experiment(
                num_games, ai_list[i][0], ai_list[j][0],
                ai_list[i][1], ai_list[j][1], False
            )
    
    print("\n### PROBABILISTYCZNE ###")
    for i in range(len(ai_list)):
        for j in range(i+1, len(ai_list)):
            run_single_experiment(
                num_games, ai_list[i][0], ai_list[j][0],
                ai_list[i][1], ai_list[j][1], True
            )
    
    print("\n" + "=" * 60)


def main_8pt():
    """Eksperymenty na 8 punktów - dodanie Expectiminimax."""
    scoring = lambda game: -100 if game.lose() else 0
    num_games = 15 
    
    print("\n" + "=" * 60)
    print("ZADANIE NA 8 PUNKTÓW - EXPECTIMINIMAX")
    print("=" * 60)
    
    ai_list = [
        (Negamax(6, scoring), "Negamax-6-AB"),
        (ExpectimaxAB(6, scoring), "Expectimax-6-AB"),
        (ExpectimaxNoAB(5, scoring), "Expectimax-5"),
    ]
    
    print("\n### DETERMINISTYCZNE (Expectimax powinien działać jak Negamax) ###")
    for i in range(len(ai_list)):
        for j in range(i+1, len(ai_list)):
            run_single_experiment(
                num_games, ai_list[i][0], ai_list[j][0],
                ai_list[i][1], ai_list[j][1], False
            )
    
    print("\n### PROBABILISTYCZNE (Expectimax powinien być lepszy) ###")
    for i in range(len(ai_list)):
        for j in range(i+1, len(ai_list)):
            run_single_experiment(
                num_games, ai_list[i][0], ai_list[j][0],
                ai_list[i][1], ai_list[j][1], True
            )
    
    print("\n" + "=" * 60)


def main():
    """Uruchamia wszystkie eksperymenty."""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "6":
            main_6pt()
        elif sys.argv[1] == "8":
            main_8pt()
        else:
            print("Użycie: python experiments.py [6|8]")
            print("  6 - eksperymenty na 6 punktów (Negamax)")
            print("  8 - eksperymenty na 8 punktów (Expectiminimax)")
    else:
        main_6pt()
        main_8pt()


if __name__ == "__main__":
    main()
