class TreeNode:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []
        self.is_epsilon = False

    def add_child(self, child):
        self.children.append(child)


def _is_left_recursive(grammar, non_terminals):
    lr = set()
    for sym, prods in grammar.items():
        for prod in prods:
            if prod and prod[0] == sym:
                lr.add(sym)
    return lr


def parse(symbol, string, pos, grammar, non_terminals, depth=0, _lr_set=None):
    MAX_DEPTH = 200
    if depth > MAX_DEPTH:
        return None, pos

    # --- epsilon ---
    if symbol == 'e':
        node = TreeNode('e')
        node.is_epsilon = True
        return node, pos

    # --- terminal ---
    if symbol not in non_terminals:
        if pos < len(string) and string[pos] == symbol:
            return TreeNode(symbol), pos + 1
        return None, pos

    if symbol not in grammar:
        return None, pos

    # compute LR set once and pass it down
    if _lr_set is None:
        _lr_set = _is_left_recursive(grammar, non_terminals)

    if symbol in _lr_set:
        return _parse_left_recursive(symbol, string, pos, grammar, non_terminals, depth, _lr_set)
    else:
        return _parse_normal(symbol, string, pos, grammar, non_terminals, depth, _lr_set)


def _parse_normal(symbol, string, pos, grammar, non_terminals, depth, _lr_set):
    for production in grammar[symbol]:
        node = TreeNode(symbol)
        current_pos = pos
        success = True
        temp_children = []

        for sym in production:
            child, next_pos = parse(sym, string, current_pos, grammar, non_terminals, depth + 1, _lr_set)
            if child is None:
                success = False
                break
            temp_children.append(child)
            current_pos = next_pos

        if success:
            for child in temp_children:
                node.add_child(child)
            return node, current_pos

    return None, pos


def _parse_left_recursive(symbol, string, pos, grammar, non_terminals, depth, _lr_set):

    base_prods = [p for p in grammar[symbol] if not p or p[0] != symbol]
    rec_prods  = [p for p in grammar[symbol] if p and p[0] == symbol]

    # Step 1: try base cases
    best_tree = None
    best_pos  = pos

    for production in base_prods:
        node = TreeNode(symbol)
        current_pos = pos
        success = True
        temp_children = []

        for sym in production:
            child, next_pos = parse(sym, string, current_pos, grammar, non_terminals, depth + 1, _lr_set)
            if child is None:
                success = False
                break
            temp_children.append(child)
            current_pos = next_pos

        if success:
            for child in temp_children:
                node.add_child(child)
            # keep the base that consumed the most input
            if current_pos > best_pos or best_tree is None:
                best_tree = node
                best_pos  = current_pos

    if best_tree is None:
        return None, pos

    # Step 2: greedily extend with recursive productions
    changed = True
    while changed:
        changed = False
        for production in rec_prods:
            # production[0] == symbol (the LHS), so the "tail" is production[1:]
            tail = production[1:]
            current_pos = best_pos
            success = True
            temp_children = []

            for sym in tail:
                child, next_pos = parse(sym, string, current_pos, grammar, non_terminals, depth + 1, _lr_set)
                if child is None:
                    success = False
                    break
                temp_children.append(child)
                current_pos = next_pos

            if success and current_pos > best_pos:
                new_node = TreeNode(symbol)
                new_node.add_child(best_tree)
                for child in temp_children:
                    new_node.add_child(child)
                best_tree = new_node
                best_pos  = current_pos
                changed   = True
                break  

    return best_tree, best_pos