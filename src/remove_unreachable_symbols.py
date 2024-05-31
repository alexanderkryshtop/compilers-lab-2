from grammar import Grammar


def remove_unreachable_symbols(g: Grammar):
    queue = [g.start_symbol]
    non_terminals = [g.start_symbol]

    new_rules = []
    new_terms = []

    while len(queue):
        current_non_terminal = queue.pop(0)
        for rule in filter(lambda x: x.left == current_non_terminal, g.rules):
            new_rules.append(rule)
            for symbol in rule.right:
                if symbol in g.non_terms and symbol not in non_terminals:
                    non_terminals.append(symbol)
                    queue.append(symbol)
                if symbol in g.terms:
                    new_terms.append(symbol)

    return Grammar(non_terminals, list(dict.fromkeys(new_terms)), new_rules, g.start_symbol)
