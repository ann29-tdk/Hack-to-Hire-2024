from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
from routes import init_routes
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
db = MongoEngine()

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.before_first_request
def initialize_database():
    try:
        db.init_app(app)
        logging.info("Successfully connected to MongoDB with MongoEngine")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")

init_routes(app, socketio)

if __name__ == '__main__':
    socketio.run(app, port=5000)
