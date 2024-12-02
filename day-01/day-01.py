from textwrap import dedent


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
    final += r - l

  return final


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
