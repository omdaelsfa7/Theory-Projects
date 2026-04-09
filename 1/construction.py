from NFA import NFA, State

EPSILON = 'ε'


def basic_nfa(symbol):
    """NFA that accepts a single character."""
    start = State()
    end = State()
    start.add_transition(symbol, end)
    return NFA(start, end)


def concat_nfa(nfa1, nfa2):
    """
    Concatenation: nfa1 followed by nfa2.
    Connect end of nfa1 to start of nfa2 via epsilon.
    """
    nfa1.end.add_transition(EPSILON, nfa2.start)
    return NFA(nfa1.start, nfa2.end)


def union_nfa(nfa1, nfa2):
    """
    Union: nfa1 | nfa2.
    New start -> nfa1.start and nfa2.start via epsilon.
    nfa1.end and nfa2.end -> new end via epsilon.
    """
    start = State()
    end = State()

    start.add_transition(EPSILON, nfa1.start)
    start.add_transition(EPSILON, nfa2.start)

    nfa1.end.add_transition(EPSILON, end)
    nfa2.end.add_transition(EPSILON, end)

    return NFA(start, end)


def kleene_star_nfa(nfa):
    """
    Kleene star: nfa*.
    New start -> nfa.start and new end via epsilon.
    nfa.end -> nfa.start and new end via epsilon.
    """
    start = State()
    end = State()

    start.add_transition(EPSILON, nfa.start)
    start.add_transition(EPSILON, end)

    nfa.end.add_transition(EPSILON, nfa.start)
    nfa.end.add_transition(EPSILON, end)

    return NFA(start, end)


def plus_nfa(nfa):
    """
    One or more: nfa+.
    Same as nfa followed by nfa*, i.e., nfa.nfa*
    Implemented as: new start -> nfa.start, nfa.end -> nfa.start and new end.
    """
    start = State()
    end = State()

    start.add_transition(EPSILON, nfa.start)

    nfa.end.add_transition(EPSILON, nfa.start)
    nfa.end.add_transition(EPSILON, end)

    return NFA(start, end)


def build_nfa(postfix):
    """
    Build NFA from postfix regex string using a stack.
    """
    stack = []

    for char in postfix:
        if char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concat_nfa(nfa1, nfa2))
        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union_nfa(nfa1, nfa2))
        elif char == '*':
            nfa = stack.pop()
            stack.append(kleene_star_nfa(nfa))
        elif char == '+':
            nfa = stack.pop()
            stack.append(plus_nfa(nfa))
        else:
            stack.append(basic_nfa(char))

    return stack.pop()
