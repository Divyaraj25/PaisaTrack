"""
Script to initialize MongoDB with info data
"""
import json
import os
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['paisatrackIN']

# Collections
info_collection = db['info']
categories_collection = db['categories']

def load_json_file(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def init_categories():
    """Initialize categories data with default values"""
    categories_collection.delete_many({})  # Clear existing data
    
    # Default categories
    default_categories = {
        "income": ["Salary", "Freelance", "Investment", "Gift", "Business", "Other"],
        "expense": ["Food", "Transport", "Entertainment", "Utilities", "Rent", "Healthcare", 
                   "Education", "Shopping", "Travel", "Personal Care", "Other"],
        "transfer": ["Cash to Bank", "Bank to Card", "Card to Cash", "Between Accounts", "Credit Card Payment"]
    }
    
    categories_collection.insert_one(default_categories)
    print(f"Initialized categories with default values")

def init_info():
    """Initialize info data"""
    info_collection.delete_many({})  # Clear existing data
    
    info_data = load_json_file('../finance_info.json')
    if info_data:
        info_collection.insert_one(info_data)
        print(f"Initialized info data from finance_info.json")
    else:
        # Create default info data
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
        info_collection.insert_one(default_info)
        print(f"Initialized info data with default values")

def main():
    """Main initialization function"""
    print("Starting fresh initialization of MongoDB...")
    
    # Initialize categories and info only
    init_categories()
    init_info()
    
    print("Fresh initialization completed successfully!")

if __name__ == "__main__":
    main()