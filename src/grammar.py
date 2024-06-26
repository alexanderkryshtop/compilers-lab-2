from common import EPSILON
from rule import Rule


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

    def __repr__(self) -> str:
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
        if output:
            output += "\n"
        return output

    @staticmethod
    def from_text(text: str) -> "Grammar":
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
