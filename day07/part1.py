from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

ABBA_RE = re.compile(r'([a-z])(?!\1)([a-z])\2\1')
ABBA_B_RE = re.compile(r'\[[a-z]*([a-z])(?!\1)([a-z])\2\1')


def compute(s: str) -> int:
    ret = 0
    for line in s.splitlines():
        if ABBA_RE.search(line) and not ABBA_B_RE.search(line):
            ret += 1
    return ret


INPUT_S = '''\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
'''
EXPECTED = 2


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
