from pathlib import Path
from collections import defaultdict

sample = Path('day-05/sample.txt').read_text()
input = Path('day-05/input.txt').read_text()

def load(instr: str):
  rules, puzzle = instr.split('\n\n')
  rules = rules.split('\n')
  puzzle_inputs = [p_in.split(',') for p_in in puzzle.split('\n')]
  less_map = defaultdict(set)
  for rule in rules:
    [l, r] = rule.split('|')
    less_map[l].add(r)

  return less_map, puzzle_inputs

def test():
  less_map, puzzle_inputs = load(sample)
  assert "53" in less_map["47"]
  assert "75" in puzzle_inputs[0]
  assert lt("97", "13", less_map), "p97 has to come before p13"

def d5p1():
  less_map, puzzle_inputs = load(sample)
  answer = sum_valid_middles(less_map, puzzle_inputs)
  print(f"Part 1: The sample answer is {answer}")
  assert answer == 143

  less_map, puzzle_inputs = load(input)
  answer = sum_valid_middles(less_map, puzzle_inputs)
  print(f"Part 1: The puzzle input answer is {answer}")
  assert answer == 5087 # First try

def sum_valid_middles(less_map, puzzle_inputs):
  middles = []
  for p_in in puzzle_inputs:
    if check_input(p_in, less_map):
      mid = p_in[len(p_in)//2]
      middles.append(int(mid))
  answer = sum(middles)
  return answer

def check_input(page_list, less_map):
  for i, page in enumerate(page_list):
    before = page_list[:i]
    after = page_list[i+1:]
    if not (
      all(lt(pb, page, less_map) for pb in before) and 
      all(lt(page, pa, less_map) for pa in after)
    ):
      return False
    
  return True


def lt(a, b, less_map):
  return b in less_map[a]


if __name__ == '__main__':
  test()
  d5p1()