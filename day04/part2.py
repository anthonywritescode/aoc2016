from __future__ import annotations

import argparse
import collections
import os.path

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def decrypt(s: str, room: int) -> str:
    return ''.join(
        ' '
        if c == '-' else
        chr(((ord(c) - ord('a')) + room) % 26 + ord('a'))
        for c in s
    )


def compute(s: str) -> int:
    for line in s.splitlines():
        enc, _, expected_checksum = line.partition('[')
        enc, _, roomid_s = enc.rpartition('-')
        expected_checksum = expected_checksum.rstrip(']')

        counts = collections.Counter(enc)
        del counts['-']
        top = sorted(counts.most_common(), key=lambda kv: (-kv[1], kv[0]))
        checksum = ''.join(c for c, _ in top[:5])
        if checksum != expected_checksum:
            continue

        roomid = int(roomid_s)
        if decrypt(enc, roomid) == 'northpole object storage':
            return roomid

    raise AssertionError('unreachable')


def test_decrypt() -> None:
    assert decrypt('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
