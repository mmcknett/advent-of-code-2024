from pathlib import Path

input = Path('day-04/input.txt').read_text().split("\n")
sample = Path('day-04/sample.txt').read_text().split("\n")

def d4p1():
  print("Part 1:")
  result = count_all_xmas(sample)
  print(f"The sample has {result} XMASes")
  assert result == 18 # The sample has 18

  result = count_all_xmas(input)
  print(f"The input has {result} XMASes")
  assert result == 2549 # The puzzle answer, first try!

def count_all_xmas(to_check: list[str]) -> int:
  total = 0
  for r, row in enumerate(to_check):
    for c in range(len(row)):
      curr = count_xmas(r, c, to_check)
      total += curr
  return total

rt = [(0, 1), (0, 2), (0, 3)]
rtdn = [(1, 1), (2, 2), (3, 3)]
dn = [(1, 0), (2, 0), (3, 0)]
ltdn = [(1, -1), (2, -2), (3, -3)]
lt = [(0, -1), (0, -2), (0, -3)]
ltup = [(-1, -1), (-2, -2), (-3, -3)]
up = [(-1, 0), (-2, 0), (-3, 0)]
rtup = [(-1, 1), (-2, 2), (-3, 3)]
all = [rt, rtdn, dn, ltdn, lt, ltup, up, rtup]

def add(t1, t2):
  a, b = t1
  c, d = t2
  return a + c, b + d

def count_xmas(r: int, c: int, to_check: list[str]) -> int:
  if to_check[r][c] != 'X':
    return 0
  
  count = 0
  for dir in all:
    if validate(r, c, dir, to_check):
      count += 1
  return count

def validate(r: int, c: int, list_offset, to_check) -> bool:
  list_offset = [(0,0)] + list_offset
  for offset, letter in zip(list_offset, "XMAS"):
    curr_r, curr_c = add(offset, (r, c))
    if curr_r >= len(to_check) or curr_r < 0:
      return False
    if curr_c >= len(to_check[curr_r]) or curr_c < 0:
      return False
    if to_check[curr_r][curr_c] != letter:
      return False
    
  return True

assert validate(4, 0, rt, sample) == True
assert validate(0, 4, rt, sample) == False

if __name__ == "__main__":
  d4p1()
