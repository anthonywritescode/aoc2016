from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    d = support.Direction4.UP
    pos = (0, 0)

    for part in s.strip().split(', '):
        if part[0] == 'L':
            d = d.ccw
        else:
            d = d.cw
        pos = d.apply(*pos, n=int(part[1:]))

    return sum(abs(c) for c in pos)


INPUT_S = '''\
R5, L5, R5, R3
'''
EXPECTED = 12


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
