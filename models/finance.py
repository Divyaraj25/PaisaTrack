from datetime import datetime
from utils.database import get_db
import json
import os

class FinanceModel:
    def __init__(self):
        self.db = get_db()
        self.accounts_collection = self.db.accounts
        self.transactions_collection = self.db.transactions
        self.budgets_collection = self.db.budgets
        self.categories_collection = self.db.categories
        self.info_collection = self.db.info
        
        # Create indices for better performance
        self.create_indices()
    
    def create_indices(self):
        """Create database indices for finance collections"""
        try:
            # Create indices with user_id for all collections
            self.accounts_collection.create_index([("user_id", 1), ("account_type", 1)])
            self.transactions_collection.create_index([("user_id", 1), ("date", -1)])
            self.transactions_collection.create_index([("user_id", 1), ("type", 1)])
            self.transactions_collection.create_index([("user_id", 1), ("category", 1)])
            self.budgets_collection.create_index([("user_id", 1), ("category", 1)])
            self.budgets_collection.create_index([("user_id", 1), ("start_date", 1), ("end_date", 1)])
        except Exception as e:
            print(f"Error creating finance indices: {e}")
    
    def load_categories_from_file(self):
        """Load categories from categories.json file"""
        try:
            categories_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'categories.json')
            if os.path.exists(categories_file):
                with open(categories_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading categories from file: {e}")
        
        # Return default categories if file not found or error
        return {
            "income": ["Salary", "Freelance", "Investment", "Gift", "Business", "Bonus", "Dividend", "Rental Income", "Other"],
            "expense": ["Food", "Transport", "Entertainment", "Utilities", "Rent", "Healthcare", 
                       "Education", "Shopping", "Travel", "Personal Care", "Insurance", "Taxes", 
                       "Subscriptions", "Maintenance", "Charity", "Other"],
            "transfer": ["Cash to Bank", "Bank to Card", "Card to Cash", "Between Accounts", 
                        "Credit Card Payment", "Bank Transfer", "Investment Transfer", "Loan Payment"]
        }
    
    def load_info_from_file(self):
        """Load info from finance_info.json file"""
        try:
            info_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'finance_info.json')
            if os.path.exists(info_file):
                with open(info_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading info from file: {e}")
        
        # Return default info if file not found or error
        return {
            "introduction": "Personal Finance Tracker helps you manage your income, expenses, and budgets effectively.",
            "features": {
                "balance_tracking": "Track balances across multiple accounts (Cash, Debit Card, Credit Card, Bank Account)",
                "transaction_management": "Record income, expenses, and transfers with categories and dates",
                "budgeting": "Set budgets with various timeframes (custom, weekly, monthly, yearly)",
                "reporting": "View transactions, budgets, and financial insights",
                "account_management": "Manage account details including last 4 digits and initial amounts"
            }
        }
    
    # Account methods
    def get_accounts(self, user_id=None):
        """Get all accounts"""
        try:
            filter_query = {"user_id": user_id} if user_id else {}
            return list(self.accounts_collection.find(filter_query))
        except Exception as e:
            print(f"Error getting accounts: {e}")
            return []
    
    def get_account(self, account_type, user_id=None):
        """Get a specific account"""
        try:
            filter_query = {"account_type": account_type}
            if user_id:
                filter_query["user_id"] = user_id
            return self.accounts_collection.find_one(filter_query)
        except Exception as e:
            print(f"Error getting account {account_type}: {e}")
            return None
    
    def create_account(self, account_data, user_id):
        """Create a new account"""
        try:
            account_data["user_id"] = user_id
            return self.accounts_collection.insert_one(account_data)
        except Exception as e:
            print(f"Error creating account: {e}")
            return None
    
    def update_account(self, account_type, account_data, user_id):
        """Update an existing account"""
        try:
            return self.accounts_collection.update_one(
                {"account_type": account_type, "user_id": user_id},
                {"$set": account_data}
            )
        except Exception as e:
            print(f"Error updating account {account_type}: {e}")
            return None
    
    def delete_account(self, account_type, user_id):
        """Delete an account"""
        try:
            return self.accounts_collection.delete_one({"account_type": account_type, "user_id": user_id})
        except Exception as e:
            print(f"Error deleting account {account_type}: {e}")
            return None
    
    # Transaction methods
    def get_transactions(self, filter_query=None, user_id=None):
        """Get transactions with optional filter"""
        try:
            if filter_query is None:
                filter_query = {}
            if user_id:
                filter_query["user_id"] = user_id
            return list(self.transactions_collection.find(filter_query))
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    def get_transaction(self, transaction_id, user_id=None):
        """Get a specific transaction"""
        try:
            filter_query = {"_id": transaction_id}
            if user_id:
                filter_query["user_id"] = user_id
            return self.transactions_collection.find_one(filter_query)
        except Exception as e:
            print(f"Error getting transaction {transaction_id}: {e}")
            return None
    
    def create_transaction(self, transaction_data, user_id):
        """Create a new transaction"""
        try:
            transaction_data["user_id"] = user_id
            return self.transactions_collection.insert_one(transaction_data)
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None
    
    def update_transaction(self, transaction_id, transaction_data, user_id):
        """Update an existing transaction"""
        try:
            return self.transactions_collection.update_one(
                {"_id": transaction_id, "user_id": user_id},
                {"$set": transaction_data}
            )
        except Exception as e:
            print(f"Error updating transaction {transaction_id}: {e}")
            return None
    
    def delete_transaction(self, transaction_id, user_id):
        """Delete a transaction"""
        try:
            return self.transactions_collection.delete_one({"_id": transaction_id, "user_id": user_id})
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return None
    
    # Budget methods
    def get_budgets(self, filter_query=None, user_id=None):
        """Get budgets with optional filter"""
        try:
            if filter_query is None:
                filter_query = {}
            if user_id:
                filter_query["user_id"] = user_id
            return list(self.budgets_collection.find(filter_query))
        except Exception as e:
            print(f"Error getting budgets: {e}")
            return []
    
    def get_budget(self, budget_id, user_id=None):
        """Get a specific budget"""
        try:
            filter_query = {"_id": budget_id}
            if user_id:
                filter_query["user_id"] = user_id
            return self.budgets_collection.find_one(filter_query)
        except Exception as e:
            print(f"Error getting budget {budget_id}: {e}")
            return None
    
    def create_budget(self, budget_data, user_id):
        """Create a new budget"""
        try:
            budget_data["user_id"] = user_id
            return self.budgets_collection.insert_one(budget_data)
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None
    
    def update_budget(self, budget_id, budget_data, user_id):
        """Update an existing budget"""
        try:
            return self.budgets_collection.update_one(
                {"_id": budget_id, "user_id": user_id},
                {"$set": budget_data}
            )
        except Exception as e:
            print(f"Error updating budget {budget_id}: {e}")
            return None
    
    def delete_budget(self, budget_id, user_id):
        """Delete a budget"""
        try:
            return self.budgets_collection.delete_one({"_id": budget_id, "user_id": user_id})
        except Exception as e:
            print(f"Error deleting budget {budget_id}: {e}")
            return None
    
    # Category methods
    def get_categories(self):
        """Get all categories"""
        try:
            categories = self.categories_collection.find_one()
            if categories:
                # Remove the MongoDB _id field if present
                if '_id' in categories:
                    del categories['_id']
                return categories
        except Exception as e:
            print(f"Error getting categories: {e}")
        
        # Load categories from file if none exist in database
        return self.load_categories_from_file()
    
    def update_categories(self, categories_data):
        """Update categories"""
        try:
            # For simplicity, we'll replace the entire document
            existing = self.categories_collection.find_one()
            if existing:
                return self.categories_collection.update_one(
                    {"_id": existing["_id"]},
                    {"$set": categories_data}
                )
            else:
                return self.categories_collection.insert_one(categories_data)
        except Exception as e:
            print(f"Error updating categories: {e}")
            return None
    
    # Info methods
    def get_info(self):
        """Get info data"""
        try:
            info = self.info_collection.find_one()
            if info:
                return info
        except Exception as e:
            print(f"Error getting info: {e}")
        
        # Load info from file if none exists in database
        return self.load_info_from_file()
    
    def update_info(self, info_data):
        """Update info data"""
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
        """Initialize default categories and info if they don't exist"""
        try:
            # Check if categories exist
            if not self.categories_collection.find_one():
                default_categories = self.load_categories_from_file()
                self.categories_collection.insert_one(default_categories)
            
            # Check if info exists
            if not self.info_collection.find_one():
                default_info = self.load_info_from_file()
                self.info_collection.insert_one(default_info)
        except Exception as e:
            print(f"Error initializing default data: {e}")