from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    d = support.Direction4.UP
    pos = (0, 0)
    seen = {pos}

    for part in s.strip().split(', '):
        if part[0] == 'L':
            d = d.ccw
        else:
            d = d.cw
        for _ in range(int(part[1:])):
            pos = d.apply(*pos)
            if pos in seen:
                break
            else:
                seen.add(pos)
        else:
            continue
        break

    return sum(abs(c) for c in pos)


INPUT_S = '''\
R8, R4, R4, R8
'''
EXPECTED = 4


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
