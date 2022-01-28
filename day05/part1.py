from __future__ import annotations

import argparse
import hashlib
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    s = s.strip()
    i = 0
    ret = ''
    for _ in range(8):
        while True:
            i += 1
            h = hashlib.md5(f'{s}{i}'.encode()).hexdigest()
            if h[:5] == '00000':
                ret += h[5]
                break
    return ret


INPUT_S = '''\
abc
'''
EXPECTED = '18f47a30'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
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
