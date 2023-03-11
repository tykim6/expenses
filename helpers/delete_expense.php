<?php

// database connection code
$servername = "localhost";
$username = "root";
$password = "tylerdkim";
$dbname = "expenses";

$conn = new mysqli($servername, $username, $password, $dbname);

// retrieve data from expenses table
$sql = "SELECT * FROM expenses";
$result = $conn->query($sql);
// Create connection
// Get expenseNo value from POST request
$expenseNo = $_POST['expenseNo'];

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

$sql = "DELETE FROM expenses WHERE expenseNo = $expenseNo";

if (mysqli_query($conn, $sql)) {
    echo "Expense deleted successfully";
} else {
    echo "Error deleting expense: " . mysqli_error($conn);
}

mysqli_close($conn);
?>