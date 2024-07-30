from .auth import auth_bp
from .flight import flight_bp

def init_routes(app, socketio):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(flight_bp, url_prefix='/flight')
    flight_bp.socketio = socketio
