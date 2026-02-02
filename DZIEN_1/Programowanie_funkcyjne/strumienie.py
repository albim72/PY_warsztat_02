from __future__ import annotations

import struct
import zlib
from typing import Iterable, Iterator, Tuple


# ============================================================
# PRZYKŁAD 1: Generator okien (sliding window) + streaming
# ============================================================
def sliding_window(seq: Iterable[float], k: int) -> Iterator[Tuple[float, ...]]:
    """
    Zwraca kolejne okna długości k, bez budowania listy wszystkich okien.
    Przydatne w analizie sygnałów, statystyce, feature engineering.
    """
    if k <= 0:
        raise ValueError("k must be > 0")

    buf: list[float] = []
    for x in seq:
        buf.append(float(x))
        if len(buf) < k:
            continue
        if len(buf) > k:
            buf.pop(0)
        yield tuple(buf)


def moving_average(seq: Iterable[float], k: int) -> Iterator[float]:
    """
    Średnia krocząca liczona strumieniowo (generator).
    """
    for w in sliding_window(seq, k):
        yield sum(w) / k


if __name__ == "__main__":
    data = [10, 11, 13, 12, 12, 14, 15, 10, 9, 8]
    print("Okna k=3:")
    for w in sliding_window(data, 3):
        print(w)

    print("\nŚrednia krocząca k=3:")
    print(list(moving_average(data, 3)))


# ============================================================
# PRZYKŁAD 2: Generator rekordów z binarnego strumienia + CRC
# (czytasz bajty -> parsujesz -> yield rekordów, zero wczytywania całości)
# ============================================================

# Format:
#   magic: 2 bytes   b'PX'
#   version: 1 byte  (0..255)
#   n_records: 4 bytes unsigned (little-endian)
#   records: n * (timestamp: uint32, value: int16)
#   crc32: 4 bytes unsigned (crc z nagłówka+rekordów, bez samego crc)
HEADER_FMT = "<2sBI"     # magic, version, n_records
RECORD_FMT = "<Ih"       # timestamp, value
HEADER_SIZE = struct.calcsize(HEADER_FMT)
RECORD_SIZE = struct.calcsize(RECORD_FMT)


def pack_stream(records: Iterable[Tuple[int, int]], version: int = 1) -> bytes:
    """
    Pomocniczo: pakuje rekordy do jednego bytes z CRC (do testów).
    """
    rec_list = list(records)
    header = struct.pack(HEADER_FMT, b"PX", version, len(rec_list))

    body = bytearray()
    for ts, val in rec_list:
        if not (0 <= ts <= 0xFFFFFFFF):
            raise ValueError("timestamp must fit uint32")
        if not (-32768 <= val <= 32767):
            raise ValueError("value must fit int16")
        body += struct.pack(RECORD_FMT, ts, val)

    payload = header + bytes(body)
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    return payload + struct.pack("<I", crc)


def iter_records_from_bytes(blob: bytes) -> Iterator[Tuple[int, int]]:
    """
    Generator: parsuje binarny blob i yield-uje rekordy po jednym.
    Można to łatwo przerobić na czytanie z pliku w kawałkach.
    """
    if len(blob) < HEADER_SIZE + 4:
        raise ValueError("Blob too small")

    # CRC check
    given_crc = struct.unpack_from("<I", blob, len(blob) - 4)[0]
    payload = blob[:-4]
    calc_crc = zlib.crc32(payload) & 0xFFFFFFFF
    if given_crc != calc_crc:
        raise ValueError("CRC mismatch: data corrupted")

    magic, version, n = struct.unpack_from(HEADER_FMT, payload, 0)
    if magic != b"PX":
        raise ValueError("Bad magic bytes")
    if version != 1:
        raise ValueError(f"Unsupported version: {version}")

    offset = HEADER_SIZE
    need = offset + n * RECORD_SIZE
    if len(payload) < need:
        raise ValueError("Truncated payload")

    for i in range(n):
        ts, val = struct.unpack_from(RECORD_FMT, payload, offset)
        offset += RECORD_SIZE
        yield ts, val


if __name__ == "__main__":
    # Demo binarnego generatora
    sample = [(1, 120), (2, -50), (3, 999), (4, 0)]
    blob = pack_stream(sample, version=1)

    print("\nRekordy z binarnego blob:")
    for rec in iter_records_from_bytes(blob):
        print(rec)
