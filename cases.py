# 0 = Bleu
# 2 = Blanc

WHITE_CROSS = {
    #devant # position:   Blanc   Bleu (autre couleur)
    0:  {"conditions": [(2,0,1),(0,2,1)], "algo": ""},
    1:  {"conditions": [(2,1,2),(3,1,0)], "algo": "R2 B U2"},
    2:  {"conditions": [(2,2,1),(5,0,1)], "algo": "D2 B2 U2"},
    3:  {"conditions": [(2,1,0),(1,1,2)], "algo": "L2 B' U2"},

    4:  {"conditions": [(0,2,1),(2,0,1)], "algo": "F R F' U"},
    5:  {"conditions": [(3,1,0),(2,1,2)], "algo": "R U"},
    6:  {"conditions": [(5,0,1),(2,2,1)], "algo": "D F R F'"},
    7:  {"conditions": [(1,1,2),(2,1,0)], "algo": "L' U'"},

    #haut
    8:  {"conditions": [(1,0,1),(0,1,0)], "algo": "U'"},
    9:  {"conditions": [(4,0,1),(0,0,1)], "algo": "U2"},
    10: {"conditions": [(3,0,1),(0,1,2)], "algo": "U"},

    11: {"conditions": [(0,1,0),(1,0,1)], "algo": "F' L F"},
    12: {"conditions": [(0,0,1),(4,0,1)], "algo": "U F R' F'"},
    13: {"conditions": [(0,1,2),(3,0,1)], "algo": "F R' F'"},
    
    #bas
    14: {"conditions": [(3,2,1),(5,1,2)], "algo": "F2 D' F2"},
    15: {"conditions": [(4,2,1),(5,2,1)], "algo": "F2 D2 F2"},
    16: {"conditions": [(1,2,1),(5,1,0)], "algo": "F2 D F2"},

    17: {"conditions": [(5,1,2),(3,2,1)], "algo": "F R F'"},
    18: {"conditions": [(5,2,1),(4,2,1)], "algo": "B R' U R"},
    19: {"conditions": [(5,1,0),(1,2,1)], "algo": "F' L' F"},

    #cotés
    20: {"conditions": [(4,1,0),(3,1,2)], "algo": "F R2 F'"},
    21: {"conditions": [(4,1,2),(1,1,0)], "algo": "F' L2 F"},

    22: {"conditions": [(3,1,2),(4,1,0)], "algo": "R' U R"},
    23: {"conditions": [(1,1,0),(4,1,2)], "algo": "L U' L'"}
    }

WHITE_CORNERS = {
    #devant             Blanc   Bleu    Rouge
    0:  {"conditions": [(2,0,2),(0,2,2),(3,0,0)], "algo": ""},
    1:  {"conditions": [(2,2,2),(3,2,0),(5,0,2)], "algo": "R' B' R U' B2 U"},
    2:  {"conditions": [(2,2,0),(5,0,0),(1,2,2)], "algo": "L B' L' U' B2 U"},
    3:  {"conditions": [(2,0,0),(1,0,2),(0,2,0)], "algo": "L' B2 L U' B U"},

    4:  {"conditions": [(0,2,2),(3,0,0),(2,0,2)], "algo": "U' B' U B U' B' U"},
    5:  {"conditions": [(3,2,0),(5,0,2),(2,2,2)], "algo": "R' B' R B2 U' B' U"},
    6:  {"conditions": [(5,0,0),(1,2,2),(2,2,0)], "algo": "D' B2 D U' B' U"},
    7:  {"conditions": [(1,0,2),(0,2,0),(2,0,0)], "algo": "U B' U' B' U' B' U"},

    8:  {"conditions": [(3,0,0),(2,0,2),(0,2,2)], "algo": "U' B U B' U' B U"},
    9:  {"conditions": [(5,0,2),(2,2,2),(3,2,0)], "algo": "U' D B U D'"},
    10: {"conditions": [(1,2,2),(2,2,0),(5,0,0)], "algo": "U' L B2 L' U"},
    11: {"conditions": [(0,2,0),(2,0,0),(1,0,2)], "algo": "U B U2 B2 U"},

    #derrière
    12: {"conditions": [(4,0,0),(3,0,2),(0,0,2)], "algo": "U' B2 U B U' B' U"},
    13: {"conditions": [(4,2,0),(5,2,2),(3,2,2)], "algo": "U' B2 U B' U' B U"},
    14: {"conditions": [(4,2,2),(1,2,0),(5,2,0)], "algo": "U' B' U B' U' B U"},
    15: {"conditions": [(4,0,2),(0,0,0),(1,0,0)], "algo": "B U' B' U B' U' B U"},

    16: {"conditions": [(3,0,2),(0,0,2),(4,0,0)], "algo": "B' U' B U"},
    17: {"conditions": [(5,2,2),(3,2,2),(4,2,0)], "algo": "U' B U"},
    18: {"conditions": [(1,2,0),(5,2,0),(4,2,2)], "algo": "U' B2 U"},
    19: {"conditions": [(0,0,0),(1,0,0),(4,0,2)], "algo": "B2 U' B U"},

    20: {"conditions": [(0,0,2),(4,0,0),(3,0,2)], "algo": "U' B' U"},
    21: {"conditions": [(3,2,2),(4,2,0),(5,2,2)], "algo": "B U' B' U"},
    22: {"conditions": [(5,2,0),(4,2,2),(1,2,0)], "algo": "B2 U' B' U"},
    23: {"conditions": [(1,0,0),(4,0,2),(0,0,0)], "algo": "B' U' B' U"}
    }

MIDDLE_LAYER = {
    #derrière           Bleu    Rouge
    0:  {"conditions": [(0,0,1),(4,0,1)], "algo": "B R B' R' B' U' B U"},
    1:  {"conditions": [(3,1,2),(4,1,0)], "algo": "B2 R B' R' B' U' B U"},
    2:  {"conditions": [(5,2,1),(4,2,1)], "algo": "B' R B' R' B' U' B U"},
    3:  {"conditions": [(1,1,0),(4,1,2)], "algo": "R B' R' B' U' B U"},

    4:  {"conditions": [(4,0,1),(0,0,1)], "algo": "B2 U' B U B R B' R'"},
    5:  {"conditions": [(4,1,0),(3,1,2)], "algo": "B' U' B U B R B' R'"},
    6:  {"conditions": [(4,2,1),(5,2,1)], "algo": "U' B U B R B' R'"},
    7:  {"conditions": [(4,1,2),(1,1,0)], "algo": "B U' B U B R B' R'"},

    #milieu
    8:  {"conditions": [(0,1,2),(3,0,1)], "algo": ""},               #
    9:  {"conditions": [(3,2,1),(5,1,2)], "algo": "D B' D' B' R' B R B U' B U B R B' R'"},
    10: {"conditions": [(5,1,0),(1,2,1)], "algo": "L B' L' B' D' B D B2 U' B U B R B' R'"},
    11: {"conditions": [(1,0,1),(0,1,0)], "algo": "U B' U' B' L' B L B' U' B U B R B' R'"},

    12: {"conditions": [(3,0,1),(0,1,2)], "algo": "R B' R' B' U' B U B' R B' R' B' U' B U"},
    13: {"conditions": [(5,1,2),(3,2,1)], "algo": "D B' D' B' R' B R R B' R' B' U' B U"},
    14: {"conditions": [(1,2,1),(5,1,0)], "algo": "L B' L' B' D' B D B R B' R' B' U' B U"},
    15: {"conditions": [(0,1,0),(1,0,1)], "algo": "U B' U' B' L' B L B2 R B' R' B' U' B U"}
    }

YELLOW_CROSS = {
    0:  {"conditions": [], "algo": ""},

    1:  {"conditions": [(4,0,1),(4,1,2)], "algo": "B"},
    2:  {"conditions": [(4,1,2),(4,2,1)], "algo": ""},
    3:  {"conditions": [(4,1,0),(4,2,1)], "algo": "B'"},
    4:  {"conditions": [(4,0,1),(4,1,0)], "algo": "B2"},
    
    5:  {"conditions": [(4,0,1),(4,2,1)], "algo": "B"},
    6:  {"conditions": [(4,1,0),(4,1,2)], "algo": ""}
    }

YELLOW_FACE = {
    0:  {"conditions": [(0,0,0),(0,0,2)], "algo": "", "algo_id": 0},
    1:  {"conditions": [(1,0,0),(1,2,0)], "algo": "B'", "algo_id": 0},
    2:  {"conditions": [(5,2,0),(5,2,2)], "algo": "B2", "algo_id": 0},
    3:  {"conditions": [(3,0,2),(3,2,2)], "algo": "", "algo_id": 1},

    4:  {"conditions": [(1,0,0),(3,0,2)], "algo": "", "algo_id": 1},
    5:  {"conditions": [(0,0,0),(5,2,0)], "algo": "B'", "algo_id": 1},
    6:  {"conditions": [(1,2,0),(3,2,2)], "algo": "B", "algo_id": 0},
    7:  {"conditions": [(0,0,2),(5,2,2)], "algo": "", "algo_id": 0},

    8:  {"conditions": [(0,0,2),(1,2,0)], "algo": "", "algo_id": 0},
    9:  {"conditions": [(1,0,0),(5,2,2)], "algo": "B'", "algo_id": 0},
    10: {"conditions": [(3,0,2),(5,2,0)], "algo": "", "algo_id": 1},
    11: {"conditions": [(0,0,0),(3,2,2)], "algo": "B", "algo_id": 0},

    12: {"conditions": [(1,2,0),(3,0,2),(5,2,2)], "algo": "", "algo_id": 1},
    13: {"conditions": [(0,0,0),(3,0,2),(5,2,2)], "algo": "B'", "algo_id": 1},
    14: {"conditions": [(0,0,0),(1,2,0),(3,0,2)], "algo": "B2", "algo_id": 1},
    15: {"conditions": [(0,0,0),(1,2,0),(5,2,2)], "algo": "B", "algo_id": 1},

    16: {"conditions": [(0,0,2),(3,2,2),(5,2,0)], "algo": "", "algo_id": 0},
    17: {"conditions": [(0,0,2),(1,0,0),(3,2,2)], "algo": "B'", "algo_id": 0},
    18: {"conditions": [(0,0,2),(1,0,0),(5,2,0)], "algo": "B2", "algo_id": 0},
    19: {"conditions": [(1,0,0),(3,2,2),(5,2,0)], "algo": "B", "algo_id": 0},

    20: {"conditions": [(0,0,0),(0,0,2),(1,2,0),(3,2,2)], "algo": "", "algo_id": 0},
    21: {"conditions": [(0,0,2),(1,0,0),(1,2,0),(5,2,2)], "algo": "", "algo_id": 0},
    22: {"conditions": [(1,0,0),(3,0,2),(5,2,0),(5,2,2)], "algo": "", "algo_id": 1},
    23: {"conditions": [(0,0,0),(3,0,2),(3,2,2),(5,2,0)], "algo": "", "algo_id": 1},

    24: {"conditions": [(0,0,0),(0,0,2),(5,2,0),(5,2,2)], "algo": "", "algo_id": 0},
    25: {"conditions": [(1,0,0),(1,2,0),(3,0,2),(3,2,2)], "algo": "", "algo_id": 1}
    }

YELLOW_FACE_SIDES = {
    0:  {"conditions": [[],[]], "algo": "", "algo_id": 0},
    1:  {"conditions": [[0,1,3,5],[]], "algo": "", "algo_id": 1},

    2:  {"conditions": [[0],[]], "algo": "B2", "algo_id": 0},
    3:  {"conditions": [[1],[]], "algo": "B", "algo_id": 0},
    4:  {"conditions": [[5],[]], "algo": "", "algo_id": 0},
    5:  {"conditions": [[3],[]], "algo": "B'", "algo_id": 0},

    6:  {"conditions": [[],[0]], "algo": "B2", "algo_id": 0},
    7:  {"conditions": [[],[1]], "algo": "B", "algo_id": 0},
    8:  {"conditions": [[],[5]], "algo": "", "algo_id": 0},
    9:  {"conditions": [[],[3]], "algo": "B'", "algo_id": 0},

    10: {"conditions": [[1,3,5],[0]], "algo": "B2", "algo_id": 1},
    11: {"conditions": [[0,3,5],[1]], "algo": "B", "algo_id": 1},
    12: {"conditions": [[0,1,3],[5]], "algo": "", "algo_id": 1},
    13: {"conditions": [[0,1,5],[3]], "algo": "B'", "algo_id": 1},
    }
