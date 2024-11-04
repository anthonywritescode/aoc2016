from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    salt = s.strip()

    @functools.lru_cache(maxsize=1024)
    def _compute(n: int) -> tuple[str | None, frozenset[str]]:
        hd = hashlib.md5(f'{salt}{n}'.encode()).hexdigest()
        three = None
        five = set()
        current = ''
        current_n = 0
        for c in hd + 'z':
            if c == current:
                current_n += 1
            else:
                if current_n >= 3 and three is None:
                    three = current
                if current_n >= 5:
                    five.add(current)
                current = c
                current_n = 1
        return three, frozenset(five)

    keys_seen = 0
    for i in itertools.count():
        three, _ = _compute(i)
        if three:
            for j in range(i + 1, i + 1000 + 1):
                _, five = _compute(j)
                if three in five:
                    keys_seen += 1
                    break
        if keys_seen == 64:
            return i

    raise AssertionError('unreachable!')


INPUT_S = '''\
abc
'''
EXPECTED = 22728


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
