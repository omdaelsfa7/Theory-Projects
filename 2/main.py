from grammar import read_grammar
from parser import parse
from display import get_derivation_steps, print_derivation, print_tree

def main():
    grammar, non_terminals, start_symbol = read_grammar()
    if not grammar: return

    while True:
        print("-" * 50)
        input_str = input("Enter string to parse (or 'exit'): ").strip()
        if input_str.lower() == 'exit': break
        
        tree, end_pos = parse(start_symbol, input_str, 0, grammar, non_terminals)

        if tree is not None and end_pos == len(input_str):
            print(f'Result: "{input_str}" --> ACCEPTED')
            steps = get_derivation_steps(tree)
            print_derivation(steps)
            print_tree(tree)
        else:
            print(f'Result: "{input_str}" --> REJECTED')

        print("-" * 50)
        if input("Try another string? (y/n): ").lower() != 'y': break

if __name__ == "__main__":
    main()