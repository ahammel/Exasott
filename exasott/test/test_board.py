from exasott import boards
import pytest
    

class SetupBoardTest(object):
    normal_board = boards.Board(8, 8)


class TestBoardMethods(SetupBoardTest):
    def test_init(self):
        for x in range(8):
            for y in range(8):
                assert self.normal_board.board[x][y] == 1

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
