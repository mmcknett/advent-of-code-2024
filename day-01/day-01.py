from textwrap import dedent
from pathlib import Path


def day1part1(input: str) -> int:
  left, right = [], []
  for line in input.split('\n'):
    if "   " not in line:
      continue
    [a, b] = line.split('   ') # All the inputs are separated by three spaces.
    left.append(int(a))
    right.append(int(b))

  left.sort()
  right.sort()

  final = 0
  for l, r in zip(left, right):
    final += abs(r - l)

  return final

def day1part2(input: str) -> int:
  pass

def load_input() -> str:
  with Path('day-01/input.txt').open('rt') as f:
    return f.read()

TEST_INPUT = dedent("""
  3   4
  4   3
  2   5
  1   3
  3   9
  3   3
  """)

def test():
  assert day1part1(TEST_INPUT) == 11
  print("Tests pass")

def test_part2():
  assert day1part2(TEST_INPUT) == 31

def part1():
  part1 = load_input()
  result = day1part1(part1)
  # 52658 is too low. We need to take the *absolute value* of the difference.
  # That did it. It's 1319616.
  print(f"Part 1 result: {result}")
  assert result == 1319616

def part2():
  pass

if __name__ == "__main__":
  test_part2()
