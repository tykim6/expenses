import os
import pandas as pd
import streamlit as st

# define filename
filename = "expenses.csv"

# Check if the CSV file exists. If not, create it with the necessary columns.
if not os.path.isfile(filename):
    db = pd.DataFrame(columns=["Who Paid", "Expense Name", "Expense Amount", "Date"])
    db.to_csv(filename, index=False)
else:
    try:
        db = pd.read_csv(filename)
        if db.empty:
            db = pd.DataFrame(
                columns=["Who Paid", "Expense Name", "Expense Amount", "Date"]
            )
    except pd.errors.EmptyDataError:
        db = pd.DataFrame(
            columns=["Who Paid", "Expense Name", "Expense Amount", "Date"]
        )


# Import the required libraries
import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

# Set the CSV filename
filename = "expenses.csv"

# Read the existing data from the CSV file, if it exists
try:
    db = pd.read_csv(filename)
except FileNotFoundError:
    db = pd.DataFrame(columns=["Who Paid", "Expense Name", "Expense Amount", "Date"])

# Calculate balance
total_by_person = db.groupby("Who Paid")["Expense Amount"].sum()
balance = total_by_person.get("Tyler", 0) - total_by_person.get("Adi", 0)

# Use markdown to style the balance text
balance_text = ""
if balance < 0:
    balance_text = f"Tyler owes Adi: <span style='color:red; background-color:yellow'>${-balance / 2:.2f}</span>"
elif balance > 0:
    balance_text = f"Adi owes Tyler: <span style='color:green; background-color:yellow'>${balance / 2:.2f}</span>"
else:
    balance_text = "All balanced!"

st.markdown(
    f"<h2 style='text-align: center;'>{balance_text}</h2>", unsafe_allow_html=True
)

# Define the inputs
expense_names = db["Expense Name"].unique().tolist()
col1, col2 = st.columns([2, 1])
with col1:
    name_input = st.text_input("Expense Name")
with col2:
    name_select = st.selectbox(
        "Or select existing Expense Name", options=["None"] + expense_names
    )
name = name_input if name_input else name_select

amount = st.number_input("Expense Amount", min_value=0.01)
who_paid = st.selectbox("Who Paid?", ["Tyler", "Adi"])
add_button = st.button("Add Expense")

# When the button is pressed, add the new expense to the dataframe and save it to the CSV file
if add_button:
    if not name:
        st.error("Please input a new expense name or select an existing one.")
    else:
    new_data = {'Who Paid': who_paid, 'Expense Name': expense_name, 'Expense Amount': expense_amount, 'Date': date}
    new_data = pd.DataFrame(new_data, index=[0]) # converting new_data to a DataFrame
    db = pd.concat([db, new_data], ignore_index=True)
    db.to_csv(filename, index=False)
    st.success('Transaction added')


# Function to visualize expenses
def visualize_expenses(df):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="Expense Name",
            y="Expense Amount",
            color="Who Paid",
            tooltip=["Expense Name", "Expense Amount", "Date"],
        )
        .properties(width=alt.Step(20))
    )  # controls width of bar
    st.altair_chart(chart, use_container_width=True)


# Dropdown for displaying past transactions, deleting transactions, or visualizing expenses
option = st.selectbox(
    "What do you want to do?",
    ("None", "Show past transactions", "Delete a transaction", "Visualize expenses"),
)

if option == "Show past transactions":
    st.write(db)

elif option == "Delete a transaction":
    # Display each transaction with a delete button
    for i in db.index:
        row = db.loc[i]
        delete_button_name = f"Delete: {row['Who Paid']} paid ${row['Expense Amount']:.2f} for {row['Expense Name']} on {row['Date']}"
        if st.button(delete_button_name, key=i):
            db = db.drop(i)
            db.to_csv(filename, index=False)
            st.success("Transaction deleted")

elif option == "Visualize expenses":
    visualize_expenses(db)
