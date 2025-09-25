from flask import Blueprint, request, jsonify, current_app, render_template
from models.user import UserModel
from models.finance import FinanceModel
import json

auth = Blueprint('auth', __name__)

# Global model variables
user_model = None
finance_model = None

def get_user_model():
    """Get or initialize the user model"""
    global user_model
    if user_model is None:
        user_model = UserModel()
    return user_model

def get_finance_model(user_id=None):
    """Get or initialize the finance model with user context"""
    global finance_model
    finance_model = FinanceModel(user_id)
    return finance_model

@auth.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'contact_number', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Get user model
        user_model = get_user_model()
        
        # Create user
        user_id = user_model.create_user(
            data['username'],
            data['email'],
            data['contact_number'],
            data['password']
        )
        
        if not user_id:
            return jsonify({'error': 'User already exists with this username or email'}), 409
        
        # Generate token
        token = user_model.generate_token(user_id)
        
        # Update last token
        user_model.update_last_token(user_id, token)
        
        # Initialize default finance data for the user
        finance_model = get_finance_model(user_id)
        finance_model.initialize_default_data()
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'username' not in data or not data['username']:
            return jsonify({'error': 'Username is required'}), 400
            
        if 'password' not in data or not data['password']:
            return jsonify({'error': 'Password is required'}), 400
        
        # Get user model
        user_model = get_user_model()
        
        # Authenticate user
        user = user_model.authenticate_user(data['username'], data['password'])
        
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Generate token
        token = user_model.generate_token(str(user['_id']))
        
        # Update last token
        user_model.update_last_token(str(user['_id']), token)
        
        # Remove sensitive data before sending response
        user_data = {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'contact_number': user['contact_number'],
            'last_login': user['last_login'],
            'created_at': user['created_at'],
            'updated_at': user['updated_at']
        }
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/api/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        data = request.get_json()
        
        if 'token' not in data or not data['token']:
            return jsonify({'error': 'Token is required'}), 400
        
        # Get user model
        user_model = get_user_model()
        
        # Verify token
        user_id = user_model.verify_token(data['token'])
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get user data
        user = user_model.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Remove sensitive data before sending response
        user_data = {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'contact_number': user['contact_number'],
            'last_login': user['last_login'],
            'created_at': user['created_at'],
            'updated_at': user['updated_at']
        }
        
        return jsonify({
            'valid': True,
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    """Handle forgot password request"""
    try:
        data = request.get_json()
        
        if 'email' not in data or not data['email']:
            return jsonify({'error': 'Email is required'}), 400
        
        # Get user model
        user_model = get_user_model()
        
        # Generate reset token
        reset_token = user_model.generate_reset_token(data['email'])
        
        if not reset_token:
            # We don't reveal if email exists or not for security reasons
            return jsonify({
                'message': 'If your email is registered with us, you will receive a password reset link shortly.'
            }), 200
        
        # In a real application, you would send an email with the reset link
        # For this implementation, we'll just return a success message
        # The frontend can simulate the email by showing the reset link
        reset_link = f"{request.url_root}auth/reset-password?token={reset_token}"
        
        return jsonify({
            'message': 'If your email is registered with us, you will receive a password reset link shortly.',
            'reset_link': reset_link  # For development/testing purposes
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/api/reset-password', methods=['POST'])
def reset_password():
    """Handle password reset"""
    try:
        data = request.get_json()
        
        if 'token' not in data or not data['token']:
            return jsonify({'error': 'Reset token is required'}), 400
            
        if 'password' not in data or not data['password']:
            return jsonify({'error': 'Password is required'}), 400
        
        # Get user model
        user_model = get_user_model()
        
        # Reset password
        success = user_model.reset_password(data['token'], data['password'])
        
        if not success:
            return jsonify({'error': 'Invalid or expired reset token'}), 400
        
        return jsonify({
            'message': 'Password has been reset successfully. You can now login with your new password.'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/api/update-profile', methods=['POST'])
def update_profile():
    """Update user profile information"""
    try:
        data = request.get_json()
        
        # Validate token
        if 'token' not in data or not data['token']:
            return jsonify({'error': 'Token is required'}), 400
        
        # Get user model
        user_model = get_user_model()
        
        # Verify token
        user_id = user_model.verify_token(data['token'])
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Validate and update profile
        success, message = user_model.update_profile(
            user_id,
            username=data.get('username'),
            email=data.get('email'),
            contact_number=data.get('contact_number')
        )
        
        if success:
            # Get updated user data
            user = user_model.get_user_profile(user_id)
            if user:
                # Format user data for response
                user_data = {
                    'id': str(user['_id']),
                    'username': user['username'],
                    'email': user['email'],
                    'contact_number': user['contact_number'],
                    'last_login': user.get('last_login'),
                    'created_at': user['created_at'],
                    'updated_at': user['updated_at']
                }
                return jsonify({
                    'message': message,
                    'user': user_data
                }), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': message}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/forgot-password')
def forgot_password_page():
    """Forgot password page"""
    return render_template('forgot_password.html')

@auth.route('/reset-password')
def reset_password_page():
    """Reset password page"""
    return render_template('reset_password.html')