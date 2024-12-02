from pathlib import Path
from textwrap import dedent

def d2p1(input: list[str]) -> int:
  results = [is_safe(line) for line in input]
  return sum(1 for r in results if r is True)

def is_safe(line: str) -> bool:
  nums = [int(n) for n in line.split(' ')]
  return is_safe_nums(nums)

def d2p2(input: list[str]) -> int:
  results = [is_safe_fuzzy(line) for line in input]
  return sum(1 for r in results if r is True)

def is_safe_fuzzy(line: str) -> bool:
  nums = [int(n) for n in line.split(' ')]
  return is_safe_fuzzy_nums(nums)

def is_safe_fuzzy_nums(nums: list[int]) -> bool:
  fail_incr_idx = all_increasing(nums)
  fail_decr_idx = all_decreasing(nums)
  inc_or_dec = fail_incr_idx == -1 or fail_decr_idx == -1

  fail_close_idx = all_close(nums)
  close = fail_close_idx == -1
  if inc_or_dec and close:
    return True
  
  # Try running the original is_safe_nums on the list with each failed index chopped out.
  indices_to_try = [i for i in [fail_incr_idx, fail_close_idx, fail_decr_idx] if i != -1]
  for i in indices_to_try:
    attempt = is_safe_nums(nums[0:i] + nums[i+1:])
    if attempt:
      return True

  # Even cutting out the first bad index didn't help, so it's false.
  return False

def is_safe_nums(nums: list[int]) -> bool:
  inc_or_dec = all_increasing(nums) == -1 or all_decreasing(nums) == -1
  close = all_close(nums) == -1
  return inc_or_dec and close

def all_increasing(nums: list[int]) -> int:
  for i, (a, b) in enumerate(zip(nums[:-1], nums[1:])):
    if a >= b:
      return i
  return -1

def all_decreasing(nums: list[int]) -> bool:
  for i, (a, b) in enumerate(zip(nums[:-1], nums[1:])):
    if a <= b:
      return i
  return -1

def all_close(nums: list[int]) -> bool:
  for i, (a, b) in enumerate(zip(nums[:-1], nums[1:])):
    if abs(a-b) > 3:
      return i
  return -1

TEST_INPUT = dedent("""
  7 6 4 2 1
  1 2 7 8 9
  9 7 6 2 1
  1 3 2 4 5
  8 6 4 4 1
  1 3 6 7 9
""")

def test():
  p1 = d2p1([line for line in TEST_INPUT.split('\n') if line != ""])
  assert p1 == 2

  p2 = d2p2([line for line in TEST_INPUT.split('\n') if line != ""])
  assert p2 == 4

  print("Tests pass!")

def part1():
  with Path("day-02/input.txt").open('rt') as f:
    input = [l for l in f.read().split("\n") if l != ""]
  result = d2p1(input)
  print(f"Number of safe lines is {result}")
  assert result == 516 # First try!

def part2():
  pass

if __name__ == "__main__":
  test()
