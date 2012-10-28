from exasott import games
import pytest

class GameTestSetup(object):
    standard_game = games.Game()
    minimum_game = games.Game((2, 2), {(1, 1): 1}, {(1, 1): 1})
    standard_sticks = {(0, 1): 1, (1, 1): 5, (1, 2): 5, (1, 3): 5}


class TestGameMethods(GameTestSetup):
    def test_init(self):
        std_board = self.standard_game.board
        assert std_board.rows == 8
        assert std_board.columns == 8
        for x in range(8):
            for y in range(8):
                assert std_board.get_token(x, y) == 1

        min_board = self.minimum_game.board
        assert min_board.rows == 2
        assert min_board.columns == 2
        for x in range(2):
            for y in range(2):
                assert min_board.get_token(x, y) == 1

        standard_sticks = {(0, 1): 1,
                           (1, 1): 5,
                           (1, 2): 5,
                           (1, 3): 5}

        assert self.standard_game.r_sticks == self.standard_sticks
        assert self.standard_game.b_sticks == self.standard_sticks
        assert self.minimum_game.r_sticks == {(1, 1): 1}
        assert self.minimum_game.b_sticks == {(1, 1): 1}

        assert self.standard_game.red_to_move
        assert self.minimum_game.red_to_move

    def test_str(self):
        assert str(self.standard_game) == (" ABCDEFGH\n"
                                          "1OOOOOOOO\n"
                                          "2OOOOOOOO\n"
                                          "3OOOOOOOO\n"
                                          "4OOOOOOOO\n"
                                          "5OOOOOOOO\n"
                                          "6OOOOOOOO\n"
                                          "7OOOOOOOO\n"
                                          "8OOOOOOOO\n"
                                          "\n"
                                          "*Red  {01: 1, 11: 5, 12: 5, 13: 5}\n"
                                          " Blue {01: 1, 11: 5, 12: 5, 13: 5}")

        self.minimum_game.move((0, 0), (1, 1))

        assert str(self.minimum_game) == (" AB\n"
                                          "1XO\n"
                                          "2OX\n"
                                          "\n"
                                          " Red  {}\n"
                                          "*Blue {11: 1}")

    def test_move(self):
        self.standard_game.move((0,0), (0,1))
        assert not self.standard_game.board.get_token(0, 0)
        assert not self.standard_game.board.get_token(0, 1)
        assert not self.standard_game.red_to_move
        assert not self.standard_game.r_sticks[(0, 1)]
        assert self.standard_game.b_sticks == self.standard_sticks

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move((0,0), (0,1))

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move((2,2), (0,10))

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move((2,2), (4,4))

        self.standard_game.move((2,2), (3,3))

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move((6,6), (6,7))
