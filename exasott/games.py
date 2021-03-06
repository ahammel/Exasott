"""Exasott game classes.

"""
from itertools import combinations
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

    def sticks_to_move(self):
        """Returns the set of sticks of the player who has the move.

        """
        if self.red_to_move:
            return self.r_sticks
        else:
            return self.b_sticks

    def remove_stick(self, stick):
        """Removes the stick from the set of the sticks of the player who has
        the move.

        """
        stick_set = self.sticks_to_move()

        if not stick in stick_set or stick_set[stick] < 1:
            raise IllegalMoveError("No stick to make move " + str(stick))
        else:
            stick_set[stick] -= 1

    def move(self, move_tuple):
        """Makes a move, removing two tokens from the board, raising an illegal
        move error if the player to move doesn't have the appropriate stick. 
        Move_tuple is a tuple of two pairs of coordinates.

        """
        token_1, token_2 = move_tuple
        stick = find_stick(token_1, token_2)
        self.remove_stick(stick)

        t1x, t1y = token_1
        t2x, t2y = token_2

        try:
            t1_exists = self.board.get_token(t1x, t1y)
            t2_exists = self.board.get_token(t2x, t2y)
        except boards.BoardRangeError as range_message:
            raise IllegalMoveError(range_message)

        if t1_exists and t2_exists:
            self.board.remove_token(t1x, t1y)
            self.board.remove_token(t2x, t2y)
        else:
            raise IllegalMoveError(str(token_1) + str(token_2))

        self.red_to_move ^= True

    def legal_moves(self):
        """Returns a generator of all the legal moves remaining on the board.

        """
        tokens = [x for x in self.board.board if self.board.board[x]]
        all_moves = combinations(tokens, 2)
        return ((x, y) for x, y in all_moves
                if find_stick(x, y) in self.sticks_to_move())

    def winner(self):
        """Returns "red" if the first player has won the game, "blue" if the
        second player has won the game, or None if the game is ongoing.
        There are no draws in Exasott.

        """
        try:
            next(self.legal_moves())
        except StopIteration:
            if self.red_to_move:
                return "blue"
            else:
                return "red"

    def is_legal_move(self, move):
        """Returns true if the supplied move is legal.
        
        """
        try:
            required_stick = find_stick(move[0], move[1])
        except ValueError:
            return False
        else:
            return required_stick in self.sticks_to_move()


def find_stick(token_1, token_2):
    """Returns the stick needed to make a move from token_1 to token_2.

    """
    t1x, t1y = token_1
    t2x, t2y = token_2

    x_dist = abs(t1x - t2x)
    y_dist = abs(t1y - t2y)
    return (min(x_dist, y_dist), max(x_dist, y_dist))
