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
    dir = GUARD[g]
    next_pos = add(self._guard_pos, dir)
    n_r, n_c = next_pos
    if not (0 <= n_r < len(self._board) and 0 <= n_c < len(self._board[0])):
      self._board[r][c] = 'X'
      self._guard_pos = None
      return False
    
    if self._board[n_r][n_c] == '#':
      self._rotate_guard()
      return True
    
    self._board[n_r][n_c] = g
    self._guard_pos = (n_r, n_c)
    self._board[r][c] = 'X'
    return True
  
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
      if debug and steps % 100 == 0:
        print(f"Steps so far: {steps}")

    return steps
  
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
  


if __name__ == "__main__":
  d6p1()
