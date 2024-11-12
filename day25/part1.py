from __future__ import annotations

import argparse
import collections
import itertools
import os.path
from collections.abc import Sequence

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _run(instructions: Sequence[Sequence[str]], n: int) -> bool:
    seen: list[int] = []

    regs: dict[str, int] = collections.defaultdict(int)
    regs['a'] = n

    def _lookup(s: str) -> int:
        if s.isalpha():
            return regs[s]
        else:
            return int(s)

    pc = 0

    while 0 <= pc < len(instructions):
        if pc == len(instructions) - 1:
            return len(seen) % 2 == 0

        match instructions[pc]:
            case 'add', src, dest:
                regs[dest] += _lookup(src)
                pc += 1
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
            case 'out', dest:
                val = _lookup(dest)
                seen.append(val)
                if val > 1:
                    return False
                elif len(seen) == 1:
                    if val != 0:
                        return False
                elif seen[-1] != (not seen[-2]):
                    return False
                pc += 1
            case 'mod2', src, dest:
                if _lookup(src) % 2 == 0:
                    regs[dest] = 2
                else:
                    regs[dest] = 1
                pc += 1
            case 'div2', dest:
                regs[dest] //= 2
                pc += 1
            case ['nop']:
                pc += 1
            case unreachable:
                raise AssertionError(unreachable)

    return False


def compute(s: str) -> int:
    instructions = [line.split() for line in s.splitlines()]

    instructions[:8] = [
        ['add', '2572', 'a'],
        ['cpy', 'a', 'd'],
    ]

    instructions[4:14] = [
        ['mod2', 'a', 'c'],
        ['div2', 'a'],
        *([['nop']] * 8),
    ]

    # _run(instructions, 158)

    for i in itertools.count(1):
        if _run(instructions, i):
            return i
        if i % 1000 == 0:
            print(i)

    raise AssertionError('unreachable')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
