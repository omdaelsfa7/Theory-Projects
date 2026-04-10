EPSILON = 'ε'

CELL_W  = 12
CELL_H  = 5
COL_GAP = 8
ROW_GAP = 4


def assign_positions(nfa):
    positions = {}
    visited   = set()
    queue     = [(nfa.start, 0, 0)]
    used      = {}
    row_next  = {}
    while queue:
        state, col, row = queue.pop(0)
        if state.id in visited:
            continue
        visited.add(state.id)
        while (col, row) in used:
            row += 1
        positions[state.id] = (col, row)
        used[(col, row)] = state.id
        row_next[col] = row + 1
        nc = col + 1
        nr = row_next.get(nc, 0)
        for sym, targets in state.transitions.items():
            for t in targets:
                if t.id not in visited:
                    queue.append((t, nc, nr))
                    nr += 1
    return positions


def _ox(col):           return col * (CELL_W + COL_GAP) + 4
def _oy(row, tm):       return tm + row * (CELL_H + ROW_GAP)
def _mid_x(col):        return _ox(col) + CELL_W // 2
def _right_out(col):    return _ox(col) + CELL_W
def _left_wall(col):    return _ox(col)
def _top_wall(row, tm): return _oy(row, tm)
def _mid_y(row, tm):    return _oy(row, tm) + CELL_H // 2


def draw_diagram(nfa):
    positions   = assign_positions(nfa)
    transitions = nfa.get_transitions()

    if not positions:
        print("  (empty NFA)")
        return

    backward = [(f, s, t) for (f, s, t) in transitions
                if f.id in positions and t.id in positions
                and positions[t.id][0] < positions[f.id][0]]
    backward.sort(key=lambda x: positions[x[0].id][0] - positions[x[2].id][0],
                  reverse=True)

    num_lanes  = len(backward)
    top_margin = max(4, num_lanes * 2 + 3)

    max_col = max(c for (c, r) in positions.values())
    max_row = max(r for (c, r) in positions.values())

    grid_w = (max_col + 1) * (CELL_W + COL_GAP) + 12
    grid_h = top_margin + (max_row + 1) * (CELL_H + ROW_GAP) + 4

    grid = [[' '] * grid_w for _ in range(grid_h)]

    def sc(x, y, ch):
        if 0 <= y < grid_h and 0 <= x < grid_w:
            grid[y][x] = ch

    def ss(x, y, s):
        for k, ch in enumerate(s):
            sc(x + k, y, ch)

    def hline(x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            sc(x, y, '-')

    def vline(x, y1, y2):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            sc(x, y, '|')

    # Draw boxes
    state_objects = nfa.get_all_states_objects()
    for sid, (col, row) in positions.items():
        x = _ox(col);  y = _oy(row, top_margin)
        w, h = CELL_W, CELL_H
        for i in range(w):
            sc(x+i, y, '-');     sc(x+i, y+h-1, '-')
        for j in range(h):
            sc(x, y+j, '|');     sc(x+w-1, y+j, '|')
        sc(x, y, '+');       sc(x+w-1, y, '+')
        sc(x, y+h-1, '+');   sc(x+w-1, y+h-1, '+')
        lbl = f"S{sid}"
        for k, ch in enumerate(lbl):
            sc(x + (w-len(lbl))//2 + k, y+h//2, ch)
        if sid == nfa.start.id:
            sc(x-2, y+h//2, '-');  sc(x-1, y+h//2, '>')
        if sid == nfa.end.id:
            sc(x+w-2, y+1, '*')

    # Forward transitions
    forward = [(f, s, t) for (f, s, t) in transitions
               if f.id in positions and t.id in positions
               and positions[t.id][0] >= positions[f.id][0]]

    for (frm, sym, to) in forward:
        c1, r1 = positions[frm.id];  c2, r2 = positions[to.id]
        label  = f"({sym})"
        my1 = _mid_y(r1, top_margin);  my2 = _mid_y(r2, top_margin)

        if c1 == c2:
            x   = _mid_x(c1)
            y_s = _oy(r1, top_margin) + CELL_H
            y_e = _top_wall(r2, top_margin) - 1
            vline(x, y_s, y_e);  sc(x, y_e, 'v')
            ss(x+1, (y_s+y_e)//2, label)
        elif r1 == r2:
            x_s = _right_out(c1);  x_e = _left_wall(c2) - 1
            hline(x_s, x_e, my1);  sc(x_e, my1, '>')
            ss((x_s+x_e)//2 - len(label)//2, my1-1, label)
        else:
            vx  = _right_out(c1) + COL_GAP // 2
            x_s = _right_out(c1);  x_e = _left_wall(c2) - 1
            hline(x_s, vx, my1)
            vline(vx, min(my1, my2), max(my1, my2))
            hline(vx, x_e, my2);  sc(x_e, my2, '>')
            ss(x_s+1, my1-1, label)

    # Backward transitions — above diagram, no box contact
    for lane_idx, (frm, sym, to) in enumerate(backward):
        c1, r1 = positions[frm.id];  c2, r2 = positions[to.id]
        label  = f"({sym})"

        lane_y  = top_margin - 2 - lane_idx
        vx_src  = _right_out(c1) + 2 + lane_idx * 2
        vx_dst  = _left_wall(c2) - 2 - lane_idx * 2
        src_top = _top_wall(r1, top_margin)
        dst_top = _top_wall(r2, top_margin)
        dst_mid = _mid_y(r2, top_margin)

        vline(vx_src, lane_y + 1, src_top - 1)
        hline(vx_dst, vx_src, lane_y)
        vline(vx_dst, lane_y + 1, dst_top - 1)
        vline(vx_dst, dst_top - 1, dst_mid)
        hline(vx_dst + 1, _left_wall(c2) - 1, dst_mid)
        sc(_left_wall(c2) - 1, dst_mid, '>')

        lx = (vx_dst + vx_src) // 2 - len(label) // 2
        ss(lx, lane_y - 1, label)

    print()
    for row in grid:
        print(''.join(row).rstrip())
    print()