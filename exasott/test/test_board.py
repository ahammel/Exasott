"""Unit tests for the exasott.boards module.

"""
from exasott import boards, test
import pytest


class SetupBoardTest(object):
    """Shared objects for all exasott.board test classes.

    """
    normal_board = boards.Board(8, 8)
    rectangle_board = boards.Board(2, 6)

    rectangle_board_str = (" AB\n"
                           "1OO\n"
                           "2OO\n"
                           "3OO\n"
                           "4OO\n"
                           "5OO\n"
                           "6OO\n")


class TestBoardMethods(SetupBoardTest):
    """Unit tests for the Board class's methods.

    """
    def test_str(self):
        """Specifications for Board.__str__

        """
        assert str(self.normal_board) == test.NORMAL_BOARD_STR
        assert str(self.rectangle_board) == self.rectangle_board_str

    def test_get_token(self):
        """Board.get_token should return the value of the token or throw a 
        pre-defined error if the toke is out of range.

        """
        for i in range(8):
            for j in range(8):
                assert self.normal_board.get_token(i, j) == 1

        with pytest.raises(boards.BoardRangeError):
            self.normal_board.get_token(1, 10)

    def test_remove_token(self):
        """Board.remove_token should change the value of the token from 1 to
        zero, throwing an exception if either the token is out of range or 
        already zero.

        """
        self.normal_board.remove_token(0, 3)
        assert self.normal_board.get_token(0, 3) == 0

        with pytest.raises(boards.BoardRangeError):
            self.normal_board.remove_token(0, 10)

        with pytest.raises(boards.MissingTokenError):
            self.normal_board.remove_token(0, 3)
