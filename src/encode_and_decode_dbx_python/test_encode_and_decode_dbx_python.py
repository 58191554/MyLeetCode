from encode_and_decode_dbx_python import Solution


def test1():
    solution = Solution()

    input = [5, 5, 5, 5, 5, 5, 5, 5, 1, 2, 3]
    encoded = solution.encode(input)
    assert encoded == ["RLE[5,8]", "BP[1,2,3]"]

    decoded = solution.decode(encoded)
    assert decoded == [5, 5, 5, 5, 5, 5, 5, 5, 1, 2, 3]

def test2():
    solution = Solution()

    input = [1, 1, 1]
    encoded = solution.encode(input)
    assert encoded == ["RLE[1,3]"]

    decoded = solution.decode(encoded)
    assert decoded == [1, 1, 1]

def test3():
    solution = Solution()

    input = [1, 1, 1, 1, 2, 3, 4, 5]
    encoded = solution.encode(input)
    assert encoded == ["BP[1,1,1,1,2,3,4,5]"]

    decoded = solution.decode(encoded)
    assert decoded == [1, 1, 1, 1, 2, 3, 4, 5]

def test4():
    solution = Solution()

    input = [1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    encoded = solution.encode(input)
    assert encoded == ["BP[1,1,1,1,2,3,4,5]", "BP[6,7,8,9,10,11,12,13]"]

    decoded = solution.decode(encoded)
    assert decoded == [1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

def test5():
    solution = Solution()

    input = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 11]
    encoded = solution.encode(input)
    assert encoded == ["RLE[0,8]", "BP[1,2,3,4,5,6,7,8]", "RLE[9,10]", "BP[10,11]"]

    decoded = solution.decode(encoded)
    assert decoded == [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 11]


def test_edge_exactly_8_rle_then_short_bp_tail():
    solution = Solution()

    input = [7] * 8 + [1, 2, 3]
    encoded = solution.encode(input)
    assert encoded == ["RLE[7,8]", "BP[1,2,3]"]
    assert solution.decode(encoded) == input


def test_edge_rle_over_8_single_run():
    solution = Solution()

    input = [5] * 10
    encoded = solution.encode(input)
    assert encoded == ["RLE[5,10]"]
    assert solution.decode(encoded) == input


def test_edge_two_full_bp_blocks_of_8():
    solution = Solution()

    input = list(range(1, 17))
    encoded = solution.encode(input)
    assert encoded == [
        "BP[1,2,3,4,5,6,7,8]",
        "BP[9,10,11,12,13,14,15,16]",
    ]
    assert solution.decode(encoded) == input


def test_edge_last_rle_shorter_than_8_allowed():
    solution = Solution()

    input = [2] * 8 + [3] * 3
    encoded = solution.encode(input)
    # Last RLE run may be shorter than 8
    assert encoded == ["RLE[2,8]", "RLE[3,3]"]
    assert solution.decode(encoded) == input


def test_edge_initial_short_repeat_grouped_into_bp():
    solution = Solution()

    input = [9] * 7 + [8, 9, 10, 11, 12, 13, 14]
    # First BP groups 7 nines plus next value to make 8; tail is last BP < 8
    encoded = solution.encode(input)
    assert encoded == [
        "BP[9,9,9,9,9,9,9,8]",
        "BP[9,10,11,12,13,14]",
    ]
    assert solution.decode(encoded) == input


def test_edge_interleaved_rle_bp_rle():
    solution = Solution()

    input = [0] * 9 + list(range(1, 11))
    encoded = solution.encode(input)
    # RLE for 9 zeros, then BP for next 8, then last BP for remaining 2
    assert encoded == [
        "RLE[0,9]",
        "BP[1,2,3,4,5,6,7,8]",
        "BP[9,10]",
    ]
    assert solution.decode(encoded) == input
