import pandas as pd
import streamlit as st
import os

# Function to read and display CSV file
def read_csv_file(file_paths):
    dfs = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        dfs.append(df)
    return dfs

def main():
    st.title("ADR File Viewer")

    # Get list of CSV files in the 'Data' folder and sort them by name
    data_folder = "./Data"
    csv_files = sorted([file for file in os.listdir(data_folder) if file.endswith(".csv")])

    # Multi-select dropdown to select CSV files
    selected_files = st.multiselect("Select CSV files", csv_files)

    if selected_files:
        # Read and display the selected CSV files
        file_paths = [os.path.join(data_folder, file) for file in selected_files]
        dfs = read_csv_file(file_paths)
        
        st.subheader("CSV File Content:")
        for i, (file_name, df) in enumerate(zip(selected_files, dfs)):
            st.write(f"File {i + 1}: {file_name}")
            st.write(df)

if __name__ == "__main__":
    main()
