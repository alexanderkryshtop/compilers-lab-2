from grammar import Grammar
from remove_left_recursion import remove_left_recursion
from remove_unreachable_symbols import remove_unreachable_symbols

grammar = Grammar.from_text(
    """
    [A,B,C,D] [a,b,c] A
    A -> A a | a | B
    B -> C b
    C -> B c
    D -> A
    """
)

print(grammar)

grammar_without_left_rec = remove_left_recursion(grammar)
print(grammar_without_left_rec)

grammar_without_unreachable_symbols = remove_unreachable_symbols(grammar)
print(grammar_without_unreachable_symbols)
