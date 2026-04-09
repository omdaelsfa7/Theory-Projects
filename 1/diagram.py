from NFA import State

EPSILON = 'ε'

CELL_W = 12
CELL_H = 5


def assign_positions(nfa):
    positions = {}
    visited = set()
    queue = [(nfa.start, 0, 0)]
    col_row_used = {}
    row_counter = {}

    while queue:
        state, col, row = queue.pop(0)
        if state.id in visited:
            continue
        visited.add(state.id)

        while (col, row) in col_row_used:
            row += 1

        positions[state.id] = (col, row)
        col_row_used[(col, row)] = state.id
        row_counter[col] = row + 1

        next_col = col + 1
        next_row = row_counter.get(next_col, 0)

        for symbol, targets in state.transitions.items():
            for t in targets:
                if t.id not in visited:
                    queue.append((t, next_col, next_row))
                    next_row += 1

    return positions


def draw_diagram(nfa):
    positions = assign_positions(nfa)
    transitions = nfa.get_transitions()

    if not positions:
        print("  (empty NFA)")
        return

    max_col = max(c for (c, r) in positions.values())
    max_row = max(r for (c, r) in positions.values())

    grid_w = (max_col + 1) * (CELL_W + 4) + 4
    grid_h = (max_row + 1) * (CELL_H + 2) + 4

    grid = [[' ' for _ in range(grid_w)] for _ in range(grid_h)]

    def cell_origin(col, row):
        x = col * (CELL_W + 4) + 4
        y = row * (CELL_H + 2) + 2
        return x, y

    def set_char(x, y, ch):
        if 0 <= y < grid_h and 0 <= x < grid_w:
            grid[y][x] = ch

    def draw_box(col, row, label, is_start, is_end):
        x, y = cell_origin(col, row)
        w = CELL_W
        h = CELL_H

        for i in range(w):
            grid[y][x + i] = '-'
            grid[y + h - 1][x + i] = '-'
        for j in range(h):
            grid[y + j][x] = '|'
            grid[y + j][x + w - 1] = '|'
        grid[y][x] = '+'
        grid[y][x + w - 1] = '+'
        grid[y + h - 1][x] = '+'
        grid[y + h - 1][x + w - 1] = '+'

        mid_y = y + h // 2
        text = label
        start_x = x + (w - len(text)) // 2
        for k, ch in enumerate(text):
            if 0 <= start_x + k < grid_w:
                grid[mid_y][start_x + k] = ch

        if is_start:
            arr = '->'
            ax = x - len(arr)
            for k, ch in enumerate(arr):
                if ax + k >= 0:
                    grid[mid_y][ax + k] = ch

        if is_end:
            grid[y + 1][x + w - 2] = '*'

    def draw_horizontal_arrow(x1, y, x2, label):
        forward = x1 < x2
        if forward:
            for x in range(x1, x2):
                set_char(x, y, '-')
            set_char(x2, y, '>')
        else:
            set_char(x2, y, '<')
            for x in range(x2 + 1, x1 + 1):
                set_char(x, y, '-')

        mid_x = (x1 + x2) // 2 - len(label) // 2
        label_y = y - 1 if forward else y + 1
        for k, ch in enumerate(label):
            set_char(mid_x + k, label_y, ch)

    def draw_vertical_arrow(x, y1, y2, label):
        if y1 < y2:
            for y in range(y1, y2):
                set_char(x, y, '|')
            set_char(x, y2, 'v')
        else:
            set_char(x, y2, '^')
            for y in range(y2 + 1, y1 + 1):
                set_char(x, y, '|')

        mid_y = (y1 + y2) // 2
        for k, ch in enumerate(label):
            set_char(x + 1 + k, mid_y, ch)

    state_objects = nfa.get_all_states_objects()
    for sid, (col, row) in positions.items():
        state = state_objects[sid]
        is_start = (sid == nfa.start.id)
        is_end = (sid == nfa.end.id)
        draw_box(col, row, f"S{sid}", is_start, is_end)

    for (frm, sym, to) in transitions:
        if frm.id not in positions or to.id not in positions:
            continue

        col1, row1 = positions[frm.id]
        col2, row2 = positions[to.id]

        x1, y1 = cell_origin(col1, row1)
        x2, y2 = cell_origin(col2, row2)

        mid_y1 = y1 + CELL_H // 2
        mid_y2 = y2 + CELL_H // 2
        mid_x1 = x1 + CELL_W // 2
        mid_x2 = x2 + CELL_W // 2

        label = f"({sym})"

        if row1 == row2 and col1 != col2:
            if col1 < col2:
                ax1 = x1 + CELL_W - 1
                ax2 = x2
            else:
                ax1 = x1
                ax2 = x2 + CELL_W - 1
            draw_horizontal_arrow(ax1, mid_y1, ax2, label)

        elif col1 == col2 and row1 != row2:
            if row1 < row2:
                ay1 = y1 + CELL_H - 1
                ay2 = y2
            else:
                ay1 = y1
                ay2 = y2 + CELL_H - 1
            draw_vertical_arrow(mid_x1, ay1, ay2, label)

        else:
            if col1 < col2:
                ax1 = x1 + CELL_W - 1
                ax2 = x2
            else:
                ax1 = x1
                ax2 = x2 + CELL_W - 1

            bend_x = (ax1 + ax2) // 2

            if ax1 <= bend_x:
                for x in range(ax1, bend_x + 1):
                    set_char(x, mid_y1, '-')
            else:
                for x in range(bend_x, ax1 + 1):
                    set_char(x, mid_y1, '-')

            if mid_y1 < mid_y2:
                for y in range(mid_y1, mid_y2 + 1):
                    set_char(bend_x, y, '|')
                set_char(bend_x, mid_y2, 'v')
            else:
                for y in range(mid_y2, mid_y1 + 1):
                    set_char(bend_x, y, '|')
                set_char(bend_x, mid_y2, '^')

            if bend_x < ax2:
                for x in range(bend_x, ax2 + 1):
                    set_char(x, mid_y2, '-')
                set_char(ax2, mid_y2, '>')
            else:
                for x in range(ax2, bend_x + 1):
                    set_char(x, mid_y2, '-')
                set_char(ax2, mid_y2, '<')

            lx = ax1 - len(label) - 1 if ax1 > bend_x else ax1 + 1
            for k, ch in enumerate(label):
                set_char(lx + k, mid_y1 - 1, ch)

    print()
    for row in grid:
        print(''.join(row).rstrip())
    print()