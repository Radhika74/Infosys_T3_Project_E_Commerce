document.querySelectorAll(".admin-btn").forEach(button => {
    button.addEventListener("click", () => {
        alert(button.textContent + " clicked!");
    });
});
