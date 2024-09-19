import pandas as pd 

df = pd.read_excel("Customer Call List.xlsx")

# Define the output file name
output_file = "cleaned_customer_list.xlsx"

df = df.drop_duplicates()

df = df.drop(columns = "Not_Useful_Column")

#df["Last_Name"] = df["Last_Name"].str.lstrip("...")
#df["Last_Name"] = df["Last_Name"].str.lstrip("/")
#df["Last_Name"] = df["Last_Name"].str.rstrip("_")
df["Last_Name"] = df["Last_Name"].str.strip("123._/")

# df["Phone_Number"] = df["Phone_Number"].str.replace('[^a-zA-Z0-9]','')

# df["Phone_Number"].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])

df["Phone_Number"] = df["Phone_Number"].apply(lambda x: str(x))

df["Phone_Number"] = df["Phone_Number"].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])

df["Phone_Number"] = df["Phone_Number"].str.replace('nan--','')

df["Phone_Number"] = df["Phone_Number"].str.replace('Na--','')

df[["Street_Address", "State", "Zip_Code"]] = df["Address"].str.split(',',2, expand=True)

df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('Yes','Y')

df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace('No','N')

#df = df.replace('N/a','')
#df = df.replace('NaN','')


df=df.fillna('')

for x in df.index:
    if df.loc[x, "Do_Not_Contact"] == 'Y':
        df.drop(x, inplace=True)

df

for x in df.index:
    if df.loc[x, "Phone_Number"] == '':
        df.drop(x, inplace=True)

df

#Another way to drop null values
#df = df.dropna(subset="Phone_Number"), inplace=True)


# Save the cleaned data back to a data_cleaned.xlsx file
# df.to_excel(output_file, index=False)

df = df.reset_index(drop=True)



# Print cleaned dataframe
print(df.head())