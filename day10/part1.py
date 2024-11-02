from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, *, target: tuple[int, int] = (17, 61)) -> int:
    outputs = {}
    bots = collections.defaultdict(list)
    instructions = {}

    for line in s.splitlines():
        parts = line.split()
        if parts[0] == 'value':
            _, val_s, *_, target_s = parts
            val, bot_target = int(val_s), int(target_s)
            bots[bot_target].append(val)
        elif parts[0] == 'bot':
            _, bot_s, _, _, _, low_tp, low_s, _, _, _, high_tp, high_s = parts
            bot, low, high = int(bot_s), int(low_s), int(high_s)
            instructions[bot] = (low, low_tp, high, high_tp)
        else:
            raise AssertionError('unreachable')

    while True:
        for bot, vals in tuple(bots.items()):
            if len(vals) != 2:
                continue

            low, high = sorted(vals)
            if (low, high) == target:
                return bot

            vals.clear()

            low_target, low_tp, high_target, high_to = instructions[bot]
            if low_tp == 'output':
                outputs[low_target] = low
            else:
                bots[low_target].append(low)

            if high_tp == 'output':
                outputs[high_target] = high
            else:
                bots[high_target].append(high)


INPUT_S = '''\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
'''
EXPECTED = 2


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, target=(2, 5)) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
