"""
Test script for categories functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.finance import FinanceModel
from models.user import UserModel

def test_categories_with_user():
    """Test categories functionality with user context"""
    print("Testing Categories with User Context...")
    
    # Initialize user model
    user_model = UserModel()
    
    # Create a test user
    username = "testuser_categories"
    email = "test_categories@example.com"
    contact = "1234567890"
    password = "testpassword"
    
    user_id = user_model.create_user(username, email, contact, password)
    if user_id:
        print(f"✓ User created successfully with ID: {user_id}")
    else:
        print("✗ Failed to create user")
        return
    
    # Initialize finance model with user context
    finance_model = FinanceModel(user_id)
    
    # Initialize default data
    finance_model.initialize_default_data()
    print("✓ Default data initialized")
    
    # Get categories for the user
    categories = finance_model.get_categories()
    if categories and "user_id" in categories and categories["user_id"] == user_id:
        print("✓ Categories correctly linked with user_id")
    else:
        print("✗ Categories not properly linked with user_id")
        print(f"Categories: {categories}")
        return
    
    # Test updating categories
    updated_categories = {
        "income": ["Salary", "Freelance", "Investment", "Gift"],
        "expense": ["Food", "Transport", "Entertainment", "Utilities"],
        "transfer": ["Cash to Bank", "Bank to Card"],
        "user_id": user_id
    }
    
    result = finance_model.update_categories(updated_categories)
    if result:
        print("✓ Categories updated successfully")
    else:
        print("✗ Failed to update categories")
        return
    
    # Verify updated categories
    updated_cats = finance_model.get_categories()
    if updated_cats and len(updated_cats["income"]) == 4:
        print("✓ Categories update verified")
    else:
        print("✗ Categories update verification failed")
        return
    
    print("\nAll tests passed! Categories functionality is working correctly with user context.")

def test_categories_without_user():
    """Test categories functionality without user context"""
    print("\nTesting Categories without User Context...")
    
    # Initialize finance model without user context
    finance_model = FinanceModel()
    
    # Get categories (should be common data)
    categories = finance_model.get_categories()
    if categories and "user_id" not in categories:
        print("✓ Categories correctly retrieved as common data")
    else:
        print("✗ Categories not properly retrieved as common data")
        return
    
    print("Categories functionality test completed.")

if __name__ == "__main__":
    test_categories_with_user()
    test_categories_without_user()