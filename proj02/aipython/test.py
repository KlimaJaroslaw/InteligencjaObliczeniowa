from stripsProblem import problem1, blocks2
from searchMPP import SearcherMPP
from stripsForwardPlanner import Forward_STRIPS
import matplotlib.pyplot as plt
def test_blocks_world():
    print("\n--- Testowanie Świata Klocków (blocks2 - 4 klocki) ---")
    print(SearcherMPP(Forward_STRIPS(blocks2)).search())
    

if __name__ == "__main__":
    test_blocks_world()

