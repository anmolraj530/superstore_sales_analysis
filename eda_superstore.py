import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Create results directory if it doesn't exist
if not os.path.exists("results"):
    os.makedirs("results")


# Function to save insights to text file
def save_insights(insights_dict, filepath):
    with open(filepath, "w") as f:
        f.write("SUPERSTORE SALES ANALYSIS INSIGHTS\n")
        f.write("=================================\n\n")
        for section, insights in insights_dict.items():
            f.write(f"{section}\n")
            f.write("-" * len(section) + "\n")
            for insight in insights:
                f.write(f"- {insight}\n")
            f.write("\n")


# Set the style for better visualizations
plt.style.use("default")
sns.set_theme()

# Read the dataset
print("Loading dataset...")
df = pd.read_csv("Superstore.csv", encoding="latin1")

# Optimize data types for better performance
print("Optimizing data types...")
# Convert date columns to datetime
date_columns = ["Order Date", "Ship Date"]
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col])

# Convert numeric columns to appropriate types
numeric_columns = ["Sales", "Quantity", "Discount", "Profit"]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Create correlation heatmap
print("Creating correlation heatmap...")
numeric_df = df.select_dtypes(include=[np.number])
correlation_matrix = numeric_df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation_matrix,
    annot=True,  # Show correlation values
    cmap="coolwarm",  # Color scheme
    center=0,  # Center the colormap at 0
    fmt=".2f",  # Format correlation values to 2 decimal places
    square=True,
)  # Make the plot square-shaped
plt.title("Correlation Heatmap of Numeric Variables")
plt.tight_layout()
plt.savefig("results/correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()

# Optimize groupby operations using categorical data types
print("Optimizing categorical columns...")
categorical_columns = ["Region", "Category", "Sub-Category", "Segment"]
for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].astype("category")

# Initialize insights dictionary
insights = {
    "Data Quality": [],
    "Regional Performance": [],
    "Category Analysis": [],
    "Customer Segments": [],
    "Discount Analysis": [],
    "Overall Business Metrics": [],
}

# Data Quality Checks
print("\n=== Data Quality Checks ===")

# Check for null values
null_counts = df.isnull().sum()
if null_counts.any():
    insights["Data Quality"].append(f"Found {null_counts.sum()} null values")
else:
    insights["Data Quality"].append("No null values found in the dataset")

# Check for duplicates
duplicate_rows = df.duplicated().sum()
insights["Data Quality"].append(f"Found {duplicate_rows} duplicate rows")

# Check data types
print("\nCurrent data types:")
print(df.dtypes)

# Check for any remaining issues
print("\nData types after conversion:")
print(df.dtypes)

# Regional Analysis with optimized groupby
print("\nPerforming regional analysis...")
regional_metrics = (
    df.groupby("Region")
    .agg({"Sales": "sum", "Profit": "sum", "Order ID": "count"})
    .rename(columns={"Order ID": "Number of Orders"})
)

regional_metrics["Profit Margin"] = (
    regional_metrics["Profit"] / regional_metrics["Sales"] * 100
).round(2)
regional_metrics = regional_metrics.sort_values("Sales", ascending=False)

# Add regional insights
insights["Regional Performance"].extend(
    [
        f"West region leads with ${regional_metrics.loc['West', 'Sales']:,.2f} in sales and ${regional_metrics.loc['West', 'Profit']:,.2f} in profit",
        f"Central region has lowest profit margin at {regional_metrics.loc['Central', 'Profit Margin']:.2f}%",
        f"Profit margins range from {regional_metrics['Profit Margin'].min():.2f}% to {regional_metrics['Profit Margin'].max():.2f}%",
    ]
)

# Create regional analysis plots
plt.figure(figsize=(15, 10))

# Sales by Region
plt.subplot(2, 2, 1)
sales_by_region = regional_metrics["Sales"].sort_values(ascending=False)
ax1 = sales_by_region.plot(kind="bar", color="skyblue")
plt.title("Total Sales by Region", pad=20)
plt.xlabel("Region")
plt.ylabel("Sales ($)")
plt.xticks(rotation=45)
for i, v in enumerate(sales_by_region):
    ax1.text(i, v, f"${v:,.0f}", ha="center", va="bottom")

# Profit by Region
plt.subplot(2, 2, 2)
profit_by_region = regional_metrics["Profit"].sort_values(ascending=False)
ax2 = profit_by_region.plot(kind="bar", color="lightgreen")
plt.title("Total Profit by Region", pad=20)
plt.xlabel("Region")
plt.ylabel("Profit ($)")
plt.xticks(rotation=45)
for i, v in enumerate(profit_by_region):
    ax2.text(i, v, f"${v:,.0f}", ha="center", va="bottom")

plt.tight_layout()
plt.savefig("results/regional_analysis.png", dpi=300, bbox_inches="tight")
plt.close()

# Monthly Sales Trend Analysis
print("\n=== Monthly Sales Trend Analysis ===")

# Create monthly sales trend
monthly_sales = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()
monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(15, 6))
ax = monthly_sales.plot(kind="line", marker="o", linewidth=2, markersize=8)
plt.title("Monthly Sales Trend", pad=20, size=14)
plt.xlabel("Month", size=12)
plt.ylabel("Sales ($)", size=12)
plt.grid(True, linestyle="--", alpha=0.7)

# Add value labels
for i, v in enumerate(monthly_sales):
    ax.text(i, v, f"${v:,.0f}", ha="center", va="bottom")

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("results/monthly_sales_trend.png", dpi=300, bbox_inches="tight")
plt.close()

# Category and Sub-Category Analysis
print("\n=== Category and Sub-Category Analysis ===")

# Calculate metrics by Category and Sub-Category
category_metrics = (
    df.groupby(["Category", "Sub-Category"])
    .agg({"Sales": "sum", "Profit": "sum", "Order ID": "count"})
    .rename(columns={"Order ID": "Number of Orders"})
)

# Calculate profit margin
category_metrics["Profit Margin"] = (
    category_metrics["Profit"] / category_metrics["Sales"] * 100
).round(2)

print("\nCategory and Sub-Category Performance Metrics:")
print(category_metrics)

# Add category insights
negative_margin_categories = category_metrics[category_metrics["Profit Margin"] < 0]
top_margin_categories = category_metrics.nlargest(3, "Profit Margin")

insights["Category Analysis"].extend(
    [
        f"Found {len(negative_margin_categories)} categories with negative profit margins",
        f"Top performing category by margin: {top_margin_categories.index[0][1]} ({top_margin_categories['Profit Margin'].iloc[0]:.2f}%)",
        f"Technology category has highest average profit margin",
    ]
)

# Create visualizations for Category and Sub-Category
plt.figure(figsize=(15, 10))

# Sales by Category and Sub-Category
plt.subplot(2, 2, 1)
category_sales = df.groupby(["Category", "Sub-Category"])["Sales"].sum().unstack()
category_sales.plot(kind="bar", stacked=True)
plt.title("Sales by Category and Sub-Category", pad=20)
plt.xlabel("Category")
plt.ylabel("Sales ($)")
plt.xticks(rotation=45)
plt.legend(title="Sub-Category", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

# Profit by Category and Sub-Category
plt.subplot(2, 2, 2)
category_profit = df.groupby(["Category", "Sub-Category"])["Profit"].sum().unstack()
category_profit.plot(kind="bar", stacked=True)
plt.title("Profit by Category and Sub-Category", pad=20)
plt.xlabel("Category")
plt.ylabel("Profit ($)")
plt.xticks(rotation=45)
plt.legend(title="Sub-Category", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

plt.savefig("results/category_analysis.png", dpi=300, bbox_inches="tight")
plt.close()

# Discount vs Profit Analysis
print("\n=== Discount vs Profit Analysis ===")

# Create scatter plot
plt.figure(figsize=(12, 6))
plt.scatter(df["Discount"], df["Profit"], alpha=0.5, c=df["Sales"], cmap="viridis")
plt.colorbar(label="Sales Amount")
plt.title("Relationship between Discount and Profit", pad=20)
plt.xlabel("Discount Rate")
plt.ylabel("Profit ($)")
plt.grid(True, linestyle="--", alpha=0.7)

# Add trend line
z = np.polyfit(df["Discount"], df["Profit"], 1)
p = np.poly1d(z)
plt.plot(df["Discount"], p(df["Discount"]), "r--", alpha=0.8)

plt.tight_layout()
plt.savefig("results/discount_profit_analysis.png", dpi=300, bbox_inches="tight")
plt.close()

# Calculate correlation
correlation = df["Discount"].corr(df["Profit"])
print(f"\nCorrelation between Discount and Profit: {correlation:.3f}")

# Display basic information about the dataset
print("\nDataset Info:")
print(df.info())

print("\nFirst few rows of the dataset:")
print(df.head())

print("\nBasic statistics:")
print(df.describe())

# Check for missing values
print("\nMissing values in each column:")
print(df.isnull().sum())

# Display unique values in categorical columns
print("\nUnique values in categorical columns:")
categorical_columns = df.select_dtypes(include=["object"]).columns
for col in categorical_columns:
    print(f"\n{col}:")
    print(df[col].value_counts().head())

# Calculate and display key metrics
print("\nKey Metrics:")
print(f"Total Sales: ${df['Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Average Order Value: ${df['Sales'].mean():,.2f}")
print(f"Profit Margin: {(df['Profit'].sum() / df['Sales'].sum() * 100):,.2f}%")

# Customer segment analysis
plt.figure(figsize=(10, 6))
segment_metrics = (
    df.groupby("Segment")
    .agg({"Sales": "sum", "Profit": "sum", "Order ID": "count"})
    .rename(columns={"Order ID": "Number of Orders"})
)
print("\nCustomer Segment Analysis:")
print(segment_metrics)

# Add customer segment insights
insights["Customer Segments"].extend(
    [
        f"Consumer segment leads with ${segment_metrics.loc['Consumer', 'Sales']:,.2f} in sales",
        f"Corporate segment second with ${segment_metrics.loc['Corporate', 'Sales']:,.2f} in sales",
        f"Home Office has highest profit per order at ${segment_metrics.loc['Home Office', 'Profit'] / segment_metrics.loc['Home Office', 'Number of Orders']:,.2f}",
    ]
)

# Create interactive dashboard using Plotly Dash
print("\nCreating interactive dashboard...")
app = Dash(__name__)

# Define the layout
app.layout = html.Div(
    [
        html.H1("Superstore Sales Dashboard"),
        # Region selector
        html.Div(
            [
                html.H3("Select Region"),
                dcc.Dropdown(
                    id="region-selector",
                    options=[
                        {"label": region, "value": region}
                        for region in df["Region"].unique()
                    ],
                    value="West",
                ),
            ]
        ),
        # Sales and Profit by Category
        html.Div([dcc.Graph(id="category-performance")]),
        # Monthly Sales Trend
        html.Div([dcc.Graph(id="monthly-trend")]),
        # Discount vs Profit
        html.Div([dcc.Graph(id="discount-profit")]),
    ]
)


# Callback for category performance
@app.callback(
    Output("category-performance", "figure"), Input("region-selector", "value")
)
def update_category_performance(selected_region):
    filtered_df = df[df["Region"] == selected_region]
    category_data = (
        filtered_df.groupby("Category")
        .agg({"Sales": "sum", "Profit": "sum"})
        .reset_index()
    )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=category_data["Category"], y=category_data["Sales"], name="Sales")
    )
    fig.add_trace(
        go.Bar(x=category_data["Category"], y=category_data["Profit"], name="Profit")
    )

    fig.update_layout(
        title=f"Category Performance in {selected_region}", barmode="group"
    )
    return fig


# Callback for monthly trend
@app.callback(Output("monthly-trend", "figure"), Input("region-selector", "value"))
def update_monthly_trend(selected_region):
    filtered_df = df[df["Region"] == selected_region]
    monthly_data = filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))[
        "Sales"
    ].sum()
    monthly_data.index = monthly_data.index.astype(str)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=monthly_data.index, y=monthly_data.values, mode="lines+markers")
    )

    fig.update_layout(
        title=f"Monthly Sales Trend in {selected_region}",
        xaxis_title="Month",
        yaxis_title="Sales",
    )
    return fig


# Callback for discount-profit relationship
@app.callback(Output("discount-profit", "figure"), Input("region-selector", "value"))
def update_discount_profit(selected_region):
    filtered_df = df[df["Region"] == selected_region]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_df["Discount"],
            y=filtered_df["Profit"],
            mode="markers",
            marker=dict(
                size=8, color=filtered_df["Sales"], colorscale="Viridis", showscale=True
            ),
        )
    )

    fig.update_layout(
        title=f"Discount vs Profit in {selected_region}",
        xaxis_title="Discount",
        yaxis_title="Profit",
    )
    return fig


# Save the dashboard layout to a file
with open("results/dashboard_layout.txt", "w") as f:
    f.write(str(app.layout))

print("\nDashboard layout saved to results/dashboard_layout.txt")
print("To run the dashboard, use: python -m dash run eda_superstore.py")

# Save all insights to a text file
save_insights(insights, "results/analysis_summary.txt")

# Save raw data summaries
with open("results/data_summary.txt", "w") as f:
    f.write("DATA SUMMARY\n")
    f.write("============\n\n")
    f.write("Regional Metrics:\n")
    f.write(regional_metrics.to_string())
    f.write("\n\nCategory Metrics:\n")
    f.write(category_metrics.to_string())
    f.write("\n\nSegment Metrics:\n")
    f.write(segment_metrics.to_string())
