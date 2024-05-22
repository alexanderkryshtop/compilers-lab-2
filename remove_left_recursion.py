from grammar import Grammar
from rule import Rule


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