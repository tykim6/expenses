<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Expenses</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>

</head>

<body>
    <div id="app">
        <header>
            <h1>Expenses</h1>
        </header>
        <main>
                <h2>Current Balance</h3>
            <div class="balance">
                <?php include 'helpers/calc_balance.php'?>
            </div>
            <hr>
            <br>
            <div class="newExpense">
                <h2>New Expense</h3>
                <form method="POST" action="/helpers/add_expense.php">
                    <fieldset>
                        <legend>Who Paid?</legend>
                        <input type="radio" id="tyler" name="payer" value="Tyler">
                        <label for="tyler">Tyler</label>
                        <input type="radio" id="adi" name="payer" value="Adi">
                        <label for="adi">Adi</label>
                    </fieldset>
                    <fieldset>
                        <legend>Expense Name</legend>
                        <input type="text" id="expenseName" name="expenseName" placeholder="Expense Name">
                    </fieldset>
                    <fieldset>
                        <legend>Expense Amount</legend>
                        <input type="number" id="expenseAmount" name="expenseAmount" placeholder="Expense Amount">
                    </fieldset>
                    <fieldset>
                        <legend>Date</legend>
                        <input type="date" id="date" name="date" placeholder="Date">
                    </fieldset>
                    <br>
                    <div class="buttonRow">
                    <button type="submit" id="addButton" name="addButton">Add Expense</button>
                    </div>
            </div>
            </form>
    </div>
    </main>
<details>
    <summary>View All Transactions</summary>  
    <table id="expenseTable">
    <tr><th>Payer</th><th>Expense Name</th><th>Amount</th><th>Date</th><th>Delete</th></tr>
    <?php include 'helpers/get_all_trans.php'?>
    </table>
</details>

    <footer>
        <p>Copyright © 2023 Expenses Web App</p>
    </footer>
    </div>

</body>
<script type="module" src="script.js"></script>

</html>