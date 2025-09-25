from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, g
from models.finance import FinanceModel
from datetime import datetime, timedelta
import calendar

main = Blueprint('main', __name__)

def get_model():
    """Get model with user context if available"""
    # Check if user_id is available in g (from token verification)
    user_id = getattr(g, 'user_id', None)
    return FinanceModel(user_id)

def require_auth():
    """Check if user is authenticated"""
    user_id = getattr(g, 'user_id', None)
    return user_id is not None

def calculate_balances(accounts, transactions):
    """Calculate current balance for all accounts"""
    # Initialize balances with initial amounts
    balances = {account['account_type']: account['initial_amount'] for account in accounts}
    
    # Process all transactions
    for transaction in transactions:
        if transaction["type"] == "income":
            if transaction["account"] in balances:
                balances[transaction["account"]] += transaction["amount"]
        
        elif transaction["type"] == "expense":
            if transaction["account"] in balances:
                balances[transaction["account"]] -= transaction["amount"]
        
        elif transaction["type"] == "transfer":
            # Special handling for credit card payments
            if transaction["category"] == "Credit Card Payment" and transaction["to_account"] == "Credit Card":
                # Paying off credit card debt (reducing liability)
                if transaction["from_account"] in balances:
                    balances[transaction["from_account"]] -= transaction["amount"]
                
                if transaction["to_account"] in balances:
                    # For credit cards, reducing debt means increasing the balance (towards zero)
                    # Since credit card balances are negative, we ADD to reduce the debt
                    balances[transaction["to_account"]] += transaction["amount"]
            else:
                # Regular transfer
                if transaction["from_account"] in balances:
                    balances[transaction["from_account"]] -= transaction["amount"]
                
                if transaction["to_account"] in balances:
                    balances[transaction["to_account"]] += transaction["amount"]
    
    return balances

@main.route('/')
def index():
    """Public home page - shows help and information only"""
    # Always show public home page for root route
    return render_template('public_home.html')

@main.route('/dashboard')
def dashboard():
    """Dashboard page - requires authentication"""
    # For the initial page load, we'll show the dashboard template
    # Authentication will be handled by the frontend JavaScript
    # which will redirect to login if no token is found
    
    # Get user model (will be None if not authenticated)
    model = get_model()
    
    # Try to get accounts and transactions
    # If not authenticated, these will be empty lists
    try:
        accounts = model.get_accounts()
        transactions = model.get_transactions()
        
        # Calculate current balances
        balances = calculate_balances(accounts, transactions)
        
        # Calculate total assets, liabilities, and net worth
        total_assets = 0
        total_liabilities = 0
        
        for account_type, balance in balances.items():
            account = next((acc for acc in accounts if acc['account_type'] == account_type), None)
            if account:
                if account_type == "Credit Card":
                    # For credit cards, the balance represents debt (negative value)
                    # Liability is the absolute value of the negative balance
                    if balance < 0:
                        total_liabilities += abs(balance)
                    else:
                        # If balance is positive, it means we've overpaid (credit)
                        # This should count as a negative liability (asset)
                        total_liabilities -= balance  # Subtract because it's a credit
                else:
                    if balance >= 0:
                        total_assets += balance
                    else:
                        total_liabilities += abs(balance)
        
        net_worth = total_assets - total_liabilities
        
        return render_template('dashboard.html', 
                              accounts=accounts, 
                              transactions=transactions,
                              balances=balances,
                              total_assets=total_assets,
                              total_liabilities=total_liabilities,
                              net_worth=net_worth)
    except Exception as e:
        # If there's an authentication error, return empty data
        # The frontend JavaScript will handle redirecting to login
        return render_template('dashboard.html', 
                              accounts=[], 
                              transactions=[],
                              balances={},
                              total_assets=0,
                              total_liabilities=0,
                              net_worth=0)

# API endpoints for dashboard data
@main.route('/api/dashboard/summary')
def api_dashboard_summary():
    """API endpoint for dashboard summary data"""
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    model = get_model()
    
    accounts = model.get_accounts()
    transactions = model.get_transactions()
    
    # Calculate current balances
    balances = calculate_balances(accounts, transactions)
    
    # Calculate total assets, liabilities, and net worth
    total_assets = 0
    total_liabilities = 0
    
    for account_type, balance in balances.items():
        account = next((acc for acc in accounts if acc['account_type'] == account_type), None)
        if account:
            if account_type == "Credit Card":
                # For credit cards, the balance represents debt (negative value)
                # Liability is the absolute value of the negative balance
                if balance < 0:
                    total_liabilities += abs(balance)
                else:
                    # If balance is positive, it means we've overpaid (credit)
                    # This should count as a negative liability (asset)
                    total_liabilities -= balance  # Subtract because it's a credit
            else:
                if balance >= 0:
                    total_assets += balance
                else:
                    total_liabilities += abs(balance)
    
    net_worth = total_assets - total_liabilities
    
    return jsonify({
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'net_worth': net_worth
    })

@main.route('/api/dashboard/accounts')
def api_dashboard_accounts():
    """API endpoint for dashboard accounts data"""
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    model = get_model()
    
    accounts = model.get_accounts()
    transactions = model.get_transactions()
    
    # Calculate current balances
    balances = calculate_balances(accounts, transactions)
    
    # Add balance to each account
    for account in accounts:
        account['balance'] = balances.get(account['account_type'], 0)
    
    return jsonify(accounts)

@main.route('/api/dashboard/recent-transactions')
def api_dashboard_recent_transactions():
    """API endpoint for recent transactions"""
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    model = get_model()
    
    # Get last 10 transactions
    transactions = model.get_transactions()
    
    # Sort by date (newest first) and take last 10
    transactions.sort(key=lambda x: x['date'], reverse=True)
    recent_transactions = transactions[:10]
    
    return jsonify(recent_transactions)

@main.route('/api/dashboard/budgets')
def api_dashboard_budgets():
    """API endpoint for active budgets"""
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    model = get_model()
    
    budgets = model.get_budgets()
    transactions = model.get_transactions()
    
    # Add status and spending info to each budget
    today = datetime.now().strftime("%Y-%m-%d")
    active_budgets = []
    
    for budget in budgets:
        # Check if budget is active
        is_active = budget["start_date"] <= today <= budget["end_date"]
        if not is_active:
            continue
            
        # Calculate spent amount for this budget period
        spent = 0
        for transaction in transactions:
            if (transaction["type"] == "expense" and 
                transaction["category"] == budget["category"] and
                budget["start_date"] <= transaction["date"] <= budget["end_date"]):
                spent += transaction["amount"]
        
        budget["spent"] = spent
        budget["remaining"] = budget["amount"] - spent
        budget["percentage"] = (spent / budget["amount"]) * 100 if budget["amount"] > 0 else 0
        
        active_budgets.append(budget)
    
    return jsonify(active_budgets)

@main.route('/accounts')
def accounts():
    """View all accounts"""
    # Let frontend JavaScript handle authentication
    # This prevents the flash of login page issue
    model = get_model()
    
    accounts = model.get_accounts()
    return render_template('accounts.html', accounts=accounts)

@main.route('/accounts/add', methods=['GET', 'POST'])
def add_account():
    """Add a new account"""
    # Let frontend JavaScript handle authentication
    # This prevents the flash of login page issue
    model = get_model()
    
    if request.method == 'POST':
        account_type = request.form['account_type']
        initial_amount = float(request.form['initial_amount'])
        last_digits = request.form.get('last_digits', '')
        
        # For credit cards, initial amount should be negative (liability)
        if account_type == "Credit Card":
            initial_amount = -abs(initial_amount)
        
        account_data = {
            "account_type": account_type,
            "initial_amount": initial_amount,
            "last_digits": last_digits,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        model.create_account(account_data)
        flash(f"Account {account_type} added successfully!", "success")
        return redirect(url_for('main.accounts'))
    
    return render_template('add_account.html')

@main.route('/transactions')
def transactions():
    """View all transactions"""
    # Let frontend JavaScript handle authentication
    # This prevents the flash of login page issue
    model = get_model()
    
    accounts = model.get_accounts()
    categories = model.get_categories()
    transactions = model.get_transactions()
    
    # Calculate current balances
    balances = calculate_balances(accounts, transactions)
    
    # Get filter parameters
    transaction_type = request.args.get('type', '')
    category = request.args.get('category', '')
    account = request.args.get('account', '')
    
    # Build filter query
    filter_query = {}
    if transaction_type:
        filter_query['type'] = transaction_type
    if category:
        filter_query['category'] = category
    if account:
        if transaction_type == 'transfer':
            filter_query['$or'] = [{'from_account': account}, {'to_account': account}]
        else:
            filter_query['account'] = account
    
    filtered_transactions = model.get_transactions(filter_query)
    
    # Sort transactions by date (newest first)
    filtered_transactions.sort(key=lambda x: x['date'], reverse=True)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_transactions = len(filtered_transactions)
    total_pages = (total_transactions + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_transactions = filtered_transactions[start_index:end_index]
    
    return render_template('transactions.html', 
                          transactions=paginated_transactions,
                          accounts=accounts,
                          categories=categories,
                          balances=balances,
                          current_page=page,
                          total_pages=total_pages,
                          total_transactions=total_transactions,
                          transaction_type=transaction_type,
                          category=category,
                          account=account)

@main.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    """Add a new transaction"""
    # Let frontend JavaScript handle authentication
    # This prevents the flash of login page issue
    model = get_model()
    
    accounts = model.get_accounts()
    categories = model.get_categories()
    
    # Calculate current balances
    transactions = model.get_transactions()
    balances = calculate_balances(accounts, transactions)
    
    if request.method == 'POST':
        transaction_type = request.form.get('transaction_type', '')
        
        if not transaction_type:
            flash("Transaction type is required!", "error")
            return redirect(url_for('main.add_transaction'))
        
        transaction_data = {
            "type": transaction_type,
            "date": request.form.get('date', ''),
            "amount": float(request.form.get('amount', 0)),
            "description": request.form.get('description', ''),
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if transaction_type == "income":
            transaction_data["account"] = request.form.get('account', '')
            transaction_data["category"] = request.form.get('category', '')
        elif transaction_type == "expense":
            transaction_data["account"] = request.form.get('account', '')
            transaction_data["category"] = request.form.get('category', '')
        elif transaction_type == "transfer":
            transaction_data["from_account"] = request.form.get('from_account', '')
            transaction_data["to_account"] = request.form.get('to_account', '')
            transaction_data["category"] = request.form.get('category', '')
        
        # Validate required fields
        if not transaction_data["date"]:
            flash("Date is required!", "error")
            return redirect(url_for('main.add_transaction'))
        
        if transaction_data["amount"] <= 0:
            flash("Amount must be greater than zero!", "error")
            return redirect(url_for('main.add_transaction'))
        
        if transaction_type in ["income", "expense"]:
            if not transaction_data["account"]:
                flash("Account is required for income/expense transactions!", "error")
                return redirect(url_for('main.add_transaction'))
            if not transaction_data["category"]:
                flash("Category is required for income/expense transactions!", "error")
                return redirect(url_for('main.add_transaction'))
        elif transaction_type == "transfer":
            if not transaction_data["from_account"]:
                flash("From account is required for transfer transactions!", "error")
                return redirect(url_for('main.add_transaction'))
            if not transaction_data["to_account"]:
                flash("To account is required for transfer transactions!", "error")
                return redirect(url_for('main.add_transaction'))
            if not transaction_data["category"]:
                flash("Category is required for transfer transactions!", "error")
                return redirect(url_for('main.add_transaction'))
        
        model.create_transaction(transaction_data)
        flash("Transaction added successfully!", "success")
        return redirect(url_for('main.transactions'))
    
    return render_template('add_transaction.html', 
                          accounts=accounts,
                          categories=categories,
                          balances=balances)

@main.route('/budgets')
def budgets():
    """View all budgets"""
    # Let frontend JavaScript handle authentication
    # This prevents the flash of login page issue
    model = get_model()
    
    budgets = model.get_budgets()
    transactions = model.get_transactions()
    
    # Add status and spending info to each budget
    today = datetime.now().strftime("%Y-%m-%d")
    for budget in budgets:
        # Check if budget is active
        is_active = budget["start_date"] <= today <= budget["end_date"]
        budget["status"] = "ACTIVE" if is_active else "INACTIVE"
        
        # Calculate spent amount for this budget period
        spent = 0
        for transaction in transactions:
            if (transaction["type"] == "expense" and 
                transaction["category"] == budget["category"] and
                budget["start_date"] <= transaction["date"] <= budget["end_date"]):
                spent += transaction["amount"]
        
        budget["spent"] = spent
        budget["remaining"] = budget["amount"] - spent
        budget["percentage"] = (spent / budget["amount"]) * 100 if budget["amount"] > 0 else 0
    
    return render_template('budgets.html', budgets=budgets)

@main.route('/budgets/add', methods=['GET', 'POST'])
def add_budget():
    """Add a new budget"""
    # Let frontend JavaScript handle authentication
    # This prevents the flash of login page issue
    model = get_model()
    
    categories = model.get_categories()
    
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        period = request.form['period']
        
        # Calculate start and end dates based on period
        today = datetime.now().date()
        start_date = ""
        end_date = ""
        
        if period == "custom":
            start_date = request.form['start_date']
            end_date = request.form['end_date']
        elif period == "weekly":
            # Calculate Monday of this week
            start_date = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
            end_date = (today + timedelta(days=6 - today.weekday())).strftime("%Y-%m-%d")
        elif period == "monthly":
            # First day of current month
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            # Last day of current month
            last_day = calendar.monthrange(today.year, today.month)[1]
            end_date = today.replace(day=last_day).strftime("%Y-%m-%d")
        elif period == "yearly":
            start_date = today.replace(month=1, day=1).strftime("%Y-%m-%d")
            end_date = today.replace(month=12, day=31).strftime("%Y-%m-%d")
        
        budget_data = {
            "category": category,
            "amount": amount,
            "start_date": start_date,
            "end_date": end_date,
            "period": period
        }
        
        model.create_budget(budget_data)
        flash(f"Budget for {category} added successfully!", "success")
        return redirect(url_for('main.budgets'))
    
    return render_template('add_budget.html', categories=categories)

@main.route('/categories')
def categories():
    """View all categories"""
    # Let frontend JavaScript handle authentication
    # This prevents the flash of login page issue
    model = get_model()
    
    categories = model.get_categories()
    return render_template('categories.html', categories=categories)

@main.route('/categories/manage', methods=['GET', 'POST'])
def manage_categories():
    """Manage categories"""
    # Let frontend JavaScript handle authentication
    # This prevents the flash of login page issue
    model = get_model()
    
    categories = model.get_categories()
    
    if request.method == 'POST':
        category_type = request.form['category_type']
        action = request.form['action']
        category_name = request.form['category_name']
        
        if category_type in categories:
            if action == 'add':
                if category_name not in categories[category_type]:
                    categories[category_type].append(category_name)
                    model.update_categories(categories)
                    flash(f"Category '{category_name}' added to {category_type}!", "success")
            elif action == 'remove':
                if category_name in categories[category_type]:
                    categories[category_type].remove(category_name)
                    model.update_categories(categories)
                    flash(f"Category '{category_name}' removed from {category_type}!", "success")
        
        return redirect(url_for('main.categories'))
    
    return render_template('manage_categories.html', categories=categories)

@main.route('/info')
def info():
    """View information page - info is common for all users"""
    # Use FinanceModel without user context for info page
    model = FinanceModel()
    
    info_data = model.get_info()
    return render_template('info.html', info=info_data)

@main.route('/login')
def login_page():
    """Login page"""
    return render_template('login.html')

@main.route('/register')
def register_page():
    """Registration page"""
    return render_template('register.html')

@main.route('/profile')
def profile_page():
    """User profile page"""
    # Let frontend JavaScript handle authentication
    # This prevents the flash of login page issue
    return render_template('profile.html')
