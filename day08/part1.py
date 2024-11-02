from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    bits = [[False] * 50 for _ in range(6)]

    for line in s.replace('x=', '').replace('y=', '').splitlines():
        match line.split():
            case 'rect', dims:
                w_s, h_s = dims.split('x')
                w, h = int(w_s), int(h_s)
                for x in range(w):
                    for y in range(h):
                        bits[y][x] = True
            case 'rotate', 'row', y_s, _, by_s:
                y, by = int(y_s), int(by_s)

                row = bits[y]
                newrow = row[-by:] + row[:-by]

                for x, val in enumerate(newrow):
                    bits[y][x] = val

            case 'rotate', 'column', x_s, _, by_s:
                x, by = int(x_s), int(by_s)

                col = [row[x] for row in bits]
                newcol = col[-by:] + col[:-by]

                for y, val in enumerate(newcol):
                    bits[y][x] = val

            case unreachable:
                raise AssertionError(unreachable)

    return sum(sum(row) for row in bits)


INPUT_S = '''\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
'''
EXPECTED = 6


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
