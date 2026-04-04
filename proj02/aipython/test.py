from stripsProblem import problem1, blocks2, gripper_problem, monkey_problem, gripper_problem_subgoal1, gripper_problem_subgoal2, blocks2_subgoal1, blocks2_subgoal2, monkey_problem_subgoal1, monkey_problem_subgoal2, gripper8_subgoal1, gripper8_subgoal2, gripper10_subgoal1, gripper10_subgoal2, gripper10_subgoal3, gripper12_subgoal1, gripper12_subgoal2, gripper12_subgoal3
from searchMPP import SearcherMPP
from stripsForwardPlanner import Forward_STRIPS
import matplotlib.pyplot as plt
import time


def gripper_heuristic(state, goal):
    """
    Heurystyka dla problemu gripper (transport piłek między pokojami).
    Liczy: liczbę piłek do przeniesienia + dodatkowe koszty transportu.
    Pomaga, bo szybciej znajduje rozwiązanie dzięki lepszemu szacowaniu.
    """
    h = 0
    balls_to_move = []
    
    for feat, goal_val in goal.items():
        if feat.startswith('at_ball'):
            if state.get(feat) != goal_val:
                balls_to_move.append(feat)
    
    if not balls_to_move:
        return 0
    
    h += len(balls_to_move)
    

    for ball in balls_to_move:
        current_loc = state.get(ball)
        if current_loc != 'left' and current_loc != 'right':
            h += 1
    
    rob_at = state.get('rob_at')
    if rob_at == 'roomA' and len(balls_to_move) > 0:
        h += 1

    elif rob_at == 'roomB':
        any_in_A = any(state.get(b) == 'roomA' for b in balls_to_move)
        if any_in_A:
            h += 1
            
    return h

def test_problems():
    print("\n--- BlockWorld problem ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(blocks2)).search())
    print(f"Time: {time.time() - start:.3f}s")
    
    print("--- Robot problem---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(problem1)).search())
    print(f"Time: {time.time() - start:.3f}s")
    
    print("\n--- Monkey problem ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(monkey_problem)).search())
    print(f"Time: {time.time() - start:.3f}s")
def test_heuristic():
    print("\n--- Gripper problem without heuristics ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(gripper_problem)).search())
    print(f"Time: {time.time() - start:.3f}s")
    
    print("\n--- Gripper problem with heuristics ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(gripper_problem,gripper_heuristic)).search())
    print(f"Time: {time.time() - start:.3f}s")

def run_subgoal_with_heuristic(label, problem):
    print(f"\n--- {label} ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(problem, gripper_heuristic)).search())
    print(f"Time: {time.time() - start:.3f}s")


if __name__ == "__main__":
    print("Zadanie 1 --- ( 4 pkt )")
    test_problems()
    test_heuristic()
    print("\n\nZadanie 2 --- (6 pkt)")
    print("Testy problemów z podcelami:")
    
    print("\n--- Gripper: Subgoal 1 (move ball1, ball2) - without heuristics ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(gripper_problem_subgoal1)).search())
    print(f"Time: {time.time() - start:.3f}s")

    print("\n--- Gripper: Subgoal 1 (move ball1, ball2) - with heuristics ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(gripper_problem_subgoal1, gripper_heuristic)).search())
    print(f"Time: {time.time() - start:.3f}s")
    
    print("\n--- Gripper: Subgoal 2 (move ball3, ball4) - without heuristics ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(gripper_problem_subgoal2)).search())
    print(f"Time: {time.time() - start:.3f}s")

    print("\n--- Gripper: Subgoal 2 (move ball3, ball4) - with heuristics ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(gripper_problem_subgoal2, gripper_heuristic)).search())
    print(f"Time: {time.time() - start:.3f}s")
    
    print("\n--- BlockWorld: Subgoal 1 (arrange d,c,b) ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(blocks2_subgoal1)).search())
    print(f"Time: {time.time() - start:.3f}s")
    
    print("\n--- BlockWorld: Subgoal 2 (final arrangement) ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(blocks2_subgoal2)).search())
    print(f"Time: {time.time() - start:.3f}s")
    
    print("\n--- Monkey: Subgoal 1 (reach box location) ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(monkey_problem_subgoal1)).search())
    print(f"Time: {time.time() - start:.3f}s")
    
    print("\n--- Monkey: Subgoal 2 (get bananas from box) ---")
    start = time.time()
    print(SearcherMPP(Forward_STRIPS(monkey_problem_subgoal2)).search())
    print(f"Time: {time.time() - start:.3f}s")

    print("\n\nZadanie 3 --- (8 pkt)")
    print("Dodatkowe 3 problemy z podcelami (co najmniej 20 akcji łącznie):")

    print("\nProblem A: 8 piłek (min 20 akcji)")
    run_subgoal_with_heuristic("A/Subgoal 1: przenieś ball1-ball4", gripper8_subgoal1)
    run_subgoal_with_heuristic("A/Subgoal 2: przenieś ball5-ball8", gripper8_subgoal2)

    print("\nProblem B: 10 piłek (min 25 akcji)")
    run_subgoal_with_heuristic("B/Subgoal 1: przenieś ball1-ball4", gripper10_subgoal1)
    run_subgoal_with_heuristic("B/Subgoal 2: przenieś ball5-ball8", gripper10_subgoal2)
    run_subgoal_with_heuristic("B/Subgoal 3: przenieś ball9-ball10", gripper10_subgoal3)

    print("\nProblem C: 12 piłek (min 30 akcji)")
    run_subgoal_with_heuristic("C/Subgoal 1: przenieś ball1-ball4", gripper12_subgoal1)
    run_subgoal_with_heuristic("C/Subgoal 2: przenieś ball5-ball8", gripper12_subgoal2)
    run_subgoal_with_heuristic("C/Subgoal 3: przenieś ball9-ball12", gripper12_subgoal3)
    
