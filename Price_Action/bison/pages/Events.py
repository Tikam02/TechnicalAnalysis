import streamlit as st
from nsepython import *

# Function to display data in a table
def display_table(data):
    st.table(data)

# Main function
def main():
    st.title("NSE Data Visualization")

    # nse_fiidii
    st.header("NSE FIIDI Data")
    fiidii_data = nse_fiidii()
    display_table(fiidii_data)

    # nse_events
    st.header("NSE Events Data")
    events_data = nse_events()
    display_table(events_data)


    # nse_results
    st.header("NSE Results Data")
    results_data = nse_results("equities", "Quarterly")
    display_table(results_data)

if __name__ == "__main__":
    main()
