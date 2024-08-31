// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    initializeBootstrapComponents();

    // Add event listeners for various interactions
    addEventListeners();

    // Initialize the shopping cart
    initializeCart();
});

function initializeBootstrapComponents() {
    // Initialize Bootstrap carousel
    $('.carousel').carousel({
        interval: 5000 // Change slide every 5 seconds
    });

    // Initialize Bootstrap tooltips
    $('[data-toggle="tooltip"]').tooltip();
}

function addEventListeners() {
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.btn-add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', addToCart);
    });

    // Search form
    const searchForm = document.querySelector('#search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearch);
    }

    // Newsletter subscription form
    const newsletterForm = document.querySelector('#newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleNewsletterSubscription);
    }
}

function addToCart(event) {
    const button = event.target;
    const productId = button.getAttribute('data-product-id');
    const productName = button.getAttribute('data-product-name');
    const productPrice = button.getAttribute('data-product-price');

    // In a real application, you would send this data to the server
    console.log(`Added to cart: ${productName} (ID: ${productId}) - Price: ${productPrice}`);

    // Update the cart count in the UI
    updateCartCount(1);

    // Show a confirmation message
    showNotification(`${productName} added to cart!`);
}

function updateCartCount(increment) {
    const cartCountElement = document.querySelector('#cart-count');
    if (cartCountElement) {
        let currentCount = parseInt(cartCountElement.textContent);
        cartCountElement.textContent = currentCount + increment;
    }
}

function handleSearch(event) {
    event.preventDefault();
    const searchInput = document.querySelector('#search-input');
    const searchTerm = searchInput.value.trim();

    if (searchTerm) {
        // In a real application, you would send this to the server or update the UI
        console.log(`Searching for: ${searchTerm}`);
        // Placeholder for search functionality
        showNotification(`Searching for "${searchTerm}"...`);
    }
}

function handleNewsletterSubscription(event) {
    event.preventDefault();
    const emailInput = document.querySelector('#newsletter-email');
    const email = emailInput.value.trim();

    if (email && isValidEmail(email)) {
        // In a real application, you would send this to the server
        console.log(`Newsletter subscription for: ${email}`);
        showNotification('Thank you for subscribing to our newsletter!');
        emailInput.value = ''; // Clear the input
    } else {
        showNotification('Please enter a valid email address.', 'error');
    }
}

function isValidEmail(email) {
    // Basic email validation
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showNotification(message, type = 'success') {
    const notificationElement = document.createElement('div');
    notificationElement.className = `alert alert-${type} alert-dismissible fade show`;
    notificationElement.role = 'alert';
    notificationElement.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    `;

    document.body.appendChild(notificationElement);

    // Remove the notification after 5 seconds
    setTimeout(() => {
        notificationElement.remove();
    }, 5000);
}

function initializeCart() {
    // This function would typically load the cart data from localStorage or a server
    console.log('Initializing shopping cart');
    // Placeholder for cart initialization
    updateCartCount(0);
}

// Add any additional functions or custom code here