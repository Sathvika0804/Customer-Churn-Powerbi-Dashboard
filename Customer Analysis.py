'''
import pandas as pd
import numpy as np

print("STEP-1: Load the Data..")
data = pd.read_csv("C:/Users/sathv/Downloads/DA --- PROJECT/WA_Fn-UseC_-Telco-Customer-Churn.csv")
#print(data)
print(data.head())
print(data.info())
print(data.describe())
# print(data.to_string())
print("Data Loaded Successfully!!")

print("------------------------------------")
print(data.isnull().sum())
print("-------------------------------------------------------------------------")
print(data.columns)
print("-------------------------------------------------------------------------")

data = data.dropna()

duplicates = data.duplicated().sum()
print("Duplicate rows:", duplicates)

data = data.drop_duplicates()
print("-------- Duplicates are removed ----------")

cols = ['Partner','Dependents','PhoneService','PaperlessBilling','Churn']

for col in cols:
    data[col] = data[col].map({'Yes':1, 'No':0})
data['SeniorCitizen'] = data['SeniorCitizen'].astype('category')
print(data.columns)
print(data)


service_cols = ['PhoneService','MultipleLines','OnlineSecurity','OnlineBackup',
                'DeviceProtection','TechSupport','StreamingTV','StreamingMovies']

for col in service_cols:
    data[col] = data[col].replace({'No internet service':'No', 'No phone service':'No'})
    data[col] = data[col].map({'Yes':1, 'No':0})

# Convert TotalCharges to numeric
data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')

# Handle missing values created due to conversion
# data['TotalCharges'] = data['TotalCharges'].fillna(0)
data['TotalCharges'] = data['TotalCharges'].fillna(data['TotalCharges'].median())

# Now safe to calculate
data['AvgMonthlySpend'] = data['TotalCharges'] / data['tenure']

# Handle division by zero (tenure = 0)
data['AvgMonthlySpend'] = data['AvgMonthlySpend'].replace([np.inf, -np.inf], 0)
data['AvgMonthlySpend'] = data['AvgMonthlySpend'].fillna(0)

data['CustomerProfile'] = data['SeniorCitizen'].astype(str) + "_" + data['Partner'].astype(str) + "_" + data['Dependents'].astype(str)

data['StreamingServices'] = data[['StreamingTV','StreamingMovies']].apply(
    lambda x: 'Both' if x.iloc[0]=='Yes' and x.iloc[1]=='Yes' else
              'None' if x.iloc[0]=='No' and x.iloc[1]=='No' else 'One', axis=1)

data['StreamingServices'] = 'One'

data.loc[(data['StreamingTV']=='Yes') & (data['StreamingMovies']=='Yes'), 'StreamingServices'] = 'Both'

data.loc[(data['StreamingTV']=='No') & (data['StreamingMovies']=='No'), 'StreamingServices'] = 'None'

def tenure_group(x):
    if x <= 12:
        return '0-1 Year'
    elif x <= 24:
        return '1-2 Years'
    elif x <= 48:
        return '2-4 Years'
    else:
        return '4+ Years'

data['TenureGroup'] = data['tenure'].apply(tenure_group)

data['ContractRisk'] = data['Contract'].map({
    'Month-to-month': 'High Risk',
    'One year': 'Medium Risk',
    'Two year': 'Low Risk'
})
data['PhoneService'] = data['PhoneService'].map({'Yes':1, 'No':0}).fillna(0)

data['PaymentType'] = data['PaymentMethod'].apply(
    lambda x: 'Auto' if 'automatic' in x else 'Manual'
)
data['InternetType'] = data['InternetService'].replace({
    'Fiber optic': 'High Speed',
    'DSL': 'Medium Speed',
    'No': 'No Internet'
})
data['HighValueCustomer'] = data['MonthlyCharges'].apply(
    lambda x: 'Yes' if x > data['MonthlyCharges'].median() else 'No'
)
data['EngagementLevel'] = data[service_cols].sum(axis=1)

data['EngagementLevel'] = data['EngagementLevel'].apply(
    lambda x: 'Low' if x <= 2 else ('Medium' if x <= 5 else 'High')
)
data['CustomerLoyalty'] = data['TenureGroup'].astype(str) + "_" + data['Contract']
print(data)
# print(data.to_string())

data.to_csv("customer_cleaned.csv", index=False)
print("\nCLEAN FILE SAVED AS: customer_cleaned.csv")

'''

import pandas as pd
import numpy as np

print("STEP-1: Load the Data..")
data = pd.read_csv("C:/Users/sathv/Downloads/DA --- PROJECT/WA_Fn-UseC_-Telco-Customer-Churn.csv")

print(data.head())
print(data.info())
print(data.describe())

print("Data Loaded Successfully!!")
print("------------------------------------")
print(data.isnull().sum())
print("------------------------------------")

# -------------------------------
# STEP-2: HANDLE MISSING VALUES
# -------------------------------

data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
data['TotalCharges'] = data['TotalCharges'].fillna(data['TotalCharges'].median())

# -------------------------------
# STEP-3: REMOVE DUPLICATES
# -------------------------------

print("Duplicate rows:", data.duplicated().sum())
data = data.drop_duplicates()

# -------------------------------
# STEP-4: CLEAN SERVICE COLUMNS
# -------------------------------

service_cols = ['PhoneService','MultipleLines',
                'StreamingTV','StreamingMovies']

for col in service_cols:
    data[col] = data[col].replace({
        'No internet service': 'No',
        'No phone service': 'No'
    })
    
    data[col] = data[col].map({'Yes':1, 'No':0})
    data[col] = pd.to_numeric(data[col], errors='coerce')
    data[col] = data[col].fillna(0)

# -------------------------------
# STEP-5: OTHER BINARY COLUMNS
# -------------------------------

binary_cols = ['Partner','Dependents','PaperlessBilling','Churn']

for col in binary_cols:
    data[col] = data[col].map({'Yes':1, 'No':0})

# -------------------------------
# STEP-6: FEATURE ENGINEERING
# -------------------------------

# Avg Monthly Spend
data['AvgMonthlySpend'] = data['TotalCharges'] / data['tenure']
data['AvgMonthlySpend'] = data['AvgMonthlySpend'].replace([np.inf, -np.inf], 0)
data['AvgMonthlySpend'] = data['AvgMonthlySpend'].fillna(0)

# Streaming Services
data['StreamingServices'] = data.apply(
    lambda x: 'TV + Movies' if x['StreamingTV']==1 and x['StreamingMovies']==1 else
              'TV Only' if x['StreamingTV']==1 else
              'Movies Only' if x['StreamingMovies']==1 else
              'No Streaming',
    axis=1
)

# Tenure Group
def tenure_group(x):
    if x <= 12:
        return '0-1 Year'
    elif x <= 24:
        return '1-2 Years'
    elif x <= 48:
        return '2-4 Years'
    else:
        return '4+ Years'

data['TenureGroup'] = data['tenure'].apply(tenure_group)

# Contract Risk
data['ContractRisk'] = data['Contract'].map({
    'Month-to-month': 'High Risk',
    'One year': 'Medium Risk',
    'Two year': 'Low Risk'
})

# Payment Type
data['PaymentType'] = data['PaymentMethod'].apply(
    lambda x: 'Auto' if 'automatic' in x else 'Manual'
)

# Internet Type
data['InternetType'] = data['InternetService'].replace({
    'Fiber optic': 'High Speed',
    'DSL': 'Medium Speed',
    'No': 'No Internet'
})

# High Value Customer
data['HighValueCustomer'] = data['MonthlyCharges'].apply(
    lambda x: 'Yes' if x > data['MonthlyCharges'].median() else 'No'
)

# Engagement Level
data['EngagementLevel'] = data[service_cols].sum(axis=1)

data['EngagementLevel'] = data['EngagementLevel'].apply(
    lambda x: 'Low' if x <= 2 else ('Medium' if x <= 5 else 'High')
)

# -------------------------------
# STEP-7: CONVERT BACK TO LABELS
# -------------------------------

for col in service_cols + binary_cols:
    data[col] = data[col].map({1:'Yes', 0:'No'})

data['SeniorCitizen'] = data['SeniorCitizen'].map({1:'Yes', 0:'No'})

# ✅ CUSTOM LABELS (IMPORTANT PART)

data['OnlineSecurity'] = data['OnlineSecurity'].replace({
    'Yes': 'Secure',
    'No': 'Not Secure'
})

data['OnlineBackup'] = data['OnlineBackup'].replace({
    'Yes': 'Backup Enabled',
    'No': 'No Backup'
})
data['DeviceProtection'] = data['DeviceProtection'].replace({
    'Yes': 'Protected',
    'No': 'Not Protected'
})

data['TechSupport'] = data['TechSupport'].replace({
    'Yes': 'Support Available',
    'No': 'No Support'
})

# ✅ FINAL CHURN LABEL (ADD HERE ONLY)

data['Churn'] = data['Churn'].replace({
    'Yes': 'Churned',
    'No': 'Retained'
})

# -------------------------------
# STEP-8: DROP UNNECESSARY COLUMNS
# -------------------------------

data = data.drop(columns=['customerID','StreamingTV','StreamingMovies'])

# -------------------------------
# STEP-9: SAVE FILE
# -------------------------------

data.to_csv("C:/Users/sathv/Downloads/DA --- PROJECT/customer_churn_cleaned.csv", index=False)

print("\n✅ CLEAN FILE SAVED SUCCESSFULLY!")
print(data.head())
