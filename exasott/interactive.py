""" Play a game of Exasott interactively in the shell.

"""
import string
import re
import sys
import os
from exasott.game_interface import GameInterface
from exasott.games import Game


TOKEN_LETTERS = dict(zip(string.ascii_uppercase, range(26)))
TOKEN_NUMBERS = dict(zip((str(i) for i in range(1, 27)), range(26)))


class InvalidMove(ValueError):
    """The exception raised when alpha_move is fed a string it can't translate
    into an exasott move
    
    """


def alpha_move(move_string):
    """Converts an alphanumeric string into an exasott move.
    
    """
    token_string = re.sub(r'\s', '', move_string).upper() # strip whitespace
                                                          # and make upper
    if not re.match(r"^([a-zA-Z]\d+){2}$", token_string):
        raise InvalidMove(move_string)

    raw_tokens = re.findall(r'([a-zA-Z])(\d+)', token_string)
    try:
        tokens = [(TOKEN_LETTERS[a], TOKEN_NUMBERS[b]) for a, b in raw_tokens]
    except KeyError:
        raise InvalidMove(token_string)

    return tuple(tokens)


def print_game_term(game):
    """Clears the screen and prints the game."""
    os.system('clos' if os.name == 'nt' else 'clear')
    print(game)


def shell_move_getter(game):
    """The function which gets moves from the console. It accomplishes this by 
    clearing the screen, grabbing the move from stdin (filtering it to make 
    sure it's legal) and then passing the move to the game.    

    """
    print_game_term(game)

    move = None
    while not move:
        try:
            raw_move = input("Enter a move: ")
            move = alpha_move(raw_move)
        except InvalidMove:
            print_game_term(game)    
            print("Invalid move")

        if not game.is_legal_move(move):
            print_game_term(game)
            print("Illegal move")
            move = None

    return move


def shell_victory_handler(game):
    """Prints a simple victory message to stdout.
    
    """
    winner = game.winner()
    print(game)
    print(winner[0].upper(), winner[1:], " wins!")


def main():
    """Play a game of exasott in the shell.
    
    """
    game = GameInterface(Game(), shell_move_getter,
                         victory_handler = shell_victory_handler)
    game.play()


if __name__ == '__main__':
    main()
