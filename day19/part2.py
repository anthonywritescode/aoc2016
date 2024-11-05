from __future__ import annotations

import argparse
import math
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _compute_but_too_slow(s: str) -> int:
    i = 0
    d = list(range(1, int(s) + 1))
    while len(d) != 1:
        victim = (i + len(d) // 2) % len(d)
        del d[victim]
        if victim > i:
            i += 1
        i %= len(d)

    return d[0]


def compute(s: str) -> int:
    target = int(s)
    power = int(math.log(target, 3))

    lower = 3 ** power
    next_power = 3 ** (power + 1)

    half = (next_power + lower) // 2

    if target == lower:
        return target
    elif target < half:
        return target - lower
    else:
        return target - lower + target - half


INPUT_S = '''\
5
'''
EXPECTED = 2


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
