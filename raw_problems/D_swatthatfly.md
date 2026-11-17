Good luck swatting
it! 

A fly has landed on the screen. You have the urge to swat
it, but since you don’t have a fly swatter handy, you decide to
try for it with your hands. Fortunately, there is a trick to
taking down flies. A fly’s eyes detect motion. Start slowly
with your hands at some distance on opposite sides of the fly,
then bring your hands together slowly so that the fly does not
notice them, and at the critical moment, just at the edge of
the strike zone (determined by the speed of your hands), clap
quickly. With any luck at all, the fly will respond to the
sudden hand motion by flying straight up off the screen
directly into the path of your hands!

As for the fly in question, its size is 4 grid lengths long
and 2 wide. It will be facing straight ahead. Your hands are
assumed to be 12 grid lengths long and 2 thick, also aligned
straight ahead, but could be initially positioned anywhere
outside the strike zone, even on the same side of the fly. You
can swat the fly anywhere along the length of your hands, which
could be offset, but must span the full length of the fly on
both sides. You may assume that the fly and hands stay aligned
with the screen grid as in the sample.

You will be provided with the initial coordinates of the
middle of your hands, as measured relative to the fly. You will
also be provided with the optimal striking distance
(illustrated as a square in the figure) as measured from the
center of the fly. You must keep your hands totally outside
that square until you are ready to strike. Otherwise, the fly
will detect them and fly away. Your left and right hands are
interchangeable, so you do not have to consider which side is
the palm and which is the back. But your hands cannot pass
through each other.

Assuming your preparatory hand movements are measured by the
Manhattan distance (sum of rectilinear distances), and the
final clap is from right angles to the sides of the fly, what
is the minimum total distance you must move your hands into
position for the final clap? In the sample, the hand on the
left optimally moves right and up a total of 8 grid lengths
while the hand on the right moves left and down 4 grid lengths
for a total of 12.

Fly at the origin, initial
hand positions in dark gray, hands ready to swat in light
gray, strike zone is outlined. 

## Input

You will be given 5 integers on a single line: the two sets
of $(x,y)$ coordinates of
each hand, relative to the center of the fly, and the minimum
strike distance. All integers will be between $-2^{16}$ and $2^{16}$ inclusive. The positions of
the fly and its strike zone will not be towards the edge of the
screen such that the hands would need to go past the edge for a
minimal distance movement prior to the final clap.

## Output

Print a single integer representing the minimum total
distance you must move your hands into position for the final
clap.

### Sample Input 1
```
-13 -8 11 6 8
```
### Sample Output 1
```
12
```