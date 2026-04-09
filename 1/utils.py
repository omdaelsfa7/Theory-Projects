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
