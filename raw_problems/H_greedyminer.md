Illustration with top down
view of Sample 1. We can’t afford to put in support
posts, so need to avoid any 2 x 2 mined squares, but
still need connected access throughout. 

A seam of valuable ore has been discovered. Miners are ready
to go after it. However, they have a choice of either bracing
the ceiling with posts every so often or leaving some of the
ore behind as supports. They decided on the latter option. It
so happens that the width of the seam would have required 3
intermediate posts. The length of the seam depends on the case.
The challenge boils down to dividing up the seam into squares,
4 squares wide and as many squares as needed for the full
length, such that the ceiling at each corner of the squares is
supported in some fashion. So rather than installing posts, at
least one square at each corner should be left unmined, or
equivalently, there should be no instances of a 2 x 2 square
area of ore all being dug out.

The ore has been assayed and numbers assigned representing
the value of the ore in each square. The general idea is to
maximize the value of ore retrieved by leaving squares with
poorer ore as supports wherever needed.

You are given the length of a seam of ore (the width is 4
squares) and the assayed values of each square. Your task is to
compute the maximum value of ore that can be safely removed,
followed by the value of the remaining ore that has to be left
as supports. Access to the mine would be made from the side (by
a tunnel) or top (by a shaft) of just one square (naturally at
a square that would be mined in an optimal solution.)
Therefore, the whole area to be mined must be connected
rectilinearly, as demonstrated in the figure.

## Input

The first line contains the length of the seam $d$ , $(1<=d<=10{,}000)$ , measured in
number of squares. Each following line presents the (integer)
values $v$, $(1<=v<=1{,}000{,}000)$ of a row
of 4 squares.

## Output

Format as demonstrated. Present the maximum total value of
ore that can be safely recovered and the amount that must
remain.

### Sample Input 1
```
11
5 10 6 5
12 8 3 4
8 7 11 8
9 10 8 3
2 12 5 13
4 9 7 5
6 4 2 4
5 1 5 7
6 7 8 4
8 7 3 4
5 6 2 5
```
### Sample Output 1
```
Retrievable: 228
Remaining: 45
```