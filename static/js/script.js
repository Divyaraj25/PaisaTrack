// Script for PaisaTrack

// Authentication utilities
const AuthUtils = {
    // Get token from localStorage
    getToken: function() {
        return localStorage.getItem('paisatrack_token');
    },
    
    // Set token in localStorage
    setToken: function(token) {
        localStorage.setItem('paisatrack_token', token);
    },
    
    // Remove token from localStorage
    removeToken: function() {
        localStorage.removeItem('paisatrack_token');
    },
    
    // Get user info from localStorage
    getUser: function() {
        const userStr = localStorage.getItem('paisatrack_user');
        return userStr ? JSON.parse(userStr) : null;
    },
    
    // Set user info in localStorage
    setUser: function(user) {
        localStorage.setItem('paisatrack_user', JSON.stringify(user));
    },
    
    // Remove user info from localStorage
    removeUser: function() {
        localStorage.removeItem('paisatrack_user');
    },
    
    // Check if user is authenticated
    isAuthenticated: function() {
        return !!this.getToken();
    },
    
    // Get authorization headers
    getAuthHeaders: function() {
        const token = this.getToken();
        return token ? {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        } : {
            'Content-Type': 'application/json'
        };
    },
    
    // Logout user
    logout: function() {
        this.removeToken();
        this.removeUser();
        window.location.href = '/auth/login';
    }
};

// API utilities
const ApiUtils = {
    // Make authenticated API request
    request: async function(url, options = {}) {
        const defaultOptions = {
            headers: AuthUtils.getAuthHeaders()
        };
        
        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };
        
        try {
            const response = await fetch(url, mergedOptions);
            
            // Handle authentication errors
            if (response.status === 401) {
                AuthUtils.logout();
                return null;
            }
            
            return response;
        } catch (error) {
            console.error('API request failed:', error);
            return null;
        }
    },
    
    // GET request
    get: function(url) {
        return this.request(url, { method: 'GET' });
    },
    
    // POST request
    post: function(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    // PUT request
    put: function(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    // DELETE request
    delete: function(url) {
        return this.request(url, { method: 'DELETE' });
    }
};

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
    // Initialize authentication state
    initializeAuth();
    
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

// Initialize authentication state
function initializeAuth() {
    // Check if we're on login page
    if (window.location.pathname === '/auth/login') {
        return;
    }
    
    // Check if user is authenticated
    if (!AuthUtils.isAuthenticated()) {
        // Redirect to login if not authenticated
        window.location.href = '/auth/login';
        return;
    }
    
    // Update UI with user info
    updateUserUI();
}

// Update UI with user information
function updateUserUI() {
    const user = AuthUtils.getUser();
    if (user) {
        // Update navbar with user info
        const userDropdown = document.getElementById('navbarDropdown');
        if (userDropdown) {
            userDropdown.innerHTML = `<i class="bi bi-person-circle"></i> ${user.username}`;
        }
    }
}

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

// Handle logout
function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        // Make logout API call
        ApiUtils.post('/auth/logout', {})
            .then(response => {
                if (response && response.ok) {
                    AuthUtils.logout();
                } else {
                    // Force logout even if API call fails
                    AuthUtils.logout();
                }
            })
            .catch(error => {
                console.error('Logout error:', error);
                // Force logout even if API call fails
                AuthUtils.logout();
            });
    }
}

// Add event listeners for logout buttons
document.addEventListener('DOMContentLoaded', function() {
    const logoutButtons = document.querySelectorAll('[data-logout]');
    logoutButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            handleLogout();
        });
    });
});