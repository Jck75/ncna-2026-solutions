Typical recursive solution
process for Towers of Hanoi 

Your roommate, Hannah, has a Towers of Hanoi puzzle
containing the usual three pegs and multiple disks with unique
diameters. The disks are initially stacked on exactly one peg
in decreasing order of size (smallest on top). For the game, a
player must transfer the disks one at a time to one of the
other pegs such that no larger disk is ever placed on a smaller
disk. The challenge is to do this in the minimum number of
steps.

One day Hannah finds that her younger brother, Rubik, has
played with the game and left the disks scrambled in a likely
illegal configuration on the three pegs. (Years later Rubik
similarly scrambled the colors on a cube that he was playing
with. Fortunately he figured out how to unscramble it.) You and
Hannah think it may be possible to bring the puzzle to a solved
state by playing the game from this scrambled configuration.
The usual rules should be followed, with these clarifications:
We may not know what the starting peg was, so we shall allow
any of the pegs to be the destination. You may move the top
disk from any peg to the top of any other peg if that other
peg’s current top disk is larger. You are done when all disks
are in correct order on the destination peg. If Rubik managed
(he is a smart kid!) to solve the game, you are already done
since any peg can be the destination!

As you are working on this, you contemplate what
configurations are solvable, and in how few steps. In trying to
resolve these questions, you come to realize that it will take
significant time to determine the number of moves, assuming the
configuration is solvable. Your task is to write a program to
compute the minimum number of steps to solve any configuration,
or declare it unsolvable.

## Input

The input will contain $3$ lines, each line describing one of
the pegs in the puzzle. A peg description begins with an
integer specifying the number of disks on the peg followed by
space-delimited integers, each representing the diameter of a
disk, starting at the bottom. If there are no disks on a peg,
the line will contain only the number 0.

The diameters of the disks will conveniently be unique
positive integer values no larger than 100. There will be at
most 8 disks total.

## Output

Print an integer representing the minimum number of steps
needed to solve the configuration, if it is indeed solvable. If
it is not solvable, print the number -1.

### Sample Input 1
```
1 3
2 1 2
0
```
### Sample Output 1
```
2
```

### Sample Input 1
```
2 1 4
0
2 3 2
```
### Sample Output 1
```
8
```