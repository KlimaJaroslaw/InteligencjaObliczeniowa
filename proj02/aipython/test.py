from stripsProblem import problem1, blocks2, gripper_problem, monkey_problem
from searchMPP import SearcherMPP
from stripsForwardPlanner import Forward_STRIPS
import matplotlib.pyplot as plt


def gripper_heuristic(state, goal):
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
    print(SearcherMPP(Forward_STRIPS(blocks2)).search())
    print("--- Robot problem---")
    print(SearcherMPP(Forward_STRIPS(problem1)).search())
    print("\n--- Monkey problem ---")
    print(SearcherMPP(Forward_STRIPS(monkey_problem)).search())
def test_heuristic():
    
    print("\n--- Gripper problem without heuristics ---")
    print(SearcherMPP(Forward_STRIPS(gripper_problem)).search())
    print("\n--- Gripper problem with heuristics ---")
    print(SearcherMPP(Forward_STRIPS(gripper_problem,gripper_heuristic)).search())


if __name__ == "__main__":
    print("Zadanie 1 --- ( 4 pkt )")
    test_problems()
    test_heuristic()
    print("\n\n Zadanie 2 --- (6 pkt)")
    
