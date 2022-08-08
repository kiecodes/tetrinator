import timeit

import moves

py = timeit.timeit("moves.evaluate_all_possible_moves(moves.Field(), moves.Stone(0))", globals=globals(), number=100)

print(py)