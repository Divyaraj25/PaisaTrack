from datetime import datetime
from utils.database import get_db

class FinanceModel:
    def __init__(self):
        self.db = get_db()
        self.accounts_collection = self.db.accounts
        self.transactions_collection = self.db.transactions
        self.budgets_collection = self.db.budgets
        self.categories_collection = self.db.categories
        self.info_collection = self.db.info
    
    # Account methods
    def get_accounts(self):
        """Get all accounts"""
        try:
            return list(self.accounts_collection.find())
        except Exception as e:
            print(f"Error getting accounts: {e}")
            return []
    
    def get_account(self, account_type):
        """Get a specific account"""
        try:
            return self.accounts_collection.find_one({"account_type": account_type})
        except Exception as e:
            print(f"Error getting account {account_type}: {e}")
            return None
    
    def create_account(self, account_data):
        """Create a new account"""
        try:
            return self.accounts_collection.insert_one(account_data)
        except Exception as e:
            print(f"Error creating account: {e}")
            return None
    
    def update_account(self, account_type, account_data):
        """Update an existing account"""
        try:
            return self.accounts_collection.update_one(
                {"account_type": account_type},
                {"$set": account_data}
            )
        except Exception as e:
            print(f"Error updating account {account_type}: {e}")
            return None
    
    def delete_account(self, account_type):
        """Delete an account"""
        try:
            return self.accounts_collection.delete_one({"account_type": account_type})
        except Exception as e:
            print(f"Error deleting account {account_type}: {e}")
            return None
    
    # Transaction methods
    def get_transactions(self, filter_query=None):
        """Get transactions with optional filter"""
        try:
            if filter_query is None:
                filter_query = {}
            return list(self.transactions_collection.find(filter_query))
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    def get_transaction(self, transaction_id):
        """Get a specific transaction"""
        try:
            return self.transactions_collection.find_one({"_id": transaction_id})
        except Exception as e:
            print(f"Error getting transaction {transaction_id}: {e}")
            return None
    
    def create_transaction(self, transaction_data):
        """Create a new transaction"""
        try:
            return self.transactions_collection.insert_one(transaction_data)
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None
    
    def update_transaction(self, transaction_id, transaction_data):
        """Update an existing transaction"""
        try:
            return self.transactions_collection.update_one(
                {"_id": transaction_id},
                {"$set": transaction_data}
            )
        except Exception as e:
            print(f"Error updating transaction {transaction_id}: {e}")
            return None
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction"""
        try:
            return self.transactions_collection.delete_one({"_id": transaction_id})
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return None
    
    # Budget methods
    def get_budgets(self, filter_query=None):
        """Get budgets with optional filter"""
        try:
            if filter_query is None:
                filter_query = {}
            return list(self.budgets_collection.find(filter_query))
        except Exception as e:
            print(f"Error getting budgets: {e}")
            return []
    
    def get_budget(self, budget_id):
        """Get a specific budget"""
        try:
            return self.budgets_collection.find_one({"_id": budget_id})
        except Exception as e:
            print(f"Error getting budget {budget_id}: {e}")
            return None
    
    def create_budget(self, budget_data):
        """Create a new budget"""
        try:
            return self.budgets_collection.insert_one(budget_data)
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None
    
    def update_budget(self, budget_id, budget_data):
        """Update an existing budget"""
        try:
            return self.budgets_collection.update_one(
                {"_id": budget_id},
                {"$set": budget_data}
            )
        except Exception as e:
            print(f"Error updating budget {budget_id}: {e}")
            return None
    
    def delete_budget(self, budget_id):
        """Delete a budget"""
        try:
            return self.budgets_collection.delete_one({"_id": budget_id})
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
        
        # Return default categories if none exist or error occurred
        return {
            "income": ["Salary", "Freelance", "Investment", "Gift", "Business", "Other"],
            "expense": ["Food", "Transport", "Entertainment", "Utilities", "Rent", "Healthcare", 
                       "Education", "Shopping", "Travel", "Personal Care", "Other"],
            "transfer": ["Cash to Bank", "Bank to Card", "Card to Cash", "Between Accounts", "Credit Card Payment"]
        }
    
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
        
        # Return default info if none exists or error occurred
        return {
            "introduction": "Personal Finance Tracker helps you manage your income, expenses, and budgets effectively.",
            "features": {
                "balance_tracking": "Track balances across multiple accounts (Cash, Debit Card, Credit Card, Bank Account)",
                "transaction_management": "Record income, expenses, and transfers with categories and dates",
                "budgeting": "Set budgets with various timeframes (custom, weekly, monthly, yearly)",
                "reporting": "View transactions, budgets, and financial insights",
                "account_management": "Manage account details including last 4 digits and initial amounts"
            },
            "calculations": {
                "net_worth": "Total Assets - Total Liabilities",
                "budget_utilization": "(Amount Spent / Budget Amount) * 100",
                "account_balance": "Initial Amount + Total Income - Total Expenses + Net Transfers"
            },
            "examples": {
                "income_example": {
                    "type": "income",
                    "account": "Bank Account",
                    "category": "Salary",
                    "amount": "50000",
                    "description": "Monthly salary credit"
                },
                "expense_example": {
                    "type": "expense",
                    "account": "Credit Card",
                    "category": "Food",
                    "amount": "1500",
                    "description": "Dinner at restaurant"
                },
                "budget_example": {
                    "category": "Food",
                    "amount": "10000",
                    "period": "monthly",
                    "start_date": "2023-11-01",
                    "end_date": "2023-11-30"
                }
            },
            "tips": [
                "Review your expenses weekly to identify spending patterns",
                "Set realistic budgets based on your historical spending",
                "Pay credit card bills in full to avoid interest charges",
                "Maintain an emergency fund equivalent to 3-6 months of expenses",
                "Categorize transactions promptly for accurate reporting",
                "Use the budgeting feature to plan for large expenses"
            ],
            "how_to_use": {
                "initial_setup": "Start by adding your accounts with initial amounts",
                "adding_transactions": "Record all income and expenses as they occur",
                "setting_budgets": "Create budgets for expense categories with appropriate timeframes",
                "reviewing_reports": "Regularly check your balance, transactions, and budget status"
            }
        }
    
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
                default_categories = {
                    "income": ["Salary", "Freelance", "Investment", "Gift", "Business", "Other"],
                    "expense": ["Food", "Transport", "Entertainment", "Utilities", "Rent", "Healthcare", 
                               "Education", "Shopping", "Travel", "Personal Care", "Other"],
                    "transfer": ["Cash to Bank", "Bank to Card", "Card to Cash", "Between Accounts", "Credit Card Payment"]
                }
                self.categories_collection.insert_one(default_categories)
            
            # Check if info exists
            if not self.info_collection.find_one():
                default_info = {
                    "introduction": "Personal Finance Tracker helps you manage your income, expenses, and budgets effectively.",
                    "features": {
                        "balance_tracking": "Track balances across multiple accounts (Cash, Debit Card, Credit Card, Bank Account)",
                        "transaction_management": "Record income, expenses, and transfers with categories and dates",
                        "budgeting": "Set budgets with various timeframes (custom, weekly, monthly, yearly)",
                        "reporting": "View transactions, budgets, and financial insights",
                        "account_management": "Manage account details including last 4 digits and initial amounts"
                    },
                    "calculations": {
                        "net_worth": "Total Assets - Total Liabilities",
                        "budget_utilization": "(Amount Spent / Budget Amount) * 100",
                        "account_balance": "Initial Amount + Total Income - Total Expenses + Net Transfers"
                    },
                    "examples": {
                        "income_example": {
                            "type": "income",
                            "account": "Bank Account",
                            "category": "Salary",
                            "amount": "50000",
                            "description": "Monthly salary credit"
                        },
                        "expense_example": {
                            "type": "expense",
                            "account": "Credit Card",
                            "category": "Food",
                            "amount": "1500",
                            "description": "Dinner at restaurant"
                        },
                        "budget_example": {
                            "category": "Food",
                            "amount": "10000",
                            "period": "monthly",
                            "start_date": "2023-11-01",
                            "end_date": "2023-11-30"
                        }
                    },
                    "tips": [
                        "Review your expenses weekly to identify spending patterns",
                        "Set realistic budgets based on your historical spending",
                        "Pay credit card bills in full to avoid interest charges",
                        "Maintain an emergency fund equivalent to 3-6 months of expenses",
                        "Categorize transactions promptly for accurate reporting",
                        "Use the budgeting feature to plan for large expenses"
                    ],
                    "how_to_use": {
                        "initial_setup": "Start by adding your accounts with initial amounts",
                        "adding_transactions": "Record all income and expenses as they occur",
                        "setting_budgets": "Create budgets for expense categories with appropriate timeframes",
                        "reviewing_reports": "Regularly check your balance, transactions, and budget status"
                    }
                }
                self.info_collection.insert_one(default_info)
        except Exception as e:
            print(f"Error initializing default data: {e}")