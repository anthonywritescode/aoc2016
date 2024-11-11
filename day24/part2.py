from __future__ import annotations

import argparse
import collections
import heapq
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class State(NamedTuple):
    done: frozenset[str]
    c: str
    returned: bool = False


def compute(s: str) -> int:
    walls = support.parse_coords_hash(s)
    digits = {
        (x, y): c
        for y, row in enumerate(s.splitlines())
        for x, c in enumerate(row)
        if c.isdigit()
    }
    start, = ((x, y) for (x, y), c in digits.items() if c == '0')

    paths: dict[str, dict[str, int]] = collections.defaultdict(dict)
    for (x, y), c in digits.items():
        seen = {(x, y)}
        todo = collections.deque([(0, (x, y))])
        while todo:
            n, pos = todo.popleft()
            if pos in digits:
                paths[c].setdefault(digits[pos], n)

            for cpos in support.adjacent_4(*pos):
                if cpos not in walls and cpos not in seen:
                    seen.add(cpos)
                    todo.append((n + 1, cpos))

    initial = State(frozenset(('0',)), '0')
    todo2 = [(0, initial)]
    while todo2:
        n, state = heapq.heappop(todo2)

        if state.returned:
            return n

        if len(state.done) == len(digits):
            newstate = state._replace(returned=True, c='0')
            heapq.heappush(todo2, (n + paths[state.c]['0'], newstate))
            continue

        for dest, dist in paths[state.c].items():
            if dest in state.done:
                continue
            newstate = State(state.done | {dest}, dest)
            heapq.heappush(todo2, (n + dist, newstate))

    raise AssertionError('unreachable')


INPUT_S = '''\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
'''
EXPECTED = 20


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
