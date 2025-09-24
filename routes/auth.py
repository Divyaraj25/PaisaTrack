from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from models.user import UserModel
from functools import wraps
import json

auth = Blueprint('auth', __name__)

# Initialize user model
user_model = UserModel()

def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            if request.is_json:
                return jsonify({'message': 'Token is missing'}), 401
            else:
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('auth.login'))
        
        # Verify token and get user
        current_user = user_model.get_user_by_token(token)
        if not current_user:
            if request.is_json:
                return jsonify({'message': 'Token is invalid or expired'}), 401
            else:
                flash('Your session has expired. Please log in again.', 'error')
                return redirect(url_for('auth.login'))
        
        # Add current user to request context
        request.current_user = current_user
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user') or request.current_user['role'] != 'admin':
            if request.is_json:
                return jsonify({'message': 'Admin access required'}), 403
            else:
                flash('Admin access required.', 'error')
                return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    
    return decorated

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and API endpoint"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
    
    if not email or not password:
        if request.is_json:
            return jsonify({'message': 'Email and password are required'}), 400
        else:
            flash('Email and password are required.', 'error')
            return render_template('auth/login.html')
    
    # Authenticate user
    user, error = user_model.authenticate_user(email, password)
    
    if error:
        if request.is_json:
            return jsonify({'message': error}), 401
        else:
            flash(error, 'error')
            return render_template('auth/login.html')
    
    if request.is_json:
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            },
            'token': user['token']
        }), 200
    else:
        # Store user info in session for template rendering
        session['user'] = {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'token': user['token']
        }
        flash('Login successful!', 'success')
        return redirect(url_for('main.index'))

@auth.route('/register', methods=['POST'])
def register():
    """Register API endpoint (backend only)"""
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
    
    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required'}), 400
    
    # Validate role
    if role not in ['user', 'admin']:
        role = 'user'
    
    # Create user
    user, error = user_model.create_user(username, email, password, role)
    
    if error:
        return jsonify({'message': error}), 400
    
    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        },
        'token': user['token']
    }), 201

@auth.route('/profile')
@token_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html', user=request.current_user)

@auth.route('/logout', methods=['POST'])
@token_required
def logout():
    """Logout endpoint"""
    user_id = request.current_user['_id']
    
    # Remove token from database
    user_model.logout_user(user_id)
    
    # Clear session
    session.clear()
    
    if request.is_json:
        return jsonify({'message': 'Logout successful'}), 200
    else:
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('auth.login'))

@auth.route('/me')
@token_required
def get_current_user():
    """Get current user info API endpoint"""
    return jsonify({
        'user': {
            'id': str(request.current_user['_id']),
            'username': request.current_user['username'],
            'email': request.current_user['email'],
            'role': request.current_user['role'],
            'last_login': request.current_user['last_login'].isoformat() if request.current_user['last_login'] else None,
            'created_at': request.current_user['created_at'].isoformat() if request.current_user['created_at'] else None
        }
    }), 200

@auth.route('/users')
@token_required
@admin_required
def get_all_users():
    """Get all users (admin only)"""
    users = user_model.get_all_users()
    
    # Convert ObjectId to string and format dates
    formatted_users = []
    for user in users:
        formatted_user = {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'last_login': user['last_login'].isoformat() if user.get('last_login') else None,
            'created_at': user['created_at'].isoformat() if user.get('created_at') else None,
            'updated_at': user['updated_at'].isoformat() if user.get('updated_at') else None
        }
        formatted_users.append(formatted_user)
    
    return jsonify({'users': formatted_users}), 200