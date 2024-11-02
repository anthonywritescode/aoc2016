from __future__ import annotations

import argparse
import os.path
import re
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


reg = re.compile(r'(\(\d+x\d+\))')


class S(NamedTuple):
    n: int
    size: int


class Repeat(NamedTuple):
    take: int
    n: int
    size: int

    def mult(self, n: int) -> Repeat:
        return self._replace(n=self.n * n)

    @classmethod
    def parse(cls, s: str) -> Repeat:
        take_s, n_s = s[1:-1].split('x')
        return cls(int(take_s), int(n_s), len(s))


def _end_idx(i: int, repeat: Repeat, parts: list[S | Repeat]) -> int:
    j = i + 1

    remaining = repeat.take
    for j, part in enumerate(parts[i + 1:], j):
        if isinstance(part, S):
            if part.size > remaining:  # need to split!
                parts.insert(j + 1, part._replace(size=part.size - remaining))
                parts[j] = part._replace(size=remaining)
                remaining = 0
            else:
                remaining -= part.size
        elif isinstance(part, Repeat):
            assert remaining >= part.size
            remaining -= part.size
        else:
            raise AssertionError('unreachable!')

        if remaining == 0:
            return j + 1
    else:
        raise AssertionError('unreachable!')


def compute(s: str) -> int:
    s = s.strip()

    parts = [
        Repeat.parse(part) if i % 2 == 1 else S(n=1, size=len(part))
        for i, part in enumerate(reg.split(s))
    ]

    total = 0

    i = 0
    for i, part in enumerate(parts):
        if isinstance(part, S):
            total += part.size * part.n
        elif isinstance(part, Repeat):
            for j in range(i + 1, _end_idx(i, part, parts)):
                if isinstance(parts[j], S):
                    parts[j] = parts[j]._replace(n=parts[j].n * part.n)
        else:
            raise AssertionError('unreachable')

    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('ADVENT', 6),
        ('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445),
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
