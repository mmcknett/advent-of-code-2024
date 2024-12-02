from textwrap import dedent
from pathlib import Path


def day1(input: str) -> int:
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

def load_part1() -> str:
  with Path('day-01/part1.txt').open('rt') as f:
    return f.read()

TEST_INPUT = dedent("""
  3   4
  4   3
  2   5
  1   3
  3   9
  3   3
  """)

if __name__ == "__main__":
  assert day1(TEST_INPUT) == 11
  print("Tests pass")

  part1 = load_part1()
  result = day1(part1)
  # 52658 is too low. We need to take the *absolute value* of the difference.
  # That did it. It's 1319616.
  print(f"Part 1 result: {result}")
