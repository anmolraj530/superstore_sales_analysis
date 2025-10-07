import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set style for better visualizations
plt.style.use('default')
sns.set_theme()

# Read the dataset
print("Loading the dataset...")
df = pd.read_csv('Superstore.csv', encoding='latin1')

# Display basic information
print("\nDataset Info:")
print(df.info())

print("\nFirst few rows of the dataset:")
print(df.head())

# Data Quality Checks
print("\nChecking for missing values:")
print(df.isnull().sum())

print("\nChecking for duplicates:")
print(f"Number of duplicate rows: {df.duplicated().sum()}")

# Convert date columns to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Basic Statistics
print("\nBasic Statistics for Sales and Profit:")
print(df[['Sales', 'Profit']].describe())

# Create a directory for saving visualizations
import os
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

# 1. Sales and Profit Analysis by Region
plt.figure(figsize=(12, 6))
regional_metrics = df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

# Create a bar plot
x = np.arange(len(regional_metrics['Region']))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width/2, regional_metrics['Sales'], width, label='Sales')
rects2 = ax.bar(x + width/2, regional_metrics['Profit'], width, label='Profit')

ax.set_ylabel('Amount ($)')
ax.set_title('Sales and Profit by Region')
ax.set_xticks(x)
ax.set_xticklabels(regional_metrics['Region'])
ax.legend()

plt.tight_layout()
plt.savefig('visualizations/regional_analysis.png')
plt.close()

# 2. Monthly Sales Trend
plt.figure(figsize=(15, 6))
monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()
monthly_sales.plot(kind='line', marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/monthly_sales_trend.png')
plt.close()

# 3. Category and Sub-Category Analysis
plt.figure(figsize=(15, 6))
category_metrics = df.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

# Create a grouped bar plot
x = np.arange(len(category_metrics['Category']))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width/2, category_metrics['Sales'], width, label='Sales')
rects2 = ax.bar(x + width/2, category_metrics['Profit'], width, label='Profit')

ax.set_ylabel('Amount ($)')
ax.set_title('Sales and Profit by Category')
ax.set_xticks(x)
ax.set_xticklabels(category_metrics['Category'])
ax.legend()

plt.tight_layout()
plt.savefig('visualizations/category_analysis.png')
plt.close()

# 4. Discount vs Profit Analysis
plt.figure(figsize=(10, 6))
plt.scatter(df['Discount'], df['Profit'], alpha=0.5)
plt.title('Relationship between Discount and Profit')
plt.xlabel('Discount')
plt.ylabel('Profit ($)')
plt.tight_layout()
plt.savefig('visualizations/discount_profit_analysis.png')
plt.close()

# Calculate correlation between discount and profit
correlation = df['Discount'].corr(df['Profit'])
print(f"\nCorrelation between Discount and Profit: {correlation:.2f}")

# 5. Customer Segment Analysis
segment_metrics = df.groupby('Segment').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).reset_index()

print("\nCustomer Segment Analysis:")
print(segment_metrics)

# Save the analysis results to a text file
with open('analysis_results.txt', 'w') as f:
    f.write("Superstore Sales Analysis Results\n")
    f.write("================================\n\n")
    
    f.write("1. Regional Performance:\n")
    f.write(regional_metrics.to_string())
    f.write("\n\n")
    
    f.write("2. Category Performance:\n")
    f.write(category_metrics.to_string())
    f.write("\n\n")
    
    f.write("3. Customer Segment Analysis:\n")
    f.write(segment_metrics.to_string())
    f.write("\n\n")
    
    f.write(f"4. Discount-Profit Correlation: {correlation:.2f}\n")

print("\nAnalysis complete! Check the 'visualizations' folder for plots and 'analysis_results.txt' for detailed metrics.") 