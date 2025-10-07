def compute_first(grammar):
    FIRST = {}
    terminals = set()
    non_terminals = set(grammar.keys())

    for non_term, productions in grammar.items():
        FIRST[non_term] = set()
        for production in productions:
            for symbol in production:
                if symbol not in non_terminals and symbol != '#':
                    terminals.add(symbol)

    for terminal in terminals:
        FIRST[terminal] = {terminal}
    FIRST['#'] = {'#'}

    changed = True
    while changed:
        changed = False
        for non_term, productions in grammar.items():
            for production in productions:
                can_derive_epsilon = True
                for symbol in production:
                    current_first = FIRST.get(symbol, {symbol})
                    new_symbols = current_first - {'#'}
                    if new_symbols - FIRST[non_term]:
                        FIRST[non_term].update(new_symbols)
                        changed = True

                    if '#' in current_first:
                        can_derive_epsilon = True
                    else:
                        can_derive_epsilon = False
                        break

                if can_derive_epsilon and '#' not in FIRST[non_term]:
                    FIRST[non_term].add('#')
                    changed = True

    return FIRST

def compute_follow(grammar, FIRST, start_symbol):
    non_terminals = set(grammar.keys())
    FOLLOW = {non_term: set() for non_term in non_terminals}

    if start_symbol in FOLLOW:
        FOLLOW[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for non_term_A, productions in grammar.items():
            for production in productions:
                for i, symbol_B in enumerate(production):
                    if symbol_B in non_terminals:
                        alpha = production[i+1:]
                        if not alpha:
                            new_symbols = FOLLOW[non_term_A]
                            if new_symbols - FOLLOW[symbol_B]:
                                FOLLOW[symbol_B].update(new_symbols)
                                changed = True
                        else:
                            first_of_alpha = set()
                            can_derive_epsilon_in_alpha = True
                            for symbol_Y in alpha:
                                symbol_first = FIRST.get(symbol_Y, {symbol_Y})
                                new_symbols = symbol_first - {'#'}
                                if new_symbols - first_of_alpha:
                                    first_of_alpha.update(new_symbols)

                                if '#' in symbol_first:
                                    can_derive_epsilon_in_alpha = True
                                else:
                                    can_derive_epsilon_in_alpha = False
                                    break

                            if first_of_alpha - FOLLOW[symbol_B]:
                                FOLLOW[symbol_B].update(first_of_alpha)
                                changed = True

                            if can_derive_epsilon_in_alpha:
                                new_symbols = FOLLOW[non_term_A]
                                if new_symbols - FOLLOW[symbol_B]:
                                    FOLLOW[symbol_B].update(new_symbols)
                                    changed = True

    return FOLLOW

def get_user_grammar():
    print("Enter the productions (type 'end' at the last of the production)")
    print("Format: E->TA|+T|# (Use '#' for epsilon, '|' for alternatives)")

    grammar = {}
    start_symbol = None

    while True:
        line = input()
        if line.lower() == 'end':
            break

        if '->' not in line:
            print("Invalid format. Use 'NonTerminal->Production'.")
            continue

        try:
            non_term, production_str = line.split('->', 1)
            non_term = non_term.strip()

            if start_symbol is None:
                start_symbol = non_term

            productions = [p.strip() for p in production_str.split('|')]

            parsed_productions = []
            for prod in productions:
                if prod == '#':
                    parsed_productions.append(['#'])
                else:
                    parsed_productions.append(list(prod))

            if non_term in grammar:
                grammar[non_term].extend(parsed_productions)
            else:
                grammar[non_term] = parsed_productions

        except Exception as e:
            print(f"Error parsing line: {line}. Skipping.")

    return grammar, start_symbol

def main():
    grammar, start_symbol = get_user_grammar()

    if not grammar:
        print("\nNo productions entered. Exiting.")
        return

    print("\n--- Parsed Grammar Productions ---")
    for nt, prods in grammar.items():
        prod_strs = [''.join(p) for p in prods]
        print(f"{nt} -> {' | '.join(prod_strs)}")
    print("-" * 34)

    FIRST = compute_first(grammar)

    print("--- Calculated FIRST Sets ---")
    for nt in sorted(grammar.keys()):
        print(f"FIRST({nt}): {sorted(list(FIRST[nt]))}")
    print("-" * 34)

    FOLLOW = compute_follow(grammar, FIRST, start_symbol)

    print("--- Calculated FOLLOW Sets ---")
    for nt in sorted(grammar.keys()):
        print(f"FOLLOW({nt}): {sorted(list(FOLLOW[nt]))}")
    print("-" * 34)

if __name__ == "__main__":
    main()
