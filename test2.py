import pandas as pd

# Read the data into a DataFrame
df = pd.read_csv("data.xlsx", delimiter='\t')

# Remove any rows with missing values
df.dropna(inplace=True)

# Remove any duplicate rows
df.drop_duplicates(inplace=True)

# Fill in missing values with the mean value for that column
df.fillna(df.mean(), inplace=True)

# Save the cleaned data back to a data.csv file
df.to_csv("cleaned_data.xlsx", index=False)
