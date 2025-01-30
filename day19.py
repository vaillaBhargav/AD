import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Load Dataset
df = pd.read_csv(r"C:\Users\Vailla Bhargav\Downloads\Day 19_E-Commerce_Data.csv")
print("Dataset loaded successfully!\n")

# Display Initial Data Overview
print("Initial Data Overview:\n", df.head())
df.info()
print("\nMissing Values Per Column:\n", df.isna().sum())

# Handle Missing Values
## Impute 'Product_Price' using Mean Imputation
imputer_mean = SimpleImputer(strategy='mean')
df[['Product_Price']] = imputer_mean.fit_transform(df[['Product_Price']])

## Impute 'Product_Category' using Most Frequent Value
if 'Product_Category' in df.columns:
    imputer_mode = SimpleImputer(strategy='most_frequent')
    df['Product_Category'] = df['Product_Category'].astype(str)
    df['Product_Category'] = imputer_mode.fit_transform(df[['Product_Category']]).ravel()
else:
    print("Warning: 'Product_Category' column not found!")

## Forward Fill for 'Order_Date'
df['Order_Date'] = df['Order_Date'].fillna(method='ffill')

## Apply KNN Imputation for 'Product_Price' (Refinement)
knn_imputer = KNNImputer(n_neighbors=5)
df[['Product_Price']] = knn_imputer.fit_transform(df[['Product_Price']])

# Remove Duplicates
df.drop_duplicates(inplace=True)

# Visualization of Missing Data (After Cleaning)
sns.heatmap(df.isna(), cbar=False, cmap='viridis')
plt.title("Missing Values After Cleaning")
plt.show()

# Summary Statistics Before Scaling
before_stats = df.describe()

# Normalize 'Product_Price' using MinMaxScaler
scaler = MinMaxScaler()
df[['Product_Price']] = scaler.fit_transform(df[['Product_Price']])

# Summary Statistics After Scaling
after_stats = df.describe()

print("Summary Statistics Before Scaling:\n", before_stats)
print("\nSummary Statistics After Scaling:\n", after_stats)

# Save Cleaned Dataset
df.to_csv('cleaned_ecommerce_data.csv', index=False)
print("Data Cleaning Completed. Cleaned dataset saved as 'cleaned_ecommerce_data.csv'")
