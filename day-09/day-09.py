from typing import NamedTuple
from pathlib import Path

FREE = -1
class Block():
  def __init__(self, id: int, size: int, next=None, prev=None):
    self.id = id
    self.size = size
    self.next = next
    self.prev = prev
    self.orig_idx = None
    self.has_moved = False

  def is_free(self):
    return self.id == FREE
  
  def __repr__(self):
    postfix = self.orig_idx if self.orig_idx is not None and self.id is FREE else ""
    return f"{self}{postfix}"
  
  def __str__(self):
    return (str(self.id) if self.id != FREE else '.') * self.size

  
  def __hash__(self) -> int:
    return (self.id, self.size).__hash__()
  
  def combine_free(self) -> tuple[list["Block"], int]:
    """
    Find connected free neighbors and combine with them.
    Return a list of removed neighbors. This object will be the one that remains.
    """
    if not self.is_free():
       return [], self.size
    
    old_size = self.size
    removed = []
    while self.next is not None and self.next.id == FREE:
      next = self.next
      removed.append(next)
      self.next = next.next
      self.size += next.size
      next.prev = None
      next.next = None
    while self.prev is not None and self.prev.id == FREE:
      prev = self.prev
      removed.append(prev)
      self.prev = prev.prev
      self.size += prev.size
      self.orig_idx = prev.orig_idx # Maintain the earliest original index as we accumulate free blocks.
      prev.prev = None
      prev.next = None

    if self.prev is not None:
      self.prev.next = self

    if self.next is not None:
      self.next.prev = self

    return removed, old_size
  
  def place_copy(self, block):
    if not self.is_free() or block.is_free():
      raise ValueError("Only place non-free blocks on free blocks")
    
    if block.has_moved:
      raise ValueError("Moving a block that was already moved")
    
    inserted = None
    if block.size > self.size:
      raise ValueError("Can't place a block bigger than this one")
    elif block.size == self.size:
      self.id = block.id
      self.has_moved = True
    else:
      self.size = self.size - block.size
      inserted = Block(block.id, block.size, next=self, prev=self.prev)
      # Set the original index for an inserted block to the current free space
      # so that we don't try to move it again.
      inserted.orig_idx = self.orig_idx
      inserted.has_moved = True
      self.prev.next = inserted
      self.prev = inserted

    return inserted


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

##
## Part 2
##

# Doubly linked list checking
def make_test_list():
  b1 = Block(0, 2)
  b2 = Block(FREE, 3, prev=b1)
  b3 = Block(FREE, 4, prev=b2)
  b4 = Block(FREE, 5, prev=b3)
  b5 = Block(1, 7, prev=b4)
  b1.next = b2
  b2.next = b3
  b3.next = b4
  b4.next = b5
  return [b1, b2, b3, b4, b5]

def combine(l: list[Block], b: Block):
  removed, old_size = b.combine_free()
  for r in removed:
    l.remove(r)
  return l

def test_combine(i):
  test_list = make_test_list()
  b = test_list[i]
  return combine(test_list, b)

original = make_test_list()
eq = lambda l, r: all(a.id == b.id and a.size == b.size for a, b in zip(l, r))
assert eq(test_combine(0), original)
assert eq(test_combine(1), [original[0], Block(FREE, 12), original[-1]])
assert eq(test_combine(2), [original[0], Block(FREE, 12), original[-1]])
assert eq(test_combine(3), [original[0], Block(FREE, 12), original[-1]])
assert eq(test_combine(4), original)

def link_blocklist(blocklist: list[Block]):
  for i in range(1, len(blocklist) - 1):
    prev, curr, next = blocklist[i-1], blocklist[i], blocklist[i+1]
    prev.next, curr.next = curr, next
    curr.prev, next.prev = prev, curr
  for i, b in enumerate(blocklist):
    b.orig_idx = i

sample = load("sample.txt")
tiny = load_from_text("12345")
link_blocklist(sample)
link_blocklist(tiny)

from collections import defaultdict
from bisect import insort
class FreeBlocks():
  def __init__(self, blocklist: list[Block]):
    self.freemap = defaultdict(list)
    self._initialize(blocklist)

  def _initialize(self, blocklist: list[Block]):
    for b in blocklist:
      if b.is_free():
        self.freemap[b.size].append(b)

  def place(self, free: Block, b: Block):
    self.freemap[free.size].remove(free)
    inserted = free.place_copy(b)
    if free.is_free():
      assert free.orig_idx is not None, "Grafted this on; hope I did it right"
      insort(self.freemap[free.size], free, key=lambda b: b.orig_idx)
    return inserted
  
  def free(self, to_free: Block):
    assert to_free.id != FREE, "Don't double-free."
    to_free.id = FREE
    free = to_free
    removed, old_size = free.combine_free()
    # self.freemap[old_size].remove(free) # We *just* freed this block, so it won't be there.
    for r in removed:
      self.freemap[r.size].remove(r)
    assert free.orig_idx is not None, "Grafted this on; hope I did it right"
    insort(self.freemap[free.size], free, key=lambda b: b.orig_idx)
    return removed, old_size
  
  def find_free_block(self, for_block: Block) -> Block | None:
    search_keys = sorted(k for k in self.freemap.keys() if k >= for_block.size)
    for k in search_keys:
      free_list = self.freemap[k]
      if len(free_list) > 0:
        first_open_spot = free_list[0]
        if first_open_spot.orig_idx is None:
          pass
        assert first_open_spot.orig_idx is not None, f"orig_idx wrong for {first_open_spot}"
        assert for_block.orig_idx is not None, f"orig_idx wrong for {for_block}"
        if first_open_spot.orig_idx > for_block.orig_idx:
          # The earliest available block is too early.
          continue

        assert first_open_spot.size == k, "We better have done the accounting right"
        return first_open_spot
      
    return None

def compact_no_frag(blocks: list[Block]):
  mem_mgr = FreeBlocks(blocks)
  start = blocks[0]

  curr = blocks[-1]
  while curr != None:
    if curr.is_free() or curr.has_moved:
      curr = curr.prev
      continue

    open_spot = mem_mgr.find_free_block(curr)
    if open_spot is None:
      curr = curr.prev
      continue

    # The current block has an ID and we can move it.
    # First place it in the new location, then combine this now-free region.
    mem_mgr.place(open_spot, curr)
    mem_mgr.free(curr)
    curr = curr.prev
  
  result = []
  curr = start
  while curr != None:
    result.append(curr)
    curr = curr.next

  return result

r = compact_no_frag(sample)
r_s = ''.join(str(b) for b in r)
assert r_s == "00992111777.44.333....5555.6666.....8888.."
assert checksum(r) == 2858

print("Part 2 tests pass!")

def d9p2():
  puzzle = load('puzzle.txt')
  link_blocklist(puzzle)
  r = compact_no_frag(puzzle)
  answer = checksum(r)
  print(f"Part 2 checksum is: {answer}")
  assert answer > 6380078139435 # First attempt, too low.

d9p2()
