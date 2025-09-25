from flask import Flask, jsonify, request
from routes import main, auth
from utils.database import init_db, init_app
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

# Application version
APP_VERSION = "1.0.0"

def create_app():
    app = Flask(__name__)
    # Use SECRET_KEY from environment variables, with fallback to default
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # JWT configuration
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)
    
    # Initialize MongoDB
    init_db(app)
    init_app(app)
    
    # Add version to app context
    @app.context_processor
    def inject_version():
        return dict(app_version=APP_VERSION)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    
    # Add token verification middleware
    @app.before_request
    def check_token():
        # Skip token check for auth routes and static files
        if request.endpoint and request.endpoint.startswith('auth'):
            return
            
        if request.endpoint and request.endpoint.startswith('static'):
            return
            
        # Skip token check for specific public routes
        exempt_routes = ['main.index', 'main.info', 'main.login_page', 'main.register_page', 'auth.forgot_password_page', 'auth.reset_password_page']
        if request.endpoint in exempt_routes:
            return
            
        # For API routes, check token
        if request.path.startswith('/api/'):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'Authorization token is required'}), 401
                
            # Extract token from "Bearer <token>" format
            if token.startswith('Bearer '):
                token = token[7:]
            else:
                return jsonify({'error': 'Invalid token format. Use "Bearer <token>"'}), 401
            
            from models.user import UserModel
            user_model = UserModel()
            user_id = user_model.verify_token(token)
            
            if not user_id:
                return jsonify({'error': 'Invalid or expired token'}), 401
                
            # Add user_id to request context
            from flask import g
            g.user_id = user_id
            return
        
        # For web routes, we let the route handler decide what to do
        # Authentication will be handled by the frontend JavaScript
        # This prevents the flash of login page issue
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Use a more Windows-compatible configuration
    app.run(debug=False, host='127.0.0.1', port=5000, threaded=False, use_reloader=False)