"""Unit tests for the game_interface module.

"""
from exasott.games import Game
from exasott.game_interface import GameInterface


class TestGameInterface(object):
    """Unit tests for the GameInterface object.

    """
    game = Game((2, 2), {(1, 1): 1})
    
    def mock_red_move_getter(self, game):
        return ((0, 0), (1, 1))

    def mock_blue_move_getter(self, game):
        return ((1, 0), (0, 1))

    def mock_win_handler(self, winner):
        return winner[::-1]

    def test_game_interface(self):
        """ The mock interfaces and win conditions should result in a trivial 
        win for blue. The mock_move_getter then returns the name of the winner 
        reversed.

        """
        interface = GameInterface(self.game, self.mock_red_move_getter,
                                  self.mock_blue_move_getter,
                                  self.mock_win_handler)

        assert interface.play() == "eulb"
