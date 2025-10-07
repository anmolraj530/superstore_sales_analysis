# Superstore Sales Analysis

## Project Overview
This project performs an in-depth Exploratory Data Analysis (EDA) of a Superstore's sales data to uncover key business insights and trends. The analysis covers various aspects including regional performance, product categories, customer segments, and the impact of discounts on profitability.

## Dataset
The dataset used in this analysis is the Superstore Sales Dataset, which contains information about:
- Sales transactions
- Product categories and subcategories
- Customer segments
- Regional performance
- Shipping details
- Profit and discount information

## Tools Used
- Python 3.x
- Pandas (Data manipulation and analysis)
- NumPy (Numerical computations)
- Matplotlib (Data visualization)
- Seaborn (Enhanced visualization)

## Project Structure
```
superstore_sales_analysis/
│
├── eda_superstore.py      # Main analysis script
├── Superstore.csv         # Dataset
├── README.md             # Project documentation
│
└── results/              # Analysis outputs
    ├── analysis_summary.txt    # Key insights
    ├── data_summary.txt        # Detailed metrics
    ├── regional_analysis.png   # Regional performance visualization
    ├── monthly_sales_trend.png # Sales trend visualization
    ├── category_analysis.png   # Category performance visualization
    └── discount_profit_analysis.png # Discount impact visualization
```

## Key Findings

### Regional Performance
- West region leads in both sales ($725,458) and profit ($108,418)
- Central region has the lowest profit margin (7.92%)
- Profit margins range from 7.92% to 14.94% across regions

### Category Analysis
- Technology category shows the highest average profit margin
- Some categories show negative profit margins:
  - Bookcases (-3.02%)
  - Tables (-8.56%)
  - Supplies (-2.55%)
- Top performing categories by margin:
  - Labels (44.42%)
  - Paper (43.39%)
  - Envelopes (42.27%)

### Customer Segments
- Consumer segment leads with highest sales ($1.16M)
- Corporate segment is second in sales
- Home Office segment shows highest profit per order

### Discount Impact
- Negative correlation (-0.219) between discounts and profit
- Higher discounts generally lead to lower profits
- Average discount rate: 15.62%

### Overall Business Metrics
- Total Sales: $2,297,200.86
- Total Profit: $286,397.02
- Overall Profit Margin: 12.47%
- Average Order Value: $229.86

## How to Run
1. Ensure you have Python 3.x installed
2. Install required packages:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
3. Place the Superstore.csv file in the project directory
4. Run the analysis script:
   ```bash
   python eda_superstore.py
   ```
5. Check the results folder for generated visualizations and insights

## Output Files
The analysis generates several output files in the results directory:
- **analysis_summary.txt**: Contains key insights and findings
- **data_summary.txt**: Detailed metrics and raw data summaries
- Various PNG files with visualizations:
  - Regional performance
  - Monthly sales trends
  - Category analysis
  - Discount-profit relationship

## Future Improvements
Potential areas for further analysis:
1. Time series forecasting for sales prediction
2. Customer segmentation analysis
3. Product recommendation system
4. Inventory optimization
5. Shipping cost analysis

## Contributing
Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch
3. Making your changes
4. Submitting a pull request

## License
This project is open source and available under the MIT License. 