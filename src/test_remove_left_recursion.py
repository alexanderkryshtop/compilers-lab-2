from grammar import Grammar
from src.remove_left_recursion import remove_left_recursion


def test_remove_left_recursion():
    grammar_text = """
        [A] [a] A
        A -> A a | a
    """
    expected_grammar_text = """
        [A,A'] [a] A
        A -> a | a A'
        A' -> a | a A'
    """
    grammar = Grammar.from_text(grammar_text)
    expected_grammar = Grammar.from_text(expected_grammar_text)
    processed_grammar = remove_left_recursion(grammar)

    assert repr(expected_grammar) == repr(processed_grammar)


def test_indirect_left_recursion():
    grammar_text = """
        [A,B,C] [a,b,c] A
        A -> B a | a
        B -> C b
        C -> A c
    """
    expected_grammar_text = """
        [A,B,C,C'] [a,b,c] A
        A -> B a | a
        B -> C b
        C -> a c | a c C'
        C' -> b a c | b a c C'
    """
    grammar = Grammar.from_text(grammar_text)
    expected_grammar = Grammar.from_text(expected_grammar_text)
    processed_grammar = remove_left_recursion(grammar)

    assert repr(expected_grammar) == repr(processed_grammar)


def test_without_left_recursion():
    grammar_text = """
        [A] [a,b] A
        A -> a b | b a
    """
    expected_grammar_text = """
        [A] [a,b] A
        A -> a b | b a
        """
    grammar = Grammar.from_text(grammar_text)
    expected_grammar = Grammar.from_text(expected_grammar_text)
    processed_grammar = remove_left_recursion(grammar)

    assert repr(expected_grammar) == repr(processed_grammar)


def test_complex():
    grammar_text = """
        [A,B,S] [a,b] S
        A -> A b | B | a
        B -> b
        S -> A | S A
    """
    expected_grammar_text = """
        [A,B,S,A',S'] [a,b] S
        A -> B | B A' | a | a A'
        A' -> b | b A'
        B -> b
        S -> B A' | B A' S' | a | a A' | a A' S' | a S' | b | b S'
        S' -> A | A S'
    """
    grammar = Grammar.from_text(grammar_text)
    expected_grammar = Grammar.from_text(expected_grammar_text)
    processed_grammar = remove_left_recursion(grammar)

    assert repr(expected_grammar) == repr(processed_grammar)
