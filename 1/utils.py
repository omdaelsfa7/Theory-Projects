def get_all_symbols(nfa):
    """Return all non-epsilon symbols used in the NFA."""
    symbols = set()
    states = nfa.get_all_states_objects()
    for state in states.values():
        for symbol in state.transitions:
            if symbol != 'ε':
                symbols.add(symbol)
    return sorted(symbols)


def print_nfa_info(nfa):
    """Print NFA details: start, end, and all transitions."""
    print(f"  Start State : S{nfa.start.id}")
    print(f"  End State   : S{nfa.end.id}")
    print(f"  Transitions :")
    transitions = nfa.get_transitions()
    transitions.sort(key=lambda t: (t[0].id, t[1], t[2].id))
    for (frm, sym, to) in transitions:
        print(f"    S{frm.id} --[{sym}]--> S{to.id}")

def print_formal_nfa(nfa):
    print("\nM = (Q, Σ, δ, q0, F)\n")

    # Get all states (objects)
    states_dict = nfa.get_all_states_objects()
    states = list(states_dict.values())

    # Q
    Q = {str(state) for state in states}
    print("Q =", Q)

    # Σ (alphabet excluding epsilon)
    alphabet = set()
    for state in states:
        for symbol in state.transitions:
            if symbol != 'ε':
                alphabet.add(symbol)
    print("Σ =", alphabet)

    # δ
    print("\nδ:")
    for state in states:
        for symbol, targets in state.transitions.items():
            for t in targets:
                print(f"({state}, {symbol}) → {{{t}}}")

    # q0
    print("\nq0 =", nfa.start)

    # F (single accept state)
    print("F =", {str(nfa.end)})

def print_transition_table(nfa):
    print("\nTransition Function δ (Table Form):\n")

    states_dict = nfa.get_all_states_objects()
    states = list(states_dict.values())

    # Collect alphabet (including ε)
    symbols = set()
    for state in states:
        for symbol in state.transitions:
            symbols.add(symbol)

    symbols = sorted(symbols)  # clean order
    states = sorted(states, key=lambda s: s.id)

    # Header
    header = ["State"] + symbols
    print("\t".join(header))

    # Rows
    for state in states:
        row = [str(state)]
        for symbol in symbols:
            if symbol in state.transitions:
                targets = ",".join(str(t) for t in state.transitions[symbol])
                row.append("{" + targets + "}")
            else:
                row.append("∅")
        print("\t".join(row))