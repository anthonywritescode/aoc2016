from __future__ import annotations

import argparse
import collections
import os.path

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

        if all(n in outputs for n in (0, 1, 2)):
            return outputs[0] * outputs[1] * outputs[2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
