"""Exasott game classes.

"""
from exasott import boards


class IllegalMoveError(ValueError):
    """The exception raised when attempting to make an illegal move.

    """


class Game(object):
    """A game of Exasott.

    """
    def __init__(self, dimensions=(8, 8), red_sticks=None, blue_sticks=None):
        self.board = boards.Board(dimensions[0], dimensions[1])

        if not red_sticks:
            self.r_sticks = {(0, 1): 1, (1, 1): 5, (1, 2): 5, (1, 3): 5}
        else:
            self.r_sticks = red_sticks

        if not blue_sticks:
            self.b_sticks = {(0, 1): 1, (1, 1): 5, (1, 2): 5, (1, 3): 5}
        else:
            self.b_sticks = blue_sticks

        self.red_to_move = True

    def __str__(self):
        board_str = str(self.board)

        r_sticks_left = [str(x) + str(y) + ": " + str(self.r_sticks[(x, y)])
                         for x, y in sorted(self.r_sticks)
                         if self.r_sticks[(x, y)]]

        b_sticks_left = [str(x) + str(y) + ": " + str(self.b_sticks[(x, y)])
                         for x, y in sorted(self.b_sticks)
                         if self.b_sticks[(x, y)]]

        if self.red_to_move:
            red_string = "*Red  {"
            blue_string = " Blue {"
        else:
            red_string = " Red  {"
            blue_string = "*Blue {"

        red_string += ", ".join(r_sticks_left) + "}"
        blue_string += ", ".join(b_sticks_left) + "}"

        return '\n'.join([board_str, red_string, blue_string])

    def remove_stick(self, stick):
        if self.red_to_move:
            stick_set = self.r_sticks
        else:
            stick_set = self.b_sticks

        if not stick in stick_set or stick_set[stick] < 1:
            raise IllegalMoveError("No stick to make move " + str(stick))
        else:
            stick_set[stick] -= 1

    def move(self, token_1, token_2):
        t1x, t1y = token_1
        t2x, t2y = token_2

        x_dist = abs(t1x - t2x)
        y_dist = abs(t1y - t2y)
        stick = (min(x_dist, y_dist), max(x_dist, y_dist))

        self.remove_stick(stick)

        try:
            t1_exists = self.board.get_token(t1x, t1y)
            t2_exists = self.board.get_token(t2x, t2y)
        except boards.BoardRangeError as r:
            raise IllegalMoveError(r)

        if t1_exists and t2_exists:
            self.board.remove_token(t1x, t1y)
            self.board.remove_token(t2x, t2y)
        else:
            raise IllegalMoveError(str((t1x, t1y))+str((t2x, t2y)))

        self.red_to_move ^= True
