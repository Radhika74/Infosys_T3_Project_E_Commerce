// Simulating fetching product data
const products = [
    { id: 1, name: 'Stylish Jacket', price: '₹2999', image: 'product1.jpg' },
    { id: 2, name: 'Casual T-shirt', price: '₹799', image: 'product2.jpg' },
    { id: 3, name: 'Elegant Dress', price: '₹4999', image: 'product3.jpg' },
    { id: 4, name: 'Leather Shoes', price: '₹2499', image: 'product4.jpg' },
];

function displayProducts() {
    const productGrid = document.querySelector('.product-grid');
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.classList.add('product');
        productCard.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>${product.price}</p>
            <button>Add to Cart</button>
        `;
        productGrid.appendChild(productCard);
    });
}

document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Basic validation (in a real app, you'd use a backend for authentication)
    if (email && password) {
        alert('Login successful!');
        // Redirect to home or dashboard
    } else {
        alert('Please enter valid credentials');
    }
});

window.onload = displayProducts;
