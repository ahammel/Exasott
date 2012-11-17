"""Interface classes for exasott.games.Game

"""
class GameInterface(object):
    """An interface combining a Game object, functions for choosing red and
    blue moves and a function for dealing with winning conditions into a 
    playable game.

    """
    def __init__(self, game, red_move_getter, blue_move_getter=None,
                 victory_handler=lambda x: None):
        self.game = game
        self.red_move_getter = red_move_getter

        if blue_move_getter:
            self.blue_move_getter = blue_move_getter
        else:
            self.blue_move_getter = red_move_getter

        self.victory_conition = victory_handler
            
    def move_getter(self):
        """Returns the result of the appropriate move_getter, depending on
        whose turn it is to move.

        """
        if self.game.red_to_move:
            return self.red_move_getter(self.game)
        else:
            return self.blue_move_getter(self.game)

    def play(self):
        """Plays the game out using the move_getter method to decide on the
        moves and then deals with the victory condition.

        """
        while not self.game.winner():
            next_move = self.move_getter()
            self.game.move(next_move)
        return self.victory_conition(self.game.winner())
