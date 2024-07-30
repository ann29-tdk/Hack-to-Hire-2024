import os

class Config:
    MONGODB_SETTINGS = {
        'db': 'flight',
        'host': 'mongodb+srv://annie29:anurag@cluster0.oo3kmna.mongodb.net/flight',
        'retryWrites': False
    }
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
