# Data_manipulation_with_Python 

pip install pandas - library for data manipulation and analysis

pip install openpyxl - Python library primarily used for reading and writing Excel files (with the .xlsx extension)

# Load the data into a pandas dataframe
df = pd.read_excel("data.xlsx")
This line reads an Excel file named data.xlsx and loads its contents into a Pandas DataFrame called df. A DataFrame is like a table that holds your data.

The inplace=True argument means that the changes are made directly to df, rather than creating a new DataFrame.

The index=False argument means that the row indices (which are usually shown on the left side of the table) will not be saved in the file.

pip install  numpy scikit-learn