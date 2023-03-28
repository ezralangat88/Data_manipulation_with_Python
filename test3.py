import pandas as pd

# Load the data into a pandas dataframe
df = pd.read_excel("data.xlsx")

# Remove any rows with missing values
df.dropna(inplace=True)

# Remove any duplicate rows
df.drop_duplicates(inplace=True)

# Fill in missing values with "null"
df.fillna("null", inplace=True)

# Save the cleaned data back to a data.xlsx file
df.to_excel("data_cleaned.xlsx", index=False)
