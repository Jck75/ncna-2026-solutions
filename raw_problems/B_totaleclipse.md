Point light source (the star)
is in the upper-left corner. Shadow boundaries are drawn
for the planets that are casting shadows. 

A minuscule neutron star, for our purposes treatable as a
point light source, shines over a planetary system. Assuming
the entire system exists in a plane, your challenge is to
determine how many planets are totally in eclipse from the star
by intervening planet(s) at the moment in time of the
description. In other words, no light from the star is directly
reaching such a planet so that the whole planet is dark. But
for ease of computation, we’ll assume that we are only
considering the plane so that it is only where the plane slices
the planet across its middle that must be fully dark. You are
provided with relevant details of each planet: its distance
from the star, the arc length (angular diameter) as viewed from
the star, and its angle to the star measured clockwise from a
horizontal line extending to the right as can be viewed in the
sample figure.

Hint: A radian is a measure of an angle. There are
$2\pi $ radians in a
circle, making a radian approximately 57.2958 degrees. For
comparison, the angular diameters of the sun and of our moon as
seen from the earth are each approximately half a degree or
equivalently 0.0093 radians. It would therefore take about 720
adjacent suns/moons to form a complete circle around the
earth.

## Input

The first line will contain the number of planets in the
system. Each subsequent line will contain three values
describing the planet: its distance from the star in AU
(Astronomical Units), arc length of the angle formed by its
diameter relative to the star (radians), and the clockwise
angle from the horizontal from the star to the planet’s center
(radians). (An AU is the distance from the earth to the sun.)
The planets in Sample Input 1 are labeled alphabetically in
order of the input data.

The number of planets can range from 0 through 2000. The
distance to a planet (it’s center) and between any two planets
will be sufficient to ensure they would never touch throughout
their circular orbits, and no more than 1,000,000 AU. The arc
length of a planet’s diameter can range from 0.0 through 1.0
radians. The angle of the planet to the star can range from 0
through $2\pi $ (or
effectively $6.283185$)
radians. All values are given with at most $6$ digits after the decimal
point.

## Output

Print the number of instances of a planet being totally
eclipsed from the star by another planet(s). In the sample, the
farther planets C and D are being totally eclipsed from the
star by the closer planets A and B. (A by itself would totally
eclipse D, but it takes the combination of A and B to totally
eclipse C.) However, planet E only partially eclipses planet F
from the star.

### Sample Input 1
```
6
5.5 0.12 0.18
10.0 0.09 0.10
13.0 0.09 0.11
14.0 0.05 0.20
2.7 0.10 0.85
9.0 0.10 0.78
```
### Sample Output 1
```
2
```