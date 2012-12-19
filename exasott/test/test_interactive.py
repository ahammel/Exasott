import pytest
from exasott import interactive

class TestInteractiveFunctions(object):
    """Unit tests for the interactive game utility functions.

    """
    def test_alpha_move(self):
        """ alpha_move should take an alphanumeric string and convert it to an
        exasott move without bothering too much about case or spaces. Should
        raise an InvalidMove error when the move isn't parsable.
        
        """
        assert interactive.alpha_move("A1A2") == ((0, 0), (0, 1))
        assert interactive.alpha_move("b6  c2  ") == ((1, 5), (2, 1))
        assert interactive.alpha_move("c10d11") == ((2, 9), (3, 10)) 

        with pytest.raises(interactive.InvalidMove):
            print(interactive.alpha_move("banana"))

        with pytest.raises(interactive.InvalidMove):
            interactive.alpha_move("1234")

        with pytest.raises(interactive.InvalidMove):
            interactive.alpha_move("ab1c2")

        with pytest.raises(interactive.InvalidMove):
            interactive.alpha_move("banana1orange2")
