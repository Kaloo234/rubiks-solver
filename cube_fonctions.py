import numpy as np
import tkinter as tk
import time, random

import refs
import cases
import cases_CFOP
import user_data

import traceback

def set_visual(cube, root):
    if not root:
        return
    for widget in root.winfo_children():
        widget.destroy()
    
    y=0
    for line in cube[0]:
        x=3
        for tile in line:
            frame = tk.Frame(root, background=refs.COLORS[tile], width=30, height=30)
            frame.grid(column=x,row=y)
            x += 1
        y +=1
        
    for side_index in range(len(cube)):
        y=3
        if side_index != 0 and side_index != 5:
            for line in cube[side_index]:
                x = (side_index - 1) * 3
                for tile in line:
                    frame = tk.Frame(root, background=refs.COLORS[tile], width=30, height=30)
                    frame.grid(column=x,row=y)
                    x += 1
                y += 1
    
    y=6
    for line in cube[5]:
        x=3
        for tile in line:
            frame = tk.Frame(root, background=refs.COLORS[tile], width=30, height=30)
            frame.grid(column=x,row=y)
            x += 1
        y +=1
    root.update_idletasks()
    root.update()
    time.sleep(0)

def print_cube(cube):
    print("")
    for i in cube[0]:
        print("      ", i)
        
    print(cube[1][0],cube[2][0],cube[3][0],cube[4][0], sep="")
    print(cube[1][1],cube[2][1],cube[3][1],cube[4][1], sep="")
    print(cube[1][2],cube[2][2],cube[3][2],cube[4][2], sep="")

    for i in cube[5]:
        print("      ", i)

def get_side_arrays(cube, face_id):
    up_col_id = None
    down_col_id = None
    row_id = None
    if face_id == 1 or face_id == 2 or face_id == 3 or face_id == 4:
        left = get_array_from_column(cube, face_id, "l")
        right = get_array_from_column(cube, face_id, "r")
        
        if face_id == 2:
            up_col_id = 2
            down_col_id = 0
            
            up = np.array(cube[refs.SIDES[face_id]["u"]][up_col_id])
            down = np.array(cube[refs.SIDES[face_id]["d"]][down_col_id])
            
        elif face_id == 4:
            up_col_id = 0
            down_col_id = 2
            
            up = np.array(cube[refs.SIDES[face_id]["u"]][up_col_id])
            down = np.array(cube[refs.SIDES[face_id]["d"]][down_col_id])

        elif face_id == 1:
            up = get_array_from_column(cube, face_id, "u")
            down = get_array_from_column(cube, face_id, "d")

        elif face_id == 3:
            up = get_array_from_column(cube, face_id, "u")
            down = get_array_from_column(cube, face_id, "d")

    elif face_id == 0 or face_id == 5:
        if face_id == 0:
            row_id = 0
        elif face_id == 5:
            row_id = 2
            
        left = np.array(cube[refs.SIDES[face_id]["l"]][row_id])
        right = np.array(cube[refs.SIDES[face_id]["r"]][row_id])
        up = np.array(cube[refs.SIDES[face_id]["u"]][row_id])
        down = np.array(cube[refs.SIDES[face_id]["d"]][row_id])

    return left, right, up, down, up_col_id, down_col_id, row_id

def rotate_face_clockwise(cube, face_id, update_callback=None, sid=None, cube_states=None):
    left, right, up, down, up_col_id, down_col_id, row_id = get_side_arrays(cube, face_id)
    
    cube[face_id] = np.rot90(cube[face_id], k=3)

    # flip the sides if needed
    if face_id == 4:
        left = left[::-1]
        right = right[::-1]
        up = up[::-1]
        down = down[::-1]
    elif face_id == 1:
        right = right[::-1]
        up = up[::-1]
    elif face_id == 3:
        left = left[::-1]
        down = down[::-1]

    if face_id == 1 or face_id == 2 or face_id == 3 or face_id == 4:
        #left
        set_column_from_array(cube, face_id, "l", down)
        #right
        set_column_from_array(cube, face_id, "r", up)
        
    elif face_id == 0 or face_id == 5:
        #left
        cube[refs.SIDES[face_id]["l"]][row_id] = down
        #right
        cube[refs.SIDES[face_id]["r"]][row_id] = up
        #up
        cube[refs.SIDES[face_id]["u"]][row_id] = left
        #down
        cube[refs.SIDES[face_id]["d"]][row_id] = right

    if face_id == 2 or face_id == 4:
        #up
        cube[refs.SIDES[face_id]["u"]][up_col_id] = left
        #down
        cube[refs.SIDES[face_id]["d"]][down_col_id] = right
        
    elif face_id == 1 or face_id == 3:
        #up
        set_column_from_array(cube, face_id, "u", left)
        #down
        set_column_from_array(cube, face_id, "d", right)

    if update_callback:
        update_callback(sid)
        time.sleep(0.01)
    if cube_states:
        #print(user_data.cube_states)
        user_data.cube_states[sid].append(cube.tolist())
        
def rotate_face_counterclockwise(cube, face_id, update_callback=None, sid=None, cube_states=None):
    left, right, up, down, up_col_id, down_col_id, row_id = get_side_arrays(cube, face_id)
    
    cube[face_id] = np.rot90(cube[face_id], k=1)

    # flip the sides if needed
    if face_id == 1:
        right = right[::-1]
        down = down[::-1]
    elif face_id == 2:
        left = left[::-1]
        right = right[::-1]
        up = up[::-1]
        down = down[::-1]
    elif face_id == 3:
        left = left[::-1]
        up = up[::-1]

    if face_id == 1 or face_id == 2 or face_id == 3 or face_id == 4:
        #left
        set_column_from_array(cube, face_id, "l", up)
        #right
        set_column_from_array(cube, face_id, "r", down)
        
    elif face_id == 0 or face_id == 5:
        #left
        cube[refs.SIDES[face_id]["l"]][row_id] = up
        #right
        cube[refs.SIDES[face_id]["r"]][row_id] = down
        #up
        cube[refs.SIDES[face_id]["u"]][row_id] = right
        #down
        cube[refs.SIDES[face_id]["d"]][row_id] = left

    if face_id == 2 or face_id == 4:
        #up
        cube[refs.SIDES[face_id]["u"]][up_col_id] = right
        #down
        cube[refs.SIDES[face_id]["d"]][down_col_id] = left
        
    elif face_id == 1 or face_id == 3:
        #up
        set_column_from_array(cube, face_id, "u", right)
        #down
        set_column_from_array(cube, face_id, "d", left)

    if update_callback:
        update_callback(sid)
        time.sleep(0.01)
    if cube_states:
        user_data.cube_states[sid].append(cube.tolist())

def rotate_middle_x(cube, direction, update_callback=None, sid=None, cube_states=None):
    front = get_array_from_middle_column(cube, 2)
    up = get_array_from_middle_column(cube, 0)
    back = get_array_from_middle_column(cube, 4)
    down = get_array_from_middle_column(cube, 5)

    if direction == "c":
        set_middle_column_from_array(cube, 5, front)
        set_middle_column_from_array(cube, 4, down[::-1])
        set_middle_column_from_array(cube, 0, back[::-1])
        set_middle_column_from_array(cube, 2, up)
    elif direction == "a":
        set_middle_column_from_array(cube, 0, front)
        set_middle_column_from_array(cube, 4, up[::-1])
        set_middle_column_from_array(cube, 5, back[::-1])
        set_middle_column_from_array(cube, 2, down)

    if update_callback:
        update_callback(sid)
        time.sleep(0.01)
    if cube_states:
        user_data.cube_states[sid].append(cube.tolist())

def rotate_middle_y(cube, direction, update_callback=None, sid=None, cube_states=None):
    front = np.array(cube[2][1])
    left = np.array(cube[1][1])
    back = np.array(cube[4][1])
    right = np.array(cube[3][1])

    if direction == "c":
        cube[3][1] = front
        cube[4][1] = right
        cube[1][1] = back
        cube[2][1] = left
    elif direction == "a":
        cube[1][1] = front
        cube[4][1] = left
        cube[3][1] = back
        cube[2][1] = right

    if update_callback:
        update_callback(sid)
        time.sleep(0.01)
    if cube_states:
        user_data.cube_states[sid].append(cube.tolist())

def rotate_middle_z(cube, direction, update_callback=None, sid=None, cube_states=None):
    up = np.array(cube[0][1])
    right = get_array_from_middle_column(cube, 3)
    down = np.array(cube[5][1])
    left = get_array_from_middle_column(cube, 1)

    if direction == "c":
        set_middle_column_from_array(cube, 3, up)
        cube[5][1] = right[::-1]
        set_middle_column_from_array(cube, 1, down)
        cube[0][1] = left[::-1]
    elif direction == "a":
        set_middle_column_from_array(cube, 1, up[::-1])
        cube[5][1] = left
        set_middle_column_from_array(cube, 3, down[::-1])
        cube[0][1] = right

    if update_callback:
        update_callback(sid)
        time.sleep(0.01)
    if cube_states:
        user_data.cube_states[sid].append(cube.tolist())

def get_col_id_from_side(face_id, side):
    if side == "l":
        col_id = 2
    elif side == "r":
        col_id = 0
    elif side == "u" or side == "d":
        if face_id == 1:
            col_id = 0
        elif face_id == 3:
            col_id = 2
        
    return col_id

def get_array_from_column(cube, face_id, side):
    col_id = get_col_id_from_side(face_id, side)
    
    return np.array([cube[refs.SIDES[face_id][side]][2][col_id],
                     cube[refs.SIDES[face_id][side]][1][col_id],
                     cube[refs.SIDES[face_id][side]][0][col_id]])

def get_array_from_middle_column(cube, face_id):
    return np.array([cube[face_id][0][1],
                     cube[face_id][1][1],
                     cube[face_id][2][1]])

def set_column_from_array(cube, face_id, side, array):
    col_id = get_col_id_from_side(face_id, side)

    cube[refs.SIDES[face_id][side]][0][col_id] = array[0]
    cube[refs.SIDES[face_id][side]][1][col_id] = array[1]
    cube[refs.SIDES[face_id][side]][2][col_id] = array[2]

def set_middle_column_from_array(cube, face_id, array):
    cube[face_id][0][1] = array[0]
    cube[face_id][1][1] = array[1]
    cube[face_id][2][1] = array[2]



def run_algo(cube, algo, root=None, update_callback=None, sid=None, cube_states=None, append_moves=None):
    if type(algo) == str:
        if algo == "":
            return
        #algo = algo.upper()
        moves_list = algo.split(" ")
    elif type(algo) == list:
        moves_list = algo
    else:
        print("")
        print(f"Algorythme invalide, (type={type(algo)})")
        print(algo)
        print("")
        return
    #print(moves_list)
    for move in moves_list:
        if append_moves:
            append_moves(move, sid)

        #print(move)
        set_visual(cube, root)
        
        move = refs.MOVES[move]
        for step in move:
            if step[0] == "tc":
                rotate_face_clockwise(cube, step[1], update_callback, sid=sid, cube_states=cube_states)
            elif step[0] == "ta":
                rotate_face_counterclockwise(cube, step[1], update_callback, sid=sid, cube_states=cube_states)
            elif step[0] == "tmx":
                rotate_middle_x(cube, step[1], update_callback, sid=sid, cube_states=cube_states)
            elif step[0] == "tmy":
                rotate_middle_y(cube, step[1], update_callback, sid=sid, cube_states=cube_states)
            elif step[0] == "tmz":
                rotate_middle_z(cube, step[1], update_callback, sid=sid, cube_states=cube_states)
        #time.sleep(0.01)
        #breakpoint()
    return cube

def get_random_algo(n):
    nb_moves = 18
    moves_list = []
    moves = list(refs.MOVES.keys())
    while n > 0:
        new_move = moves[random.randint(0,nb_moves-1)]
        moves_list.append(new_move)
        n -= 1
    print("        Scramble :", ' '.join(moves_list))
    return moves_list

# solving logic
def solve_cube(cube, root=None, update_callback=None, sid=None, cube_states=None, append_moves=None):
    print("Solving...")
    solve_white_cross(cube, root, update_callback, sid, cube_states, append_moves)

    #solve_white_corners(cube, root, update_callback, append_moves)

    #solve_middle_layer(cube, root, update_callback, append_moves)
    #breakpoint()
    solve_F2L(cube, root, update_callback, sid, cube_states, append_moves)

    #solve_yellow_cross(cube, root, update_callback, cube_states, append_moves)

    #solve_yellow_face(cube, root, update_callback, cube_states, append_moves)

    solve_OLL(cube, root, update_callback, sid, cube_states, append_moves)

    #solve_yellow_face_sides(cube, root, update_callback, sid, cube_states, append_moves)

    solve_PLL(cube, root, update_callback, sid, cube_states, append_moves)

    set_visual(cube, root)
    print("Solved!")

def find_algo_white_cross(cube, side_color):
    for possibility in cases.WHITE_CROSS:
        conditions = cases.WHITE_CROSS[possibility]["conditions"]
        if cube[conditions[0][0]][conditions[0][1]][conditions[0][2]] == 2:
            if cube[conditions[1][0]][conditions[1][1]][conditions[1][2]] == side_color:
                return cases.WHITE_CROSS[possibility]["algo"]
    print("White cross error")
    breakpoint()

def find_algo_white_corner(cube, up_side_color, rt_side_color):
    for possibility in cases.WHITE_CORNERS:
        conditions = cases.WHITE_CORNERS[possibility]["conditions"]
        if cube[conditions[0][0]][conditions[0][1]][conditions[0][2]] == 2:
            if (cube[conditions[1][0]][conditions[1][1]][conditions[1][2]] == up_side_color and
                cube[conditions[2][0]][conditions[2][1]][conditions[2][2]] == rt_side_color):
                return cases.WHITE_CORNERS[possibility]["algo"]
    print("White corner error")
    breakpoint()

def find_algo_middle_layer(cube, up_side_color, rt_side_color):
    for possibility in cases.MIDDLE_LAYER:
        conditions = cases.MIDDLE_LAYER[possibility]["conditions"]
        if cube[conditions[0][0]][conditions[0][1]][conditions[0][2]] == up_side_color:
            if cube[conditions[1][0]][conditions[1][1]][conditions[1][2]] == rt_side_color:
                return cases.MIDDLE_LAYER[possibility]["algo"]
    print("Middle layer error")
    breakpoint()

def find_algo_yellow_cross(cube):
    yellow_pos = []
    for line in range(3):
        for value in range(3):
            if ((line,value) != (0,0) and
                (line,value) != (0,2) and
                (line,value) != (2,0) and
                (line,value) != (2,2) and
                (line,value) != (1,1)):
                
                if cube[4][line][value] == 4:
                    yellow_pos.append((4,line,value))

    for possibility in cases.YELLOW_CROSS:
        conditions = cases.YELLOW_CROSS[possibility]["conditions"]
        if conditions == yellow_pos:
            return cases.YELLOW_CROSS[possibility]["algo"]
    print("Yellow cross error")
    breakpoint()

def find_algo_yellow_face(cube):
    yellow_pos = []
    for side in [0, 1, 3, 5]:
        for line in range(3):
            for value in range(3):
                if cube[side][line][value] == 4:
                    yellow_pos.append((side, line, value))

    for possibility in cases.YELLOW_FACE:
        conditions = cases.YELLOW_FACE[possibility]["conditions"]
        if conditions == yellow_pos:
            return cases.YELLOW_FACE[possibility]["algo"], cases.YELLOW_FACE[possibility]["algo_id"]
    print("Yellow face error")
    breakpoint()

def find_algo_yellow_sides(cube):
    pairs_and_sides = [[],[]]
    for side in [0,1,3,5]:
        if side == 0:
            if cube[side][0][0] == cube[side][0][1] == cube[side][0][2]:
                pairs_and_sides[1].append(side)
            elif cube[side][0][0] == cube[side][0][2] != cube[side][0][1]:
                pairs_and_sides[0].append(side)
        elif side == 1:
            if cube[side][0][0] == cube[side][1][0] == cube[side][2][0]:
                pairs_and_sides[1].append(side)
            elif cube[side][0][0] == cube[side][2][0] != cube[side][1][0]:
                pairs_and_sides[0].append(side)
        elif side == 3:
            if cube[side][0][2] == cube[side][1][2] == cube[side][2][2]:
                pairs_and_sides[1].append(side)
            elif cube[side][0][2] == cube[side][2][2] != cube[side][1][2]:
                pairs_and_sides[0].append(side)
        elif side == 5:
            if cube[side][2][0] == cube[side][2][1] == cube[side][2][2]:
                pairs_and_sides[1].append(side)
            elif cube[side][2][0] == cube[side][2][2] != cube[side][2][1]:
                pairs_and_sides[0].append(side)

    for possibility in cases.YELLOW_FACE_SIDES:
        conditions = cases.YELLOW_FACE_SIDES[possibility]["conditions"]
        if conditions == pairs_and_sides:
            return cases.YELLOW_FACE_SIDES[possibility]["algo"], cases.YELLOW_FACE_SIDES[possibility]["algo_id"]
    print("Yellow face sides error")
    breakpoint()
    
def solve_white_cross(cube, root, update_callback=None, sid=None, cube_states=None, append_moves=None):
    for side in [0,1,5,3]:
        algo = find_algo_white_cross(cube, side)
        run_algo(cube, algo, root, update_callback, sid, cube_states, append_moves)
        run_algo(cube, "F", root, update_callback, sid, cube_states, append_moves)

def solve_white_corners(cube, root, update_callback=None, sid=None, append_moves=None):
    sides = [0,1,5,3]
    for side in range(len(sides)):
        run_algo(cube, find_algo_white_corner(cube, sides[side], sides[side-1]), root, update_callback, sid, append_moves)
        run_algo(cube, "F", root, update_callback, sid, append_moves)

def solve_middle_layer(cube, root, update_callback=None, sid=None, append_moves=None):
    sides = [0,1,5,3]
    for side in range(len(sides)):
        run_algo(cube, find_algo_middle_layer(cube, sides[side], sides[side-1]), root, update_callback, sid, append_moves)
        run_algo(cube, "S", root, update_callback, sid, append_moves)

def solve_yellow_cross(cube, root, update_callback=None, sid=None, cube_states=None, append_moves=None):
    while (cube[4][0][1] != 4 or
           not np.array_equal(cube[4][1], np.array([4,4,4])) or
           cube[4][2][1] != 4):
        run_algo(cube, find_algo_yellow_cross(cube), root, update_callback, sid, cube_states, append_moves)
        run_algo(cube, "U R B R' B' U'", root, update_callback, sid, cube_states, append_moves)

def solve_yellow_face(cube, root, update_callback=None, sid=None, cube_states=None, append_moves=None):
    while not np.array_equal(cube[4], np.array([[4,4,4],[4,4,4],[4,4,4]])):
        algo, algo_id = find_algo_yellow_face(cube)
        run_algo(cube, algo, root, update_callback, sid, cube_states, append_moves)
        if algo_id == 0:
            run_algo(cube, "R B R' B R B2 R'", root, update_callback, sid, cube_states, append_moves)
        elif algo_id == 1:
            run_algo(cube, "B2 R B2 R' B' R B' R'", root, update_callback, sid, cube_states, append_moves)

def solve_yellow_face_sides(cube, root, update_callback=None, sid=None, cube_states=None, append_moves=None):
    while (not cube[0][0][0] == cube[0][0][1] == cube[0][0][2] or
           not cube[1][0][0] == cube[1][1][0] == cube[1][2][0] or
           not cube[3][0][2] == cube[3][1][2] == cube[3][2][2] or
           not cube[5][2][0] == cube[5][2][1] == cube[5][2][2]):
        algo, algo_id = find_algo_yellow_sides(cube)
        run_algo(cube, algo, root, update_callback, sid, cube_states, append_moves)
        if algo_id == 0:
            run_algo(cube, "R' U R' D2 R U' R' D2 R2", root, update_callback, sid, cube_states, append_moves)
        elif algo_id == 1:
            run_algo(cube, "R B' R B R B R B' R' B' R2", root, update_callback, sid, cube_states, append_moves)

    if cube[0][0][1] == 1:
        run_algo(cube, "B", root, update_callback, sid, cube_states, append_moves)
    elif cube[0][0][1] == 5:
        run_algo(cube, "B2", root, update_callback, sid, cube_states, append_moves)
    elif cube[0][0][1] == 3:
        run_algo(cube, "B'", root, update_callback, sid, cube_states, append_moves)

def list_to_array(_list):
    return np.array(_list)

def reduce_move_list_lenght(moves_list):
    simplified = []
    
    for move in moves_list:
        if simplified and simplified[-1] == refs.OPPOSITE_MOVE[move]:
            simplified.pop()  # Annule les mouvements inverses
        elif len(simplified) > 1 and simplified[-2:] == [move, move]:
            simplified[-2:] = [move + "2"]  # Fusionne trois mouvements identiques
        elif simplified and simplified[-1] == move + "2":
            simplified.pop()  # Supprime `X2, X2` (car équivalent à rien)
        elif simplified and simplified[-1] == move:
            simplified[-1] = move + "2"  # Fusionne `X, X` en `X2`
        else:
            simplified.append(move)

    return simplified

def combine_moves(m1, m2):
    """Combine deux mouvements de la même face"""
    base = m1[0]  # La face du mouvement (ex: 'F', 'L', 'B'...)
    moves = {base: 0, base + "2": 2, base + "'": 3}

    count = (moves.get(m1, 1) + moves.get(m2, 1)) % 4  # Somme des rotations modulo 4

    for key, value in moves.items():
        if value == count:
            return key if key != base else None  # Retourne None si le mouvement est annulé

    return None

def shorten_moves_list(moves_list):
    liste = moves_list.copy()
    no_modif = False
    while no_modif == False:
        no_modif = True
        for i in range(len(liste)):
            try:
                if liste[i] == liste[i+1] == liste[i+2] == liste[i+3]:
                    no_modif = False
                    liste.pop(i+3)
                    liste.pop(i+2)
                    liste.pop(i+1)
                    liste.pop(i)
                elif liste[i] == liste[i+1] == liste[i+2]:
                    no_modif = False
                    liste.pop(i+2)
                    liste.pop(i+1)
                    if len(liste[i]) == 1:
                        liste[i] += "'"
                    elif len(liste[i]) == 2:
                        if liste[i][1] == "'":
                            liste[i] = liste[i][0]
                elif liste[i] == liste[i+1]:
                    no_modif = False
                    liste.pop(i+1)
                    if len(liste[i]) == 1:
                        liste[i] += "2"
                    elif len(liste[i]) == 2:
                        if liste[i][0] == "'":
                            liste[i] = liste[i][0] + "2"
                        elif liste[i][0] == "2":
                            liste.pop(i)
                elif liste[i] == get_opposite_move(liste[i+1]):
                    no_modif = False
                    liste.pop(i+1)
                    liste.pop(i)
                elif liste[i][0] == liste[i+1][0]:
                    no_modif = False
                    if len(liste[i]) == 1 and len(liste[i+1]) == 2:
                        if liste[i+1][1] == "2":
                            liste.pop(i+1)
                            liste[i] += "'"
                    elif len(liste[i]) == 2 and len(liste[i+1]) == 1:
                        if liste[i][1] == "2":
                            liste.pop(i+1)
                            lst = list(liste.copy()[i])
                            lst[1] = "'"
                            liste[i] = "".join(lst)
                    elif len(liste[i]) == 2 and len(liste[i+1]) == 2:
                        if ((liste[i][1] == "'" and liste[i+1][1] == "2") or
                            (liste[i][1] == "2" and liste[i+1][1] == "'")):
                            liste.pop(i+1)
                            lst = list(liste.copy()[i])
                            lst[1] = ""
                            liste[i] = "".join(lst)
                else:
                    replacement = is_in_cancel_move(liste[i], liste[i+1])
                    if replacement:
                        liste.pop(i+1)
                        liste[i] = replacement
                        
            except IndexError:
                print("end of moves list")
                break
            except Exception:
                print("erreur produite")
                traceback.print_exc()
    #print("------------------------  liste",liste)
    return liste

def is_in_cancel_move(move, move_plus_1):
    for possibility in refs.CANCEL_MOVES:
        canceling = refs.CANCEL_MOVES[possibility]["cancel"]
        if move == canceling[0] and move_plus_1 == canceling[1]:
            return refs.CANCEL_MOVES[possibility]["result"]

def get_opposite_move(move):
    return refs.OPPOSITE_MOVE[move]


















def find_algo_F2L(cube, col_up, col_right):
    for possibility in cases_CFOP.F2L:
        conditions = cases_CFOP.F2L[possibility]["conditions"]
        if cube[conditions[0][0][0]][conditions[0][0][1]][conditions[0][0][2]] == 2:
            if (cube[conditions[1][0][0]][conditions[1][0][1]][conditions[1][0][2]] == col_up and
                cube[conditions[1][1][0]][conditions[1][1][1]][conditions[1][1][2]] == col_up):
                if (cube[conditions[2][0][0]][conditions[2][0][1]][conditions[2][0][2]] == col_right and
                    cube[conditions[2][1][0]][conditions[2][1][1]][conditions[2][1][2]] == col_right):
                    #print(possibility)
                    return cases_CFOP.F2L[possibility]["algo"]
    #print("F2L error")
    #breakpoint()
                

def solve_F2L(cube, root, update_callback=None, sid=None, cube_states=None, append_moves=None):
    run_algo(cube, "x'", root, update_callback, sid, cube_states, append_moves)
    countA = 0
    while (not np.array_equal(cube[5], np.array([[2,2,2],[2,2,2],[2,2,2]])) or
           not np.array_equal(cube[1][1], np.array([1,1,1])) or
           not np.array_equal(cube[1][2], np.array([1,1,1])) or
           not np.array_equal(cube[2][1], np.array([0,0,0])) or
           not np.array_equal(cube[2][2], np.array([0,0,0])) or
           not np.array_equal(cube[3][1], np.array([3,3,3])) or
           not np.array_equal(cube[3][2], np.array([3,3,3])) or
           not np.array_equal(cube[4][1], np.array([5,5,5])) or
           not np.array_equal(cube[4][2], np.array([5,5,5]))):
        count = 0
        
        while (cube[5][0][2] != 2 or
               cube[2][2][2] != cube[2][1][1] or
               cube[2][1][2] != cube[2][1][1] or
               cube[3][2][0] != cube[3][1][1] or
               cube[3][1][0] != cube[3][1][1]):
            algo = find_algo_F2L(cube, cube[2][1][1], cube[3][1][1])
            if algo:
                run_algo(cube, algo, root, update_callback, sid, cube_states, append_moves)
            else:
                if count < 4:
                    run_algo(cube, "U", root, update_callback, sid, cube_states, append_moves)
                    count += 1
                else:
                    break
        if countA < 4:
            countA += 1
        else:
            # special case
            solve_F2L_supp(cube, root, update_callback, sid, cube_states, append_moves)
            countA = 0
        run_algo(cube, "d", root, update_callback, sid, cube_states, append_moves)
    run_algo(cube, "x", root, update_callback, sid, cube_states, append_moves)

def solve_F2L_supp(cube, root, update_callback=None, sid=None, cube_states=None, append_moves=None):
    col_up = cube[2][1][1]
    col_right = cube[3][1][1]
    for possibility in cases_CFOP.F2L_SUPP:
        conditions = cases_CFOP.F2L_SUPP[possibility]["conditions"]
        if len(conditions) == 2:
            if ((cube[conditions[0][0]][conditions[0][1]][conditions[0][2]] == col_up and
                 cube[conditions[1][0]][conditions[1][1]][conditions[1][2]] == col_right) or
                (cube[conditions[0][0]][conditions[0][1]][conditions[0][2]] == col_right and
                 cube[conditions[1][0]][conditions[1][1]][conditions[1][2]] == col_up)):
                algo = cases_CFOP.F2L_SUPP[possibility]["algo"]
                run_algo(cube, algo, root, update_callback, sid, cube_states, append_moves)
                return
                
        if len(conditions) == 3:
            if ((cube[conditions[0][0]][conditions[0][1]][conditions[0][2]] == col_up and
                 cube[conditions[1][0]][conditions[1][1]][conditions[1][2]] == col_right and
                 cube[conditions[2][0]][conditions[2][1]][conditions[2][2]] == 2) or
                (cube[conditions[0][0]][conditions[0][1]][conditions[0][2]] == 2 and
                 cube[conditions[1][0]][conditions[1][1]][conditions[1][2]] == col_up and
                 cube[conditions[2][0]][conditions[2][1]][conditions[2][2]] == col_right) or
                (cube[conditions[0][0]][conditions[0][1]][conditions[0][2]] == col_right and
                 cube[conditions[1][0]][conditions[1][1]][conditions[1][2]] == 2 and
                 cube[conditions[2][0]][conditions[2][1]][conditions[2][2]] == col_up)):
                algo = cases_CFOP.F2L_SUPP[possibility]["algo"]
                run_algo(cube, algo, root, update_callback, sid, cube_states, append_moves)
                return


def find_algo_OLL(cube):
    for possibility in cases_CFOP.OLL:
        result = True
        for condition in cases_CFOP.OLL[possibility]["conditions"]:
            if cube[condition[0]][condition[1]][condition[2]] != 4: # 4 = yellow
                result = False
                break
        
        if result:
            return cases_CFOP.OLL[possibility]["algo"]

def solve_OLL(cube, root, update_callback=None, sid=None, cube_states=None, append_moves=None):
    run_algo(cube, "x'", root, update_callback, sid, cube_states, append_moves)
    count = 0
    while not np.array_equal(cube[0], np.array([[4,4,4],[4,4,4],[4,4,4]])):
        algo = find_algo_OLL(cube)
        if algo:
            run_algo(cube, algo, root, update_callback, sid, cube_states, append_moves)
        else:
            if count <= 5:
                run_algo(cube, "U", root, update_callback, sid, cube_states, append_moves)
                count += 1
            else:
                breakpoint()
    run_algo(cube, "x", root, update_callback, sid, cube_states, append_moves)

def find_algo_PLL(cube):
    for possibility in cases_CFOP.PLL:
        conditions = cases_CFOP.PLL[possibility]["conditions"]
        result = True
        used_pos = []
        for condition in conditions:
            if len(condition) == 2:
                if not (cube[condition[0][0]][condition[0][1]][condition[0][2]] == cube[condition[1][0]][1][1] and
                        cube[condition[1][0]][condition[1][1]][condition[1][2]] == cube[condition[0][0]][1][1]):
                    result = False
                    break
                else:
                    used_pos.extend(condition)
            elif len(condition) == 3:
                if not (cube[condition[0][0]][condition[0][1]][condition[0][2]] == cube[condition[1][0]][1][1] and
                        cube[condition[1][0]][condition[1][1]][condition[1][2]] == cube[condition[2][0]][1][1] and
                        cube[condition[2][0]][condition[2][1]][condition[2][2]] == cube[condition[0][0]][1][1]):
                    result = False
                    break
                else:
                    used_pos.extend(condition)
                
        if result:
            result2 = True
            valid_pos = [(1,0,0),(1,0,1),(1,0,2),(2,0,0),(2,0,1),(2,0,2),(3,0,0),(3,0,1),(3,0,2),(4,0,0),(4,0,1),(4,0,2)]
            for pos in valid_pos:
                if not pos in used_pos:
                    if not cube[pos[0]][pos[1]][pos[2]] == cube[pos[0]][1][1]:
                        result2 = False

            if result2:
                return cases_CFOP.PLL[possibility]["algo"]

def solve_PLL(cube, root, update_callback=None, sid=None, cube_states=None, append_moves=None):
    run_algo(cube, "x'", root, update_callback, sid, cube_states, append_moves)
    count = 0
    countB = 0
    while not np.array_equal(cube, np.array([
                                            [[4,4,4],[4,4,4],[4,4,4]],
                                            [[1,1,1],[1,1,1],[1,1,1]],
                                            [[0,0,0],[0,0,0],[0,0,0]],
                                            [[3,3,3],[3,3,3],[3,3,3]],
                                            [[5,5,5],[5,5,5],[5,5,5]],
                                            [[2,2,2],[2,2,2],[2,2,2]]
                                            ])):
        algo = find_algo_PLL(cube)
        if algo:
            run_algo(cube, algo, root, update_callback, sid, cube_states, append_moves)
        else:
            if count < 4:
                run_algo(cube, "U", root, update_callback, sid, cube_states, append_moves)
                count += 1
            else:
                if countB < 4:
                    count=0
                    run_algo(cube, "d", root, update_callback, sid, cube_states, append_moves)
                    countB += 1
                else:
                    breakpoint()
                    break
    run_algo(cube, "x", root, update_callback, sid, cube_states, append_moves)
