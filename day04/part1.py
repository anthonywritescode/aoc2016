from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    ret = 0
    for line in s.splitlines():
        enc, _, expected_checksum = line.partition('[')
        enc, _, roomid_s = enc.rpartition('-')
        expected_checksum = expected_checksum.rstrip(']')

        counts = collections.Counter(enc)
        del counts['-']
        top = sorted(counts.most_common(), key=lambda kv: (-kv[1], kv[0]))
        checksum = ''.join(c for c, _ in top[:5])
        if checksum == expected_checksum:
            ret += int(roomid_s)

    return ret


INPUT_S = '''\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
'''
EXPECTED = 1514


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
