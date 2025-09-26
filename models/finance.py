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
<<<<<<< HEAD
<<<<<<< HEAD
        """Create a new account for the user. Returns inserted_id on success, None on failure."""
        if not self.user_id:
            return None
        try:
            account_data["user_id"] = self.user_id
            result = self.accounts_collection.insert_one(account_data)
            return result.inserted_id if result.acknowledged else None
=======
        """Create a new account for the user"""
        try:
=======
        """Create a new account for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
            if self.user_id:
                account_data["user_id"] = self.user_id
            return self.accounts_collection.insert_one(account_data)
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error creating account: {e}")
            return None

    def update_account(self, account_type, account_data):
<<<<<<< HEAD
<<<<<<< HEAD
        """Update an existing account. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.accounts_collection.update_one(
                {"account_type": account_type, "user_id": self.user_id},
                {"$set": account_data}
            )
            return result.modified_count > 0
=======
        """Update an existing account for the user"""
        try:
=======
        """Update an existing account for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
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
<<<<<<< HEAD
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error updating account {account_type}: {e}")
            return False

    def delete_account(self, account_type):
<<<<<<< HEAD
<<<<<<< HEAD
        """Delete an account. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.accounts_collection.delete_one({"account_type": account_type, "user_id": self.user_id})
            return result.deleted_count > 0
=======
        """Delete an account for the user"""
        try:
=======
        """Delete an account for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
            if self.user_id:
                return self.accounts_collection.delete_one({"account_type": account_type, "user_id": self.user_id})
            else:
                return self.accounts_collection.delete_one({"account_type": account_type})
<<<<<<< HEAD
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error deleting account {account_type}: {e}")
            return False

    # Transaction methods
    def get_transactions(self, filter_query=None):
        """Get transactions with optional filter for the user"""
        try:
<<<<<<< HEAD
            query = filter_query or {}
            query["user_id"] = self.user_id
            return list(self.transactions_collection.find(query))
=======
            if filter_query is None:
                filter_query = {}
            
            if self.user_id:
                filter_query["user_id"] = self.user_id
                
            return list(self.transactions_collection.find(filter_query))
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []

    def get_transaction(self, transaction_id):
<<<<<<< HEAD
<<<<<<< HEAD
        """Get a specific transaction by its ID for the user"""
        if not self.user_id:
            return None
        try:
            return self.transactions_collection.find_one({"_id": ObjectId(transaction_id), "user_id": self.user_id})
=======
        """Get a specific transaction for the user"""
        try:
=======
        """Get a specific transaction for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
            if self.user_id:
                return self.transactions_collection.find_one({"_id": transaction_id, "user_id": self.user_id})
            else:
                return self.transactions_collection.find_one({"_id": transaction_id})
<<<<<<< HEAD
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error getting transaction {transaction_id}: {e}")
            return None

    def create_transaction(self, transaction_data):
<<<<<<< HEAD
<<<<<<< HEAD
        """Create a new transaction. Returns inserted_id on success, None on failure."""
        if not self.user_id:
            return None
        try:
            transaction_data["user_id"] = self.user_id
            result = self.transactions_collection.insert_one(transaction_data)
            return result.inserted_id if result.acknowledged else None
=======
        """Create a new transaction for the user"""
        try:
=======
        """Create a new transaction for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
            if self.user_id:
                transaction_data["user_id"] = self.user_id
            return self.transactions_collection.insert_one(transaction_data)
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None

    def update_transaction(self, transaction_id, transaction_data):
<<<<<<< HEAD
<<<<<<< HEAD
        """Update a transaction. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.transactions_collection.update_one(
                {"_id": ObjectId(transaction_id), "user_id": self.user_id},
                {"$set": transaction_data}
            )
            return result.modified_count > 0
=======
        """Update an existing transaction for the user"""
        try:
=======
        """Update an existing transaction for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
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
<<<<<<< HEAD
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error updating transaction {transaction_id}: {e}")
            return False

    def delete_transaction(self, transaction_id):
<<<<<<< HEAD
<<<<<<< HEAD
        """Delete a transaction. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.transactions_collection.delete_one({"_id": ObjectId(transaction_id), "user_id": self.user_id})
            return result.deleted_count > 0
=======
        """Delete a transaction for the user"""
        try:
=======
        """Delete a transaction for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
            if self.user_id:
                return self.transactions_collection.delete_one({"_id": transaction_id, "user_id": self.user_id})
            else:
                return self.transactions_collection.delete_one({"_id": transaction_id})
<<<<<<< HEAD
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return False

    # Budget methods
    def get_budgets(self, filter_query=None):
        """Get budgets with optional filter for the user"""
        try:
<<<<<<< HEAD
            query = filter_query or {}
            query["user_id"] = self.user_id
            return list(self.budgets_collection.find(query))
=======
            if filter_query is None:
                filter_query = {}
            
            if self.user_id:
                filter_query["user_id"] = self.user_id
                
            return list(self.budgets_collection.find(filter_query))
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error getting budgets: {e}")
            return []

    def get_budget(self, budget_id):
<<<<<<< HEAD
<<<<<<< HEAD
        """Get a specific budget by its ID for the user"""
        if not self.user_id:
            return None
        try:
            return self.budgets_collection.find_one({"_id": ObjectId(budget_id), "user_id": self.user_id})
=======
        """Get a specific budget for the user"""
        try:
=======
        """Get a specific budget for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
            if self.user_id:
                return self.budgets_collection.find_one({"_id": budget_id, "user_id": self.user_id})
            else:
                return self.budgets_collection.find_one({"_id": budget_id})
<<<<<<< HEAD
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error getting budget {budget_id}: {e}")
            return None

    def create_budget(self, budget_data):
<<<<<<< HEAD
<<<<<<< HEAD
        """Create a new budget. Returns inserted_id on success, None on failure."""
        if not self.user_id:
            return None
        try:
            budget_data["user_id"] = self.user_id
            result = self.budgets_collection.insert_one(budget_data)
            return result.inserted_id if result.acknowledged else None
=======
        """Create a new budget for the user"""
        try:
=======
        """Create a new budget for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
            if self.user_id:
                budget_data["user_id"] = self.user_id
            return self.budgets_collection.insert_one(budget_data)
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None

    def update_budget(self, budget_id, budget_data):
<<<<<<< HEAD
<<<<<<< HEAD
        """Update a budget. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.budgets_collection.update_one(
                {"_id": ObjectId(budget_id), "user_id": self.user_id},
                {"$set": budget_data}
            )
            return result.modified_count > 0
=======
        """Update an existing budget for the user"""
        try:
=======
        """Update an existing budget for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
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
<<<<<<< HEAD
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error updating budget {budget_id}: {e}")
            return False

    def delete_budget(self, budget_id):
<<<<<<< HEAD
<<<<<<< HEAD
        """Delete a budget. Returns True on success, False on failure."""
        if not self.user_id:
            return False
        try:
            result = self.budgets_collection.delete_one({"_id": ObjectId(budget_id), "user_id": self.user_id})
            return result.deleted_count > 0
=======
        """Delete a budget for the user"""
        try:
=======
        """Delete a budget for the user"""
        try:
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
            if self.user_id:
                return self.budgets_collection.delete_one({"_id": budget_id, "user_id": self.user_id})
            else:
                return self.budgets_collection.delete_one({"_id": budget_id})
<<<<<<< HEAD
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        except Exception as e:
            print(f"Error deleting budget {budget_id}: {e}")
            return False

    # Category methods
    def get_categories(self):
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
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
<<<<<<< HEAD
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
        return {
            "income": ["Salary", "Freelance", "Investment", "Gift", "Business", "Bonus"],
            "expense": ["Food", "Transport", "Entertainment", "Utilities", "Rent", "Healthcare"],
            "transfer": ["Cash to Bank", "Bank to Card", "Credit Card Payment"]
        }
    
    def update_categories(self, categories_data):
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
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
=======
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
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
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
<<<<<<< HEAD
            print(f"Error initializing default data: {e}")
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
=======
            print(f"Error initializing default data: {e}")
>>>>>>> parent of 97d0d24 (updated from firebase studio of auth module and user isolation issue)
