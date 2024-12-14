import numpy as np
from pathlib import Path
from collections import Counter

class Robot():
  def __init__(self, line: str, dims = (101, 103)):
    p_str, v_str = line.split(' ')
    self.p = np.array([int(n) for n in p_str[2:].split(',')])
    self.v = np.array([int(n) for n in v_str[2:].split(',')])
    self.dims = np.array(dims)

  def predict(self, steps=100):
    result = (self.p + steps * self.v) % self.dims
    return result

assert np.array_equal(Robot("p=2,4 v=2,-3", (11, 7)).predict(5), np.array([1, 3]))

def quadrant(pos: np.ndarray, dims = (101, 103)):
  w, h = dims
  x, y = pos
  mid_w, mid_h = w // 2, h // 2
  if x == mid_w or y == mid_h:
    return -1
  
  if x < mid_w and y < mid_h:
    return 0
  if x > mid_w and y < mid_h:
    return 1
  if x < mid_w and y > mid_h:
    return 2
  if x > mid_w and y > mid_h:
    return 3
  
  raise RuntimeError("This shouldn't happen ever.")

r = Robot("p=2,4 v=2,-3", (11, 7))
assert quadrant(r.predict(4), (11, 7)) == 3
assert quadrant(r.predict(5), (11, 7)) == -1

def d14p1():
  sample_dims = (11,7)
  robots = [Robot(line, sample_dims) for line in Path('day-14/sample.txt').read_text().split('\n')]
  final_positions = [r.predict(100) for r in robots]
  quadrant_counts = Counter(quadrant(pos, sample_dims) for pos in final_positions)
  answer = np.prod(np.array([v for c, v in quadrant_counts.items() if c > -1]))
  print(f"Safety Factor for the sample is: {answer}")
  assert answer == 12

  robots = [Robot(line) for line in Path('day-14/puzzle.txt').read_text().split('\n')]
  final_positions = [r.predict(100) for r in robots]
  quadrant_counts = Counter(quadrant(pos) for pos in final_positions)
  answer = np.prod(np.array([v for c, v in quadrant_counts.items() if c > -1]))
  print(f"Safety Factor for the puzzle is: {answer}")
  assert answer == 219150360

d14p1()