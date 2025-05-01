import json, numpy, os

def init():
    global cubes, cubes_scrambled, cube_states, cube_states_scramble
    global moves_lists, move_ids, prev_move_locks, next_move_locks
    cubes = {}
    cubes_scrambled = {}
    cube_states = {}
    cube_states_scramble = {}
    moves_lists = {}
    move_ids = {}

def save(sid, username):
    # On crée les données à ajouter
    new_entry = {
        username: {
            'cube': cubes[sid].tolist()
        }
    }

    # Si le fichier existe, on lit les anciennes données
    if os.path.exists("save_file.json"):
        with open("save_file.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # On met à jour ou ajoute le nouvel utilisateur
    data.update(new_entry)

    # On réécrit le tout dans le fichier avec une jolie indentation
    with open("save_file.json", "w") as file:
        json.dump(data, file, indent=4)

def load(sid, username):
    if os.path.exists("save_file.json"):
        with open("save_file.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        return "ERROR"

    cubes[sid] = data[username]['cube']

    return
        
