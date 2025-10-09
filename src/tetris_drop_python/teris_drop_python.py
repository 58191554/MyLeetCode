def drop(piece, background, offset):
    """
    Compute the maximum drop depth for a Tetris piece given a background and horizontal offset.

    The piece starts with its bottom row at background row index -1 (i.e., the piece top at -Ph),
    and drops vertically until moving one more row would either overlap an occupied background cell
    or exceed the bottom boundary of the background.

    Args:
        piece: 2D list of 0/1 (or '0'/'1') representing the falling piece.
        background: 2D list of 0/1 (or '0'/'1') representing the board.
        offset: integer horizontal offset (0-based) for the piece's left edge.

    Returns:
        Integer drop depth d.
    """
    piece_height, piece_width = len(piece), len(piece[0])
    bg_height, bg_width = len(background), len(background[0])

    def is_valid(depth):
        # piece top row index relative to background is -piece_height + depth
        for i in range(piece_height):
            for j in range(piece_width):
                if int(piece[i][j]) == 0:
                    continue
                bi = i + depth - piece_height
                bj = j + offset
                if bi < 0:
                    # Still above the visible background; no overlap possible.
                    continue
                if bi >= bg_height:
                    # Exceeds bottom boundary; invalid placement.
                    return False
                if int(background[bi][bj]) == 1:
                    return False
        return True

    depth = 0
    while is_valid(depth + 1):
        depth += 1
    return depth
