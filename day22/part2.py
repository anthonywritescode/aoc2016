from __future__ import annotations

import argparse
import heapq
import os.path
from typing import NamedTuple

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Node(NamedTuple):
    size: int
    used: int
    goal: bool

    @classmethod
    def parse(cls, line: str) -> tuple[int, int, Node]:
        name, size_s, used_s, _, _ = line.split()
        _, x_s, y_s = name.split('-')
        return int(x_s), int(y_s), cls(int(size_s), int(used_s), False)


class State(NamedTuple):
    empty: tuple[int, int]
    goal: tuple[int, int]


def compute(s: str) -> int:
    nodes = []
    s = s.replace('T', '').replace('x', '').replace('y', '')

    nodes = [Node.parse(line) for line in s.splitlines()[2:]]

    (ex, ey, empty), = ((x, y, node) for x, y, node in nodes if node.used == 0)
    immovable = set()
    for x, y, node in nodes:
        if node.used > empty.size:
            immovable.add((x, y))

    bx, by = support.bounds((x, y) for x, y, _ in nodes)
    bx_range, by_range = bx.range, by.range

    initial = State((ex, ey), (bx.max, 0))
    seen = {initial}
    todo = [(0, initial)]
    while todo:
        n, state = heapq.heappop(todo)

        if state.goal == (0, 0):
            return n

        for cx, cy in support.adjacent_4(*state.empty):
            if cx not in bx_range or cy not in by_range:
                continue
            elif (cx, cy) in immovable:
                continue

            if (cx, cy) == state.goal:
                newstate = State((cx, cy), state.empty)
            else:
                newstate = State((cx, cy), state.goal)

            if newstate not in seen:
                heapq.heappush(todo, (n + 1, newstate))
                seen.add(newstate)

    raise AssertionError('unreachable')


EXAMPLE = '''\
# df
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
'''


def test() -> None:
    assert compute(EXAMPLE) == 7


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
