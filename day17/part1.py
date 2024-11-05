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


def compute(s: str) -> str:
    s = s.strip()

    todo = [(0, (0, 0), '')]
    while todo:
        n, (x, y), path = heapq.heappop(todo)

        if (x, y) == (3, 3):
            return path

        hd = hashlib.md5(f'{s}{path}'.encode()).hexdigest()
        for c, d in zip(hd[:4], DIRS):
            if int(c, 16) > 10:
                cx, cy = d.apply(x, y)
                if 0 <= cx <= 3 and 0 <= cy <= 3:
                    heapq.heappush(
                        todo,
                        (n + 1, (cx, cy), f'{path}{d.name[0]}'),
                    )

    raise AssertionError('unreachable!')


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (

        ('ihgpwlah', 'DDRRRD'),
        ('kglvqrro', 'DDUDRLRRUDRD'),
        ('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'),
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
