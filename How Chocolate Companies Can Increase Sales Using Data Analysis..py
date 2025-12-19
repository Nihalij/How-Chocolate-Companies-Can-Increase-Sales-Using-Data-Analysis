import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv(r"C:\Users\aadis\Downloads\Chocolate Sales.csv")
print(df.head())


#1️⃣ Which products generate most of the revenue?
df["Amount"] = (df["Amount"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).astype(float))
top_product = df.groupby("Product")["Amount"].sum().nlargest(1)
print(top_product)

#2️⃣ Which countries give poor revenue despite high shipments?
country_perf = df.groupby("Country").agg( Total_Shipments = ("Boxes Shipped","sum") , Total_Amount = ("Amount","sum"))

country_perf["Revenue_per_Box"] = (country_perf["Total_Amount"] / country_perf["Total_Shipments"])

poor_revenue_countries = (country_perf.sort_values(by=["Total_Shipments", "Revenue_per_Box"],ascending=[False, True]).head(3))
print(poor_revenue_countries)

#3️⃣ Who are the most efficient salespersons?
top_salesperson = df.groupby("Sales Person").agg(Total_Amount = ("Amount","sum") , Total_Shipments = ("Boxes Shipped","sum"))

top_salesperson["Revenue_per_Box"] = top_salesperson["Total_Amount"] / top_salesperson["Total_Shipments"]

eff_salesperson = (top_salesperson.sort_values(by=["Revenue_per_Box", "Total_Shipments"], ascending=[False, False]).head(3))
print(eff_salesperson)

#4️⃣If we remove 2 worst products, do we lose money or gain profit?
worst_product = df.groupby("Product")["Amount"].sum().sort_values(ascending = True).head(2)
print(worst_product)

#Revenue vs Efficiency
df['Revenue_per_Box'] = df['Amount'] / df['Boxes Shipped']

plt.figure(figsize=(10,6))
colour = "#6a0dad" 
sns.scatterplot(data = df, x="Boxes Shipped", y="Amount", size="Revenue_per_Box", sizes = (40,400), color = colour )
plt.xlabel("Number of Boxes Shipped")
plt.ylabel("Amount")
plt.title("Revenue vs Shipment Volume with Efficiency Indicator",fontweight="bold")
sns.despine()
plt.show()

#Heatmap
plt.figure(figsize=(5,4))
sns.heatmap(df[["Amount", "Boxes Shipped"]].corr(),annot=True,cmap="Purples",linewidths=0.5)
plt.title("Correlation", fontweight="bold")
plt.show()

#Monthly trend 
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

monthly_revenue = df.groupby("Month")["Amount"].sum()
plt.figure(figsize=(10,5))
colour = sns.color_palette("Set1")[4]
monthly_revenue.plot(color = colour, label= "Amount",linewidth=5,linestyle="-")
plt.title("Monthly Revenue Trend", fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.legend()
plt.grid(linestyle=":")
sns.despine()
plt.show()


