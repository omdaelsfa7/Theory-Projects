def print_derivation(steps):
    print("\nDerivation:")
    unique_steps = []
    for s in steps:
        filtered = [sym for sym in s if sym != 'e']
        joined = " ".join(filtered)
        if not unique_steps or joined != unique_steps[-1]:
            unique_steps.append(joined)
    print("  " + " => ".join(unique_steps))


def get_derivation_steps(tree):
    steps = []
    current_nodes = [tree]
    steps.append([node.symbol for node in current_nodes])
    while True:
        expand_idx = -1
        for i, node in enumerate(current_nodes):
            if node.children:
                expand_idx = i
                break
        if expand_idx == -1:
            break
        target_node = current_nodes.pop(expand_idx)
        for j, child in enumerate(target_node.children):
            current_nodes.insert(expand_idx + j, child)
        steps.append([node.symbol for node in current_nodes])
        if len(steps) > 100:
            break
    return steps


# ─── Visual Tree Renderer ────────────────────────────────────────────────────

class _Block:
    """Represents a subtree's rendered block: a 2-D grid of characters."""

    def __init__(self, lines, root_col):
        self.lines = lines          # list[str], all same width
        self.width = len(lines[0]) if lines else 0
        self.root_col = root_col    # column index of the node's centre

    @staticmethod
    def _pad(lines, width):
        return [l.ljust(width) for l in lines]


def _box(symbol):
    """Return the lines that draw ( symbol ) with a border."""
    inner = f" {symbol} "
    top    = "┌" + "─" * len(inner) + "┐"
    mid    = "│" + inner             + "│"
    bot    = "└" + "─" * len(inner) + "┘"
    return [top, mid, bot]          # height = 3


def _build_block(node):
    """Recursively build a _Block for `node`."""
    if node.is_epsilon:
        # epsilon shown as a visible ε leaf
        box_lines = _box("ε")
        mid_col   = len(box_lines[0]) // 2
        return _Block(box_lines, mid_col)

    visible_children = node.children  # include epsilon children so they render

    # ── Leaf node ──────────────────────────────────────────────────────────
    if not visible_children:
        box_lines = _box(node.symbol)
        mid_col   = len(box_lines[0]) // 2
        return _Block(box_lines, mid_col)

    # ── Build child blocks ─────────────────────────────────────────────────
    H_GAP = 2          # horizontal space between sibling boxes
    child_blocks = [_build_block(c) for c in visible_children]

    # Total width needed to lay children side-by-side
    total_child_width = (
        sum(b.width for b in child_blocks)
        + H_GAP * (len(child_blocks) - 1)
    )

    # Our box
    my_box      = _box(node.symbol)
    my_box_w    = len(my_box[0])

    # Ensure we are at least as wide as our children
    canvas_width = max(my_box_w, total_child_width)

    # ── Position children on canvas ────────────────────────────────────────
    # Centre the group of children horizontally
    children_start_x = (canvas_width - total_child_width) // 2

    child_x = []      # left-edge x of each child block
    cx = children_start_x
    for b in child_blocks:
        child_x.append(cx)
        cx += b.width + H_GAP

    child_centres = [child_x[i] + child_blocks[i].root_col
                     for i in range(len(child_blocks))]

    # Centre our own box
    my_box_x = (canvas_width - my_box_w) // 2
    my_root_col = my_box_x + my_box_w // 2

    # ── Draw connector lines ───────────────────────────────────────────────
    # We draw 3 rows of connectors:
    #   row 0: vertical stub down from parent centre  (│)
    #   row 1: horizontal bar + T/L-pieces            (├─…─┤ etc.)
    #   row 2: vertical stubs up to each child        (│)
    def blank(w):
        return list(" " * w)

    row0 = blank(canvas_width)
    row1 = blank(canvas_width)
    row2 = blank(canvas_width)

    # vertical stub down from parent
    row0[my_root_col] = "│"

    if len(child_centres) == 1:
        # single child → straight line
        cc = child_centres[0]
        lo, hi = sorted([my_root_col, cc])
        for col in range(lo, hi + 1):
            row1[col] = "─"
        row1[my_root_col] = "│"
        row1[cc]           = "│"
        row2[cc]           = "│"
    else:
        lo = min(child_centres)
        hi = max(child_centres)
        for col in range(lo, hi + 1):
            row1[col] = "─"
        for cc in child_centres:
            row1[cc] = "┬"
            row2[cc] = "│"
        row1[lo] = "┌" if child_centres[0] != my_root_col else "┬"
        row1[hi] = "┐" if child_centres[-1] != my_root_col else "┬"
        # parent connection
        if lo <= my_root_col <= hi:
            row1[my_root_col] = "┼" if row1[my_root_col] == "┬" else "┬"
        row0[my_root_col] = "│"

    connector_lines = [
        "".join(row0),
        "".join(row1),
        "".join(row2),
    ]

    # ── Merge child blocks side-by-side ────────────────────────────────────
    max_child_height = max(len(b.lines) for b in child_blocks)
    # Pad all child blocks to same height (bottom-pad)
    padded = []
    for b in child_blocks:
        extra = max_child_height - len(b.lines)
        lines = b.lines + [" " * b.width] * extra
        padded.append(lines)

    child_row_lines = []
    for row in range(max_child_height):
        pieces = []
        for i, lines in enumerate(padded):
            pieces.append(lines[row] if row < len(lines) else " " * child_blocks[i].width)
            if i < len(padded) - 1:
                pieces.append(" " * H_GAP)
        child_row_lines.append("".join(pieces))

    # Pad child area to canvas_width
    child_row_lines = [l.ljust(canvas_width) for l in child_row_lines]

    # Place our box on the canvas (top row)
    box_lines_on_canvas = []
    for bl in my_box:
        row = list(" " * canvas_width)
        for idx, ch in enumerate(bl):
            row[my_box_x + idx] = ch
        box_lines_on_canvas.append("".join(row))

    all_lines = (
        box_lines_on_canvas   # 3 lines: top border, label, bottom border
        + connector_lines     # 3 lines: stubs + horizontal bar
        + child_row_lines     # child subtrees
    )

    # Normalise width
    final_width = max(len(l) for l in all_lines)
    all_lines = [l.ljust(final_width) for l in all_lines]

    return _Block(all_lines, my_root_col)


def print_tree(root):
    print("\nParse Tree:")
    block = _build_block(root)
    for line in block.lines:
        print("  " + line.rstrip())
    print()