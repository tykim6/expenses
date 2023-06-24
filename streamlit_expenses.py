# Import the required libraries
import streamlit as st
import pandas as pd
import altair as alt
import datetime
import os

# Define filename
filename = "expenses.csv"

# Check if the CSV file exists. If not, create it with the necessary columns.
if not os.path.isfile(filename):
    db = pd.DataFrame(columns=["Who Paid", "Expense Name", "Expense Amount", "Date"])
else:
    db = pd.read_csv(filename)

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
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    name_input = st.text_input("Expense Name")
with col2:
    name_select = st.selectbox(
        "Or select existing Expense Name", options=["None"] + expense_names
    )
with col3:
    charge_full_amount = st.checkbox("Charge Entire Amount?")

name = name_input if name_input else name_select
amount = st.number_input("Expense Amount", min_value=0.01)
who_paid = st.selectbox("Who Paid?", ["Tyler", "Adi"])

add_button = st.button("Add Expense")

# Calculate balance
total_by_person = db.groupby("Who Paid")["Expense Amount"].sum()

if charge_full_amount:
    balance = total_by_person.get("Adi", 0) - total_by_person.get("Tyler", 0)
else:
    balance = (total_by_person.get("Adi", 0) - total_by_person.get("Tyler", 0)) / 2


# When the button is pressed, add the new expense to the dataframe and save it to the CSV file
if add_button:
    if not name:
        st.error("Please input a new expense name or select an existing one.")
    else:
        date = datetime.date.today()
        new_data = {
            "Who Paid": who_paid,
            "Expense Name": name,
            "Expense Amount": amount,
            "Date": date.strftime("%Y-%m-%d"),
        }
        new_data = pd.DataFrame(
            new_data, index=[0]
        )  # converting new_data to a DataFrame
        db = pd.concat([db, new_data], ignore_index=True)
        db.to_csv(filename, index=False)
        st.success("Transaction added")


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


# Function to preprocess data
def preprocess_data(df):
    # Replace NaN values with 'unknown'
    df["Expense Name"] = df["Expense Name"].fillna("unknown")

    # Convert 'Expense Name' to string type
    df["Expense Name"] = df["Expense Name"].astype(str)

    # Convert 'Expense Name' to lower case for case insensitive grouping
    df["Expense Name"] = df["Expense Name"].str.lower()

    # Group by 'Expense Name'
    grouped = df.groupby("Expense Name").sum().reset_index()

    return grouped


# Dropdown for displaying past transactions, deleting transactions, or visualizing expenses
option = st.selectbox(
    "What do you want to do?",
    ("Show past transactions", "Delete a transaction", "Visualize expenses"),
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
    db_processed = preprocess_data(db)
    visualize_expenses(db_processed)
