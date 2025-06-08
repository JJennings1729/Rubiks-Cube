import py5
import numpy as np
from Solve_Cube import solve

all_colors = ("#fc1303", "#fc9d03", "#f5f3f0", "#f5f505", "#0569f5", "#35f505", "#999c98")
f_col, b_col, t_col, d_col, r_col, l_col, blank = all_colors

axes = {
    "F": np.array([0,0,1]),
    "B": np.array([0,0,-1]),
    "T": np.array([0,1,0]),
    "D": np.array([0,-1,0]),
    "R": np.array([1,0,0]),
    "L": np.array([-1,0,0])
}

all_moves = [
    (f, d, a) for a in [2,1] for f in ["F","B","R","L","T","D"] for d in [1,-1] if a*d != -2
]

class Cubie:

    size = 50   # Edge length

    color_solved = lambda x, y, z: [
        0 if z > 0 else 6, 1 if z < 0 else 6, 2 if y > 0 else 6, 
        3 if y < 0 else 6, 4 if x > 0 else 6, 5 if x < 0 else 6
    ]

    def __init__ (self, center, colors):
        self.verts = [center + np.array(face)*0.5 for face in (list(axes.values()) + [np.array([0,0,0])])]
        self.colors = colors 


class Cube:

    num_spins = 30    #  Number of iterations to fully rotate a side
    ang_speed = np.pi / (2 * num_spins)

    def __init__ (self, start_solved):
        self.cubies = [Cubie(np.array([x,y,z]), Cubie.color_solved(x, y, z) if start_solved else [6]*6)
                       for x in range(-1,2) for y in range(-1,2) for z in range(-1,2)]
        self.moves = []
        
    def draw_cube (self):

        if self.moves:
            if self.moves[0][0] == "Solve":
                solution = solve(self.simple_rep())
                if solution:
                    self.moves += [[all_moves[s], Cube.num_spins] for s in solution]
            else:
                face, dir, speed = self.moves[0][0]
                for cubie in self.cubies:
                    if np.round(np.dot(cubie.verts[-1], axes[face])) > 0:
                        ang = Cube.ang_speed * dir * speed
                        for v in range(7):
                            cubie.verts[v] = cubie.verts[v] * np.cos(ang) + \
                                np.cross(axes[face],cubie.verts[v]) * np.sin(ang) \
                                + axes[face] * np.dot(axes[face],cubie.verts[v]) * (1-np.cos(ang))
                self.moves[0][1] -= 1
            if self.moves[0][1] == 0:
                self.moves.pop(0)

        for cubie in self.cubies:
            for face in range(6):
                perp_axes = [cubie.verts[v] for v in range(6) if v//2 != face//2]
                py5.fill(all_colors[cubie.colors[face]])
                py5.begin_shape()
                for v in range(-1, 4):
                    vert = (perp_axes[(v in (1,2))] + perp_axes[2+(v in (0,1))] + cubie.verts[face] \
                            - 2 * cubie.verts[-1]) * Cubie.size
                    py5.vertex(vert[0], vert[1], vert[2])
                py5.end_shape()

        
    def simple_rep (self):

        cubie_order = [[-1,0,1],[1,0,1],[1,0,-1],[-1,0,-1],[0,-1,1],[0,1,1],[0,1,-1],[0,-1,-1],
                       [-1,1,0],[1,1,0],[1,-1,0],[-1,-1,0],[1,1,1],[-1,1,-1],[-1,-1,1],[1,-1,-1],
                       [1,1,-1],[-1,1,1],[-1,-1,-1],[1,-1,1]]  # Order in the solve algorithm
        
        final_rep = []
        cubie_colors = [Cubie.color_solved(c[0],c[1],c[2]) for c in cubie_order]
        for cubie in self.cubies:
            x, y, z = np.round(cubie.verts[-1], 0)
            if [x,y,z] in cubie_order:
                final_rep.append(tuple([
                    cubie_order.index([x, y, z]),  # Current position
                    cubie_colors.index(cubie.colors),  # Home position
                    [0, 2 if (x+y+z) in [1,-3] else 1, 1 if (x+y+z) in [1,-3] else 2][  #  Orientation
                    [col == min(cubie.colors) for col in                    
                    [col for _,col in sorted(zip([tuple(np.abs(np.round(v,1))) 
                                    for v in cubie.verts[:-1]],cubie.colors)) if col < 6]
                    ].index(True)]
                ]))

        rep = lambda index, home: (2 + int(index>11)) * home - (36 if index>11 else 0)
        return tuple([rep(f[0],f[1])+f[2] for f in sorted(final_rep)])


cube = Cube(True)


def setup():
    py5.size(1200, 900, py5.P3D)
    py5.stroke_weight(4)

def draw():
    py5.background(0)
    py5.translate(py5.width/2, py5.height/2)
    py5.rotate_x(py5.mouse_y/200)
    py5.rotate_y(py5.mouse_x/200)
    cube.draw_cube()

def key_pressed():
    commands = ['1','2','3','4','5','6','f','F','b',
                'B','r','R','l','L','t','T','d','D']
    if py5.key in commands:
        chosen_move = all_moves[commands.index(py5.key)]
        cube.moves.append([chosen_move, Cube.num_spins])
    elif py5.key == 's':
        cube.moves.append(["Solve", 0])

py5.run_sketch()