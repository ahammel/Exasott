"""Unit tests for the exasot.games module.

"""
from exasott import games, test
import pytest


class GameTestSetup(object):
    """Shared variables for all of the exasott.games unit tests.

    """
    standard_game = games.Game()
    minimum_game = games.Game((2, 2), {(1, 1): 1}, {(1, 1): 1})
    six_game = games.Game((3, 2), {(1, 1): 3}, {(1, 1): 3})
    standard_sticks = {(0, 1): 1, (1, 1): 5, (1, 2): 5, (1, 3): 5}


class TestGameMethods(GameTestSetup):
    """Unit tests for the exasott.games.Game class.

    """
    def test_init(self):
        """Game() should instantiate an 8x8 game with standard sticks with no
        arguments, or a custom game if the dimensions of the board and the
        sticks are supplied.

        """
        std_board = self.standard_game.board
        assert std_board.rows == 8
        assert std_board.columns == 8
        for i in range(8):
            for j in range(8):
                assert std_board.get_token(i, j) == 1

        min_board = self.minimum_game.board
        assert min_board.rows == 2
        assert min_board.columns == 2
        for i in range(2):
            for j in range(2):
                assert min_board.get_token(i, j) == 1

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

    def test_str(self):
        """Game.__str__ should return the Board.__str__, plus an additional
        two lines specifying who is to move and what sticks remain. This
        is all the information required to determine the state of the game.

        """
        assert str(self.standard_game) == test.NORMAL_BOARD_STR + \
                                         ("\n"
                                         "*Red  {01: 1, 11: 5, 12: 5, 13: 5}\n"
                                         " Blue {01: 1, 11: 5, 12: 5, 13: 5}")

        self.minimum_game.move(((0, 0), (1, 1)))

        assert str(self.minimum_game) == (" AB\n"
                                          "1XO\n"
                                          "2OX\n"
                                          "\n"
                                          " Red  {}\n"
                                          "*Blue {11: 1}")

    def test_move(self):
        """A move should remove the tokens and the stick in question, throwing
        IllegalMoveErrors if either of the tokens is missing, if the move is
        outside the range of the board, or if the stick to make the move is
        unavailable. The player to move should then be toggled.

        """
        self.standard_game.move(((0, 0), (0, 1)))
        assert not self.standard_game.board.get_token(0, 0)
        assert not self.standard_game.board.get_token(0, 1)
        assert not self.standard_game.red_to_move
        assert not self.standard_game.r_sticks[(0, 1)]
        assert self.standard_game.b_sticks == self.standard_sticks

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move(((0, 0), (0, 1)))

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move(((2, 2), (0, 10)))

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move(((2, 2), (4, 4)))

        self.standard_game.move(((2, 2), (3, 3)))

        with pytest.raises(games.IllegalMoveError):
            self.standard_game.move(((6, 6), (6, 7)))

    def test_legal_moves(self):
        """Game.legal_moves() should return a generator consisting of all the
        legal moves in the present game state.

        """
        assert list(self.minimum_game.legal_moves()) == [((0, 1), (1, 0))]

        assert set(self.six_game.legal_moves()) == set([((0, 0), (1, 1)),
                                                        ((0, 1), (1, 0)),
                                                        ((1, 0), (2, 1)),
                                                        ((2, 0), (1, 1))])

    def test_winner(self):
        """The game is won when there are no legal moves remaining. Therefore,
        game.test_winner() should return None if there are legal moves
        available, "blue" if there are no legal moves with red to move, or 
        "red" if there are no legal moves with blue to move.

        """
        assert self.standard_game.winner() == None
        assert self.six_game.winner() == None
        assert self.minimum_game.winner() == None

        self.minimum_game.move(((0, 1), (1, 0)))

        assert self.minimum_game.winner() == "blue"
