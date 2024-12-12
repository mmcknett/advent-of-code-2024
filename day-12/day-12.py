from pathlib import Path
from collections import defaultdict

def load(filename):
  raw_grid = [list(line) for line in Path(filename).read_text().split('\n')]
  seen = set()

  for r, row in enumerate(raw_grid):
    for c, val in enumerate(row):
      if len(val) < 2:
        add_group_id(r, c, raw_grid, seen)

  return raw_grid

def add_group_id(r, c, grid, seen):
  prefix = grid[r][c]
  id = 0
  while (new_val := f"{prefix}{id}") in seen:
    id += 1
  # We have a new group id; make sure everything connected
  # to this square gets it.

  floodfill(r, c, grid, new_val)
  seen.add(new_val)

def floodfill(r, c, grid, new):
  offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
  old = grid[r][c]
  grid[r][c] = new
  for o_r, o_c in offsets:
    n_r, n_c = r + o_r, c + o_c
    if (n_r < 0 or n_c < 0 or
        n_r >= len(grid) or n_c >= len(grid[0]) or
        grid[n_r][n_c] != old
    ):
      continue

    floodfill(n_r, n_c, grid, new)


sample = load('day-12/sample.txt')
small_sample = load('day-12/small_sample.txt')
small_sample_2 = load('day-12/small_sample_2.txt')



def perim(r, c, grid):
  result = 0
  offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
  for o_r, o_c in offsets:
    n_r, n_c = r + o_r, c + o_c
    if (n_r < 0 or n_c < 0 or
        n_r >= len(grid) or n_c >= len(grid[0]) or
        grid[n_r][n_c] != grid[r][c]
    ):
      result += 1
  return result

def calc(grid):
  area = defaultdict(int)
  perimeter = defaultdict(int)

  for r, row in enumerate(grid):
    for c, val in enumerate(row):
      # BUG: This doesn't allow us to group separated regions independently.
      # Four separate Xs should have a price of 4 * 1 each, for a total of 16,
      # but if we accumulate the area & perimeter like this, it will get 16 * 4 = 64.
      # Regions need to be uniquely identified.
      area[val] += 1
      perimeter[val] += perim(r, c, grid)

  return area, perimeter

s_area, s_perimeter = calc(small_sample)
assert s_area['A0'] == 4
assert s_perimeter['A0'] == 10
assert s_perimeter['B0'] == 8
assert s_area['D0'] == 1
assert s_perimeter['D0'] == 4

s_area, s_perimeter = calc(small_sample_2)
assert s_perimeter['O0'] == 36
assert s_perimeter['X0'] == 4
assert s_perimeter['X1'] == 4
assert s_perimeter['X2'] == 4
assert s_perimeter['X3'] == 4

def price(area, perim):
  id_end = 0
  price_sum_all_regions = 0
  for region in area:
    assert region in perim
    id_end += 1
    price_sum_all_regions += area[region] * perim[region]
  return price_sum_all_regions

assert price(s_area, s_perimeter) == 772

s_area, s_perimeter = calc(sample)
assert price(s_area, s_perimeter) == 1930

def d12p1():
  area, perim = calc(load("day-12/puzzle.txt"))
  answer = price(area, perim)
  print(f"Part 1 puzzle is {answer}")
  assert answer == 1319878

d12p1()