from __future__ import annotations

import argparse
import hashlib
import heapq
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRS = (
    support.Direction4.UP,
    support.Direction4.DOWN,
    support.Direction4.LEFT,
    support.Direction4.RIGHT,
)


def compute(s: str) -> int:
    s = s.strip()

    longest = -1
    todo = [(0, (0, 0), '')]
    while todo:
        n, (x, y), path = heapq.heappop(todo)

        if (x, y) == (3, 3):
            longest = max(longest, len(path))
            continue

        hd = hashlib.md5(f'{s}{path}'.encode()).hexdigest()
        for c, d in zip(hd[:4], DIRS):
            if int(c, 16) > 10:
                cx, cy = d.apply(x, y)
                if 0 <= cx <= 3 and 0 <= cy <= 3:
                    heapq.heappush(
                        todo,
                        (n + 1, (cx, cy), f'{path}{d.name[0]}'),
                    )

    return longest


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('ihgpwlah', 370),
        ('kglvqrro', 492),
        ('ulqzkmiv', 830),
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
