from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

ABA_RE = re.compile(r'(?:^|\])[a-z]*([a-z])(?!\1)([a-z])\1.*\[[a-z]*\2\1\2')
ABA_2_RE = re.compile(r'\[[a-z]*([a-z])(?!\1)([a-z])\1.*\][a-z]*\2\1\2')


def compute(s: str) -> int:
    ret = 0
    for line in s.splitlines():
        if ABA_RE.search(line) or ABA_2_RE.search(line):
            ret += 1
    return ret


INPUT_S = '''\
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
'''
EXPECTED = 3


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
