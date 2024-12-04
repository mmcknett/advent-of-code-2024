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
  if not is_mul(expr):
    raise ValueError(f"Didn't get a mul, got '{expr}'")
  stripped = expr[4:-1]
  a, b = stripped.split(",")
  return int(a) * int(b)

def is_mul(expr:str):
  return expr.startswith("mul(") and expr.endswith(")")

def day3p2():
  matches = re.findall('mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)', input)
  exprs_to_sum = []
  enabled = True
  for m in matches:
    match m:
      case "don't()": enabled = False
      case "do()": enabled = True
      case _:
        if is_mul(m) and enabled:
          exprs_to_sum.append(m)
        elif not is_mul(m):
          raise ValueError(f"Didn't expect {m}")
  
  evaluated = (mul(expr) for expr in exprs_to_sum)
  answer = sum(evaluated)
  print(f"Part 2: {answer}")
  assert answer == "63013756" # First try


if __name__ == "__main__":
  day3p1()
  day3p2()