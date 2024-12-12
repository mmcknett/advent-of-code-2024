# Advent of code 2024

## Day 01

## Day 02

## Day 03

## Day 04

## Day 05

## Day 06
### Part 2
Proposal:

At each position in the run, see what would happen if an obstruction was placed in front of the guard vs not. The guard is in a loop if they step on the same location in the same orientation. They're *not* in a loop if they exit the board eventually.

This will be quadratic in the number of steps taken, so not great, but probably fast enough?

## Day 08

## Day 11
Skipped days 9 and 10 to do the current day today.

It's probably useful to know the factors of 2024, which are (11, 23, 2, 2, 2). It might also be worth knowing that the final digit of 2024^i is 6 for even `i` and 4 for odd `i`. This also might be useful:

```python
[len(str(2024**i)) for i in range(25)]
[1, 4, 7, 10, 14, 17, 20, 24, 27, 30, 34, 37, 40, 43, 47, 50, 53, 57, 60, 63, 67, 70, 73, 77, 80]
```

Turned out, recursion with memoization was the simplest way.
