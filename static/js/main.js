document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
        themeToggle.textContent = theme === 'light' ? '🌓' : '☀️';
    }
    
    // Mobile Navigation Toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.querySelector('.nav-links');
    
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        
        // Update aria-expanded
        const isExpanded = navLinks.classList.contains('active');
        navToggle.setAttribute('aria-expanded', isExpanded);
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    });
    
    // Message Auto-dismiss
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
    
    // Form Validation Enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Show validation message on blur
            input.addEventListener('blur', () => {
                validateInput(input);
            });
            
            // Live validation as user types
            input.addEventListener('input', () => {
                if (input.classList.contains('invalid')) {
                    validateInput(input);
                }
            });
        });
        
        form.addEventListener('submit', (e) => {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
    
    function validateInput(input) {
        const validityState = input.validity;
        const errorElement = input.nextElementSibling;
        
        if (!validityState.valid) {
            input.classList.add('invalid');
            
            if (!errorElement || !errorElement.classList.contains('error-message')) {
                const error = document.createElement('div');
                error.className = 'error-message';
                error.textContent = input.validationMessage;
                input.parentNode.insertBefore(error, input.nextSibling);
            }
            return false;
        } else {
            input.classList.remove('invalid');
            if (errorElement && errorElement.classList.contains('error-message')) {
                errorElement.remove();
            }
            return true;
        }
    }
    
    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));

    const featuredProducts = []; // Replace with actual logic to fetch featured products

    const productsList = document.getElementById('products-list');
    const categoriesButton = document.getElementById('categories-button');

    if (featuredProducts.length === 0) {
        // No featured products, show the categories button
        categoriesButton.style.display = 'block';
    } else {
        // Logic to display featured products
        featuredProducts.forEach(product => {
            const productItem = document.createElement('div');
            productItem.className = 'product-item';
            productItem.textContent = product.name; // Adjust to display product details
            productsList.appendChild(productItem);
        });
    }
}); 

// Function to show the popup after 3 seconds
function showPopup() {
    const popup = document.getElementById("whatsapp-popup");
    if (popup) {
        popup.style.display = "flex";
    }
}

window.onload = function () {
    // Check if the popup has been shown before
    const popupShown = localStorage.getItem('whatsappPopupShown');
    
    // Check if the current page is the home page
    const isHomePage = window.location.pathname === '/'; // Adjust this if your home page path is different

    if (!popupShown && isHomePage) {
        setTimeout(() => {
            showPopup();
            // Mark the popup as shown
            localStorage.setItem('whatsappPopupShown', 'true');
        }, 3000);
    }
};

// Function to close the popup
function closePopup() {
    const popup = document.getElementById("whatsapp-popup");
    if (popup) {
        popup.style.display = "none";
    }
}

// Attach the closePopup function to the close button of the popup
const closeButton = document.querySelector("#whatsapp-popup .close-button");
if (closeButton) {
    closeButton.addEventListener('click', closePopup);
}

// Prevent popup from being triggered by other actions
document.addEventListener('click', (e) => {
    if (e.target.closest('#whatsapp-popup') || e.target.closest('.close-button')) {
        return;
    }
    closePopup();
});

