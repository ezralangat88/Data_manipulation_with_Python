import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime

# Load the dataset
# Assume you have the dataset in Excel or CSV format
# df = pd.read_excel('example_dataset.xlsx')
# Or generate a sample dataset with some issues
data = {
    'ID': [1, 2, 2, np.nan, 4, 5, 5, 5],
    'Name': ['John', 'Anna', 'Anna', 'Tom', 'Jerry', None, 'Jane', 'Jane'],
    'Age': [29, np.nan, 25, 40, 33, 21, 21, 22],
    'Date_of_Birth': ['1992-01-01', '1995/02/28', None, '1981-05-14', '1988/12/12', '2001-06-22', '2001-06-22', '2001-06-23'],
    'Salary': [55000, 48000, 48000, np.nan, 72000, 50000, 50000, 51000],
    'Join_Date': ['2021-01-10', '2020/10/25', '2020-10-25', '2019/03/15', '2021-06-30', None, '2021-07-01', '2021-07-02'],
    'Category': ['A', 'A', 'a', 'B', 'C', None, 'C', 'c'],
    'Location': ['New York', 'NewYork', 'new york', 'Chicago', 'Chicago', 'San Francisco', 'SF', 'sf'],
    'Score': [99, 85, None, 75, -10, 60, 60, 120],
    'Target': [1, 1, 1, 0, 0, 0, 0, 1]
}

df = pd.DataFrame(data)

# ========== Data Cleaning and Manipulation Functions ==========

# 1. Handling Missing Values
def handle_missing_values(df):
    # Ensure None values are treated as NaN
    df.replace({None: np.nan}, inplace=True)
    
    # Dropping columns where all values are missing
    df.dropna(axis=1, how='all', inplace=True)
    
    # For columns with missing values, decide whether to impute or drop
    # Example: Impute numerical columns with the mean
    num_cols = df.select_dtypes(include=[np.number])
    imputer_num = SimpleImputer(strategy='mean')
    df[num_cols.columns] = imputer_num.fit_transform(num_cols)
    
    # Impute categorical columns with the most frequent value
    cat_cols = df.select_dtypes(exclude=[np.number])
    imputer_cat = SimpleImputer(strategy='most_frequent')
    df[cat_cols.columns] = imputer_cat.fit_transform(cat_cols)
    
    return df

# 2. Removing Duplicate Records
def remove_duplicates(df):
    df.drop_duplicates(inplace=True)
    return df

# 3. Fixing Inconsistent Formatting (e.g., date formats, string cases)
def fix_inconsistent_formatting(df):
    # Convert all date columns to the same format
    df['Date_of_Birth'] = pd.to_datetime(df['Date_of_Birth'], errors='coerce')
    df['Join_Date'] = pd.to_datetime(df['Join_Date'], errors='coerce')
    
    # Standardize string columns (lowercase everything, remove extra spaces)
    df['Name'] = df['Name'].str.strip().str.title()
    df['Location'] = df['Location'].str.strip().str.title()
    df['Category'] = df['Category'].str.strip().str.upper()
    
    return df

# 4. Identifying and Handling Outliers
def handle_outliers(df):
    # Here we define any negative or above 100 score as an outlier
    df['Score'] = np.where((df['Score'] < 0) | (df['Score'] > 100), np.nan, df['Score'])
    df['Score'].fillna(df['Score'].mean(), inplace=True)
    return df

# 5. Correcting Data Types
def correct_data_types(df):
    # Ensure 'ID' column is integer
    df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)
    
    # Ensure categorical variables are of 'category' type
    df['Category'] = df['Category'].astype('category')
    df['Location'] = df['Location'].astype('category')
    
    return df

# 6. Handling Whitespace and Typos
def handle_whitespace_typos(df):
    # Removing leading/trailing whitespaces
    df.columns = df.columns.str.strip()
    
    # Example: standardizing similar categories
    df['Location'] = df['Location'].replace({
        'NewYork': 'New York', 'new york': 'New York',
        'SF': 'San Francisco', 'sf': 'San Francisco'
    })
    
    return df

# 7. Fixing Mixed Data Types in Columns
def fix_mixed_data_types(df):
    # Ensuring numeric columns have consistent types
    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
    return df

# 8. Handling Invalid Values (outliers, incorrect entries)
def handle_invalid_values(df):
    # Example: Negative salary is not possible, set invalid salaries to NaN
    df.loc[df['Salary'] < 0, 'Salary'] = np.nan
    return df

# 9. Handling Inconsistent Units of Measurement (Assume salary in thousands or dollars)
def standardize_units(df):
    # Example: Assume Salary column has inconsistent units (e.g., thousands)
    df['Salary'] = np.where(df['Salary'] < 1000, df['Salary'] * 1000, df['Salary'])
    return df

# 10. Handling Non-standardized Categories (Category normalization)
def standardize_categories(df):
    df['Category'] = df['Category'].str.upper()
    return df

# 11. Handling Temporal Issues (e.g., date ranges)
def handle_temporal_issues(df):
    # Example: Ensure that Join Date is after Date of Birth
    df['Join_Date'] = pd.to_datetime(df['Join_Date'], errors='coerce')
    df = df[df['Join_Date'] > df['Date_of_Birth']]
    return df

# 12. Splitting Training and Testing Data (For ML purposes)
def split_train_test(df, target_column):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# 13. Feature Scaling (Normalize features)
def feature_scaling(df, columns):
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

# ========== Running All Functions ==========

# Apply all the cleaning steps
df_cleaned = handle_missing_values(df)
df_cleaned = remove_duplicates(df_cleaned)
df_cleaned = fix_inconsistent_formatting(df_cleaned)
df_cleaned = handle_outliers(df_cleaned)
df_cleaned = correct_data_types(df_cleaned)
df_cleaned = handle_whitespace_typos(df_cleaned)
df_cleaned = fix_mixed_data_types(df_cleaned)
df_cleaned = handle_invalid_values(df_cleaned)
df_cleaned = standardize_units(df_cleaned)
df_cleaned = standardize_categories(df_cleaned)
df_cleaned = handle_temporal_issues(df_cleaned)

# Print cleaned dataframe
print(df_cleaned.head())

# Example: If you want to export the cleaned data to a file
df_cleaned.to_excel('cleaned_dataset.xlsx', index=False)
