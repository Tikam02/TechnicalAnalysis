import streamlit as st
import pandas as pd
import os
import uuid
from PIL import Image

# Ensure "Data" folder exists
if not os.path.exists("Data"):
    os.makedirs("Data")

# Function to save journal entry to CSV
def save_to_journal(trade_type, stock_name, price, date, quantity, reason, strategy, image_path, buy_avg_price, sell_price):
    # Format the date as a string
    date_str = date.strftime('%Y-%m-%d')
    
    entry = {'Trade Type': trade_type,
             'Stock Name': stock_name,
             'Current Market Price': price,
             'Date': date_str,
             'Quantity': quantity,
             'Buy Average Price': buy_avg_price,
             'Sell Price': sell_price,
             'Reason': reason,
             'Strategy': strategy,
             'Image': image_path}

    # Check if the file exists and read the existing data
    if os.path.exists("./Data/Journal.csv"):
        df_existing = pd.read_csv("./Data/Journal.csv")
        df_new = pd.DataFrame(entry, index=[0])
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        # If the file doesn't exist, create a new DataFrame with the entry
        df = pd.DataFrame(entry, index=[0])

    # Write the DataFrame back to the CSV file, including the column headers
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
        buy_avg_price = st.number_input("Buy Average Price", step=0.01)
        sell_price = st.number_input("Sell Price", step=0.01)
        reason = st.text_area("Why / Reason to Buy")
        strategy = st.text_input("Which Strategy")
        image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

        if st.button("Save Entry"):
            image_path = None
            if image:
                # Generate a unique identifier for the image
                image_uid = str(uuid.uuid4())
                image_path = f"./Data/img/{stock_name}_{date}_{trade_type}_{image_uid}_image.jpg"
                with open(image_path, "wb") as f:
                    f.write(image.read())
            save_to_journal(trade_type, stock_name, price, date, quantity, reason, strategy, image_path, buy_avg_price, sell_price)
            st.success("Entry saved successfully.")

    # Tabs layout
    tabs = ["Input Form", "Journal Output"]
    selected_tab = st.sidebar.radio("Select Tab", tabs, index=1)

    if selected_tab == "Input Form":
        pass # Already displayed above
    elif selected_tab == "Journal Output":
        st.subheader("Journal Output")
        display_journal()
        if os.path.exists("./Data/Journal.csv"):
            df = pd.read_csv("./Data/Journal.csv")
            for index, row in df.iterrows():
                with st.expander(f"{row.get('Stock Name', 'N/A')} {row.get('Date', 'N/A')} "):
                    st.write(f"Trade Type: {row.get('Trade Type', 'N/A')}")
                    st.write(f"Stock Name: {row.get('Stock Name', 'N/A')}")
                    st.write(f"Current Price: {row.get('Current Market Price', 'N/A')}")
                    st.write(f"Date: {row.get('Date', 'N/A')}")
                    st.write(f"Quantity: {row.get('Quantity', 'N/A')}")
                    st.write(f"Buy Average Price: {row.get('Buy Average Price', 'N/A')}")
                    st.write(f"Sell Price: {row.get('Sell Price', 'N/A')}")
                    st.write(f"Reason: {row.get('Reason', 'N/A')}")
                    st.write(f"Strategy: {row.get('Strategy', 'N/A')}")
                    # Check if 'Image' column exists and if the row has an image path
                    if 'Image' in df.columns and row['Image']:
                        st.image(row['Image'], caption='Uploaded Image', use_column_width=True)

if __name__ == "__main__":
    main()
