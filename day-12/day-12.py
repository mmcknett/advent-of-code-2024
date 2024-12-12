from pathlib import Path
from collections import defaultdict

sample = [list(line) for line in Path('day-12/sample.txt').read_text().split('\n')]
small_sample = [list(line) for line in Path('day-12/small_sample.txt').read_text().split('\n')]
small_sample_2 = [list(line) for line in Path('day-12/small_sample_2.txt').read_text().split('\n')]

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
assert s_area['A'] == 4
assert s_perimeter['A'] == 10
assert s_perimeter['B'] == 8
assert s_area['D'] == 1
assert s_perimeter['D'] == 4

s_area, s_perimeter = calc(small_sample_2)
assert s_perimeter['O'] == 36

def price(region, area, perim):
  return area[region] * perim[region]
