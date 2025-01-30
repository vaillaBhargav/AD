import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from textblob import TextBlob
import os

# Load the dataset
file_path = r"C:\Users\Vailla Bhargav\Downloads\Day_18_Tours_and_Travels.csv"

try:
    df = pd.read_csv(file_path)
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
    exit()

# Display basic information
print("\nInitial Data Overview:\n", df.head())
df.info()
print("\nMissing Values Per Column:\n", df.isna().sum())

# Strip any extra spaces from column names
df.columns = df.columns.str.strip()

# Handle missing values
if 'Customer_Age' in df.columns:
    imputer = SimpleImputer(strategy='median')
    df['Customer_Age'] = imputer.fit_transform(df[['Customer_Age']])
else:
    print("Warning: 'Customer_Age' column not found!")

if 'Review_Text' in df.columns:
    def fill_missing_text(text):
        return str(TextBlob(text).correct()) if pd.notnull(text) else "No Review"
    df['Review_Text'] = df['Review_Text'].apply(fill_missing_text)
    df.drop_duplicates(subset=['Review_Text'], inplace=True)
else:
    print("Warning: 'Review_Text' column not found!")

# Clip Ratings between 1 and 5
if 'Rating' in df.columns:
    df['Rating'] = df['Rating'].clip(1, 5)
else:
    print("Warning: 'Rating' column not found!")

# Handle spelling correction if 'Tour_Package' column exists
if 'Tour_Package' in df.columns:
    def correct_spelling(text):
        return str(TextBlob(text).correct()) if pd.notnull(text) else text
    df['Tour_Package'] = df['Tour_Package'].apply(correct_spelling)
else:
    print("Warning: 'Tour_Package' column not found!")

# Outlier treatment for numerical columns
for col in ['Package_Price', 'Rating']:
    if col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
    else:
        print(f"Warning: '{col}' column not found!")

# Label Encoding for categorical columns
label_encoders = {}
if 'Tour_Package' in df.columns:
    le = LabelEncoder()
    df['Tour_Package'] = le.fit_transform(df['Tour_Package'])
    label_encoders['Tour_Package'] = le

# Scaling numerical columns
scaler = MinMaxScaler()
scalable_cols = ['Customer_Age', 'Package_Price', 'Rating']
for col in scalable_cols:
    if col in df.columns:
        df[[col]] = scaler.fit_transform(df[[col]])
    else:
        print(f"Warning: '{col}' column not found!")

# Save the cleaned dataset
output_path = 'cleaned_travel_reviews.csv'
df.to_csv(output_path, index=False)
print(f"\nData Cleaning Completed. Cleaned dataset saved as '{output_path}'")
