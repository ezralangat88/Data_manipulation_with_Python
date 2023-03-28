import pandas as pd

# load the data into a pandas dataframe
df = pd.read_csv("data.xlsx")

# remove any rows with missing values
df = df.dropna()

# remove any duplicate rows
df = df.drop_duplicates()

# # replace any values that are outside of a specified range with NaN
# df['column_name'] = df['column_name'].mask((df['column_name'] < lower_bound) | (df['column_name'] > upper_bound), other=pd.NaT)

# # fill in missing values with the mean value for that column
# df['column_name'] = df['column_name'].fillna(df['column_name'].mean())

# save the cleaned data back to a csv file
df.to_csv("cleaned_data.xlsx", index=False)
