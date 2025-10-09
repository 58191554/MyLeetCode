import pytest

from teris_drop_python import drop


def _to_grid(lines):
    return [list(row.strip()) for row in lines]


def test_sample_1_depth_3():
    piece = _to_grid([
        "010",
        "011",
        "000",
    ])
    background = _to_grid([
        "0000000",
        "0000000",
        "0000100",
        "0010100",
    ])
    offset = 2
    assert drop(piece, background, offset) == 3


def test_sample_2_depth_1():
    piece = _to_grid([
        "010",
        "011",
        "010",
    ])
    background = _to_grid([
        "0000100",
        "0010100",
    ])
    offset = 2
    assert drop(piece, background, offset) == 1


def test_sample_3_depth_3():
    piece = _to_grid([
        "010",
        "011",
        "000",
    ])
    background = _to_grid([
        "0000000",
        "0000000",
    ])
    offset = 2
    assert drop(piece, background, offset) == 3


