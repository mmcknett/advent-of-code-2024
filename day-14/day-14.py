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

sample_dims = (11,7)
sample_robots = [Robot(line, sample_dims) for line in Path('day-14/sample.txt').read_text().split('\n')]
puzzle_robots = [Robot(line) for line in Path('day-14/puzzle.txt').read_text().split('\n')]

def d14p1():
  
  
  final_positions = [r.predict(100) for r in sample_robots]
  quadrant_counts = Counter(quadrant(pos, sample_dims) for pos in final_positions)
  answer = np.prod(np.array([v for c, v in quadrant_counts.items() if c > -1]))
  print(f"Safety Factor for the sample is: {answer}")
  assert answer == 12

  final_positions = [r.predict(100) for r in puzzle_robots]
  quadrant_counts = Counter(quadrant(pos) for pos in final_positions)
  answer = np.prod(np.array([v for c, v in quadrant_counts.items() if c > -1]))
  print(f"Safety Factor for the puzzle is: {answer}")
  assert answer == 219150360

d14p1()

def image_robots(robots: list[Robot], step, dims=(101, 103)):
  grid = np.zeros(dims)
  for r in robots:
    x, y = r.predict(step)
    grid[x, y] += 1

  return grid

def has_line(image):
  line_len = 11
  for x in range(0, image.shape[0] - line_len, line_len):
    for y in range(image.shape[1]):
      if image[x:x+line_len, y].all():
        return True
      
  return False

assert has_line(image_robots(puzzle_robots, 60_068))
assert not has_line(image_robots(puzzle_robots, 60_067))

import cv2 as cv

key = -1
# It's between 50000 and 100000
# i = 50_000
# PART 2
# This step count *does* display a Christmas tree, but this isn't the answer
# It must be smaller? I guessed too many times to be told.
i = 8053


max_i = 100_000
min_i = 5_000

def d14p2():
  answer = -1
  for ii in range(i):
    if has_line(image_robots(puzzle_robots, ii)):
      answer = ii
      break
  print(f"Part 2: first with a tree is {answer}")
  assert answer == 8053

d14p2()

pause = True
backward = False
fast = False
while key != ord('x') and i <= max_i and i >= min_i:
  if not pause:
    if backward:
      i -= 1
    else:
      i += 1
  image = image_robots(puzzle_robots, i)
  image = np.interp(image, (0, 3), (0, 255)).astype(np.uint8)
  image = cv.resize(image, None, fx=10, fy=10, interpolation=cv.INTER_NEAREST)
  image = cv.applyColorMap(image, cv.COLORMAP_SUMMER)
  cv.putText(image, str(i), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
  cv.imshow('Part 2', image)

  key = cv.waitKey(25 if fast else 500)
  if key == ord(' '):
    pause = not pause
  if key == ord('b'):
    backward = True
  if key == ord('f'):
    backward = False
  if key == ord('s'):
    fast = not fast

cv.destroyAllWindows()