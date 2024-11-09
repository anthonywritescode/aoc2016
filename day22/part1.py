from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple

import support


class Node(NamedTuple):
    size: int
    used: int

    @classmethod
    def parse(cls, line: str) -> tuple[int, int, Node]:
        name, size_s, used_s, _, _ = line.split()
        _, x_s, y_s = name.split('-')
        return int(x_s), int(y_s), cls(int(size_s), int(used_s))


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _viable(node: Node, other: Node) -> bool:
    return (
        node.used != 0 and
        other.size >= other.used + node.used
    )


def compute(s: str) -> int:
    nodes = []
    s = s.replace('T', '').replace('x', '').replace('y', '')
    for line in s.splitlines()[2:]:
        _, _, node = Node.parse(line)
        nodes.append(node)

    total = 0
    for i, node in enumerate(nodes):
        for other in nodes[i + 1:]:
            total += _viable(node, other) + _viable(other, node)

    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
