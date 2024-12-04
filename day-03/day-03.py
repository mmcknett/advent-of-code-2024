from pathlib import Path
import re

input = Path('day-03/input.txt').read_text()

def day3p1():
  matches = re.findall('mul\(\d{1,3},\d{1,3}\)', input)
  evaluated = (mul(expr) for expr in matches)
  answer = sum(evaluated)
  print(f"Part 1: {answer}")
  assert answer == 189527826 # First try

def mul(expr: str):
  if not expr.startswith("mul(") and expr.endswith(")"):
    raise ValueError(f"Didn't get a mul, got '{expr}'")
  stripped = expr[4:-1]
  a, b = stripped.split(",")
  return int(a) * int(b)


if __name__ == "__main__":
  day3p1()