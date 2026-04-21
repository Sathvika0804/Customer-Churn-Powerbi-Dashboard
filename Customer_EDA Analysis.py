import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("C:/Users/sathv/Downloads/DA --- PROJECT/customer_churn_cleaned.csv")

sns.set_style("whitegrid")

# -------------------------------
# 1. CHURN DISTRIBUTION (PIE CHART)
# -------------------------------
plt.figure()
data['Churn'].value_counts().plot.pie(
    autopct='%1.1f%%',
    colors=['skyblue','orange']
)
plt.title("Churn Distribution")
plt.ylabel('')
plt.show()

# -------------------------------
# 2. CONTRACT vs CHURN
# -------------------------------
plt.figure()
sns.countplot(x='Contract', hue='Churn', data=data, palette='Set2')
plt.title("Churn by Contract Type")
plt.xticks(rotation=20)
plt.show()

# -------------------------------
# 3. TENURE GROUP (STACKED BAR)
# -------------------------------
ct = pd.crosstab(data['TenureGroup'], data['Churn'])
ct.plot(kind='bar', stacked=True, colormap='coolwarm')
plt.title("Churn by Tenure Group")
plt.show()

# -------------------------------
# 4. PAYMENT TYPE (DONUT CHART)
# -------------------------------
plt.figure()
data['PaymentType'].value_counts().plot.pie(
    autopct='%1.1f%%',
    colors=['lightgreen','coral'],
    wedgeprops={'width':0.4}
)
plt.title("Payment Type Distribution")
plt.ylabel('')
plt.show()

# -------------------------------
# 5. INTERNET TYPE
# -------------------------------
plt.figure()
sns.countplot(x='InternetType', hue='Churn', data=data, palette='viridis')
plt.title("Churn by Internet Type")
plt.show()

# -------------------------------
# 6. STREAMING SERVICES
# -------------------------------
plt.figure()
sns.countplot(y='StreamingServices', hue='Churn', data=data, palette='magma')
plt.title("Churn by Streaming Services")
plt.show()

# -------------------------------
# 7. ENGAGEMENT LEVEL
# -------------------------------
plt.figure()
sns.countplot(x='EngagementLevel', hue='Churn', data=data, palette='Set1')
plt.title("Churn by Engagement Level")
plt.show()

# -------------------------------
# 8. ONLINE SECURITY
# -------------------------------
plt.figure()
sns.countplot(x='OnlineSecurity', hue='Churn', data=data, palette='cool')
plt.title("Churn by Online Security")
plt.xticks(rotation=20)
plt.show()

# -------------------------------
# 9. MONTHLY CHARGES (HISTOGRAM)
# -------------------------------
plt.figure()
sns.histplot(data=data, x='MonthlyCharges', hue='Churn', kde=True, palette='husl')
plt.title("Monthly Charges Distribution")
plt.show()

# -------------------------------
# 10. AVG MONTHLY SPEND (BOX PLOT)
# -------------------------------
plt.figure()
sns.boxplot(x='Churn', y='AvgMonthlySpend', data=data, palette='pastel')
plt.title("Avg Monthly Spend vs Churn")
plt.show()

# -------------------------------
# 11. TENURE (BOX PLOT)
# -------------------------------
plt.figure()
sns.boxplot(x='Churn', y='tenure', data=data, palette='Set3')
plt.title("Tenure vs Churn")
plt.show()

# -------------------------------
# 12. CORRELATION HEATMAP
# -------------------------------
plt.figure()
numeric_data = data.select_dtypes(include=['int64','float64'])
sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()
