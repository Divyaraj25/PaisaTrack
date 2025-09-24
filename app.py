from flask import Flask
from routes import main
from utils.database import init_db, init_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application version
APP_VERSION = "1.0.0"

def create_app():
    app = Flask(__name__)
    # Use SECRET_KEY from environment variables, with fallback to default
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Initialize MongoDB
    init_db(app)
    init_app(app)
    
    # Add version to app context
    @app.context_processor
    def inject_version():
        return dict(app_version=APP_VERSION)
    
    # Register blueprints
    app.register_blueprint(main)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)