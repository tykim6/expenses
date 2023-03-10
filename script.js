const url = "/data.json";

// Define the ID of the HTML table element to display the data
const tableId = "expenseTable";

// Fetch the data from the JSON file
fetch(url)
  .then((response) => response.json())
  .then((data) => {
    // Get a reference to the HTML table element
    const table = document.getElementById(tableId);

    // Loop through the data and add a row to the HTML table for each item
    console.log(data);
    data.forEach((item) => {
      const row = table.insertRow();
      Object.values(item).forEach((value) => {
        const cell = row.insertCell();
        cell.textContent = value;
      });
    });
  })
  .catch((error) => console.error(error));
