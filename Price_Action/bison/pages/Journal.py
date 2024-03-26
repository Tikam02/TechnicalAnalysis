import streamlit as st
import pandas as pd
import os

# Ensure "Data" folder exists
if not os.path.exists("Data"):
    os.makedirs("Data")

# Function to save journal entry to CSV
def save_to_journal(trade_type, stock_name, price, date, quantity, reason, strategy):
    entry = {'Trade Type': trade_type,
             'Stock Name': stock_name,
             'Price': price,
             'Date': date,
             'Quantity': quantity,
             'Reason': reason,
             'Strategy': strategy}
    df = pd.DataFrame(entry, index=[0])
    if os.path.exists("./Data/Journal.csv"):
        df.to_csv("./Data/Journal.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("./Data/Journal.csv", index=False)

# Function to display journal entries
def display_journal():
    if os.path.exists("./Data/Journal.csv"):
        df = pd.read_csv("./Data/Journal.csv")
        st.write(df)
    else:
        st.write("No journal entries yet.")

# Main function
def main():
    st.title('Trading Journal')

    # Sidebar for input form
    with st.sidebar:
        st.subheader("Input Form")
        trade_type = st.selectbox("Trade Type", ["Entry", "Exit"])
        stock_name = st.text_input("Name of the Stock")
        price = st.number_input("Price", step=0.01)
        date = st.date_input("Date")
        quantity = st.number_input("Quantity", min_value=1)
        reason = st.text_area("Why / Reason to Buy")
        strategy = st.text_input("Which Strategy")

        if st.button("Save Entry"):
            save_to_journal(trade_type, stock_name, price, date, quantity, reason, strategy)
            st.success("Entry saved successfully.")

    # Tabs layout
    tabs = ["Input Form", "Journal Output"]
    selected_tab = st.sidebar.radio("Select Tab", tabs)

    if selected_tab == "Input Form":
        pass  # Already displayed above
    elif selected_tab == "Journal Output":
        st.subheader("Journal Output")
        display_journal()

if __name__ == "__main__":
    main()
