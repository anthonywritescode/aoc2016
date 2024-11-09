from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, *, password: str = 'abcdefgh') -> str:
    lst = list(password)

    def _rotate(sign: int, n: int) -> None:
        lst[:] = lst[sign * n:] + lst[:sign * n]

    s = s.replace('steps', 'step')
    for line in s.splitlines():
        match line.split():
            case ['swap', 'position', pos1_s, 'with', 'position', pos2_s]:
                pos1, pos2 = int(pos1_s), int(pos2_s)
                lst[pos1], lst[pos2] = lst[pos2], lst[pos1]
            case ['swap', 'letter', let1, 'with', 'letter', let2]:
                pos1, pos2 = lst.index(let1), lst.index(let2)
                lst[pos1], lst[pos2] = lst[pos2], lst[pos1]
            case ['rotate', direction, n_s, 'step']:
                n = int(n_s)
                sign = -1 if direction == 'right' else 1
                _rotate(sign, n)
            case ['rotate', 'based', 'on', 'position', 'of', 'letter', let1]:
                n = lst.index(let1)
                _rotate(-1, 1)
                _rotate(-1, n)
                if n >= 4:
                    _rotate(-1, 1)
            case ['reverse', 'positions', pos1_s, 'through', pos2_s]:
                pos1, pos2 = int(pos1_s), int(pos2_s)
                lst[pos1:pos2 + 1] = lst[pos1:pos2 + 1][::-1]
            case ['move', 'position', pos1_s, 'to', 'position', pos2_s]:
                pos1, pos2 = int(pos1_s), int(pos2_s)
                lst.insert(pos2, lst.pop(pos1))
            case unreachable:
                raise AssertionError(unreachable)

    return ''.join(lst)


INPUT_S = '''\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
'''
EXPECTED = 'decab'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: str) -> None:
    assert compute(input_s, password='abcde') == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
