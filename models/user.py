from datetime import datetime, timedelta
from utils.database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from flask import current_app

class UserModel:
    def __init__(self):
        self.db = get_db()
        self.users_collection = self.db.users
    
    def create_user(self, username, email, contact_number, password):
        """Create a new user with hashed password"""
        # Check if user already exists
        if self.users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
            return None
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Create user document
        user_data = {
            "username": username,
            "email": email,
            "contact_number": contact_number,
            "password_hash": hashed_password,
            "last_login": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "last_token": None,
            "reset_token": None,
            "reset_token_expires": None
        }
        
        # Insert user and return the inserted ID
        result = self.users_collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""
        user = self.users_collection.find_one({"username": username})
        if user and check_password_hash(user['password_hash'], password):
            # Update last login
            self.users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.now(), "updated_at": datetime.now()}}
            )
            return user
        return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        from bson import ObjectId
        return self.users_collection.find_one({"_id": ObjectId(user_id)})
    
    def get_user_by_username(self, username):
        """Get user by username"""
        return self.users_collection.find_one({"username": username})
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return self.users_collection.find_one({"email": email})
    
    def update_last_token(self, user_id, token):
        """Update user's last token"""
        from bson import ObjectId
        self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_token": token, "updated_at": datetime.now()}}
        )
    
    def generate_token(self, user_id):
        """Generate JWT token for user"""
        token = jwt.encode({
            'user_id': str(user_id),
            'exp': datetime.now() + current_app.config.get('JWT_EXPIRATION_DELTA', 
                      timedelta(hours=24))
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    
    def verify_token(self, token):
        """Verify JWT token and return user ID"""
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def generate_reset_token(self, email):
        """Generate reset token for password reset"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        # Generate reset token
        reset_token = jwt.encode({
            'user_id': str(user['_id']),
            'email': email,
            'exp': datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        # Store reset token in user document
        from bson import ObjectId
        self.users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "reset_token": reset_token,
                "reset_token_expires": datetime.now() + timedelta(hours=1),
                "updated_at": datetime.now()
            }}
        )
        
        return reset_token
    
    def verify_reset_token(self, reset_token):
        """Verify reset token and return user email"""
        try:
            payload = jwt.decode(reset_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            email = payload['email']
            
            # Check if token is still valid in database
            from bson import ObjectId
            user = self.users_collection.find_one({
                "_id": ObjectId(user_id),
                "reset_token": reset_token,
                "reset_token_expires": {"$gt": datetime.now()}
            })
            
            if user:
                return email
            return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def reset_password(self, reset_token, new_password):
        """Reset user password"""
        # Verify reset token
        email = self.verify_reset_token(reset_token)
        if not email:
            return False
        
        # Get user by email
        user = self.get_user_by_email(email)
        if not user:
            return False
        
        # Hash new password
        hashed_password = generate_password_hash(new_password)
        
        # Update password and clear reset token
        from bson import ObjectId
        self.users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "password_hash": hashed_password,
                "reset_token": None,
                "reset_token_expires": None,
                "updated_at": datetime.now()
            }}
        )
        
        return True
    
    def update_profile(self, user_id, username=None, email=None, contact_number=None):
        """Update user profile information"""
        from bson import ObjectId
        update_data = {}
        
        if username:
            # Check if username is already taken by another user
            existing_user = self.users_collection.find_one({
                "username": username, 
                "_id": {"$ne": ObjectId(user_id)}
            })
            if existing_user:
                return False, "Username already exists"
            update_data["username"] = username
            
        if email:
            # Check if email is already taken by another user
            existing_user = self.users_collection.find_one({
                "email": email, 
                "_id": {"$ne": ObjectId(user_id)}
            })
            if existing_user:
                return False, "Email already exists"
            update_data["email"] = email
            
        if contact_number:
            update_data["contact_number"] = contact_number
            
        if update_data:
            update_data["updated_at"] = datetime.now()
            self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            return True, "Profile updated successfully"
        else:
            return False, "No data to update"
    
    def get_user_profile(self, user_id):
        """Get user profile information"""
        from bson import ObjectId
        user = self.users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            # Remove sensitive data
            user.pop('password_hash', None)
            user.pop('reset_token', None)
            user.pop('reset_token_expires', None)
            user.pop('last_token', None)
            return user
        return None
