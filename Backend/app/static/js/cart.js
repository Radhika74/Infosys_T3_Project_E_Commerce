document.addEventListener("DOMContentLoaded", function () {
    // Sample Cart Data (You can replace this with real data from a database)
    let cartItems = [
        { id: 1, name: "T-Shirt", price: 499, quantity: 1, image: "tshirt.jpg" },
        { id: 2, name: "Jeans", price: 999, quantity: 1, image: "jeans.jpg" },
        { id: 3, name: "Shoes", price: 1499, quantity: 1, image: "shoes.jpg" }
    ];

    const cartContainer = document.querySelector(".cart-items");
    const totalItemsElement = document.getElementById("total-items");
    const totalPriceElement = document.getElementById("total-price");

    function renderCart() {
        cartContainer.innerHTML = "";
        let totalItems = 0;
        let totalPrice = 0;

        cartItems.forEach(item => {
            totalItems += item.quantity;
            totalPrice += item.price * item.quantity;

            const cartItem = document.createElement("div");
            cartItem.classList.add("cart-item");

            cartItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}">
                <div class="cart-item-details">
                    <h4>${item.name}</h4>
                    <p>Price: ₹${item.price}</p>
                    <div class="quantity-container">
                        <button class="quantity-btn decrease" data-id="${item.id}">-</button>
                        <span>${item.quantity}</span>
                        <button class="quantity-btn increase" data-id="${item.id}">+</button>
                    </div>
                </div>
                <button class="remove-btn" data-id="${item.id}">Remove</button>
            `;

            cartContainer.appendChild(cartItem);
        });

        totalItemsElement.textContent = totalItems;
        totalPriceElement.textContent = totalPrice.toFixed(2);
    }

    cartContainer.addEventListener("click", function (e) {
        const id = parseInt(e.target.dataset.id);
        if (e.target.classList.contains("increase")) {
            cartItems = cartItems.map(item => item.id === id ? { ...item, quantity: item.quantity + 1 } : item);
        } else if (e.target.classList.contains("decrease")) {
            cartItems = cartItems.map(item => item.id === id && item.quantity > 1 ? { ...item, quantity: item.quantity - 1 } : item);
        } else if (e.target.classList.contains("remove-btn")) {
            cartItems = cartItems.filter(item => item.id !== id);
        }
        renderCart();
    });

    document.querySelector(".checkout-btn").addEventListener("click", function () {
        alert("Proceeding to checkout...");
    });

    renderCart();
});
