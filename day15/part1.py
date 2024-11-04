from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Disk(NamedTuple):
    period: int
    offset: int

    @classmethod
    def parse(cls, s: str) -> Disk:
        _, _, _, period_s, *_, pos_s = s.split()
        return cls(int(period_s), int(pos_s))


def compute(s: str) -> int:
    t = 0
    mult = 1
    for i, line in enumerate(s.replace('.', '').splitlines()):
        disk = Disk.parse(line)
        while (t + i + 1 + disk.offset) % disk.period != 0:
            t += mult
        mult *= disk.period

    return t


INPUT_S = '''\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
'''
EXPECTED = 5


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
