import numpy as np
import tkinter as tk
import time, random

from refs import *
from cases_CFOP import *

def find_algo_F2L(cube, col_up, col_right):
    for possibility in F2L:
        conditions = F2L[possibility]["conditions"]
        if cube[conditions[0][0][0]][conditions[0][0][1]][conditions[0][0][2]] == 2:
            if (cube[conditions[1][0][0]][conditions[1][0][1]][conditions[1][0][2]] == col_up and
                cube[conditions[1][1][0]][conditions[1][1][1]][conditions[1][1][2]] == col_up):
                if (cube[conditions[2][0][0]][conditions[2][0][1]][conditions[2][0][2]] == col_right and
                    cube[conditions[2][1][0]][conditions[2][1][1]][conditions[2][1][2]] == col_right):
                    print(possibility)
                    return F2L[possibility]["algo"]
    print("F2L error")
    #breakpoint()
                

def solve_F2L(cube, root, update_callback=None, append_moves=None):
    run_algo(cube, "x'", root, update_callback, append_moves)
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
    #for side in [0,1,3,5]:
        while (cube[5][0][2] != 2 or
               cube[2][2][2] != cube[2][1][1] or
               cube[2][1][2] != cube[2][1][1] or
               cube[3][2][0] != cube[3][1][1] or
               cube[3][1][0] != cube[3][1][1]):
            #print("test")
            algo = find_algo_F2L(cube, cube[2][1][1], cube[3][1][1])
            if algo:
                run_algo(cube, algo, root, update_callback, append_moves)
            else:
                if count < 4:
                    run_algo(cube, "U", root, update_callback, append_moves)
                    count += 1
                else:
                    break
        if countA < 4:
            run_algo(cube, "d", root, update_callback, append_moves)
            countA += 1
        else:
            # special case
            run_algo(cube, "D2", root, update_callback, append_moves)
            algo = find_algo_F2L(cube, cube[2][1][1], cube[3][1][1])
            if algo:
                run_algo(cube, algo, root, update_callback, append_moves)
            else:
                run_algo(cube, "D2 U R U' R' U' F' U F", root, update_callback, append_moves)
                algo = find_algo_F2L(cube, cube[2][1][1], cube[3][1][1])
                if algo:
                    run_algo(cube, algo, root, update_callback, append_moves)
                else:
                    pass
                    #breakpoint()
            countA = 0
            #breakpoint()
    run_algo(cube, "x", root, update_callback, append_moves)
