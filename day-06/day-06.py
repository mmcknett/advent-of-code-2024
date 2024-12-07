import copy
from pathlib import Path

sample = Path('day-06/sample.txt').read_text()
puzzle = Path('day-06/input.txt').read_text()

GUARD = {
  '^': (-1, 0),
  '>': (0, 1),
  'v': (1, 0),
  '<': (0, -1)
}

class Board:
  def __init__(self, puz):
    self._board = [list(row) for row in puz.split('\n')]
    self._guard_pos = self._find_guard()
    self._history = set()

  def _find_guard(self):
    board = self._board
    for r in range(len(board)):
      for c in range(len(board[r])):
        if board[r][c] in GUARD:
          return (r, c)

    raise ValueError("Guard not found!")

  def _move_guard(self) -> bool:
    if self._guard_pos is None:
      return False

    r, c = self._guard_pos
    g = self._board[r][c]
    next_pos = self._next_guard_pos()
    n_r, n_c = next_pos
    if not (0 <= n_r < len(self._board) and 0 <= n_c < len(self._board[0])):
      self._board[r][c] = 'X'
      self._history.add((r, c, g))
      self._guard_pos = None
      return False
    
    if self._board[n_r][n_c] == '#':
      self._rotate_guard()
      return True
    
    self._board[n_r][n_c] = g
    self._guard_pos = (n_r, n_c)
    self._board[r][c] = 'X'
    if (r, c, g) in self._history:
      return False # We're in a loop, don't keep moving.

    self._history.add((r, c, g))
    return True
  
  def _next_guard_pos(self):
    r, c = self._guard_pos
    g = self._board[r][c]
    dir = GUARD[g]
    next_pos = add(self._guard_pos, dir)
    return next_pos
  
  def _rotate_guard(self):
    orientations = list(GUARD)
    r, c = self._guard_pos
    g = self._board[r][c]
    i = orientations.index(g)
    g = orientations[(i + 1) % len(orientations)]
    self._board[r][c] = g

  def run(self, debug=False):
    steps = 0

    while self._move_guard():
      steps += 1
      if debug and steps % 1000 == 0:
        print(f"Steps so far: {steps}")

    return steps
  
  def run_try_obs(self, debug=False):
    steps = 0
    possible_obstructions = set()
    obstructions_tried = set()

    while self._move_guard():
      steps += 1
      if debug and steps % 1000 == 0:
        print(f"Steps so far: {steps}")

      # Would placing an obstruction in the next spot create a loop?
      obstruction_candidate = self._next_guard_pos()
      o_r, o_c = obstruction_candidate
      if not (0 <= o_r < len(self._board) and 0 <= o_c < len(self._board[0])):
        # Can't put an obstruction off the board!
        continue
      fut = copy.deepcopy(self)
      fut._board[o_r][o_c] = '#'
      obstructions_tried.add(obstruction_candidate)
      if fut.is_loop(debug=False):
        possible_obstructions.add(obstruction_candidate)
        if debug:
          print(f"Loop for ({o_r}, {o_c})")

    return possible_obstructions
  
  def is_loop(self, debug=False):
    self.run(debug=debug)
    # If the guard is still present after running, it's a loop.
    return self._guard_pos is not None
  
  def space_count(self):
    return sum(1 for r in self._board for c in r if c == 'X')
  
  def print(self):
    for r in self._board:
      print(''.join(r))


def add(t1, t2):
  a, b = t1
  c, d = t2
  return a + c, b + d

def d6p1():
  b = Board(sample)
  b.run()
  answer = b.space_count()
  print(f"Part 1 (sample): {answer} unique spaces")
  assert answer == 41

  b = Board(puzzle)
  b.run()
  answer = b.space_count()
  print(f"Part 1 (input): {answer} unique spaces")
  assert answer == 4939 # First try!

def d6p2():
  b = Board(sample)
  obstruction_candidates = b.run_try_obs(debug=True)
  count = len(obstruction_candidates)
  print(f"Part 2 (sample): {count} places to put an obstruction")
  assert count == 6

  b = Board(puzzle)
  os = b.run_try_obs(debug=True)
  count = len(os)
  print(f"Part 2 (input): {count} candidates")

  mistakes = set()
  for obs in os:
    rerun = Board(puzzle)
    o_r, o_c = obs
    rerun._board[o_r][o_c] = '#'
    does_loop = rerun.is_loop()
    if not does_loop:
      print(f"{obs} was wrong!")
      mistakes.add(obs)

  fixed = os - mistakes
  count = len(fixed)
  print(f"Actually, maybe it's {count}")

  assert count != 1545 # This is too high.
  assert count == 1434 # This is it. Removing the wrong ones afterward apparently worked.


if __name__ == "__main__":
  d6p1()
  d6p2()
