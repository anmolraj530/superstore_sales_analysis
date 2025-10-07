import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Read the dataset
df = pd.read_csv('Superstore.csv', encoding='latin1')
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Superstore Sales Dashboard", className="text-center my-4"), width=12)
    ]),
    
    # Filters
    dbc.Row([
        dbc.Col([
            html.H5("Select Region"),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': 'All Regions', 'value': 'All'}] + 
                        [{'label': region, 'value': region} for region in df['Region'].unique()],
                value='All'
            )
        ], width=3),
        dbc.Col([
            html.H5("Select Category"),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': 'All Categories', 'value': 'All'}] + 
                        [{'label': category, 'value': category} for category in df['Category'].unique()],
                value='All'
            )
        ], width=3),
        dbc.Col([
            html.H5("Date Range"),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['Order Date'].min(),
                end_date=df['Order Date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], width=6)
    ], className="mb-4"),
    
    # Key Metrics
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Sales", className="card-title"),
                    html.H2(id="total-sales", className="card-text")
                ])
            ], className="mb-4")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Profit", className="card-title"),
                    html.H2(id="total-profit", className="card-text")
                ])
            ], className="mb-4")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Profit Margin", className="card-title"),
                    html.H2(id="profit-margin", className="card-text")
                ])
            ], className="mb-4")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Number of Orders", className="card-title"),
                    html.H2(id="num-orders", className="card-text")
                ])
            ], className="mb-4")
        ], width=3)
    ]),
    
    # Charts
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sales-profit-by-region')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='monthly-trend')
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='category-performance')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='discount-profit')
        ], width=6)
    ])
], fluid=True)

# Callback for updating metrics
@app.callback(
    [Output('total-sales', 'children'),
     Output('total-profit', 'children'),
     Output('profit-margin', 'children'),
     Output('num-orders', 'children')],
    [Input('region-filter', 'value'),
     Input('category-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_metrics(region, category, start_date, end_date):
    filtered_df = df.copy()
    
    if region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category]
    if start_date:
        filtered_df = filtered_df[filtered_df['Order Date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Order Date'] <= end_date]
    
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    num_orders = len(filtered_df['Order ID'].unique())
    
    return f'${total_sales:,.2f}', f'${total_profit:,.2f}', f'{profit_margin:.1f}%', f'{num_orders:,}'

# Callback for sales and profit by region
@app.callback(
    Output('sales-profit-by-region', 'figure'),
    [Input('category-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_regional_chart(category, start_date, end_date):
    filtered_df = df.copy()
    
    if category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category]
    if start_date:
        filtered_df = filtered_df[filtered_df['Order Date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Order Date'] <= end_date]
    
    regional_data = filtered_df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=regional_data['Region'],
        y=regional_data['Sales'],
        name='Sales',
        marker_color='#27ae60'
    ))
    fig.add_trace(go.Bar(
        x=regional_data['Region'],
        y=regional_data['Profit'],
        name='Profit',
        marker_color='#2980b9'
    ))
    
    fig.update_layout(
        title='Sales and Profit by Region',
        barmode='group',
        template='plotly_white'
    )
    
    return fig

# Callback for monthly trend
@app.callback(
    Output('monthly-trend', 'figure'),
    [Input('region-filter', 'value'),
     Input('category-filter', 'value')]
)
def update_monthly_trend(region, category):
    filtered_df = df.copy()
    
    if region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category]
    
    monthly_data = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly_data['Order Date'] = monthly_data['Order Date'].astype(str)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_data['Order Date'],
        y=monthly_data['Sales'],
        name='Sales',
        line=dict(color='#27ae60')
    ))
    fig.add_trace(go.Scatter(
        x=monthly_data['Order Date'],
        y=monthly_data['Profit'],
        name='Profit',
        line=dict(color='#2980b9')
    ))
    
    fig.update_layout(
        title='Monthly Sales and Profit Trend',
        template='plotly_white'
    )
    
    return fig

# Callback for category performance
@app.callback(
    Output('category-performance', 'figure'),
    [Input('region-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_category_chart(region, start_date, end_date):
    filtered_df = df.copy()
    
    if region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if start_date:
        filtered_df = filtered_df[filtered_df['Order Date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Order Date'] <= end_date]
    
    category_data = filtered_df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=category_data['Category'],
        y=category_data['Sales'],
        name='Sales',
        marker_color='#27ae60'
    ))
    fig.add_trace(go.Bar(
        x=category_data['Category'],
        y=category_data['Profit'],
        name='Profit',
        marker_color='#2980b9'
    ))
    
    fig.update_layout(
        title='Category Performance',
        barmode='group',
        template='plotly_white'
    )
    
    return fig

# Callback for discount vs profit
@app.callback(
    Output('discount-profit', 'figure'),
    [Input('region-filter', 'value'),
     Input('category-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_discount_chart(region, category, start_date, end_date):
    filtered_df = df.copy()
    
    if region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category]
    if start_date:
        filtered_df = filtered_df[filtered_df['Order Date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Order Date'] <= end_date]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df['Discount'],
        y=filtered_df['Profit'],
        mode='markers',
        marker=dict(
            size=8,
            color=filtered_df['Sales'],
            colorscale='Viridis',
            showscale=True
        )
    ))
    
    fig.update_layout(
        title='Discount vs Profit Relationship',
        xaxis_title='Discount',
        yaxis_title='Profit',
        template='plotly_white'
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
