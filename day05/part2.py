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
    ret: dict[int, str] = {}
    while len(ret) != 8:
        while True:
            i += 1
            h = hashlib.md5(f'{s}{i}'.encode()).hexdigest()
            if h[:5] == '00000':
                idx = int(h[5], 16)
                if idx <= 7:
                    ret.setdefault(idx, h[6])
                break

    return ''.join(v for _, v in sorted(ret.items()))


INPUT_S = '''\
abc
'''
EXPECTED = '05ace8e3'


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
