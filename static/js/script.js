// Script for PaisaTrack

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