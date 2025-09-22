from pymongo import MongoClient
from flask import current_app, g
import os

def init_db(app):
    """Initialize MongoDB connection"""
    # For simplicity, using default MongoDB connection
    # In production, you would use environment variables
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/paisatrackIN'
    
def get_db():
    """Get database connection"""
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGO_URI'])
        g.db = client.get_default_database()
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