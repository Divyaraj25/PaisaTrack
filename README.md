# PaisaTrack - Personal Finance Tracker

![PaisaTrack Dashboard](screenshots/dashboard.png)

PaisaTrack is a comprehensive personal finance management web application built with Python Flask and MongoDB. It helps you track income, expenses, transfers, budgets, and monitor your net worth over time.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Account Management**: Track multiple account types (Cash, Bank, Credit Card, etc.)
- **Transaction Tracking**: Record income, expenses, and transfers between accounts
- **Budget Management**: Set and monitor budgets for different categories
- **Category Management**: Customizable income, expense, and transfer categories
- **Financial Dashboard**: Overview of account balances, net worth, and recent transactions
- **Reporting**: Detailed transaction history with filtering and pagination
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Data Persistence**: MongoDB database for reliable data storage
- **User Authentication**: Secure user registration and login with JWT tokens
- **Data Isolation**: Each user has their own private data
- **Password Recovery**: Forgot password functionality with email verification

## Technologies Used

- **Backend**: Python 3, Flask
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Template Engine**: Jinja2
- **Styling**: Bootstrap 5, Custom CSS
- **Icons**: Bootstrap Icons
- **Authentication**: JWT (JSON Web Tokens)

## Project Structure

```
paisatrack/
│
├── app.py                 # Main application entry point
├── init_mongo.py          # Database initialization script
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
│
├── models/
│   ├── finance.py         # Finance model with database operations
│   └── user.py            # User model with authentication
│
├── routes/
│   ├── main.py            # Flask routes and controllers
│   └── auth.py            # Authentication routes
│
├── utils/
│   └── database.py        # Database connection utilities
│
├── templates/
│   ├── base.html          # Base template with common layout
│   ├── index.html         # Dashboard page
│   ├── accounts.html      # Accounts management page
│   ├── add_account.html   # Add new account page
│   ├── transactions.html  # Transactions listing page
│   ├── add_transaction.html # Add new transaction page
│   ├── budgets.html       # Budgets management page
│   ├── add_budget.html    # Add new budget page
│   ├── categories.html    # Categories management page
│   ├── manage_categories.html # Manage categories page
│   ├── info.html          # Information page
│   ├── login.html         # User login page
│   ├── register.html      # User registration page
│   ├── profile.html       # User profile page
│   ├── forgot_password.html # Forgot password page
│   └── reset_password.html # Reset password page
│
├── static/
│   ├── css/
│   │   └── style.css      # Custom CSS styles
│   └── js/
│       └── script.js      # Custom JavaScript
│
└── screenshots/           # Application screenshots
    ├── dashboard.png      # Dashboard screenshot
    ├── transactions.png   # Transactions page screenshot
    ├── accounts.png       # Accounts page screenshot
    ├── budgets.png        # Budgets page screenshot
    └── add_transaction.png # Add transaction page screenshot
```

## Setup and Installation

### Prerequisites

- Python 3.7 or higher
- MongoDB 4.0 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd paisatrack
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install MongoDB**:
   - Download and install MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Follow the installation instructions for your operating system

## Database Setup

1. **Start MongoDB service**:
   - On Windows: Start the MongoDB service from Services
   - On macOS: `brew services start mongodb-community`
   - On Linux: `sudo systemctl start mongod`

2. **Initialize the database**:
   ```bash
   python init_mongo.py
   ```

   This script will:
   - Create the `paisatrackIN` database
   - Initialize default categories
   - Set up default information data
   - Prepare user collection with proper indexes

## Running the Application

1. **Start the Flask application**:
   ```bash
   python app.py
   ```

2. **Access the application**:
   Open your web browser and navigate to `http://localhost:5000`

## Usage

### Adding Accounts

1. Navigate to the "Accounts" page
2. Click "Add Account"
3. Enter account details:
   - Account Type (Cash, Bank Account, Credit Card, etc.)
   - Initial Amount
   - Last 4 digits (optional, for credit/debit cards)

### Recording Transactions

1. Navigate to the "Transactions" page
2. Click "Add Transaction"
3. Select transaction type:
   - **Income**: Money received
   - **Expense**: Money spent
   - **Transfer**: Money moved between accounts
4. Fill in the required details and submit

### Setting Budgets

1. Navigate to the "Budgets" page
2. Click "Add Budget"
3. Select a category and set budget amount
4. Choose time period (weekly, monthly, yearly, or custom)

### Managing Categories

1. Navigate to the "Categories" page
2. Click "Manage Categories"
3. Add or remove categories as needed

## Authentication

PaisaTrack now includes user authentication to ensure each user's financial data remains private and secure.

### Registration

1. Navigate to the registration page (`/register`)
2. Fill in your details:
   - Username
   - Email address
   - Contact number
   - Password (minimum 6 characters)
3. Click "Register"
4. You'll be automatically logged in and redirected to the dashboard

### Login

1. Navigate to the login page (`/login`)
2. Enter your username and password
3. Click "Login"
4. You'll be redirected to the dashboard

### Forgot Password

1. Navigate to the login page (`/login`)
2. Click "Forgot Password?" link
3. Enter your email address
4. If the email exists in the system, you'll receive a reset link
5. Click the reset link to set a new password
6. Login with your new password

### Profile Management

1. Click on your username in the top navigation bar
2. View your profile information
3. Update your details as needed
4. Change your password (coming soon)
5. Logout when finished

### Security Features

- Passwords are securely hashed using Werkzeug
- JWT tokens for session management
- Token expiration after 24 hours
- Automatic token validation on all protected routes
- Data isolation - users can only access their own data
- Password recovery with secure token-based reset

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)
*Overview of account balances, net worth, and recent transactions*

### Transactions
![Transactions](screenshots/transactions.png)
*Detailed transaction history with filtering and pagination*

### Accounts
![Accounts](screenshots/accounts.png)
*Account management interface*

### Budgets
![Budgets](screenshots/budgets.png)
*Budget tracking and management*

### Add Transaction
![Add Transaction](screenshots/add_transaction.png)
*Transaction creation form with dynamic category selection*

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard with account balances and net worth |
| `/accounts` | GET | List all accounts |
| `/accounts/add` | GET/POST | Add new account |
| `/transactions` | GET | List all transactions with filtering |
| `/transactions/add` | GET/POST | Add new transaction |
| `/budgets` | GET | List all budgets |
| `/budgets/add` | GET/POST | Add new budget |
| `/categories` | GET | List all categories |
| `/categories/manage` | GET/POST | Manage categories |
| `/info` | GET | Application information |

## Folder Structure Details

### Models (`models/`)
- `finance.py`: Contains the FinanceModel class with all database operations for accounts, transactions, budgets, categories, and info.
- `user.py`: Contains the UserModel class with authentication logic.

### Routes (`routes/`)
- `main.py`: Contains all Flask routes and controller logic for the application.
- `auth.py`: Contains authentication routes for user registration and login.

### Utilities (`utils/`)
- `database.py`: Database connection utilities and helper functions.

### Templates (`templates/`)
- Base template and all HTML pages with Jinja2 templating.

### Static Files (`static/`)
- CSS stylesheets and JavaScript files for frontend styling and functionality.

### Screenshots (`screenshots/`)
- Visual documentation of the application interface.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**PaisaTrack** - Your personal finance management solution