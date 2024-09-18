import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import re

# Load the dataset
df = pd.read_csv('food_coded.csv')

# ========== Data Cleaning and Manipulation Functions ==========

# 1. Handling Missing Values
def handle_missing_values(df):
    df.replace({None: np.nan}, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)  # Drop columns with all NaNs
    
    # Impute numeric columns with the mean
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
    for col in df.select_dtypes(include='object'):
        df[col] = df[col].str.strip().str.lower()
    return df

# 4. Identifying and Handling Outliers
def handle_outliers(df):
    for col in df.select_dtypes(include=[np.number]):
        mean = df[col].mean()
        std_dev = df[col].std()
        df[col] = np.where((df[col] < mean - 3 * std_dev) | (df[col] > mean + 3 * std_dev), np.nan, df[col])
    
    df.fillna(df.mean(), inplace=True)
    return df

# 5. Correcting Data Types
def correct_data_types(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                continue
    return df

# 6. Handling Whitespace and Typos
def handle_whitespace_typos(df):
    df.columns = df.columns.str.strip()
    return df

# 7. Fixing Mixed Data Types in Columns (like numeric data mixed with text)
def fix_mixed_data_types(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            # Extract numeric values from mixed-type columns (e.g., "200 lbs" -> 200)
            df[col] = df[col].apply(lambda x: extract_numeric(x) if isinstance(x, str) else x)
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric after cleaning
            
    return df

# Utility function to extract numeric values from strings
def extract_numeric(text):
    # Use regex to extract digits from the string
    match = re.search(r'\d+', text)
    if match:
        return float(match.group(0))
    return np.nan  # If no numeric value, return NaN

# 8. Handling Invalid Values (e.g., negative values where inappropriate)
def handle_invalid_values(df):
    for col in df.select_dtypes(include=[np.number]):
        df[col] = np.where(df[col] < 0, np.nan, df[col])  # Replace negative values with NaN
    return df

# 9. Handling Non-standardized Categories
def standardize_categories(df):
    for col in df.select_dtypes(include=['object', 'category']):
        df[col] = df[col].str.upper()
    return df

# ========== Running All Functions ==========

# Apply all the cleaning steps
df_cleaned = handle_missing_values(df)
df_cleaned = remove_duplicates(df_cleaned)
df_cleaned = fix_inconsistent_formatting(df_cleaned)
df_cleaned = fix_mixed_data_types(df_cleaned)  # Clean mixed data types before outlier handling
df_cleaned = handle_outliers(df_cleaned)
df_cleaned = correct_data_types(df_cleaned)
df_cleaned = handle_whitespace_typos(df_cleaned)
df_cleaned = handle_invalid_values(df_cleaned)
df_cleaned = standardize_categories(df_cleaned)

# Save the cleaned dataset
df_cleaned.to_csv('cleaned_food_coded.csv', index=False)

# Output cleaned data for review
print(df_cleaned.head())

# Example: If you want to export the cleaned data to a file
df_cleaned.to_excel('food_cleaned_dataset.xlsx', index=False)
