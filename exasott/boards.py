"""Exasott board classes.

"""
import string


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
        self.columns = cols
        self.rows = rows
        self.board = {(column, row): 1 
                      for column in range(cols) for row in range(rows)}

    def __str__(self):
        board_str = " " + string.ascii_uppercase[:self.columns] + "\n"

        for row in range(self.rows):
            board_str += str(row + 1)
            for column in range(self.columns):
                if self.get_token(column, row):
                    board_str += 'O'
                else:
                    board_str += 'X'
            board_str += '\n'

        return board_str

    def get_token(self, col, row):
        """Returns the token at position (col, row).

        """
        try:
            return self.board[(col, row)]
        except KeyError:
            bad_index = str((col, row))
            raise BoardRangeError(bad_index)

    def remove_token(self, col, row):
        """Flips the token at position (col, row) to zero.

        """
        try:
            token = self.board[(col, row)]
        except KeyError:
            bad_index = str((col, row))
            raise BoardRangeError(bad_index)

        if not token:
            raise MissingTokenError(str((col, row)))

        self.board[(col, row)] = 0
