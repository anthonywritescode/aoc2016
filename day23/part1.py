from __future__ import annotations

import argparse
import collections
import os.path

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

TOGGLE = {
    'inc': 'dec',
    'dec': 'inc',
    'tgl': 'inc',
    'jnz': 'cpy',
    'cpy': 'jnz',
}


def compute(s: str) -> int:
    regs: dict[str, int] = collections.defaultdict(int)
    regs['a'] = 7

    def _lookup(s: str) -> int:
        if s.isalpha():
            return regs[s]
        else:
            return int(s)

    instructions = [line.split() for line in s.splitlines()]
    pc = 0

    while 0 <= pc < len(instructions):
        match instructions[pc]:
            case 'cpy', src, dest:
                if dest.isalpha():
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
                    pc += _lookup(jump)
                else:
                    pc += 1
            case 'tgl', dest:
                target = pc + _lookup(dest)
                if 0 <= target < len(instructions):
                    instructions[target][0] = TOGGLE[instructions[target][0]]
                pc += 1

    return regs['a']


EXAMPLE = '''\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
'''


def test() -> None:
    assert compute(EXAMPLE) == 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
