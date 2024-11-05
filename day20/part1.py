from __future__ import annotations

import argparse
import bisect
import os.path
import sys

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _split(ranges: list[tuple[int, int]], n: int) -> None:
    left = bisect.bisect_right(ranges, (n, sys.maxsize)) - 1
    if ranges[left][0] < n < ranges[left][1]:
        ranges.insert(left + 1, (n, ranges[left][1]))
        ranges[left] = (ranges[left][0], n)


def compute(s: str, *, maxval: int = 4294967295) -> int:
    ranges = [(0, maxval + 1)]

    for line in s.splitlines():
        n0_s, n1_s = line.split('-')
        n0, n1 = int(n0_s), int(n1_s)
        n1 += 1

        _split(ranges, n0)
        _split(ranges, n1)

        left = bisect.bisect_right(ranges, (n0, sys.maxsize)) - 1
        if ranges[left][0] != n0:
            left += 1

        right = bisect.bisect_right(ranges, (n1, sys.maxsize)) - 1
        if ranges[right][-1] <= n1:
            right += 1

        del ranges[left:right]

    return ranges[0][0]


INPUT_S = '''\
5-8
0-2
4-7
'''
EXPECTED = 3


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, maxval=9) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
