from __future__ import annotations

import argparse
import heapq
import itertools
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class State(NamedTuple):
    floors: tuple[frozenset[str], ...]
    pos: int

    @property
    def valid(self) -> bool:
        for floor in self.floors:
            gens = {s for s in floor if not s.endswith('-compatible')}
            for s in floor:
                if not s.endswith('-compatible'):
                    continue
                elif s.split('-')[0] in gens:
                    continue
                elif gens:
                    return False
        else:
            return True

    @property
    def finished(self) -> bool:
        return not any(self.floors[:-1])


def compute(s: str) -> int:
    s = s.replace(' and ', ' ').replace('.', '')

    floors = [
        frozenset(
            part.split()[1]
            for part in line.split(maxsplit=4)[-1].split(', ')
        )
        for line in s.splitlines()
    ]
    floors[-1] = frozenset()  # nothing relevant!

    seen = set()
    todo = [(0, State(floors=tuple(floors), pos=0))]
    while todo:
        n, state = heapq.heappop(todo)

        if state.finished:
            return n

        floor = state.floors[state.pos]

        directions = []
        if state.pos < 3:
            directions.append(1)
        if state.pos > 0:
            directions.append(-1)

        nitems = [1]
        if len(floor) > 1:
            nitems.append(2)

        for nitem in nitems:
            for take in itertools.combinations(floor, nitem):
                for direction in directions:
                    floors = list(state.floors)
                    floors[state.pos] -= frozenset(take)
                    floors[state.pos + direction] |= frozenset(take)

                    newstate = State(
                        floors=tuple(floors),
                        pos=state.pos + direction,
                    )
                    if newstate.valid and newstate not in seen:
                        heapq.heappush(todo, (n + 1, newstate))
                        seen.add(newstate)

    raise AssertionError('unreachable')


INPUT_S = '''\
The first floor contains a hydrogen-compatible microchip, and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
'''  # noqa: E501
EXPECTED = 11


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
