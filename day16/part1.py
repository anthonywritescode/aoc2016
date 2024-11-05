from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _checksum(s: str) -> str:
    ret = []
    for a, b in itertools.batched(s, 2):
        ret.append(str(int(a == b)))
    return ''.join(ret)


def compute(s: str, *, size: int = 272) -> str:
    s = s.strip()

    while len(s) < size:
        flipped = s[::-1]
        flipped = flipped.replace('0', '2')
        flipped = flipped.replace('1', '0')
        flipped = flipped.replace('2', '1')
        s = f'{s}0{flipped}'

    cs = s[:size]
    cs = _checksum(cs)
    while len(cs) % 2 == 0:
        cs = _checksum(cs)

    return cs


INPUT_S = '''\
10000
'''
EXPECTED = '01100'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: str) -> None:
    assert compute(input_s, size=20) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
