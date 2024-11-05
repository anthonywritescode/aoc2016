from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

TRAP = frozenset((
    ('.', '.', '^'),
    ('^', '.', '.'),
    ('^', '^', '.'),
    ('.', '^', '^'),
))


def compute(s: str, *, nrows: int = 400000) -> int:
    rows = [s.strip()]

    for _ in range(nrows - 1):
        newrow = []
        for comp in zip(f'.{rows[-1]}', rows[-1], f'{rows[-1][1:]}.'):
            if comp in TRAP:
                newrow.append('^')
            else:
                newrow.append('.')
        rows.append(''.join(newrow))

    return sum(sum(c == '.' for c in row) for row in rows)


INPUT_S = '''\
.^^.^.^^^^
'''
EXPECTED = 38


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, nrows=10) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
