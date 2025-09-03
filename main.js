// Main JavaScript for Marcos Jr. Sentiment Analysis System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeComponents();
});

function initializeComponents() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add smooth scrolling to anchor links
    initializeSmoothScrolling();
    
    // Add loading states to forms
    initializeFormLoadingStates();
    
    // Initialize animations
    initializeAnimations();
    
    // Add keyboard navigation support
    initializeKeyboardNavigation();
}

function initializeSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initializeFormLoadingStates() {
    // Add loading states to all forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
                submitBtn.disabled = true;
                
                // Re-enable button after 10 seconds as fallback
                setTimeout(() => {
                    if (submitBtn.disabled) {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }
                }, 10000);
            }
        });
    });
}

function initializeAnimations() {
    // Add fade-in animation to cards when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
}

function initializeKeyboardNavigation() {
    // Add keyboard navigation for star ratings
    document.querySelectorAll('.stars').forEach(starsContainer => {
        const stars = starsContainer.querySelectorAll('.star');
        
        starsContainer.addEventListener('keydown', function(e) {
            const currentFocus = document.activeElement;
            const currentIndex = Array.from(stars).indexOf(currentFocus);
            
            switch(e.key) {
                case 'ArrowRight':
                case 'ArrowUp':
                    e.preventDefault();
                    const nextIndex = Math.min(currentIndex + 1, stars.length - 1);
                    stars[nextIndex].focus();
                    break;
                case 'ArrowLeft':
                case 'ArrowDown':
                    e.preventDefault();
                    const prevIndex = Math.max(currentIndex - 1, 0);
                    stars[prevIndex].focus();
                    break;
                case 'Enter':
                case ' ':
                    e.preventDefault();
                    if (currentFocus && currentFocus.classList.contains('star')) {
                        currentFocus.click();
                    }
                    break;
            }
        });
        
        // Make stars focusable
        stars.forEach((star, index) => {
            star.setAttribute('tabindex', index === 0 ? '0' : '-1');
            star.setAttribute('role', 'button');
            star.setAttribute('aria-label', `Rate ${index + 1} star${index + 1 > 1 ? 's' : ''}`);
        });
    });
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for use in other scripts
window.SentimentAnalysis = {
    showNotification,
    validateForm,
    formatDate,
    debounce
};

// Handle network errors gracefully
window.addEventListener('online', function() {
    showNotification('Connection restored!', 'success');
});

window.addEventListener('offline', function() {
    showNotification('You are currently offline. Some features may not work.', 'warning');
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('An unexpected error occurred. Please try again.', 'danger');
});

// Add print functionality
function printPage() {
    window.print();
}

// Add export functionality for admin data
function exportTableData(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = Array.from(cols).map(col => 
            '"' + col.textContent.trim().replace(/"/g, '""') + '"'
        );
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Make functions available globally
window.printPage = printPage;
window.exportTableData = exportTableData;
