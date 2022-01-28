from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

CS = (
    (None, None, '1'),
    (None, '2', '3', '4'),
    ('5', '6', '7', '8', '9'),
    (None, 'A', 'B', 'C'),
    (None, None, 'D'),
)

POS = {
    (x, y): val
    for y, row in enumerate(CS)
    for x, val in enumerate(row)
    if val is not None
}
CHAR_TO_DIR = {
    'U': support.Direction4.UP,
    'D': support.Direction4.DOWN,
    'L': support.Direction4.LEFT,
    'R': support.Direction4.RIGHT,
}


def compute(s: str) -> str:
    pos = (0, 2)
    ret = ''
    for line in s.splitlines():
        for c in line:
            new_pos = CHAR_TO_DIR[c].apply(*pos)
            if new_pos in POS:
                pos = new_pos

        ret += POS[pos]

    return ret


INPUT_S = '''\
ULL
RRDDD
LURDL
UUUUD
'''
EXPECTED = '5DB3'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: str) -> None:
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
