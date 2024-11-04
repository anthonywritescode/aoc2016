from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    regs: dict[str, int] = collections.defaultdict(int)

    def _lookup(s: str) -> int:
        if s.isdigit():
            return int(s)
        else:
            return regs[s]

    instructions = [line.split() for line in s.splitlines()]
    pc = 0

    while 0 <= pc < len(instructions):
        match instructions[pc]:
            case 'cpy', src, dest:
                regs[dest] = _lookup(src)
                pc += 1
            case 'inc', dest:
                regs[dest] += 1
                pc += 1
            case 'dec', dest:
                regs[dest] -= 1
                pc += 1
            case 'jnz', cond, jump:
                if _lookup(cond):
                    pc += int(jump)
                else:
                    pc += 1

    return regs['a']


INPUT_S = '''\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
'''
EXPECTED = 42


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
