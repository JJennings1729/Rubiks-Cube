from Search import breadth_search

def tables (make_move, rep):

    solved_cube     = ( 0, 2, 4, 6, 8,10,12,14,16,18,20,22, 0, 3, 6, 9,12,15,18,21)
    blank           = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    middle_slice    = ( 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)
    edges           = ( 0, 2, 4, 6, 8,10,12,14,16,18,20,22, 0, 0, 0, 0, 0, 0, 0, 0)
    corners         = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 9,12,15,18,21)

    no_ori = lambda c, m: make_move(c, m, True)  # Make move without modifying orientations
    rep3 = lambda c: rep(c, 3)

    return {
        "Middle Slice": breadth_search(middle_slice, None, list(range(14)), no_ori, 20, return_table=True),
        "Corner Orts": breadth_search(blank, None, list(range(14)), make_move, 20, return_table=True),
        "Stage3": breadth_search(solved_cube, None, list(range(10)), make_move, 6, return_table=True, represent=rep3),
        "Edges": breadth_search(edges, None, list(range(6)), make_move, 20, return_table=True),
        "Corners": breadth_search(corners, None, list(range(6)), make_move, 20, return_table=True)
    }