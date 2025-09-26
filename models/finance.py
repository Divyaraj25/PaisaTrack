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
        """Create a new account for the user. Returns inserted_id on success, None on failure."""
        if not self.user_id:
            return None
        try:
            account_data["user_id"] = self.user_id
            result = self.accounts_collection.insert_one(account_data)
            return result.inserted_id if result.acknowledged else None
        except Exception as e:
            print(f"Error creating account: {e}")
            return None

    def update_account(self, account_type, account_data):
        """Update an existing account. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.accounts_collection.update_one(
                {"account_type": account_type, "user_id": self.user_id},
                {"$set": account_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating account {account_type}: {e}")
            return False

    def delete_account(self, account_type):
        """Delete an account. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.accounts_collection.delete_one({"account_type": account_type, "user_id": self.user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting account {account_type}: {e}")
            return False

    # Transaction methods
    def get_transactions(self, filter_query=None):
        """Get transactions with optional filter for the user"""
        if not self.user_id:
            return []
        try:
            query = filter_query or {}
            query["user_id"] = self.user_id
            return list(self.transactions_collection.find(query))
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []

    def get_transaction(self, transaction_id):
        """Get a specific transaction by its ID for the user"""
        if not self.user_id:
            return None
        try:
            return self.transactions_collection.find_one({"_id": ObjectId(transaction_id), "user_id": self.user_id})
        except Exception as e:
            print(f"Error getting transaction {transaction_id}: {e}")
            return None

    def create_transaction(self, transaction_data):
        """Create a new transaction. Returns inserted_id on success, None on failure."""
        if not self.user_id:
            return None
        try:
            transaction_data["user_id"] = self.user_id
            result = self.transactions_collection.insert_one(transaction_data)
            return result.inserted_id if result.acknowledged else None
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None

    def update_transaction(self, transaction_id, transaction_data):
        """Update a transaction. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.transactions_collection.update_one(
                {"_id": ObjectId(transaction_id), "user_id": self.user_id},
                {"$set": transaction_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating transaction {transaction_id}: {e}")
            return False

    def delete_transaction(self, transaction_id):
        """Delete a transaction. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.transactions_collection.delete_one({"_id": ObjectId(transaction_id), "user_id": self.user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return False

    # Budget methods
    def get_budgets(self, filter_query=None):
        """Get budgets with optional filter for the user"""
        if not self.user_id:
            return []
        try:
            query = filter_query or {}
            query["user_id"] = self.user_id
            return list(self.budgets_collection.find(query))
        except Exception as e:
            print(f"Error getting budgets: {e}")
            return []

    def get_budget(self, budget_id):
        """Get a specific budget by its ID for the user"""
        if not self.user_id:
            return None
        try:
            return self.budgets_collection.find_one({"_id": ObjectId(budget_id), "user_id": self.user_id})
        except Exception as e:
            print(f"Error getting budget {budget_id}: {e}")
            return None

    def create_budget(self, budget_data):
        """Create a new budget. Returns inserted_id on success, None on failure."""
        if not self.user_id:
            return None
        try:
            budget_data["user_id"] = self.user_id
            result = self.budgets_collection.insert_one(budget_data)
            return result.inserted_id if result.acknowledged else None
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None

    def update_budget(self, budget_id, budget_data):
        """Update a budget. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.budgets_collection.update_one(
                {"_id": ObjectId(budget_id), "user_id": self.user_id},
                {"$set": budget_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating budget {budget_id}: {e}")
            return False

    def delete_budget(self, budget_id):
        """Delete a budget. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.budgets_collection.delete_one({"_id": ObjectId(budget_id), "user_id": self.user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting budget {budget_id}: {e}")
            return False

    # Category methods
    def get_categories(self):
        """Get categories for the user, or default if not set."""
        # If user is authenticated, try to find their categories first
        if self.user_id:
            try:
                categories = self.categories_collection.find_one({"user_id": self.user_id})
                if categories:
                    # Clean up internal fields before returning
                    if '_id' in categories:
                        del categories['_id']
                    if 'user_id' in categories:
                        del categories['user_id']
                    return categories
            except Exception as e:
                print(f"Error getting user-specific categories: {e}")
        
        # Fallback for unauthenticated users or if user has no categories
        default_categories = self.load_json_file('categories.json')
        return default_categories or self.get_default_categories()

    def get_default_categories(self):
        """Returns a default set of categories if JSON is missing."""
        return {
            "income": ["Salary", "Freelance", "Investment", "Gift", "Business", "Bonus"],
            "expense": ["Food", "Transport", "Entertainment", "Utilities", "Rent", "Healthcare"],
            "transfer": ["Cash to Bank", "Bank to Card", "Credit Card Payment"]
        }

    def update_categories(self, categories_data):
        """Update categories for the user. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            query = {"user_id": self.user_id}
            # Remove _id from data if it exists to prevent update errors
            if '_id' in categories_data:
                del categories_data['_id']
            
            update_data = {"$set": categories_data}
            result = self.categories_collection.update_one(query, update_data, upsert=True)
            # Success if a document was inserted or modified
            return result.upserted_id is not None or result.modified_count > 0
        except Exception as e:
            print(f"Error updating categories: {e}")
            return False

    # Info methods (common for all users)
    def get_info(self):
        """Get info data - common for all users"""
        try:
            return self.info_collection.find_one() or {}
        except Exception as e:
            print(f"Error getting info: {e}")
            return {}

    # Initialize default data
    def initialize_default_data(self):
        """Initializes default categories for a user if they don't exist."""
        if not self.user_id:
            return False
        try:
            if self.categories_collection.count_documents({"user_id": self.user_id}) == 0:
                default_categories = self.load_json_file('categories.json') or self.get_default_categories()
                default_categories["user_id"] = self.user_id
                self.categories_collection.insert_one(default_categories)
                return True
            return False
        except Exception as e:
            print(f"Error initializing default data: {e}")
            return False
