from jigsolver.puzzle import *
import numpy as np


def greedy_placer(puzzle, compatibilites, rolling=True, display=False):
    """Place the remaining pieces of a given a partially contructed puzzle
    in a greedy manner.
    For each remaining piece and for each available
    position, a score is computed (average of the compatibilities between the
    piece and the already placed pieces adjacent to the available position).
    The greedy criteria to choose the piece and its position is simply the
    pair (piece - position) that gets the highest score.
    Args:
        puzzle [Puzzle]: puzzle with empty or partially filled board
        compatibilites [N×N array]: compatibilities[p,q] is the compatibility
            score between pieces #p and #q in the puzzle.
        rolling [bool, optional]: If set to True, the puzzle pieces are in a
            "floating" state: Each time a piece is placed at a border, all
            pieces are shifted to keep the border empty.
        display [bool, optional]: If set to True, the puzzle is displayed at
            each iteration.
    """
    n, m = puzzle.shape
    n_pieces = n * m

    ## The scores between pieces and empty positions on the board are stored
    # in a 3D matrix M.
    # M[i,j,p] is the avg compatibility if piece #p was placed at (i,j) in the board
    # A negative value (e.g. -1) indicated that the piece / position is no more
    # available (the piece has already been placed or the position is already
    # occupied by an other piece)
    M = np.zeros((n, m, n_pieces))

    def update_M(piece_id, slot_coords):
        ## Remove the placed piece and the filled slot from matrix M
        M[:, :, piece_id] = -1
        M[slot_coords[0], slot_coords[1]] = -1

        ## Update the scores (of all remaining pieces) for all neighboring slots
        for i, j in puzzle.board.adjacent_empty_slots(*slot_coords):  # fore each neighboring slot
            adjacent_pieces = [(position, piece) for position, piece in puzzle.board.neighbors(i, j) if
                               isinstance(piece, Piece)]
            for piece in puzzle.pieces_remaining:
                scores = [compatibilites[piece.id, adjacent.id, position] for position, adjacent in adjacent_pieces]
                M[i, j, piece.id] = sum(scores) / len(scores)

    def border_is_empty(M, border):
        return np.all(M[border.slice] <= 0) and np.any(M[border.slice] != -1)

    def roll(M, i, j):
        """Move the puzzle  (and the score matrix M) if a border is reached"""
        new_i, new_j = i, j
        if i == 0 and border_is_empty(M, Border.BOTTOM):
            puzzle.board._grid = np.roll(puzzle.board._grid, 1, axis=0)
            M = np.roll(M, 1, axis=0)
            new_i = 1
        elif i == n - 1 and border_is_empty(M, Border.TOP):
            puzzle.board._grid = np.roll(puzzle.board._grid, -1, axis=0)
            M = np.roll(M, -1, axis=0)
            new_i = n - 2

        if j == 0 and border_is_empty(M, Border.RIGHT):
            puzzle.board._grid = np.roll(puzzle.board._grid, 1, axis=1)
            M = np.roll(M, 1, axis=1)
            new_j = 1
        elif j == m - 1 and border_is_empty(M, Border.LEFT):
            puzzle.board._grid = np.roll(puzzle.board._grid, -1, axis=1)
            M = np.roll(M, -1, axis=1)
            new_j = m - 2
        return new_i, new_j, M

    ## Init
    n_pieces_remaining = len(list(puzzle.pieces_remaining))
    if any(puzzle.pieces_placed):
        for piece in puzzle.pieces_placed:
            update_M(piece.id, piece.position)
    else:
        M[n // 2, m // 2, 0] = 1

    ## Main loop: find the best piece-slot pair and place it
    for _ in range(n_pieces_remaining):
        *coords, piece_id = np.unravel_index(np.argmax(M), M.shape)
        piece = puzzle.bag_of_pieces[piece_id]
        puzzle.place(piece, coords)
        if rolling:
            *coords, M = roll(M, *coords)
        update_M(piece_id, coords)
        if display:
            puzzle.display()


# %%
def naiv_greedy_placer(puzzle, compatibilities, display=False):
    def decide_piece_to_add(puzzle, compatibilities):
        positions = list(available_positions(puzzle))
        assert len(positions) != 0, "No empty slot left!"
        best_value = -1
        best_position = None
        best_piece = None
        for slot_coord in positions:
            piece, value = find_best_piece_for_slot(puzzle, slot_coord, compatibilities)
            if value >= best_value:
                best_value = value
                best_position = slot_coord
                best_piece = piece
        return best_position, best_piece

    def find_best_piece_for_slot(puzzle, slot_coord, compatibilities):
        best_diss_value = -1
        best_piece = None

        for piece in puzzle.pieces_remaining:
            diss_value = []
            for position, neigh in puzzle.board.neighbors(*slot_coord):
                if isinstance(neigh, Piece):
                    diss_value.append(compatibilities[piece.id, neigh.id, position])

            diss_value_avg = np.mean(diss_value)
            if diss_value_avg >= best_diss_value:
                best_diss_value = diss_value_avg
                best_piece = piece

        return best_piece, best_diss_value

    def available_positions(puzzle):
        """Return a generator that yields the coordinates of "available" place"""
        return (
            (i, j) for (i, j), elmt in puzzle.board.enumerate()
            if isinstance(elmt, Slot) and elmt.available
        )

    n_pieces = len(list(puzzle.pieces_remaining))

    ## INIT: no piece
    if all(not piece._is_placed for piece in puzzle.bag_of_pieces):
        n_rows, n_cols = puzzle.shape
        puzzle.place(puzzle.bag_of_pieces[0], (n_rows // 2, n_cols // 2))
        n_pieces -= 1
        if display:
            puzzle.display()
    for _ in range(n_pieces):
        position, piece = decide_piece_to_add(puzzle, compatibilities)
        puzzle.place(piece, position)
        if display:
            puzzle.display()