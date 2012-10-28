from exasott import games
import pytest

class GameTestSetup(object):
    standard_game = games.Game()
    minimum_game = games.Game((2, 2), {(1, 1): 1}, {(1, 1): 1})


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

        assert self.standard_game.r_sticks == standard_sticks
        assert self.standard_game.b_sticks == standard_sticks
        assert self.minimum_game.r_sticks == {(1, 1): 1}
        assert self.minimum_game.b_sticks == {(1, 1): 1}

        assert self.standard_game.red_to_move
        assert self.minimum_game.red_to_move

    def test_move(self):
        self.standard_game.move((0,0), (0,1))
        assert not self.standard_game.board.get_token(0, 0)
        assert not self.standard_game.board.get_token(0, 1)
        assert not self.standard_game.red_to_move
        assert not self.standard_game.r_sticks[(0, 1)]

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move((0,0), (0,1))

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move((2,2), (0,10))

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move((2,2), (4,4))

        self.standard_game.move((2,2), (3,3))

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move((6,6), (6,7))
