from datetime import datetime, timedelta
from utils.database import get_db
import bcrypt
import jwt
import os
from bson import ObjectId

class UserModel:
    def __init__(self):
        self.db = get_db()
        self.users_collection = self.db.users
        self.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
        
        # Create indices for better performance
        self.create_indices()
    
    def create_indices(self):
        """Create database indices for users collection"""
        try:
            # Create unique index on email
            self.users_collection.create_index("email", unique=True)
            # Create unique index on username
            self.users_collection.create_index("username", unique=True)
            # Create index on token for faster lookups
            self.users_collection.create_index("token")
            # Create index on role
            self.users_collection.create_index("role")
        except Exception as e:
            print(f"Error creating indices: {e}")
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def generate_jwt_token(self, user_id, username, email, role):
        """Generate JWT token"""
        payload = {
            'user_id': str(user_id),
            'username': username,
            'email': email,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_jwt_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def create_user(self, username, email, password, role='user'):
        """Create a new user"""
        try:
            # Check if user already exists
            if self.users_collection.find_one({"$or": [{"email": email}, {"username": username}]}):
                return None, "User with this email or username already exists"
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Create user document
            user_data = {
                "username": username,
                "email": email,
                "password": hashed_password,
                "role": role,
                "token": None,
                "last_login": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = self.users_collection.insert_one(user_data)
            
            # Generate JWT token
            token = self.generate_jwt_token(result.inserted_id, username, email, role)
            
            # Update user with token
            self.users_collection.update_one(
                {"_id": result.inserted_id},
                {"$set": {"token": token, "updated_at": datetime.utcnow()}}
            )
            
            # Return user data without password
            user_data['_id'] = result.inserted_id
            user_data['token'] = token
            del user_data['password']
            
            return user_data, None
            
        except Exception as e:
            return None, str(e)
    
    def authenticate_user(self, email, password):
        """Authenticate user with email and password"""
        try:
            # Find user by email
            user = self.users_collection.find_one({"email": email})
            
            if not user:
                return None, "Invalid email or password"
            
            # Verify password
            if not self.verify_password(password, user['password']):
                return None, "Invalid email or password"
            
            # Generate new JWT token
            token = self.generate_jwt_token(user['_id'], user['username'], user['email'], user['role'])
            
            # Update user with new token and last login
            self.users_collection.update_one(
                {"_id": user['_id']},
                {
                    "$set": {
                        "token": token,
                        "last_login": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            # Return user data without password
            user_data = {
                "_id": user['_id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role'],
                "token": token,
                "last_login": datetime.utcnow(),
                "created_at": user['created_at'],
                "updated_at": datetime.utcnow()
            }
            
            return user_data, None
            
        except Exception as e:
            return None, str(e)
    
    def get_user_by_token(self, token):
        """Get user by JWT token"""
        try:
            # Verify token
            payload = self.verify_jwt_token(token)
            if not payload:
                return None
            
            # Find user by ID and token
            user = self.users_collection.find_one({
                "_id": ObjectId(payload['user_id']),
                "token": token
            })
            
            if not user:
                return None
            
            # Return user data without password
            user_data = {
                "_id": user['_id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role'],
                "token": user['token'],
                "last_login": user['last_login'],
                "created_at": user['created_at'],
                "updated_at": user['updated_at']
            }
            
            return user_data
            
        except Exception as e:
            print(f"Error getting user by token: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user = self.users_collection.find_one({"_id": ObjectId(user_id)})
            
            if not user:
                return None
            
            # Return user data without password
            user_data = {
                "_id": user['_id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role'],
                "last_login": user['last_login'],
                "created_at": user['created_at'],
                "updated_at": user['updated_at']
            }
            
            return user_data
            
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def update_user(self, user_id, update_data):
        """Update user data"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            
            result = self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def logout_user(self, user_id):
        """Logout user by removing token"""
        try:
            result = self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "token": None,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            print(f"Error logging out user: {e}")
            return False
    
    def get_all_users(self):
        """Get all users (admin only)"""
        try:
            users = list(self.users_collection.find({}, {"password": 0}))
            return users
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []