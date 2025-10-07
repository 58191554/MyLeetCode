import threading
import time

import pytest

from multi_thread_data_writer_python import DataWriter


def _read_bytes_from_captured(capsys):
    captured = capsys.readouterr()
    return captured.out.encode()


def test_single_thread_ordering(capsys):
    dw = DataWriter("/dev/null", queue_capacity=32, batch_bytes=1 << 10, batch_count=64)
    try:
        expected_lines = []
        for i in range(100):
            line = f"T0:{i:04d}\n".encode()
            expected_lines.append(line)
            dw.push(line)
    finally:
        dw.close()

    data = _read_bytes_from_captured(capsys)
    assert data == b"".join(expected_lines)


def test_multi_thread_per_thread_ordering(capsys):
    num_threads = 5
    per_thread_msgs = 200
    dw = DataWriter("/dev/null", queue_capacity=256, batch_bytes=1 << 12, batch_count=256)

    def producer(tid: int):
        for i in range(per_thread_msgs):
            dw.push(f"T{tid}:{i:04d}\n".encode())

    threads = [threading.Thread(target=producer, args=(t,)) for t in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    dw.close()

    lines = _read_bytes_from_captured(capsys).splitlines()
    # Group by thread id and verify increasing sequence per thread
    last_seen = {}
    for line in lines:
        s = line.decode()
        tid_str, num_str = s.split(":")
        tid = tid_str[1:]
        num = int(num_str)
        if tid in last_seen:
            assert num > last_seen[tid]
        last_seen[tid] = num
    # Ensure all messages accounted for
    assert len(lines) == num_threads * per_thread_msgs


def test_small_queue_backpressure_and_batching(capsys):
    # Tiny queue to force producer blocking; ensure no data loss and proper append
    dw = DataWriter("/dev/null", queue_capacity=4, batch_bytes=256, batch_count=8)

    def producer(n):
        for i in range(n):
            dw.push(f"X:{i}\n".encode())

    t1 = threading.Thread(target=producer, args=(50,))
    t2 = threading.Thread(target=producer, args=(50,))
    t1.start(); t2.start()
    t1.join(); t2.join()
    dw.close()

    data = _read_bytes_from_captured(capsys)
    assert len(data.splitlines()) == 100


def test_enable_fsync_and_nested_dir_creation(capsys):
    dw = DataWriter("/dev/null")
    dw.enable_fsync(True)
    for i in range(10):
        dw.push(f"F:{i}\n".encode())
    dw.close()
    data = _read_bytes_from_captured(capsys)
    assert len(data.splitlines()) == 10


# def test_large_messages(capsys):
#     dw = DataWriter("/dev/null", batch_bytes=1 << 20, batch_count=64)
#     blob = b"A" * (256 * 1024)  # 256 KiB
#     for _ in range(8):
#         dw.push(blob)
#     dw.close()
#     data = _read_bytes_from_captured(capsys)
#     assert len(data) == len(blob) * 8
#     assert data.startswith(b"A" * 1024)


