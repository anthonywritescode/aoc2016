from __future__ import annotations

import argparse
import itertools
import os.path
from collections.abc import Generator
from collections.abc import Iterable
from typing import TypeVar

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

T = TypeVar('T')


def chunk_iter(
        iterable: Iterable[T],
        n: int,
) -> Generator[tuple[T, ...]]:
    """Yields an iterator in chunks

    For example you can do

    for a, b in chunk_iter([1, 2, 3, 4, 5, 6], 2):
        print('{} {}'.format(a, b))

    # Prints
    # 1 2
    # 3 4
    # 5 6

    Args:
        iterable - Some iterable
        n - Chunk size (must be greater than 0)
    """
    assert n > 0
    iterable = iter(iterable)

    chunk = tuple(itertools.islice(iterable, n))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(iterable, n))


def compute(s: str) -> int:
    ret = 0

    parsed = [
        [int(part) for part in line.split()]
        for line in s.splitlines()
    ]

    for col in zip(*parsed):
        for sides in chunk_iter(col, 3):
            sides = tuple(sorted(sides))
            ret += sum(sides[:2]) > sides[-1]

    return ret


INPUT_S = '''\
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
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
