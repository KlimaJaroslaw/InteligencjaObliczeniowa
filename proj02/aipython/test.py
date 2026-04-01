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

def test_blocks_world():
    # print("\n--- Testowanie Świata Klocków (blocks2 - 4 klocki) ---")
    # print(SearcherMPP(Forward_STRIPS(blocks2)).search())
    # print("-------------------------")
    # print(SearcherMPP(Forward_STRIPS(problem1)).search())
    print("\n--- Gripper problem bez heurystyki ---")
    print(SearcherMPP(Forward_STRIPS(gripper_problem)).search())
    print("\n--- Gripper problem z heurystyką ---")
    print(SearcherMPP(Forward_STRIPS(gripper_problem,gripper_heuristic)).search())
    # print("\n--- Monkey problem ---")
    # print(SearcherMPP(Forward_STRIPS(monkey_problem)).search())

if __name__ == "__main__":
    test_blocks_world()

