from flask_socketio import SocketIO, emit,send
from flask_setup import socketio

@socketio.on('message')
def mes(msg):
    print(msg)
