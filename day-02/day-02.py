from pathlib import Path
from textwrap import dedent

def d2p1(input: list[str]) -> int:
  results = [is_safe(line) for line in input]
  return sum(1 for r in results if r is True)

def is_safe(line: str) -> bool:
  nums = [int(n) for n in line.split(' ')]
  inc_or_dec = all_increasing(nums) or all_decreasing(nums)
  close = all_close(nums)
  return inc_or_dec and close

def all_increasing(nums: list[int]) -> bool:
  for a, b in zip(nums[:-1], nums[1:]):
    if a >= b:
      return False
  return True

def all_decreasing(nums: list[int]) -> bool:
  for a, b in zip(nums[:-1], nums[1:]):
    if a <= b:
      return False
  return True

def all_close(nums: list[int]) -> bool:
  for a, b in zip(nums[:-1], nums[1:]):
    if abs(a-b) > 3:
      return False
  return True

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
  print("Tests pass!")

def part1():
  with Path("day-02/input.txt").open('rt') as f:
    input = [l for l in f.read().split("\n") if l != ""]
  result = d2p1(input)
  print(f"Number of safe lines is {result}")

if __name__ == "__main__":
  test()
