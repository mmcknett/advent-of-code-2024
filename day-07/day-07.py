from pathlib import Path

sample = Path("day-07/sample.txt").read_text().split('\n')
puzzle = Path("day-07/input.txt").read_text().split('\n')

def d7p1s():
  eqns = [Equation(line) for line in sample]
  answer = sum(e.test_value for e in eqns if e.is_valid())
  print(f"Part 1 sample: {answer}")
  assert answer == 3749

def d7p1p():
  eqns = [Equation(line) for line in puzzle]
  answer = sum(e.test_value for e in eqns if e.is_valid())
  print(f"Part 1 puzzle: {answer}")
  assert answer == 303876485655 # First try!

def d7p2s():
  eqns = [Equation(line) for line in sample]
  answer = sum(e.test_value for e in eqns if e.is_valid_with_concat())
  print(f"Part 2 sample: {answer}")
  assert answer == 11387

def d7p2p():
  eqns = [Equation(line) for line in puzzle]
  answer = sum(e.test_value for e in eqns if e.is_valid_with_concat())
  print(f"Part 2 puzzle: {answer}")
  assert answer == 146111650210682 # First try!

class Equation():
  def __init__(self, line):
    value, rest = line.split(': ')
    self._total = int(value)
    self._numbers = [int(v) for v in rest.split(" ")]

  @property
  def test_value(self):
    return self._total

  def is_valid(self):
    return self._total in possible_results(self._numbers)
  
  def is_valid_with_concat(self):
    return self._total in possible_results(self._numbers, with_cat=True)

def possible_results(numbers, with_cat=False):
  if len(numbers) == 0:
    raise ValueError("Don't call this with an empty list.")
  if len(numbers) == 1:
    return set(numbers)
  
  [*rest, last] = numbers
  possibles = possible_results(rest, with_cat=with_cat)
  mults = {last * p for p in possibles}
  adds = {last + p for p in possibles}

  if with_cat:
    cats = {concat(p, last) for p in possibles}
    return cats.union(adds).union(mults)

  return mults.union(adds)

def concat(a, b):
  return int(str(a) + str(b))

assert possible_results([2, 3]) == {5, 6}
assert possible_results([2, 5, 7]) == {17, 70, 14, 49}
assert possible_results([2, 3], with_cat=True) == {5, 6, 23}
assert possible_results([2, 5, 7], with_cat=True) == {17, 70, 14, 49, 32, 175, 77, 107, 257}

if __name__ == "__main__":
  d7p1s()
  d7p1p()
  d7p2s()
  d7p2p()
