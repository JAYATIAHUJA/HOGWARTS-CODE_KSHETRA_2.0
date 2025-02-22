// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Update cart counter function
    function updateCartCounter(count) {
        const counter = document.querySelector('.cart-counter');
        if (counter) {
            counter.textContent = count;
            // Add animation class
            counter.classList.add('bounce');
            // Remove animation class after animation completes
            setTimeout(() => {
                counter.classList.remove('bounce');
            }, 300);
        }
    }

    // Add to cart function
    async function addToCart(productId, quantity = 1) {
        try {
            const response = await fetch(`/products/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ quantity: quantity })
            });

            const data = await response.json();
            
            if (response.ok) {
                updateCartCounter(data.cart_total);
                showNotification('Item added to cart successfully!', 'success');
            } else {
                showNotification(data.error || 'Failed to add item to cart', 'error');
            }
        } catch (error) {
            console.error('Error adding to cart:', error);
            showNotification('Failed to add item to cart', 'error');
        }
    }

    // Get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Show notification function
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Add event listeners to "Add to Cart" buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const productId = button.dataset.productId;
            const quantity = parseInt(button.dataset.quantity || 1);
            addToCart(productId, quantity);
        });
    });

    // Update quantity functionality
    const quantityInputs = document.querySelectorAll('.cart-quantity');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.dataset.itemId;
            const newQuantity = this.value;
            updateCartItem(itemId, newQuantity);
        });
    });

    // Remove item functionality
    const removeButtons = document.querySelectorAll('.remove-item-btn');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            removeFromCart(itemId);
        });
    });
});

// Function to update cart item quantity
function updateCartItem(itemId, quantity) {
    fetch(`/products/cart/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            updateCartDisplay(data);
            showNotification('Cart updated successfully!', 'success');
        } else {
            showNotification(data.message || 'Error updating cart', 'error');
            // Reset to previous quantity if error
            document.querySelector(`[data-item-id="${itemId}"]`).value = data.current_quantity;
        }
    })
    .catch(error => {
        showNotification('Error updating cart', 'error');
    });
}

// Function to remove item from cart
function removeFromCart(itemId) {
    fetch(`/products/cart/remove/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const itemElement = document.querySelector(`#cart-item-${itemId}`);
            itemElement.remove();
            updateCartDisplay(data);
            showNotification('Item removed from cart', 'success');
            
            // Check if cart is empty
            if (data.cart_total === 0) {
                showEmptyCartMessage();
            }
        } else {
            showNotification(data.message || 'Error removing item', 'error');
        }
    })
    .catch(error => {
        showNotification('Error removing item', 'error');
    });
}

// Helper function to update cart display
function updateCartDisplay(data) {
    // Update cart counter
    updateCartCounter(data.cart_total);
    
    // Update subtotal and total
    const subtotalElement = document.querySelector('.cart-subtotal');
    const totalElement = document.querySelector('.cart-total');
    if (subtotalElement) subtotalElement.textContent = `$${data.subtotal}`;
    if (totalElement) totalElement.textContent = `$${data.total}`;
    
    // Update item subtotal
    if (data.item_subtotal && data.item_id) {
        const itemSubtotalElement = document.querySelector(`#item-subtotal-${data.item_id}`);
        if (itemSubtotalElement) {
            itemSubtotalElement.textContent = `$${data.item_subtotal}`;
        }
    }
}

// Helper function to show empty cart message
function showEmptyCartMessage() {
    const cartContent = document.querySelector('.cart-content');
    const emptyCartMessage = `
        <div class="empty-cart">
            <h2>Your cart is empty</h2>
            <p>Looks like you haven't added any items to your cart yet.</p>
            <a href="/products/" class="btn btn-primary">Continue Shopping</a>
        </div>
    `;
    if (cartContent) {
        cartContent.innerHTML = emptyCartMessage;
    }
} 