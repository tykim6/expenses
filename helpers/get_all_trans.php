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

// create table to display data
if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    echo "<tr><td>" . $row["payer"] . "</td><td>" . $row["expenseName"] . "</td><td>" . $row["expenseAmount"] . "</td><td>" . $row["date"] . "</td><td>
    <button class='deleteButton' data-id='" . $row['expenseNo'] . "'>X</button></td>
          </tr>";
  }
} else {
  echo "0 results";
}

?>
