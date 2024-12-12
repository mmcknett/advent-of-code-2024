from collections import Counter

sample = "0 1 10 99 999"
sample_after_blink = "1 2024 1 0 9 9 2021976"

puzzle = "7725 185 2 132869 0 1840437 62 26310"

def to_ints(s):
  return [int(n) for n in s.split(' ')]

def apply_rule(n):
  if n == 0:
    return [1]

  s = str(n)
  digs = len(str(n))
  if digs % 2 == 0:
    return [int(s[:digs//2]), int(s[digs//2:])]
  
  return [2024 * n]

def apply_all(l_n):
  res = []
  for n in l_n:
    res += apply_rule(n)
  return res

assert apply_all(to_ints(sample)) == to_ints(sample_after_blink)

def blink(l_n, blinks):
  res = l_n
  for _ in range(blinks):
    res = apply_all(res)
  return res

assert len(blink(to_ints("125 17"), 6)) == 22
assert len(blink(to_ints("125 17"), 25))== 55312

memo = {}

def blink_recursive(n, remaining_blinks):
  if remaining_blinks == 0:
    return 1
  
  if (n, remaining_blinks) in memo:
    return memo[(n, remaining_blinks)]

  l_n = apply_rule(n)
  result = sum(blink_recursive(x, remaining_blinks - 1) for x in l_n)
  memo[(n, remaining_blinks)] = result
  return result

def blink_all_rec(l_n, remaining_blinks):
  return sum(blink_recursive(x, remaining_blinks) for x in l_n)

assert blink_all_rec(to_ints("125 17"), 6) == 22
assert blink_all_rec(to_ints("125 17"), 25)== 55312

def d11p1():
  # answer = len(blink(to_ints(puzzle), 25))
  answer = blink_all_rec(to_ints(puzzle), 25)
  print(f"After 25 blinks, it's {answer}")
  assert answer == 233050

def d11p2():
  N = 75
  answer = blink_all_rec(to_ints(puzzle), N)
  print(f"After {N} blinks, it's {answer}")

if __name__ == "__main__":
  d11p1()
  d11p2()
