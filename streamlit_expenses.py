# Import the required libraries
import streamlit as st
import pandas as pd
import altair as alt
import datetime
from pymongo import MongoClient

# Create a MongoDB client
MONGODB_URI = "mongodb+srv://tylerkim:safe_password@expenses.qkuauvo.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)

# Specify the database and collection
db = client["database"]
collection = db["expenses"]

# Convert MongoDB collection to DataFrame
expenses = pd.DataFrame(list(collection.find()))

# Handle empty database case
if expenses.empty:
    expenses = pd.DataFrame(
        columns=["Who Paid", "Expense Name", "Expense Amount", "Date"]
    )

# Calculate balance
total_by_person = expenses.groupby("Who Paid")["Expense Amount"].sum()
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
expense_names = expenses["Expense Name"].unique().tolist()
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

# When the button is pressed, add the new expense to the DataFrame and save it to MongoDB
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
        collection.insert_one(new_data)
        st.success("Transaction added")


# Function to visualize expenses
def visualize_expenses(df):
    if "Expense Amount" in df.columns:
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x="Expense Name:N",  # Nominal type for categorical data
                y="sum(Expense Amount):Q",
                tooltip=["sum(Expense Amount):Q"],
            )
            .properties(width=alt.Step(20))  # controls width of bar
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("No data to visualize")


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
    st.write(expenses.drop("_id", axis=1))  # Drop _id column
elif option == "Delete a transaction":
    transaction_select = st.selectbox(
        "Select a transaction to delete",
        expenses.apply(
            lambda x: f"{x['Who Paid']} paid ${x['Expense Amount']:.2f} for {x['Expense Name']} on {x['Date']}",
            axis=1,
        ),
    )
    delete_button = st.button("Delete selected transaction")
    if delete_button:
        index_to_delete = expenses.index[
            expenses.apply(
                lambda x: f"{x['Who Paid']} paid ${x['Expense Amount']:.2f} for {x['Expense Name']} on {x['Date']}",
                axis=1,
            )
            == transaction_select
        ][0]
        collection.delete_one({"_id": expenses.loc[index_to_delete, "_id"]})
        st.success("Transaction deleted")

elif option == "Visualize expenses":
    expenses_processed = preprocess_data(expenses)
    visualize_expenses(expenses_processed)
