import pandas as pd

# load the data from the data.xlsx file
data = pd.read_excel("data.xlsx")

# remove rows with missing values
data = data.dropna()

# remove duplicate rows
data = data.drop_duplicates()

# fill in missing values with the word "null"
data = data.fillna("null")

# save the cleaned data to a clean_data.xlsx file
data.to_excel("clean_data.xlsx", index=False)
