"""Exasott board classes."""

class BoardRangeError(ValueError):
    """The exception raised when attempting to access a token which is not on
    the board.

    """


class MissingTokenError(ValueError):
    """The exception raised when attempting to remove a token that is already
    gone.

    """

class Board(object):
    """An Exasott board. Duh.

    """
    def __init__(self, cols, rows):
        self.board = {c: {r: 1 for r in range(cols)} for c in range(rows)}

    def get_token(self, col, row):
        """Returns the token at position (col, row).

        """
        try:
            return self.board[col][row]
        except KeyError:
            bad_index = str((col, row))
            raise BoardRangeError(bad_index)

    def remove_token(self, col, row):
        """Flips the token at position (col, row) to zero.

        """
        try:
            token = self.board[col][row]
        except KeyError:
            bad_index = str((col, row))
            raise BoardRangeError(bad_index)

        if not token:
            raise MissingTokenError(str((col, row)))

        self.board[col][row] = 0
