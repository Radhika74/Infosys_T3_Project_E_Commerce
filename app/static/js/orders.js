// Sample Order Data
const orders = [
    { id: "#5552875", name: "Rahul Sharma", location: "Bengaluru, Karnataka", amount: "₹7,510.00", status: "In Transit" },
    { id: "#5552876", name: "Priya Mehta", location: "Mumbai, Maharashtra", amount: "₹2,140.00", status: "Delivered" },
    { id: "#5552878", name: "Anjali Singh", location: "Kolkata, West Bengal", amount: "₹910.00", status: "In Transit" },
    { id: "#5552879", name: "Amit Gupta", location: "Noida, Uttar Pradesh", amount: "₹7,220.00", status: "Delivered" },
    { id: "#5552899", name: "Sunita Nair", location: "Kochi, Kerala", amount: "₹950.00", status: "In Transit" },
];

// Function to Render Orders
function renderOrders() {
    const ordersTable = document.getElementById("orders-list");
    ordersTable.innerHTML = ""; // Clear previous orders

    orders.forEach((order, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.name}</td>
            <td>${order.location}</td>
            <td>${order.amount}</td>
            <td>
                <select class="status-select" id="status-${index}">
                    <option value="In Transit" ${order.status === "In Transit" ? "selected" : ""}>In Transit</option>
                    <option value="Delivered" ${order.status === "Delivered" ? "selected" : ""}>Delivered</option>
                </select>
            </td>
            <td><button class="update-btn" onclick="updateStatus(${index})">Update</button></td>
        `;

        ordersTable.appendChild(row);
    });
}

// Function to Update Order Status
function updateStatus(index) {
    const newStatus = document.getElementById(`status-${index}`).value;
    orders[index].status = newStatus;
    alert(`Order ${orders[index].id} status updated to "${newStatus}"`);
}

// Initialize Orders on Load
document.addEventListener("DOMContentLoaded", renderOrders);
