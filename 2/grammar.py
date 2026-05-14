def read_grammar():
    grammar = {}
    non_terminals = set()

    print("=" * 50)
    print("           CFG PARSER (CSCI419)")
    print("=" * 50)
    print("\nInput Format:")
    print("  - Separate symbols with spaces: S -> a S b")
    print("  - Use '|' for alternatives")
    print("  - Use 'e' for epsilon (will be hidden in output)\n")

    try:
        n = int(input("Number of productions: "))
    except ValueError:
        return None, None, None

    start_symbol = None
    for i in range(n):
        line = input(f"Production {i + 1}: ").strip()
        if "->" not in line: return None, None, None

        left, right = [part.strip() for part in line.split("->")]
        if start_symbol is None: start_symbol = left
        non_terminals.add(left)
        
        alternatives = right.split("|")
        for alt in alternatives:
            symbols = alt.strip().split()
            if symbols:
                if left not in grammar: grammar[left] = []
                grammar[left].append(symbols)

    return grammar, non_terminals, start_symbol