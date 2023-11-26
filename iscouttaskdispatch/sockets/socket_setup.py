from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")  # Set appropriate CORS settings

def init_socketio(app):
    socketio.init_app(app)