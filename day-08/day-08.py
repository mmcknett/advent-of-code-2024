from pathlib import Path
from collections import defaultdict

load = lambda filename: [list(line) for line in Path(filename).read_text().split('\n')]
sample = load("day-08/sample.txt")
puzzle = load("day-08/input.txt")
onepair = load("day-08/sample_onepair.txt")
onepair_expected = load("day-08/sample_onepair_expectedantinodes.txt")

def griderate(grid):
  for r, row in enumerate(grid):
    for c, val in enumerate(row):
      yield (r, c, val)

def in_bounds(r, c, grid):
  if len(grid) == 0:
    return False
  return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def freqs(grid):
  freq_pos = defaultdict(set)
  for (r, c, entry) in griderate(grid):
    if entry != '.':
      freq_pos[entry].add((r, c))
  return freq_pos

assert freqs(sample).keys() == {'A', '0'}
assert freqs(puzzle).keys() == {'4', '1', 'Y', 'f', 'r', 'c', 'w', 'P', 'U', 'A', 'W', '8', 'L', 'n', 'T', '9', 'O', 'N', '6', 's', '0', 'Z', 'q', 'S', 'H', 'l', 't', 'o', '5', 'X', 'R', 'a', 'E', 'e', 'p', 'd', 'h', 'g', 'x', 'y', 'C', '7', 'z', '2', '3', 'D', 'i', 'I', 'G', 'j', 'J', 'u', 'Q', 'F'}

def sub(p1, p2):
  return (p1[0] - p2[0], p1[1] - p2[1])

assert sub((3, 4), (1, 1)) == (2, 3)

def add(p1, p2):
  return (p1[0] + p2[0], p1[1] + p2[1])

assert add((1, 2), (3, 4)) == (4, 6)

def neg(p):
  return (-p[0], -p[1])

assert neg((1, -2)) == (-1, 2)

def get_antinodes(freq_id, freqs):
  positions = list(freqs[freq_id])
  antinodes = set()
  for i, pos in enumerate(positions):
    for j in range(i+1, len(positions)):
      pos_2 = positions[j]
      diff = sub(pos_2, pos)
      a1 = sub(pos, diff)
      a2 = add(pos_2, diff)
      antinodes.add(a1)
      antinodes.add(a2)

  return antinodes

def repr_antinodes(grid, antinode_set):
  gridcopy = grid.copy()
  res = []
  for (r, c) in antinode_set:
    if 0 <= r < len(gridcopy) and 0 <= c < len(gridcopy[0]):
      gridcopy[r][c] = '#'
  for row in gridcopy:
    res.append(''.join(row))
  return '\n'.join(res)

assert repr_antinodes(onepair, get_antinodes('a', freqs(onepair))) == Path("day-08/sample_onepair_expectedantinodes.txt").read_text()

def count_antinodes(grid):
  all_freqs = freqs(grid)
  all_antinodes = set()
  for f in all_freqs:
    ans = get_antinodes(f, all_freqs)
    ans = {an for an in ans if in_bounds(an[0], an[1], grid)}
    all_antinodes = all_antinodes.union(ans)
  answer = len(all_antinodes)
  return answer

def d8p1():
  answer = count_antinodes(sample)
  print(f"Part 1 sample: {answer} antinodes")
  assert answer == 14

  answer = count_antinodes(puzzle)
  print(f"Part 1 puzzle: {answer} antinodes")
  assert answer == 336

if __name__ == "__main__":
  d8p1()
