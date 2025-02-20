document.getElementById("addProductForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const name = document.getElementById("productName").value;
    const price = document.getElementById("productPrice").value;
    const category = document.getElementById("productCategory").value;
    
    const productList = document.getElementById("productList");
    const newRow = document.createElement("tr");
    
    newRow.innerHTML = `
        <td><img src="placeholder.jpg" width="50"></td>
        <td>${name}</td>
        <td>₹${price}</td>
        <td>${category}</td>
        <td><button class="delete-btn">Delete</button></td>
    `;
    
    productList.appendChild(newRow);
    
    document.getElementById("addProductForm").reset();
    
    // Delete functionality
    newRow.querySelector(".delete-btn").addEventListener("click", function() {
        newRow.remove();
    });
});
