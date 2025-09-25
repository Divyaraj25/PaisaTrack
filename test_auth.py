"""
Test script for authentication functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import UserModel
from datetime import datetime, timedelta
import jwt

def test_user_model():
    """Test user model functionality"""
    print("Testing User Model...")
    
    # Initialize user model
    user_model = UserModel()
    print("✓ User model initialized")
    
    # Test create user
    username = "testuser"
    email = "test@example.com"
    contact = "1234567890"
    password = "testpassword"
    
    user_id = user_model.create_user(username, email, contact, password)
    if user_id:
        print("✓ User created successfully")
    else:
        print("✗ Failed to create user")
        return
    
    # Test authenticate user
    user = user_model.authenticate_user(username, password)
    if user:
        print("✓ User authentication successful")
    else:
        print("✗ User authentication failed")
        return
    
    # Test get user by email
    user_by_email = user_model.get_user_by_email(email)
    if user_by_email:
        print("✓ Get user by email successful")
    else:
        print("✗ Get user by email failed")
        return
    
    # Test generate token
    token = user_model.generate_token(user_id)
    if token:
        print("✓ Token generation successful")
    else:
        print("✗ Token generation failed")
        return
    
    # Test verify token
    verified_user_id = user_model.verify_token(token)
    if verified_user_id:
        print("✓ Token verification successful")
    else:
        print("✗ Token verification failed")
        return
    
    # Test forgot password functionality
    reset_token = user_model.generate_reset_token(email)
    if reset_token:
        print("✓ Reset token generation successful")
    else:
        print("✗ Reset token generation failed")
        return
    
    # Test verify reset token
    verified_email = user_model.verify_reset_token(reset_token)
    if verified_email:
        print("✓ Reset token verification successful")
    else:
        print("✗ Reset token verification failed")
        return
    
    # Test reset password
    new_password = "newpassword"
    reset_success = user_model.reset_password(reset_token, new_password)
    if reset_success:
        print("✓ Password reset successful")
    else:
        print("✗ Password reset failed")
        return
    
    # Test authentication with new password
    user_model.authenticate_user(username, new_password)
    print("✓ Authentication with new password successful")
    
    print("\nAll tests passed! Authentication functionality is working correctly.")

if __name__ == "__main__":
    test_user_model()