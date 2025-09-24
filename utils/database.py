from pymongo import MongoClient
from flask import current_app, g
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def init_db(app):
    """Initialize MongoDB connection"""
    # Use MONGO_URI from environment variables, with fallback to default
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    
def get_db():
    """Get database connection"""
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGO_URI'])
        g.db = client['paisatrackIN']  # Use specific database by name
        g.mongo_client = client  # Store client reference to prevent premature closing
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    client = g.pop('mongo_client', None)
    if client is not None:
        # Don't close the client here as it may be reused
        pass

def init_app(app):
    """Initialize application with database"""
    app.teardown_appcontext(close_db)