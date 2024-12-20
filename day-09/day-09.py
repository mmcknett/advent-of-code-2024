from typing import NamedTuple
from pathlib import Path

FREE = -1
class Block():
  def __init__(self, id: int, size: int, next=None, prev=None):
    self.id = id
    self.size = size
    self.next = next
    self.prev = prev

  def is_free(self):
    return self.id == FREE
  
  def __repr__(self):
    return str(self)
  
  def __str__(self):
    return (str(self.id) if self.id != FREE else '.') * self.size

class IdGen():
  def __init__(self):
    self.next_id = 0

  def next(self):
    nid = self.next_id
    self.next_id += 1
    return nid

def load(filename):
  path = Path('./day-09') / filename
  inp = path.read_text()
  return load_from_text(inp)

def load_from_text(inp):
  descriptors = [int(s) for s in inp]
  ids = IdGen()
  blocks = [Block(ids.next(), n) if i % 2 == 0 else Block(FREE, n) for i, n in enumerate(descriptors)]
  return [b for b in blocks if b.size > 0]

sample = load("sample.txt")
tiny = load_from_text("12345")

def compact_blocks(blocks: list[Block]):
  compacted = []
  last_seen_id = FREE
  for b in blocks:
    if b.is_free():
      available = b.size
      from_end = get_n_from_end(blocks, available, last_seen_id)
      compacted.extend(from_end)
    else:
      compacted.append(b)
      last_seen_id = b.id

  return compacted

def get_n_from_end(blocks: list[Block], n: int, id_floor: int):
  result = []
  while b := blocks[-1]:
    if b.id == FREE:
      blocks.pop()
      continue

    if b.id <= id_floor or n <= 0:
      break

    if b.size <= n:
      result.append(b)
      blocks.pop()
      n -= b.size
    else:
      b.size = b.size - n
      result.append(Block(b.id, n))
      n = 0
  return result

r = compact_blocks(tiny)
r_s = ''.join(str(b) for b in r)
assert r_s == "022111222"

r = compact_blocks(sample)
r_s = ''.join(str(b) for b in r)
assert r_s == "0099811188827773336446555566"

def checksum(blocks):
  start_pos = 0
  sum_checked = 0
  for b in blocks:
    if b.is_free():
      start_pos += b.size
      continue
    blocksum = sum(b.id * i for i in range(start_pos, start_pos + b.size))
    sum_checked += blocksum
    start_pos += b.size

  return sum_checked

assert checksum(r) == 1928
print('Part 1 tests pass!')

def d9p1():
  puzzle = load("puzzle.txt")
  r = compact_blocks(puzzle)
  check = checksum(r)
  print(f"Part 1 checksum is: {check}")

d9p1()
