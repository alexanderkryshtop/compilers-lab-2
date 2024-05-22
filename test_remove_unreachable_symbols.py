import pytest

from grammar import Grammar
from remove_unreachable_symbols import remove_unreachable_symbols


def test_not_change_grammar():
    grammar_text = """
        [A,B,C] [a,b,c] A
        A -> B a
        B -> C b
        C -> c
    """

    grammar = Grammar.from_text(grammar_text)
    expected_grammar = Grammar.from_text(
        """
        [A,B,C] [a,b,c] A
        A -> B a
        B -> C b
        C -> c
        """
    )
    processed_grammar = remove_unreachable_symbols(grammar)
    assert repr(processed_grammar) == repr(expected_grammar)


def test_remove_symbol():
    grammar_text = """
        [A,B,C,D] [a,b,c] A
        A -> B a
        B -> C b
        C -> c
        D -> A
        """
    expected_grammar_text = """
        [A,B,C] [a,b,c] A
        A -> B a
        B -> C b
        C -> c
        """
    grammar = Grammar.from_text(grammar_text)
    expected_grammar = Grammar.from_text(expected_grammar_text)
    assert repr(remove_unreachable_symbols(grammar)) == repr(expected_grammar)


def test_remove_complex():
    grammar_text = """
        [S,A,B,C,D] [a,b,c] S
        S -> A a
        A -> B
        B -> C b
        C -> c
        D -> S
    """
    expected_grammar_text = """
        [S,A,B,C] [a,b,c] S
        S -> A a
        A -> B
        B -> C b
        C -> c
    """
    grammar = Grammar.from_text(grammar_text)
    expected_grammar = Grammar.from_text(expected_grammar_text)
    assert repr(remove_unreachable_symbols(grammar)) == repr(expected_grammar)


def test_remove_all_unreachable():
    grammar_text = """
        [S,A,B,C] [a] S
        S -> a
        A -> B
        B -> C
        C -> a
    """
    expected_grammar_text = """
        [S] [a] S
        S -> a
    """
    grammar = Grammar.from_text(grammar_text)
    expected_grammar = Grammar.from_text(expected_grammar_text)
    assert repr(remove_unreachable_symbols(grammar)) == repr(expected_grammar)
