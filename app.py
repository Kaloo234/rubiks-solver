from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import numpy as np
import json, ssl, time, threading
import os

import cube_fonctions, user_data
import refs

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

##cube = np.array([[[0,0,0],[0,0,0],[0,0,0]],
##                 [[1,1,1],[1,1,1],[1,1,1]],
##                 [[2,2,2],[2,2,2],[2,2,2]],
##                 [[3,3,3],[3,3,3],[3,3,3]],
##                 [[4,4,4],[4,4,4],[4,4,4]],
##                 [[5,5,5],[5,5,5],[5,5,5]]])
##
##cube_scrambled = np.array([[[0,0,0],[0,0,0],[0,0,0]],
##                           [[1,1,1],[1,1,1],[1,1,1]],
##                           [[2,2,2],[2,2,2],[2,2,2]],
##                           [[3,3,3],[3,3,3],[3,3,3]],
##                           [[4,4,4],[4,4,4],[4,4,4]],
##                           [[5,5,5],[5,5,5],[5,5,5]]])
#moves = []
#move_id = 0

user_data.init()

def generate_solved_cube():
    return np.array([[[0,0,0],[0,0,0],[0,0,0]],
                     [[1,1,1],[1,1,1],[1,1,1]],
                     [[2,2,2],[2,2,2],[2,2,2]],
                     [[3,3,3],[3,3,3],[3,3,3]],
                     [[4,4,4],[4,4,4],[4,4,4]],
                     [[5,5,5],[5,5,5],[5,5,5]]])

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    sid = request.sid
    print(f"Un client s'est connecté. Sid: {sid}")
    user_data.cubes[sid] = generate_solved_cube()
    user_data.cubes_scrambled[sid] = generate_solved_cube()
    user_data.cube_states[sid] = []
    user_data.cube_states_scramble[sid] = []
    user_data.moves_lists[sid] = []
    user_data.move_ids[sid] = 0
    send_cube_update(sid)
    send_moves_list_update(sid)

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    print(f"Un client s'est déconnecté. Sid: {sid}")
    user_data.cubes.pop(sid)
    user_data.cubes_scrambled.pop(sid)
    user_data.cube_states.pop(sid)
    user_data.cube_states_scramble.pop(sid)
    user_data.moves_lists.pop(sid)
    user_data.move_ids.pop(sid)

@socketio.on('run_algo_bypass')
def run_algo_bypass(data):
    global cube
    sid = request.sid
    cube = cube_fonctions.run_algo(cube, data['algo'], update_callback=send_cube_update, sid=sid)
    socketio.emit('response', {
                'status': 'success',
                'message': 'Bypass successfull'
                }, room=sid)
    return

@socketio.on('solve')
def solve():
    sid = request.sid
    user_data.cube_states[sid].clear()
    user_data.moves_lists[sid].clear()
    user_data.move_ids[sid] = 0

    if not np.array_equal(user_data.cubes[sid], refs.CUBE_SOLVED):
        user_data.cubes_scrambled[sid] = user_data.cubes[sid].copy()

        cube_fonctions.solve_cube(user_data.cubes[sid], cube_states=True, sid=sid, append_moves=append_moves)

        user_data.cubes[sid] = user_data.cubes_scrambled[sid].copy()

        #moves = shorten_moves_list(moves)
    else:
        send_cube_update(sid)
        send_moves_list_update(sid)
        socketio.emit('response', {
                    'status': 'failed',
                    'message': "Le cube n'est pas mélangé.",
                    }, room=sid)
        return

    #send_cube_update()
    send_moves_list_update(sid)
    
    socketio.emit('response', {
                'status': 'success',
                'message': 'Solved.',
                'cube_states': user_data.cube_states[sid],
                'scrambled': user_data.cubes_scrambled[sid].tolist()
                }, room=sid)
    return

@socketio.on('scramble')
def scramble():
    sid = request.sid
    #print("          data received:", data)
    user_data.cube_states[sid].clear()
    user_data.moves_lists[sid].clear()
    send_moves_list_update(sid)
    user_data.cubes[sid] = cube_fonctions.run_algo(user_data.cubes[sid], cube_fonctions.get_random_algo(10), cube_states=True, sid=sid)
    user_data.cubes_scrambled[sid] = user_data.cubes[sid].copy()

    socketio.emit('response', {
                'status': 'success',
                'message': 'Scrambled',
                'cube_states': user_data.cube_states[sid]
                }, room=sid)
    return

@socketio.on('execute_move')
def execute_move(data):
    sid = request.sid
    move = data['move']
    user_data.cubes[sid] = cube_fonctions.list_to_array(data['cube'])

    user_data.cubes[sid] = cube_fonctions.run_algo(user_data.cubes[sid], move, update_callback=send_cube_update, sid=sid)

    socketio.emit('response', {
                'status': 'success',
                'cube': user_data.cubes[sid].tolist()
                }, room=sid)
    return

@socketio.on('reset')
def reset():
    sid = request.sid
    user_data.cubes[sid] = refs.CUBE_SOLVED.copy()
    send_cube_update(sid)
    
    socketio.emit('response', {
                'status': 'success'
                }, room=sid)
    return

#@app.route('/next', methods=['POST'])
@socketio.on('next')
def next_move():
    sid = request.sid
    
    if user_data.move_ids[sid] >= len(user_data.moves_lists[sid]):  # On ne peut pas aller plus loin
        socketio.emit('response', {
                    'status': 'failed',
                    'message': 'Aucun mouvement suivant.'
                    }, room=sid)
        return
    
    # Exécuter le mouvement actuel
    user_data.cubes[sid] = cube_fonctions.run_algo(user_data.cubes[sid],
                                    user_data.moves_lists[sid][user_data.move_ids[sid]])
    send_cube_update(sid)

    user_data.move_ids[sid] += 1  # Passer au prochain mouvement

    socketio.emit('response', {
                'status': 'success',
                }, room=sid)
    return

#@app.route('/previous', methods=['POST'])
@socketio.on('previous')
def previous_move():
    sid = request.sid
    
    if user_data.move_ids[sid] <= 0:  # On ne peut pas revenir en arrière
        socketio.emit('response', {
                    'status': 'failed',
                    'message': 'Aucun mouvement précédent.'
                    }, room=sid)
        return

    user_data.move_ids[sid] -= 1  # Reculer d’un mouvement avant d’exécuter l’inverse

    user_data.cubes[sid] = cube_fonctions.run_algo(user_data.cubes[sid],
                                    refs.OPPOSITE_MOVE[user_data.moves_lists[sid][user_data.move_ids[sid]]])  # Exécuter l’inverse du mouvement précédent
    send_cube_update(sid)

    socketio.emit('response', {
                'status': 'success',
                }, room=sid)
    return

#@app.route('/recolored', methods=['POST'])
@socketio.on('recolored')
def cube_recolored(data):
    sid = request.sid
    user_data.cubes[sid] = np.array(data['cube'])
    send_cube_update(sid)
    socketio.emit('response', {
                'status': 'success',
                }, room=sid)
    return

@socketio.on('save_cube')
def save_cube(data):
    sid = request.sid
    username = data['usernam']
    user_data.save(sid, username)
    socketio.emit('response', {
                'status': 'saved',
                }, room=sid)
    return

@socketio.on('load_cube')
def load_cube(data):
    sid = request.sid
    username = data['username']
    retour = user_data.load(sid, username)
    if retour == "ERROR":
        socketio.emit('response', {
                    'status': 'failed',
                    }, room=sid)
    else:
        socketio.emit('response', {
                    'status': 'loaded',
                    'cube': user_data.cubes[sid],
                    }, room=sid)

def send_cube_update(sid):
    socketio.emit('update_cube', {'cube': user_data.cubes[sid].tolist()}, room=sid)

def send_moves_list_update(sid):
    un_modif = user_data.moves_lists[sid].copy()
    user_data.moves_lists[sid] = cube_fonctions.shorten_moves_list(user_data.moves_lists[sid].copy())
    moves_str = " ".join(user_data.moves_lists[sid])
    #print(un_modif)
    socketio.emit('update_moves_list', {'moves': moves_str}, room=sid)

def append_moves(move, sid):
    user_data.moves_lists[sid].append(move)

if __name__ == '__main__':
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    try:
        socketio.run(app, host="0.0.0.0", debug=True, port=5000, ssl_context=ssl_context)
    except AssertionError:
        print("Une erreur d'écriture a été ignorée")
