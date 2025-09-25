// Script for PaisaTrack

// Function to get authentication headers
function getAuthHeaders() {
    const token = localStorage.getItem('authToken');
    if (token) {
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }
    return {
        'Content-Type': 'application/json'
    };
}

// Function to check if user is authenticated
function isAuthenticated() {
    return !!localStorage.getItem('authToken');
}

// Function to redirect to login if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/login';
    }
}

// Function to format currency
function formatCurrency(amount) {
    // Format as Indian Rupees
    if (amount < 0) {
        return "-₹" + Math.abs(amount).toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }
    return "₹" + amount.toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Function to update transaction form based on type
function updateTransactionForm() {
    const type = document.getElementById('transaction_type').value;
    const accountGroup = document.getElementById('account_group');
    const fromAccountGroup = document.getElementById('from_account_group');
    const toAccountGroup = document.getElementById('to_account_group');
    const categoryGroup = document.getElementById('category_group');
    
    // Hide all groups first
    accountGroup.style.display = 'none';
    fromAccountGroup.style.display = 'none';
    toAccountGroup.style.display = 'none';
    categoryGroup.style.display = 'none';
    
    if (type === 'income' || type === 'expense') {
        accountGroup.style.display = 'block';
        categoryGroup.style.display = 'block';
    } else if (type === 'transfer') {
        fromAccountGroup.style.display = 'block';
        toAccountGroup.style.display = 'block';
        categoryGroup.style.display = 'block';
    }
}

// Function to handle credit card payment special case
function handleCreditCardPayment() {
    const toAccount = document.getElementById('to_account');
    const category = document.getElementById('category');
    
    if (toAccount && toAccount.value === 'Credit Card') {
        category.value = 'Credit Card Payment';
        category.disabled = true;
    } else {
        category.disabled = false;
    }
}

// Initialize date pickers
document.addEventListener('DOMContentLoaded', function() {
    // Set today's date as default for date inputs
    const today = new Date().toISOString().split('T')[0];
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            input.value = today;
        }
    });
    
    // Add event listeners
    const transactionType = document.getElementById('transaction_type');
    if (transactionType) {
        transactionType.addEventListener('change', updateTransactionForm);
        updateTransactionForm(); // Initial call
    }
    
    const toAccount = document.getElementById('to_account');
    if (toAccount) {
        toAccount.addEventListener('change', handleCreditCardPayment);
        handleCreditCardPayment(); // Initial call
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Validate amount
            const amountInput = form.querySelector('input[name="amount"]');
            if (amountInput && (isNaN(amountInput.value) || parseFloat(amountInput.value) <= 0)) {
                e.preventDefault();
                alert('Please enter a valid positive amount.');
                return;
            }
            
            // Validate account selection for income (Credit Card not allowed)
            const accountSelect = form.querySelector('select[name="account"]');
            if (accountSelect && form.querySelector('select[name="transaction_type"]') && 
                form.querySelector('select[name="transaction_type"]').value === 'income' &&
                accountSelect.value === 'Credit Card') {
                e.preventDefault();
                alert('Credit Card cannot receive income.');
                return;
            }
        });
    });
    
    // Responsive enhancements
    handleResponsiveLayout();
    window.addEventListener('resize', handleResponsiveLayout);
});

// Function to confirm deletion
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Function to toggle advanced filters
function toggleFilters() {
    const filterSection = document.getElementById('filter-section');
    if (filterSection) {
        filterSection.style.display = filterSection.style.display === 'none' ? 'block' : 'none';
    }
}

// Handle responsive layout adjustments
function handleResponsiveLayout() {
    const width = window.innerWidth;
    
    // Adjust navbar behavior for mobile
    const navbar = document.querySelector('.navbar-collapse');
    if (navbar) {
        if (width < 992) {
            // On mobile, ensure navbar is collapsed by default
            navbar.classList.remove('show');
        }
    }
    
    // Adjust card layouts for different screen sizes
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        if (width < 576) {
            // On extra small screens, reduce padding
            card.classList.add('px-2');
        } else {
            card.classList.remove('px-2');
        }
    });
    
    // Adjust button layouts for mobile
    const actionButtons = document.querySelectorAll('.btn-action');
    actionButtons.forEach(button => {
        if (width < 576) {
            // On mobile, make buttons full width
            button.classList.add('w-100');
            button.classList.remove('me-2');
        } else {
            button.classList.remove('w-100');
            button.classList.add('me-2');
        }
    });
    
    // Adjust table responsiveness
    const tables = document.querySelectorAll('.table-responsive');
    tables.forEach(table => {
        if (width < 768) {
            // On mobile, ensure tables are scrollable
            table.classList.add('overflow-auto');
        }
    });
}

// Enhanced toggle filters function with responsive behavior
function toggleFilters() {
    const filterSection = document.getElementById('filter-section');
    if (filterSection) {
        const isHidden = filterSection.style.display === 'none';
        filterSection.style.display = isHidden ? 'block' : 'none';
        
        // On mobile, scroll to filters when opened
        if (isHidden && window.innerWidth < 768) {
            filterSection.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// Check authentication on page load and redirect if needed
document.addEventListener('DOMContentLoaded', function() {
    // Get current path
    const path = window.location.pathname;
    
    // Define protected routes
    const protectedRoutes = [
        '/dashboard',
        '/accounts',
        '/accounts/add',
        '/transactions',
        '/transactions/add',
        '/budgets',
        '/budgets/add',
        '/categories',
        '/categories/manage',
        '/profile'
    ];
    
    // Check if current path is a protected route
    const isProtectedRoute = protectedRoutes.some(route => path.startsWith(route));
    
    // If it's a protected route and user is not authenticated, redirect to login
    if (isProtectedRoute && !isAuthenticated()) {
        window.location.href = '/login';
    }
    
    // If user is authenticated and on login/register page, redirect to dashboard
    const isAuthPage = path === '/login' || path === '/register';
    if (isAuthPage && isAuthenticated()) {
        window.location.href = '/dashboard';
    }
});

// Intercept all AJAX requests to add auth token
(function() {
    const originalFetch = window.fetch;
    window.fetch = function() {
        const args = Array.prototype.slice.call(arguments);
        const url = args[0];
        const options = args[1] || {};
        
        // Add auth token to headers if user is authenticated
        if (isAuthenticated()) {
            options.headers = options.headers || {};
            if (!options.headers['Authorization']) {
                options.headers['Authorization'] = 'Bearer ' + localStorage.getItem('authToken');
            }
        }
        
        return originalFetch.apply(this, [url, options]);
    };
    
    // Also intercept XMLHttpRequest for older code
    const originalXHROpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function() {
        const xhr = this;
        const originalSend = xhr.send;
        
        xhr.addEventListener('readystatechange', function() {
            if (xhr.readyState === 1) { // OPENED
                if (isAuthenticated()) {
                    xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('authToken'));
                }
            }
        });
        
        xhr.send = function() {
            return originalSend.apply(xhr, arguments);
        };
        
        return originalXHROpen.apply(xhr, arguments);
    };
})();