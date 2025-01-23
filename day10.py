import pandas as pd
idata = pd.read_csv("C:\\Users\\Vailla Bhargav\\Downloads\\Day_10_banking_data.csv")
filtered = idata[idata["Transaction_Amount"] > 2000]
loan = idata[(idata["Transaction_Type"] == "Loan Payment") & (idata["Account_Balance"] > 5000)]
uptown = idata[idata["Branch"] == "Uptown"]
print(filtered)
print(loan)
print(uptown)
idata["Transaction_Fee"] = idata["Transaction_Amount"] * 0.02
idata["Balance_Status"] = idata["Account_Balance"].apply(
    lambda x: "High Balance" if x > 5000 else "Low Balance"
)
print(idata)