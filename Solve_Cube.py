from Search import breadth_search
from Stage_Tables import tables
import time


# The cube is stored as below:  (Front-Back-Top-Down-Right-Left)
#               FL  FR  BR  BL  FD  FT   BT   BD   TL   TR   DR   DL  FTR BTL FDL BDR  BTR  FTL  BDL  FDR 
solved_cube = ( 0,  2,  4,  6,  8,  10,  12,  14,  16,  18,  20,  22,  0,  3,  6,  9,  12,  15,  18,  21 )

all_moves = [
    (f, d, a) for a in [2,1] for f in ["F","B","R","L","T","D"] for d in [1,-1] if a*d != -2
]

move_orders = {

    "Edges" : {
        "F": [5, 0, 4, 1],
        "B": [6, 2, 7, 3],
        "R": [9, 1, 10, 2],
        "L": [8, 3, 11, 0],
        "T": [6, 8, 5, 9],
        "D": [4, 11, 7, 10]
    },

    "Corners" : {
        "F": [12, 17, 14, 19],
        "B": [13, 16, 15, 18],
        "R": [19, 15, 16, 12],
        "L": [18, 14, 17, 13],
        "T": [13, 17, 12, 16],
        "D": [14, 18, 15, 19]
    }
}


def make_move (current, move_num, no_ori=None):

    face, dir, amt = all_moves[move_num]
    new_cube = list(current)
    for c_type in ["Edges", "Corners"]:
        for x in range(-2, 2):
            a = move_orders[c_type][face][x]
            b = move_orders[c_type][face][x + dir * amt]
            new_cube[b] = current[a]

            if amt == 1 and not no_ori:
                if c_type == "Edges" and face in ["T", "D"]:
                    new_cube[b] += [1,-1][new_cube[b]%2]
                if c_type == "Corners" and face in ["T","D","R","L"]:
                    new_cube[b] += [[1,2],[1,-1],[-2,-1]][new_cube[b]%3][x%2]

    return tuple(new_cube)



def rep (current, stage):

    match stage:

        case 1: return tuple(c%2 for c in current[:12])
        
        case 2: return tuple([c//16 for c in current[:12]] \
                    + [c%3 for c in current[12:]])

        case 3: 
            tetrads = [0]*8
            tetr2 = 0; tetr1 = 0
            for corner in range(12,20):
                corn_val = current[corner]//3
                if corn_val > 3:
                    tetr2 += 1; tetrads[corn_val] = tetr2
                else:
                    tetr1 += 1; tetrads[tetr1] = corn_val
            twist = [tetrads[tetrads[t]+4] for t in range(4)]
            for t in range(1,4):
                twist[t] ^= twist[0]
            return tuple([c//8 for c in current[:12]] + \
                         [c//12 for c in current[12:]] + twist[1:])
        
        case _: return current


solved_stages = [rep(solved_cube, stage) for stage in range(5)]

stage_tables = tables(make_move, rep)

def heuristics (current, stage):

    edges = tuple(list(current[:12]) + [0]*8)
    corners = tuple([0]*12 + list(current[12:20]))

    match stage:
        case 2: 
            return max(
                stage_tables["Middle Slice"][edges].depth,
                stage_tables["Corner Orts"][corners].depth
            )
        case 3: 
            if current in stage_tables["Stage3"]:
                return stage_tables["Stage3"][current].depth
            else:
                return 10
        case 4: 
            return max(
                stage_tables["Edges"][edges].depth,
                stage_tables["Corners"][corners].depth
            )


def solve (current):

    stage_depths = [5, 12, 15, 20, 20]

    solution = []
    for stage, depth in zip(range(5), stage_depths):

        stage_time = time.time()
        stage_cube = current
        for move in solution:
            stage_cube = make_move(stage_cube, move)
        stage_moves = list(range(18 if stage==0 else 22-4*stage))
        stage_rep = lambda cube: rep(cube, stage)

        stage_solution = breadth_search(stage_cube, solved_stages[stage], 
                    stage_moves, make_move, depth, represent = stage_rep,
                    heuristic = None if stage < 2 else lambda c: heuristics(c, stage))
        
        if stage_solution == "No solution found":
            if stage > 0:
                print("No solution found in stage " + str(stage))
                return solution
        else:
            solution += stage_solution

            stage_time = round(time.time()-stage_time, 3)
            print("Stage " + str(stage) + " solved in " + str(stage_time) + " sec")
    
    print("Solution found in " + str(len(solution)) + " moves")
    for num, move in enumerate([all_moves[s] for s in solution]):
        face, dir, amt = move
        print(str(1+num) + ":  " + face + ("2" if amt==2 else "cc" if dir<0 else ""))

    return solution