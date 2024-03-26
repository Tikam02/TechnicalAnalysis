
# # Function to read and display a CSV file
# def display_csv_file(uploaded_file, header):
#     if uploaded_file is not None:
#         # Read the CSV file into a pandas DataFrame
#         df = pd.read_csv(uploaded_file)
        
#         # Display the header
#         st.subheader(header)
        
#         # Display the DataFrame as a table
#         st.table(df)

# # Upload CSV files
# uploaded_file_a = st.file_uploader("Upload CSV file A", type=["csv"])
# uploaded_file_b = st.file_uploader("Upload CSV file B", type=["csv"])

# # Display the contents of the uploaded CSV files
# display_csv_file(uploaded_file_a, "Header A")
# display_csv_file(uploaded_file_b, "Header B")


import streamlit as st
import pandas as pd

# Function to read and display a CSV file
def display_csv_file(file_path, header):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Display the header
    st.subheader(header)
    
    # Display the DataFrame as an interactive table
    st.dataframe(df)

# Define the file paths for the CSV files
file_path_a = "./Data/bnf_results.csv"
file_path_b = "./Data/mm_results.csv"
file_path_c = "./Data/plain_adr_results.csv"
file_path_d = "./Data/qm_adr_results.csv"

# Display the contents of the predefined CSV files
display_csv_file(file_path_a, "BNF Scanner Results")
display_csv_file(file_path_b, "Mark Minervini Results")
display_csv_file(file_path_c, "Plain ADR Results")
display_csv_file(file_path_d, "Quallamaggie ADR Results")

