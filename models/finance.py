from datetime import datetime
from utils.database import get_db
from bson import ObjectId
import json
import os

class FinanceModel:
    def __init__(self, user_id=None):
        self.db = get_db()
        self.accounts_collection = self.db.accounts
        self.transactions_collection = self.db.transactions
        self.budgets_collection = self.db.budgets
        self.categories_collection = self.db.categories
        self.info_collection = self.db.info
        self.user_id = user_id
    
    def load_json_file(self, filename):
        """Load data from JSON file"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return None
    
    # Account methods
    def get_accounts(self):
        """Get all accounts for the user"""
        if not self.user_id:
            return []
        try:
            return list(self.accounts_collection.find({"user_id": self.user_id}))
        except Exception as e:
            print(f"Error getting accounts: {e}")
            return []
    
    def get_account(self, account_type):
        """Get a specific account for the user"""
        if not self.user_id:
            return None
        try:
            return self.accounts_collection.find_one({"account_type": account_type, "user_id": self.user_id})
        except Exception as e:
            print(f"Error getting account {account_type}: {e}")
            return None
    
    def create_account(self, account_data):
        """Create a new account for the user"""
        if not self.user_id:
            return None
        try:
            account_data["user_id"] = self.user_id
            return self.accounts_collection.insert_one(account_data)
        except Exception as e:
            print(f"Error creating account: {e}")
            return None
    
    def update_account(self, account_type, account_data):
        """Update an existing account for the user"""
        if not self.user_id:
            return None
        try:
            return self.accounts_collection.update_one(
                {"account_type": account_type, "user_id": self.user_id},
                {"$set": account_data}
            )
        except Exception as e:
            print(f"Error updating account {account_type}: {e}")
            return None
    
    def delete_account(self, account_type):
        """Delete an account for the user"""
        if not self.user_id:
            return None
        try:
            return self.accounts_collection.delete_one({"account_type": account_type, "user_id": self.user_id})
        except Exception as e:
            print(f"Error deleting account {account_type}: {e}")
            return None
    
    # Transaction methods
    def get_transactions(self, filter_query=None):
        """Get transactions with optional filter for the user"""
        if not self.user_id:
            return []
        try:
            if filter_query is None:
                filter_query = {}
            filter_query["user_id"] = self.user_id
            return list(self.transactions_collection.find(filter_query))
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    def get_transaction(self, transaction_id):
        """Get a specific transaction for the user"""
        if not self.user_id:
            return None
        try:
            return self.transactions_collection.find_one({"_id": transaction_id, "user_id": self.user_id})
        except Exception as e:
            print(f"Error getting transaction {transaction_id}: {e}")
            return None
    
    def create_transaction(self, transaction_data):
        """Create a new transaction for the user"""
        if not self.user_id:
            return None
        try:
            transaction_data["user_id"] = self.user_id
            return self.transactions_collection.insert_one(transaction_data)
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None
    
    def update_transaction(self, transaction_id, transaction_data):
        """Update an existing transaction for the user"""
        if not self.user_id:
            return None
        try:
            return self.transactions_collection.update_one(
                {"_id": transaction_id, "user_id": self.user_id},
                {"$set": transaction_data}
            )
        except Exception as e:
            print(f"Error updating transaction {transaction_id}: {e}")
            return None
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction for the user"""
        if not self.user_id:
            return None
        try:
            return self.transactions_collection.delete_one({"_id": transaction_id, "user_id": self.user_id})
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return None
    
    # Budget methods
    def get_budgets(self, filter_query=None):
        """Get budgets with optional filter for the user"""
        if not self.user_id:
            return []
        try:
            if filter_query is None:
                filter_query = {}
            filter_query["user_id"] = self.user_id
            return list(self.budgets_collection.find(filter_query))
        except Exception as e:
            print(f"Error getting budgets: {e}")
            return []
    
    def get_budget(self, budget_id):
        """Get a specific budget for the user"""
        if not self.user_id:
            return None
        try:
            return self.budgets_collection.find_one({"_id": budget_id, "user_id": self.user_id})
        except Exception as e:
            print(f"Error getting budget {budget_id}: {e}")
            return None
    
    def create_budget(self, budget_data):
        """Create a new budget for the user"""
        if not self.user_id:
            return None
        try:
            budget_data["user_id"] = self.user_id
            return self.budgets_collection.insert_one(budget_data)
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None
    
    def update_budget(self, budget_id, budget_data):
        """Update an existing budget for the user"""
        if not self.user_id:
            return None
        try:
            return self.budgets_collection.update_one(
                {"_id": budget_id, "user_id": self.user_id},
                {"$set": budget_data}
            )
        except Exception as e:
            print(f"Error updating budget {budget_id}: {e}")
            return None
    
    def delete_budget(self, budget_id):
        """Delete a budget for the user"""
        if not self.user_id:
            return None
        try:
            return self.budgets_collection.delete_one({"_id": budget_id, "user_id": self.user_id})
        except Exception as e:
            print(f"Error deleting budget {budget_id}: {e}")
            return None
    
    # Category methods
    def get_categories(self):
        """Get all categories for the user"""
        if not self.user_id:
            # Return default categories if no user is authenticated
            return self.load_json_file('categories.json') or self.get_default_categories()
        
        try:
            categories = self.categories_collection.find_one({"user_id": self.user_id})
            if categories:
                if '_id' in categories:
                    del categories['_id']
                if 'user_id' in categories:
                    del categories['user_id']
                return categories
        except Exception as e:
            print(f"Error getting categories: {e}")
        
        # Load from JSON file if no categories in database
        categories_data = self.load_json_file('categories.json')
        if categories_data:
            return categories_data
        
        # Return default categories if none exist or error occurred
        return self.get_default_categories()

    def get_default_categories(self):
        """Returns a default set of categories."""
        return {
            "income": ["Salary", "Freelance", "Investment", "Gift", "Business", "Bonus", "Dividend", "Rental Income", "Other"],
            "expense": ["Food", "Transport", "Entertainment", "Utilities", "Rent", "Healthcare", 
                       "Education", "Shopping", "Travel", "Personal Care", "Insurance", "Taxes", 
                       "Subscriptions", "Maintenance", "Charity", "Other"],
            "transfer": ["Cash to Bank", "Bank to Card", "Card to Cash", "Between Accounts", 
                        "Credit Card Payment", "Bank Transfer", "Investment Transfer", "Loan Payment"]
        }

    def update_categories(self, categories_data):
        """Update categories for the user"""
        if not self.user_id:
            return None
        try:
            # Ensure user_id is set for the query
            query = {"user_id": self.user_id}
            
            # Prepare the update data, ensuring user_id is included
            update_data = {"$set": categories_data}
            
            # Use upsert to create if it doesn't exist or update if it does
            return self.categories_collection.update_one(query, update_data, upsert=True)
        except Exception as e:
            print(f"Error updating categories: {e}")
            return None
    
    # Info methods (common for all users)
    def get_info(self):
        """Get info data - common for all users"""
        try:
            info = self.info_collection.find_one()
            if info:
                return info
        except Exception as e:
            print(f"Error getting info: {e}")
        
        # Return default info if none exists or error occurred
        return self.load_json_file("finance_info.json")
    
    def update_info(self, info_data):
        """Update info data - common for all users"""
        try:
            existing = self.info_collection.find_one()
            if existing:
                return self.info_collection.update_one(
                    {"_id": existing["_id"]},
                    {"$set": info_data}
                )
            else:
                return self.info_collection.insert_one(info_data)
        except Exception as e:
            print(f"Error updating info: {e}")
            return None
    
    # Initialize default data
    def initialize_default_data(self):
        """Initialize default categories and info if they don't exist for the user"""
        if not self.user_id:
            return

        try:
            # Check if categories exist for the user
            categories_exist = self.categories_collection.find_one({"user_id": self.user_id})
            if not categories_exist:
                default_categories = self.load_json_file('categories.json') or self.get_default_categories()
                
                # Add user_id to the default categories
                default_categories["user_id"] = self.user_id
                self.categories_collection.insert_one(default_categories)
            
            # Check if info exists (common for all users)
            info_exist = self.info_collection.find_one()
            if not info_exist:
                default_info = self.load_json_file('finance_info.json')
                if default_info:
                    self.info_collection.insert_one(default_info)
        except Exception as e:
            print(f"Error initializing default data: {e}")
