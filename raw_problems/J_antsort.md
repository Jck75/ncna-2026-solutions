Illustration of Sample 1.
Positions at time 24 - Both ants 2 and 3 will follow the
newer path of ant 1 while ants 4 and 5 are already inside
the loop. 

In the Northern Centralized Numbered Anthill (NCNA) each ant
is assigned a unique ID number. When the ants head out for a
day of marching, the leader heads out first. She sets the route
for the march by leaving a pheromone trail where she walks. The
remainder of the ants emerge one at a time to follow this trail
at specified times (integral numbers of seconds), but they may
eventually merge to go by twos or more (as will be explained
shortly). They all march at the same speed. If there is a
choice as to which path to follow (as can happen if the leader
crosses her own path), an ant will follow the path with the
stronger, more recent pheromone signal. (The later ants do not
lay down pheromones of their own - they just follow the
leader.) And if ants converge simultaneously on such an
intersection, they will merge into numerical order left to
right as a single row and march abreast the rest of the way.
Any such intersections must be created at integral numbers of
seconds into the march by the leader and must be located at
integral grid coordinates. Otherwise, the path is not bound by
grid lines. In order to make this problem more tractable, you
can assume the leader doesn’t cross her path again until every
ant has passed the previous crossing.

Your task is to determine the fewest number of
self-crossings by the leader that will result in the ants being
in total numeric order (including those already marching
abreast) when they reach the end of the march. You are not
given any one path to consider, nor specific end points, nor
the total length of the path. You do not have to report what
that path might be.

Consider the first sample and the figure above illustrating
it. It shows the number 1 ant (the leader) at time unit 24
about to cross its path to the right, after which ants number 2
and 3 (remember that they come out of the hill in scrambled
numerical order, other than the leader) will sense the new
trail and not follow the loop. Ants 4 and 5 came out of the
hill sooner and are already in the loop at this time. Thus with
just one crossing the ants end up in order 1, 2, 3, 4, and 5
after having emerged from the hill in order 1, 4, 5, 2, 3.

## Input

The first line will contain a positive integer indicating
the number of ants, not to exceed 31. The following lines will
contain integer pairs presenting the sequence that ants leave
the ant hill. The first number is the ID number of the ant,
between 0 and 10,000 inclusive. The second number represents
the time of emergence in seconds after the leader leaves the
ant hill, between 0 and 30 inclusive. The leader will appear as
the first pair at time 0 and the minimum ID number (but which
might not be 0).

## Output

Display the fewest number of self-crossings by the leader
that can result in the ants being in total numeric order
(including those already merged in order into any rows) when
they reach the end of the march, following the path constraints
given above. If it is impossible to get all the ants sorted,
display the number -1.

### Sample Input 1
```
5
1 0
4 8
5 9
2 21
3 23
```
### Sample Output 1
```
1
```

### Sample Input 1
```
3
5 0
15 1
10 2
```
### Sample Output 1
```
1
```