from __future__ import annotations

import argparse
import os.path

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


_REVERSE_8 = {
    0: 7,
    7: -4,
    6: 0,
    5: -3,
    4: 1,
    3: -2,
    2: 2,
    1: -1,
}


def compute(s: str, *, password: str = 'fbgdceah') -> str:
    lst = list(password)

    def _rotate(sign: int, n: int) -> None:
        lst[:] = lst[sign * n:] + lst[:sign * n]

    s = s.replace('steps', 'step')
    for line in reversed(s.splitlines()):
        match line.split():
            case ['swap', 'position', pos1_s, 'with', 'position', pos2_s]:
                pos1, pos2 = int(pos1_s), int(pos2_s)
                lst[pos1], lst[pos2] = lst[pos2], lst[pos1]
            case ['swap', 'letter', let1, 'with', 'letter', let2]:
                pos1, pos2 = lst.index(let1), lst.index(let2)
                lst[pos1], lst[pos2] = lst[pos2], lst[pos1]
            case ['rotate', direction, n_s, 'step']:
                n = int(n_s)
                sign = 1 if direction == 'right' else -1
                _rotate(sign, n)
            case ['rotate', 'based', 'on', 'position', 'of', 'letter', let1]:
                n = lst.index(let1)
                _rotate(-1, _REVERSE_8[n])
            case ['reverse', 'positions', pos1_s, 'through', pos2_s]:
                pos1, pos2 = int(pos1_s), int(pos2_s)
                lst[pos1:pos2 + 1] = lst[pos1:pos2 + 1][::-1]
            case ['move', 'position', pos1_s, 'to', 'position', pos2_s]:
                pos1, pos2 = int(pos1_s), int(pos2_s)
                lst.insert(pos1, lst.pop(pos2))
            case unreachable:
                raise AssertionError(unreachable)

    return ''.join(lst)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
