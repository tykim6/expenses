<?php
// Connect to the database
$mysqli = new mysqli('localhost', 'root', 'tylerdkim', 'expenses');

// Check for connection errors
if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli->connect_error;
    exit();
}
// Calculate total expenses paid by each payer
$result = $mysqli->query("SELECT payer, SUM(expenseAmount) AS totalExpenses FROM expenses GROUP BY payer");
$paid = array('Tyler' => 0, 'Adi' => 0);
while ($row = $result->fetch_assoc()) {
    $paid[$row['payer']] = $row['totalExpenses'];
}
// Calculate balance for each payer
$totalBalance = $paid['Tyler'] - $paid['Adi'];
$adiOwes = abs($totalBalance) / 2;
if ($totalBalance < 0) {
    echo "Tyler owes Adi: $" . number_format($adiOwes, 2);
} else if ($totalBalance > 0) {
    echo "Adi owes Tyler: $" . number_format($adiOwes, 2);
} else {
    echo "Balanced!";
}


// Close database connection
$mysqli->close();
?>