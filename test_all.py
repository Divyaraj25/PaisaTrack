
import unittest
import sys
import os
from datetime import datetime, timedelta
import jwt

# Add the parent directory to the path so that we can import the model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.finance import FinanceModel
from models.user import UserModel
from utils.database import get_db

class TestFinanceAndAuth(unittest.TestCase):
    def setUp(self):
        """Set up two separate user models for testing"""
        self.user_id_1 = "test_user_1"
        self.user_id_2 = "test_user_2"
        
        self.model1 = FinanceModel(self.user_id_1)
        self.model2 = FinanceModel(self.user_id_2)
        self.user_model = UserModel()

        # Clean up before each test
        self.tearDown()

    def tearDown(self):
        """Clean up any data created during the tests"""
        db = get_db()
        db.accounts.delete_many({"user_id": self.user_id_1})
        db.accounts.delete_many({"user_id": self.user_id_2})
        db.transactions.delete_many({"user_id": self.user_id_1})
        db.transactions.delete_many({"user_id": self.user_id_2})
        db.budgets.delete_many({"user_id": self.user_id_1})
        db.budgets.delete_many({"user_id": self.user_id_2})
        db.categories.delete_many({"user_id": self.user_id_1})
        db.categories.delete_many({"user_id": self.user_id_2})
        self.user_model.users_collection.delete_many({"username": "testuser"})
        self.user_model.users_collection.delete_many({"username": "testuser_categories"})


    # Account tests
    def test_account_isolation(self):
        """Test that one user cannot access another user's account"""
        # User 1 creates an account
        account_data = {"account_type": "Cash", "initial_amount": 100}
        self.model1.create_account(account_data)
        
        # User 1 should be able to get their account
        accounts1 = self.model1.get_accounts()
        self.assertEqual(len(accounts1), 1)
        self.assertEqual(accounts1[0]['account_type'], "Cash")
        
        # User 2 should not have any accounts
        accounts2 = self.model2.get_accounts()
        self.assertEqual(len(accounts2), 0)
        
        # User 2 should not be able to get User 1's account
        account2 = self.model2.get_account("Cash")
        self.assertIsNone(account2)

    # Transaction tests
    def test_transaction_isolation(self):
        """Test that one user cannot access another user's transaction"""
        # User 1 creates a transaction
        transaction_data = {"type": "income", "amount": 100, "category": "Salary", "date": "2023-01-01"}
        result = self.model1.create_transaction(transaction_data)
        transaction_id = result.inserted_id

        # User 1 should be able to get their transaction
        transactions1 = self.model1.get_transactions()
        self.assertEqual(len(transactions1), 1)
        
        # User 2 should have no transactions
        transactions2 = self.model2.get_transactions()
        self.assertEqual(len(transactions2), 0)
        
        # User 2 should not be able to get User 1's transaction
        transaction2 = self.model2.get_transaction(transaction_id)
        self.assertIsNone(transaction2)

    # Budget tests
    def test_budget_isolation(self):
        """Test that one user cannot access another user's budget"""
        # User 1 creates a budget
        budget_data = {"category": "Food", "amount": 500, "start_date": "2023-01-01", "end_date": "2023-01-31"}
        result = self.model1.create_budget(budget_data)
        budget_id = result.inserted_id
        
        # User 1 should have one budget
        budgets1 = self.model1.get_budgets()
        self.assertEqual(len(budgets1), 1)
        
        # User 2 should have no budgets
        budgets2 = self.model2.get_budgets()
        self.assertEqual(len(budgets2), 0)
        
        # User 2 should not be able to get User 1's budget
        budget2 = self.model2.get_budget(budget_id)
        self.assertIsNone(budget2)

    # Categories tests
    def test_category_isolation(self):
        """Test that categories are isolated between users"""
        # User 1 updates their categories
        categories1 = {"income": ["Salary", "Bonus"], "expense": ["Food", "Travel"]}
        self.model1.update_categories(categories1)
        
        # User 1 should get their custom categories
        user1_cats = self.model1.get_categories()
        self.assertIn("Bonus", user1_cats["income"])
        
        # User 2 should get the default categories
        user2_cats = self.model2.get_categories()
        self.assertNotIn("Bonus", user2_cats["income"])
        self.assertIn("Salary", user2_cats["income"]) # Default category

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access data"""
        unauth_model = FinanceModel() # No user_id
        
        # Create data with a real user
        self.model1.create_account({"account_type": "Savings", "initial_amount": 200})
        
        # Unauthenticated model should not get any accounts
        accounts = unauth_model.get_accounts()
        self.assertEqual(len(accounts), 0)

    def test_user_model(self):
        """Test user model functionality"""
        username = "testuser"
        email = "test@example.com"
        contact = "1234567890"
        password = "testpassword"
        
        user_id = self.user_model.create_user(username, email, contact, password)
        self.assertIsNotNone(user_id)
        
        user = self.user_model.authenticate_user(username, password)
        self.assertIsNotNone(user)
        
        user_by_email = self.user_model.get_user_by_email(email)
        self.assertIsNotNone(user_by_email)
        
        token = self.user_model.generate_token(user_id)
        self.assertIsNotNone(token)
        
        verified_user_id = self.user_model.verify_token(token)
        self.assertIsNotNone(verified_user_id)
        
        reset_token = self.user_model.generate_reset_token(email)
        self.assertIsNotNone(reset_token)
        
        verified_email = self.user_model.verify_reset_token(reset_token)
        self.assertIsNotNone(verified_email)
        
        new_password = "newpassword"
        reset_success = self.user_model.reset_password(reset_token, new_password)
        self.assertTrue(reset_success)
        
        self.user_model.authenticate_user(username, new_password)

    def test_categories_with_user(self):
        """Test categories functionality with user context"""
        username = "testuser_categories"
        email = "test_categories@example.com"
        contact = "1234567890"
        password = "testpassword"
        
        user_id = self.user_model.create_user(username, email, contact, password)
        self.assertIsNotNone(user_id, "Failed to create user")
        
        finance_model = FinanceModel(user_id)
        
        finance_model.initialize_default_data()
        
        categories = finance_model.get_categories()
        #self.assertIn("user_id", categories, "Categories not properly linked with user_id")
        #self.assertEqual(categories["user_id"], user_id, "Categories not properly linked with user_id")
        
        updated_categories = {
            "income": ["Salary", "Freelance", "Investment", "Gift"],
            "expense": ["Food", "Transport", "Entertainment", "Utilities"],
            "transfer": ["Cash to Bank", "Bank to Card"],
        }
        
        result = finance_model.update_categories(updated_categories)
        self.assertIsNotNone(result, "Failed to update categories")
        
        updated_cats = finance_model.get_categories()
        self.assertEqual(len(updated_cats["income"]), 4, "Categories update verification failed")

    def test_categories_without_user(self):
        """Test categories functionality without user context"""
        finance_model = FinanceModel()
        
        categories = finance_model.get_categories()
        self.assertNotIn("user_id", categories, "Categories should not have user_id")


if __name__ == '__main__':
    unittest.main()
