from pathlib import Path


def load(file_name):
  path = Path("day-19") / file_name
  contents = path.read_text()
  available_patterns, desired_patterns = contents.split('\n\n')
  available_patterns = available_patterns.split(', ')
  desired_patterns = desired_patterns.split('\n')
  return available_patterns, desired_patterns

sample_a, sample_d = load('sample.txt')
puzzle_a, puzzle_d = load('puzzle.txt')

def can_make(available_patterns: list[str], desired_result: str):
  if desired_result == "":
    return True
  
  for a in available_patterns:
    if desired_result.startswith(a):
      can_make_remainder = can_make(available_patterns, desired_result[len(a):])
      if can_make_remainder:
        return True

  return False

assert can_make(['a'], 'aaa')

assert can_make(sample_a, sample_d[0])
assert not can_make(sample_a, sample_d[4])

def ways_to_make(available_patterns: list[str], desired_result: str, answer_cache = None):
  if desired_result == "":
    return 1
  
  answer_cache = answer_cache if answer_cache is not None else {}
  if desired_result in answer_cache:
    return answer_cache[desired_result]

  ways = 0
  for a in available_patterns:
    if desired_result.startswith(a):
      w = ways_to_make(available_patterns, desired_result[len(a):], answer_cache)
      ways += w

  answer_cache[desired_result] = ways
  return ways

assert ways_to_make(sample_a, sample_d[2]) == 4
assert ways_to_make(sample_a, sample_d[4]) == 0
print('Tests pass!')

def day19p1():
  possible_designs = 0
  for design in puzzle_d:
    if can_make(puzzle_a, design):
      possible_designs += 1
  print(f"Part 1: {possible_designs} designs possible")
  assert possible_designs == 209

day19p1()

def day19p2():
  ways_sample_designs = [ways_to_make(sample_a, design) for design in sample_d]
  all_ways = sum(ways_sample_designs)
  print(f"Part 2 (sample): {all_ways} is the sum of all ways to make each design")

  ways_each_design = [ways_to_make(puzzle_a, design) for design in puzzle_d]
  all_ways = sum(ways_each_design)
  print(f"Part 2: {all_ways} is the sum of all ways to make each design")
  assert all_ways < 811572281042468 # First try was too high
  assert all_ways == 777669668613191 # Defaulting the dictionary for answer_cache was the bug? Weird.

day19p2()
