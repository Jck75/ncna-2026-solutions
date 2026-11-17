$1.10 in loose change, as
specified in the sample 

Here’s some loose change totaling $1.10. Let’s imagine that
we replace some of these coins, centering the replacements at
the exact same coordinates and such that the resulting
collection is worth more, yet having none of the coins overlap.
For example, it is trivial to replace all the pennies and
nickels with dimes because dimes are worth more but are
physically smaller. Doing so increases the total to $1.65. Now
there is space for the former pennies at the left and at the
top to be replaced by quarters. Now we are up to $1.95. There
may be additional improvements.

You will be presented with an initial arrangement of coins
as in the example. None of the coins will be overlapping, but
could be touching. Your task is to determine the maximum value
of any set of non-overlapping but possibly touching coins
centered at those positions. There must still be a coin at each
of the original locations. There are plenty of coins of each
kind for you to use as replacements. The number of coins will
not be more than 12. All diameters and coordinates will be
measured in mils (thousandths of an inch). Coordinates will
fall within $(-1*10^9,
1*10^9)$.

Coin

Value

Diameter

Penny

1

750

Nickel

5

835

Dime

10

705

Quarter

25

955

Half

50

1205

## Input

The first line will contain an integer representing the
number of coins in the set. Each subsequent line will contain
three space-delimited integers representing the value of the
initial coin (in cents) followed the X and Y coordinates (in
mils) for the center of the coin.

## Output

Print the maximum value of the coins after possible
replacements. Use dollars and cents format (eg. $1.10).

### Sample Input 1
```
12
5 2008 3896
1 2880 3924
10 2240 3160
10 2972 3052
25 1372 2924
1 3680 2612
1 2056 2412
25 2844 2068
1 1000 1876
1 3616 1492
5 1912 1396
25 2796 1000
```
### Sample Output 1
```
$2.50
```