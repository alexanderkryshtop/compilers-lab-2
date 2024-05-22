EPSILON = "ε"


class Rule:
    def __init__(self, left: str, right: list[str]):
        self.left = left.strip()
        self.right = [elem.strip() for elem in right]

    def __repr__(self):
        right_str = " ".join(self.right) or EPSILON
        return f"{self.left} -> {right_str}"


class Grammar:
    non_terms = []
    terms = []
    rules = []
    start_symbol = ''

    def __init__(
        self,
        non_terms: list[str],
        terms: list[str],
        rules: list[Rule],
        start_symbol: str
    ):
        self.non_terms = non_terms
        self.terms = terms
        self.rules = rules
        self.start_symbol = start_symbol

    def print(self):
        output = ""
        output += f"Non-terminals = {self.non_terms}\nTerminals = {self.terms}\nStart symbol = {self.start_symbol}\n"

        for non_term in sorted(self.non_terms):
            rules = [rule for rule in self.rules if rule.left == non_term]

            if not len(rules):
                continue

            rule_strs = [
                " ".join(rule.right) if rule.right else EPSILON
                for rule in rules
            ]
            sorted_rule_strs = sorted(rule_strs)
            joined_rules = " | ".join(sorted_rule_strs)
            output += '\n' + f"{non_term} -> {joined_rules}"
        print(output)

    @staticmethod
    def parse_grammar(text: str):
        text = text.strip()

        header, *body = text.split("\n")
        non_term_str, terminal_str, start_symbol = header.split(" ")
        non_terms = non_term_str[1:-1].split(",")
        terminals = terminal_str[1:-1].split(",")

        rules = []

        for rule_str in body:
            if not rule_str:
                continue

            left, right = rule_str.split(' -> ')
            rule_variants = right.split(" | ")

            for variant in rule_variants:
                right_symbols = variant.split(' ')
                if right_symbols[0] == EPSILON:
                    right_symbols = []
                rules.append(Rule(left, right_symbols))
        return Grammar(non_terms, terminals, rules, start_symbol)


def remove_left_recursion(grammar: Grammar):
    new_rules: list[Rule] = grammar.rules.copy()
    non_terminals = grammar.non_terms.copy()

    for i, current_non_terminal in enumerate(grammar.non_terms):
        for previous_non_terminal in grammar.non_terms[:i]:
            left_recursive_rules = filter(
                lambda r: r.left == current_non_terminal and r.right and r.right[0] == previous_non_terminal, new_rules
            )

            for rule in left_recursive_rules:
                new_rules.remove(rule)
                previous_rules = filter(lambda r: r.left == previous_non_terminal, new_rules)

                for previous_rule in previous_rules:
                    new_rules.append(Rule(current_non_terminal, previous_rule.right + rule.right[1:]))

        current_rules = list(filter(lambda r: r.left == current_non_terminal, new_rules))
        has_immediate_left_recursion = any(
            rule.right and rule.right[0] == current_non_terminal for rule in current_rules
        )

        if has_immediate_left_recursion:
            new_non_terminal = current_non_terminal + "'"
            non_terminals.append(new_non_terminal)

            for rule in current_rules:
                new_rules.remove(rule)

                if rule.right and rule.right[0] == current_non_terminal:
                    new_rules += [
                        Rule(new_non_terminal, rule.right[1:]),
                        Rule(new_non_terminal, rule.right[1:] + [new_non_terminal])
                    ]
                else:
                    new_rules += [
                        Rule(rule.left, rule.right.copy()),
                        Rule(rule.left, rule.right + [new_non_terminal])
                    ]

    return Grammar(non_terminals, grammar.terms.copy(), new_rules, grammar.start_symbol)


grammar = Grammar.parse_grammar(
    """
    [A,B,C,D] [a,b,c] A
    A -> A a | a | B
    B -> C b
    C -> B c
    D -> A
    """
)
# display(grammar.show())
# grammar = Grammar.parse_grammar(
#     """
#     [A,B,C,S] [a,b,c] S
#     A -> a A | ε
#     B -> b B | ε
#     C -> c C | ε
#     S -> A B C
#     """
# )
# display(grammar.show())
grammar.print()

print()

g2 = remove_left_recursion(grammar)
g2.print()
