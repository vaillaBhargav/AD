import pandas as pd

data = pd.read_csv(r"C:\Users\Vailla Bhargav\Downloads\Day_7_sales_data.csv")
print(data.head())

print(data.describe())

total = data.groupby('Region')['Sales'].sum()
print(total)

most = data.groupby('Product')['Quantity'].sum().idxmax()
print(most)

data['Profit_Margin'] = (data['Profit'] / data['Sales']) * 100
average = data.groupby('Product')['Profit_Margin'].mean()
print(average)