from exasott import boards
import pytest


class SetupBoardTest(object):
    normal_board = boards.Board(8, 8)
    rectangle_board = boards.Board(2, 6)

    normal_board_str = (" ABCDEFGH\n"
                        "1OOOOOOOO\n"
                        "2OOOOOOOO\n"
                        "3OOOOOOOO\n"
                        "4OOOOOOOO\n"
                        "5OOOOOOOO\n"
                        "6OOOOOOOO\n"
                        "7OOOOOOOO\n"
                        "8OOOOOOOO\n")

    rectangle_board_str = (" AB\n"
                           "1OO\n"
                           "2OO\n"
                           "3OO\n"
                           "4OO\n"
                           "5OO\n"
                           "6OO\n")


class TestBoardMethods(SetupBoardTest):
    def test_str(self):
        assert str(self.normal_board) == self.normal_board_str
        assert str(self.rectangle_board) == self.rectangle_board_str

    def test_get_token(self):
        for x in range(8):
            for y in range(8):
                assert self.normal_board.get_token(x, y) == 1

        with pytest.raises(boards.BoardRangeError):
            self.normal_board.get_token(1, 10)

    def test_remove_token(self):
        self.normal_board.remove_token(0, 3)
        assert self.normal_board.get_token(0, 3) == 0

        with pytest.raises(boards.BoardRangeError):
            self.normal_board.remove_token(0, 10)

        with pytest.raises(boards.MissingTokenError):
            self.normal_board.remove_token(0, 3)
