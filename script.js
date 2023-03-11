const url = "data.json";

// Define the ID of the HTML table element to display the data
const tableId = "expenseTable";

// Add event listener to all delete buttons
const deleteButtons = document.querySelectorAll(".deleteButton");
deleteButtons.forEach((deleteButton) => {
  deleteButton.addEventListener("click", () => {
    const expenseNo = deleteButton.getAttribute("data-id");

    // Send AJAX request to delete expense from database
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "helpers/delete_expense.php", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
      if (this.status === 200) {
        // Remove row from HTML table
        const row = deleteButton.closest("tr");
        row.parentNode.removeChild(row);
      }
    };
    xhr.send(`expenseNo=${expenseNo}`);
  });
});
