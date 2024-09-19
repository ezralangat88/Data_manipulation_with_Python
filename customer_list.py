import pandas as pd

# Load the dataset
df = pd.read_excel("Customer Call List.xlsx")

# Define the output file name
output_file = "cleaned_customer_list.xlsx"

# ========== Data Cleaning ==========

# 1. Drop duplicate records
df = df.drop_duplicates()

# 2. Drop the column "Not_Useful_Column" if it exists
if "Not_Useful_Column" in df.columns:
    df = df.drop(columns="Not_Useful_Column")

# 3. Clean the "Last_Name" column by stripping unwanted characters
# This will remove any leading/trailing "1", "2", "3", ".", "_", or "/" from the names
df["Last_Name"] = df["Last_Name"].str.strip("123._/")

# 4. Clean and format phone numbers
# Ensure phone numbers are strings for consistent processing
df["Phone_Number"] = df["Phone_Number"].astype(str)

# Remove any non-numeric characters (e.g., "-", "/", "|") from the phone numbers
df["Phone_Number"] = df["Phone_Number"].str.replace('[^0-9]', '', regex=True)

# Ensure phone numbers have exactly 10 digits, and format them as XXX-XXX-XXXX
df["Phone_Number"] = df["Phone_Number"].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10] if len(x) == 10 else '')

# 5. Split "Address" column into "Street_Address", "State", and "Zip_Code"
# Assuming the address is in the format: "Street Address, State, Zip Code"
address_split = df["Address"].str.split(',', expand=True, n=2)
df["Street_Address"] = address_split[0].str.strip()
df["State"] = address_split[1].str.strip() if address_split.shape[1] > 1 else ''
df["Zip_Code"] = address_split[2].str.strip() if address_split.shape[1] > 2 else ''

# 6. Standardize the "Do_Not_Contact" column
# Replace 'Yes' with 'Y' and 'No' with 'N', and fill NaN values with 'N' (no contact restriction)
df["Do_Not_Contact"] = df["Do_Not_Contact"].replace({'Yes': 'Y', 'No': 'N'}).fillna('N')

# 7. Replace missing or NaN values with empty strings in other columns
df.fillna('', inplace=True)

# 8. Drop rows where "Do_Not_Contact" is 'Y' (customer opted out of contact)
df = df[df["Do_Not_Contact"] != 'Y']

# 9. Drop rows where "Phone_Number" is missing or invalid
df = df[df["Phone_Number"] != '']

df["Paying Customer"] = df["Paying Customer"].str.replace('Yes','Y')

df["Paying Customer"] = df["Paying Customer"].str.replace('No','N')


# 10. Reset index after dropping rows, without adding the old index as a column
df = df.reset_index(drop=True)

# ========== Save the cleaned data ==========

# Save the cleaned dataframe to an Excel file
df.to_excel(output_file, index=False)

# Print the first few rows of the cleaned dataframe for verification
print(df.head())
