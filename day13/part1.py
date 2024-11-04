from __future__ import annotations

import argparse
import functools
import heapq
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, *, target: tuple[int, int] = (31, 39)) -> int:
    favorite = int(s)

    @functools.lru_cache(maxsize=2048)
    def _is_open(x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return False

        n = x * x + 3 * x + 2 * x * y + y + y * y + favorite
        return n.bit_count() % 2 == 0

    todo = [(0, 1, 1)]
    seen = {(1, 1)}
    while todo:
        n, x, y = heapq.heappop(todo)

        if (x, y) == target:
            return n

        for cx, cy in support.adjacent_4(x, y):
            if (cx, cy) not in seen and _is_open(cx, cy):
                heapq.heappush(todo, (n + 1, cx, cy))
                seen.add((cx, cy))

    raise AssertionError('unreachable!')


INPUT_S = '''\
10
'''
EXPECTED = 11


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, target=(7, 4)) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
