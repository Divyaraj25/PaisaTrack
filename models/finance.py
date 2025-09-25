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
        try:
            if self.user_id:
                return list(self.accounts_collection.find({"user_id": self.user_id}))
            else:
                return list(self.accounts_collection.find())
        except Exception as e:
            print(f"Error getting accounts: {e}")
            return []
    
    def get_account(self, account_type):
        """Get a specific account for the user"""
        try:
            if self.user_id:
                return self.accounts_collection.find_one({"account_type": account_type, "user_id": self.user_id})
            else:
                return self.accounts_collection.find_one({"account_type": account_type})
        except Exception as e:
            print(f"Error getting account {account_type}: {e}")
            return None
    
    def create_account(self, account_data):
        """Create a new account for the user"""
        try:
            if self.user_id:
                account_data["user_id"] = self.user_id
            return self.accounts_collection.insert_one(account_data)
        except Exception as e:
            print(f"Error creating account: {e}")
            return None
    
    def update_account(self, account_type, account_data):
        """Update an existing account for the user"""
        try:
            if self.user_id:
                return self.accounts_collection.update_one(
                    {"account_type": account_type, "user_id": self.user_id},
                    {"$set": account_data}
                )
            else:
                return self.accounts_collection.update_one(
                    {"account_type": account_type},
                    {"$set": account_data}
                )
        except Exception as e:
            print(f"Error updating account {account_type}: {e}")
            return None
    
    def delete_account(self, account_type):
        """Delete an account for the user"""
        try:
            if self.user_id:
                return self.accounts_collection.delete_one({"account_type": account_type, "user_id": self.user_id})
            else:
                return self.accounts_collection.delete_one({"account_type": account_type})
        except Exception as e:
            print(f"Error deleting account {account_type}: {e}")
            return None
    
    # Transaction methods
    def get_transactions(self, filter_query=None):
        """Get transactions with optional filter for the user"""
        try:
            if filter_query is None:
                filter_query = {}
            
            if self.user_id:
                filter_query["user_id"] = self.user_id
                
            return list(self.transactions_collection.find(filter_query))
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    def get_transaction(self, transaction_id):
        """Get a specific transaction for the user"""
        try:
            if self.user_id:
                return self.transactions_collection.find_one({"_id": transaction_id, "user_id": self.user_id})
            else:
                return self.transactions_collection.find_one({"_id": transaction_id})
        except Exception as e:
            print(f"Error getting transaction {transaction_id}: {e}")
            return None
    
    def create_transaction(self, transaction_data):
        """Create a new transaction for the user"""
        try:
            if self.user_id:
                transaction_data["user_id"] = self.user_id
            return self.transactions_collection.insert_one(transaction_data)
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None
    
    def update_transaction(self, transaction_id, transaction_data):
        """Update an existing transaction for the user"""
        try:
            if self.user_id:
                return self.transactions_collection.update_one(
                    {"_id": transaction_id, "user_id": self.user_id},
                    {"$set": transaction_data}
                )
            else:
                return self.transactions_collection.update_one(
                    {"_id": transaction_id},
                    {"$set": transaction_data}
                )
        except Exception as e:
            print(f"Error updating transaction {transaction_id}: {e}")
            return None
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction for the user"""
        try:
            if self.user_id:
                return self.transactions_collection.delete_one({"_id": transaction_id, "user_id": self.user_id})
            else:
                return self.transactions_collection.delete_one({"_id": transaction_id})
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return None
    
    # Budget methods
    def get_budgets(self, filter_query=None):
        """Get budgets with optional filter for the user"""
        try:
            if filter_query is None:
                filter_query = {}
            
            if self.user_id:
                filter_query["user_id"] = self.user_id
                
            return list(self.budgets_collection.find(filter_query))
        except Exception as e:
            print(f"Error getting budgets: {e}")
            return []
    
    def get_budget(self, budget_id):
        """Get a specific budget for the user"""
        try:
            if self.user_id:
                return self.budgets_collection.find_one({"_id": budget_id, "user_id": self.user_id})
            else:
                return self.budgets_collection.find_one({"_id": budget_id})
        except Exception as e:
            print(f"Error getting budget {budget_id}: {e}")
            return None
    
    def create_budget(self, budget_data):
        """Create a new budget for the user"""
        try:
            if self.user_id:
                budget_data["user_id"] = self.user_id
            return self.budgets_collection.insert_one(budget_data)
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None
    
    def update_budget(self, budget_id, budget_data):
        """Update an existing budget for the user"""
        try:
            if self.user_id:
                return self.budgets_collection.update_one(
                    {"_id": budget_id, "user_id": self.user_id},
                    {"$set": budget_data}
                )
            else:
                return self.budgets_collection.update_one(
                    {"_id": budget_id},
                    {"$set": budget_data}
                )
        except Exception as e:
            print(f"Error updating budget {budget_id}: {e}")
            return None
    
    def delete_budget(self, budget_id):
        """Delete a budget for the user"""
        try:
            if self.user_id:
                return self.budgets_collection.delete_one({"_id": budget_id, "user_id": self.user_id})
            else:
                return self.budgets_collection.delete_one({"_id": budget_id})
        except Exception as e:
            print(f"Error deleting budget {budget_id}: {e}")
            return None
    
    # Category methods
    def get_categories(self):
        """Get all categories for the user"""
        try:
            if self.user_id:
                categories = self.categories_collection.find_one({"user_id": self.user_id})
            else:
                categories = self.categories_collection.find_one()
                
            if categories:
                # Remove the MongoDB _id field if present
                if '_id' in categories:
                    del categories['_id']
                return categories
        except Exception as e:
            print(f"Error getting categories: {e}")
        
        # Load from JSON file if no categories in database
        categories_data = self.load_json_file('categories.json')
        if categories_data:
            return categories_data
        
        # Return default categories if none exist or error occurred
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
        try:
            if self.user_id:
                categories_data["user_id"] = self.user_id
                # For simplicity, we'll replace the entire document
                existing = self.categories_collection.find_one({"user_id": self.user_id})
            else:
                existing = self.categories_collection.find_one()
                
            if existing:
                if self.user_id:
                    return self.categories_collection.update_one(
                        {"_id": existing["_id"]},
                        {"$set": categories_data}
                    )
                else:
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
        """Get info data - common for all users"""
        try:
            # Info data is common for all users, so we don't filter by user_id
            info = self.info_collection.find_one()
            if info:
                return info
        except Exception as e:
            print(f"Error getting info: {e}")
        
        # Return default info if none exists or error occurred
        return load_json_file("../finance_info.json")
    
    def update_info(self, info_data):
        """Update info data - common for all users"""
        try:
            # Info data is common for all users, so we don't filter by user_id
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
        try:
            # Check if categories exist for the user
            if self.user_id:
                categories_exist = self.categories_collection.find_one({"user_id": self.user_id})
            else:
                categories_exist = self.categories_collection.find_one()
                
            if not categories_exist:
                default_categories = self.load_json_file('categories.json')
                if not default_categories:
                    default_categories = {
                        "income": ["Salary", "Freelance", "Investment", "Gift", "Business", "Bonus", "Dividend", "Rental Income", "Other"],
                        "expense": ["Food", "Transport", "Entertainment", "Utilities", "Rent", "Healthcare", 
                                   "Education", "Shopping", "Travel", "Personal Care", "Insurance", "Taxes", 
                                   "Subscriptions", "Maintenance", "Charity", "Other"],
                        "transfer": ["Cash to Bank", "Bank to Card", "Card to Cash", "Between Accounts", 
                                    "Credit Card Payment", "Bank Transfer", "Investment Transfer", "Loan Payment"]
                    }
                
                if self.user_id:
                    default_categories["user_id"] = self.user_id
                self.categories_collection.insert_one(default_categories)
            
            # Check if info exists - info is common for all users
            info_exist = self.info_collection.find_one()
            if not info_exist:
                default_info = self.load_json_file('finance_info.json')
                if not default_info:
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
                            },
                            "comprehensive_example": {
                                "scenario": "Monthly Financial Management",
                                "description": "A real-world example showing how to manage personal finances for a month with multiple accounts, income sources, and expenses",
                                "accounts": [
                                    {
                                        "type": "Bank Account",
                                        "initial_amount": 100000,
                                        "description": "Primary savings account with initial balance"
                                    },
                                    {
                                        "type": "Credit Card",
                                        "initial_amount": -25000,
                                        "description": "Credit card with existing debt (negative balance)"
                                    },
                                    {
                                        "type": "Cash",
                                        "initial_amount": 5000,
                                        "description": "Physical cash on hand"
                                    },
                                    {
                                        "type": "Investment Account",
                                        "initial_amount": 200000,
                                        "description": "Long-term investment portfolio"
                                    }
                                ],
                                "transactions": [
                                    {
                                        "type": "income",
                                        "account": "Bank Account",
                                        "category": "Salary",
                                        "amount": 75000,
                                        "date": "2023-11-01",
                                        "description": "Monthly salary deposit"
                                    },
                                    {
                                        "type": "income",
                                        "account": "Bank Account",
                                        "category": "Investment",
                                        "amount": 5000,
                                        "date": "2023-11-02",
                                        "description": "Dividend income from stocks"
                                    },
                                    {
                                        "type": "expense",
                                        "account": "Credit Card",
                                        "category": "Rent",
                                        "amount": 25000,
                                        "date": "2023-11-02",
                                        "description": "Monthly rent payment"
                                    },
                                    {
                                        "type": "transfer",
                                        "from_account": "Bank Account",
                                        "to_account": "Credit Card",
                                        "category": "Credit Card Payment",
                                        "amount": 25000,
                                        "date": "2023-11-03",
                                        "description": "Credit card bill payment"
                                    },
                                    {
                                        "type": "expense",
                                        "account": "Cash",
                                        "category": "Food",
                                        "amount": 3000,
                                        "date": "2023-11-05",
                                        "description": "Weekly grocery shopping"
                                    },
                                    {
                                        "type": "transfer",
                                        "from_account": "Bank Account",
                                        "to_account": "Cash",
                                        "category": "Cash Withdrawal",
                                        "amount": 5000,
                                        "date": "2023-11-06",
                                        "description": "ATM cash withdrawal"
                                    },
                                    {
                                        "type": "expense",
                                        "account": "Credit Card",
                                        "category": "Utilities",
                                        "amount": 2500,
                                        "date": "2023-11-07",
                                        "description": "Electricity and water bills"
                                    },
                                    {
                                        "type": "expense",
                                        "account": "Bank Account",
                                        "category": "Insurance",
                                        "amount": 8000,
                                        "date": "2023-11-10",
                                        "description": "Annual health insurance premium"
                                    },
                                    {
                                        "type": "transfer",
                                        "from_account": "Bank Account",
                                        "to_account": "Investment Account",
                                        "category": "Investment Transfer",
                                        "amount": 15000,
                                        "date": "2023-11-15",
                                        "description": "Monthly investment contribution"
                                    },
                                    {
                                        "type": "expense",
                                        "account": "Credit Card",
                                        "category": "Entertainment",
                                        "amount": 3500,
                                        "date": "2023-11-20",
                                        "description": "Movie tickets and dinner"
                                    },
                                    {
                                        "type": "expense",
                                        "account": "Bank Account",
                                        "category": "Shopping",
                                        "amount": 12000,
                                        "date": "2023-11-22",
                                        "description": "Clothing and household items"
                                    },
                                    {
                                        "type": "transfer",
                                        "from_account": "Investment Account",
                                        "to_account": "Bank Account",
                                        "category": "Investment Transfer",
                                        "amount": 10000,
                                        "date": "2023-11-25",
                                        "description": "Withdrawal for emergency fund"
                                    }
                                ],
                                "budgets": [
                                    {
                                        "category": "Food",
                                        "amount": 12000,
                                        "period": "monthly",
                                        "start_date": "2023-11-01",
                                        "end_date": "2023-11-30",
                                        "description": "Monthly food budget including groceries and dining out"
                                    },
                                    {
                                        "category": "Entertainment",
                                        "amount": 5000,
                                        "period": "monthly",
                                        "start_date": "2023-11-01",
                                        "end_date": "2023-11-30",
                                        "description": "Monthly entertainment budget for movies, events, etc."
                                    },
                                    {
                                        "category": "Shopping",
                                        "amount": 10000,
                                        "period": "monthly",
                                        "start_date": "2023-11-01",
                                        "end_date": "2023-11-30",
                                        "description": "Monthly shopping budget for clothing and household items"
                                    },
                                    {
                                        "category": "Utilities",
                                        "amount": 3000,
                                        "period": "monthly",
                                        "start_date": "2023-11-01",
                                        "end_date": "2023-11-30",
                                        "description": "Monthly utilities budget for electricity, water, internet, etc."
                                    }
                                ],
                                "financial_summary": {
                                    "total_income": 80000,
                                    "total_expenses": 56000,
                                    "net_savings": 24000,
                                    "account_balances": {
                                        "Bank Account": 147000,
                                        "Credit Card": 0,
                                        "Cash": 2000,
                                        "Investment Account": 205000
                                    },
                                    "net_worth": 354000
                                }
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