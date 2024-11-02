from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


reg = re.compile(r'\((\d+)x(\d+)\)')


def compute(s: str) -> int:
    s = s.strip()

    length = 0
    i = 0
    while True:
        match = reg.search(s, pos=i)
        if match:
            length += match.start() - i
            length += int(match[1]) * int(match[2])
            i = match.end() + int(match[1])
        else:
            length += len(s) - i
            break

    return length


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('ADVENT', 6),
        ('X(8x2)(3x3)ABCY', 18),
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
