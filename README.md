advent of code 2016
===================

https://adventofcode.com/2016

### stream / youtube

- [Streamed daily on twitch](https://twitch.tv/anthonywritescode)
- [Streams uploaded to youtube afterwards](https://www.youtube.com/channel/UChPxcypesw8L-iqltstSI4Q)

### about

for 2016, I'm planning to implement in python

### timing

- comparing to these numbers isn't necessarily useful
- normalize your timing to day 1 part 1 and compare
- alternate implementations are listed in parens
- these timings are very non-scientific (sample size 1)

```console
$ find -maxdepth 1 -type d -name 'day*' -not -name day00 | sort | xargs --replace bash -xc 'python {}/part1.py {}/input.txt; python {}/part2.py {}/input.txt'
+ python day01/part1.py day01/input.txt
246
> 434 μs
+ python day01/part2.py day01/input.txt
124
> 660 μs
+ python day02/part1.py day02/input.txt
76792
> 1852 μs
+ python day02/part2.py day02/input.txt
A7AC3
> 1795 μs
+ python day03/part1.py day03/input.txt
862
> 3581 μs
+ python day03/part2.py day03/input.txt
1577
> 5994 μs
```
