from regex import parse_regex
from construction import build_nfa
from NFA import State


def extract_nfa(regex):
    """
    Full pipeline: regex string -> NFA object.
    Steps:
      1. Parse regex to postfix
      2. Build NFA using Thompson's Construction
    """
    # Reset state counter for clean IDs each run
    State._id_counter = 0

    postfix = parse_regex(regex)
    nfa = build_nfa(postfix)
    return nfa, postfix
