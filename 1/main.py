from thompson_extraction import extract_nfa
from diagram import draw_diagram
from utils import print_nfa_info ,print_formal_nfa ,print_transition_table


def main():
    print("=" * 50)
    print("      Regex to NFA Converter")
    print("      Using Thompson's Construction")
    print("=" * 50)
    print("  Supported operators:")
    print("    |   -> Union")
    print("    *   -> Kleene Star (zero or more)")
    print("    +   -> One or more")
    print("    ()  -> Grouping")
    print("    Concatenation is implicit")
    print("=" * 50)

    while True:
        print()
        regex = input("  Enter regex (or 'q' to quit): ").replace(" ", "")

        if regex.lower() == 'q':
            print("\n  Goodbye!\n")
            break

        if not regex:
            print("  [!] Empty input. Please enter a valid regex.")
            continue

        try:
            nfa, postfix = extract_nfa(regex)

            print(f"\n  Postfix form : {postfix}")
            print()
            print_nfa_info(nfa)
            print()
            print("  NFA Diagram:")
            print("-" * 60)
            draw_diagram(nfa)
            print("-" * 60)
            print("  NFA FD:")
            print_formal_nfa(nfa)
            print_transition_table(nfa)
            print("-" * 60)
        except Exception as e:
            print(f"\n  [!] Error: {e}")
            print("  Please check your regex and try again.")


if __name__ == "__main__":
    main()