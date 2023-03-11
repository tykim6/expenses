<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Expense</title>
    <link rel="stylesheet" href="../style.css">
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>

</head>

<?php
session_start();

// connect to the database
$mysqli = new mysqli('localhost', 'id20436433_root', 'evyQrn1C2Wz!|MBx', 'expenses');

// check for connection errors
if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli->connect_error;
    exit();
}

// check if form was submitted
if(isset($_POST['addButton']))  {
    // get form data
    $payer = $_POST['payer'];
    $expenseName = $_POST['expenseName'];
    $expenseAmount = $_POST['expenseAmount'];
    $date = $_POST['date'];

    // check if any required form fields are empty
    if(empty($payer) || empty($expenseName) || empty($expenseAmount) || empty($date)) {
        echo "<br>";
        echo "Please fill out all fields before submitting the form.";
        echo "<hr>";
        echo "<br>";
        echo "<div class='buttonRow'><a href='../index.php'><button class=tryAgain type='button'>Try Again</button></a></div>";
        exit();
    }

    // insert form data into database
    $sql = "INSERT INTO expenses (payer, expenseName, expenseAmount, date) VALUES ('$payer', '$expenseName', '$expenseAmount', '$date')";
    if ($mysqli->query($sql) === TRUE) {
        echo "New expense record created successfully!";
    } else {
        echo "Error: " . $sql . "<br>" . $mysqli->error;
    }
}

// close database connection
$mysqli->close();
session_destroy();
?>
<hr>
<div class='buttonRow'><a href='../index.php'><button class=tryAgain type='button'>Add Something Else</button></a></div>