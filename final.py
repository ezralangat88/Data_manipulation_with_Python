import pandas as pd
import os

# Define the output file name
output_file = "data_cleaned.xlsx"

# Remove the output file if it exists
if os.path.exists(output_file):
    os.remove(output_file)

# Load the data into a pandas dataframe
df = pd.read_excel("data.xlsx")

# Remove any rows where all cells are missing
df.dropna(how='all', inplace=True)

# Convert the DataFrame to object type to allow mixed types
df = df.astype(object)

# Fill in missing values with "null" if at least one cell in the row is not null
df.fillna("null", inplace=True)

# Remove any duplicate rows
df.drop_duplicates(inplace=True)

# Save the cleaned data back to a data_cleaned.xlsx file
df.to_excel(output_file, index=False)
