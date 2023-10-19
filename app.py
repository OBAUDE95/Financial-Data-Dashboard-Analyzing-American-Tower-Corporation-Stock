import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf

# Load your data. You need to have 'data' and 'groupbymonth' DataFrames defined.
# Make sure to load your financial data accordingly.

# Loading stock data
yf.pdr_override()
retrieved_data = yf.download('AMT', start='2023-01-01')
data = retrieved_data

def x(month):
    # Define a dictionary to map month numbers to month names
    month_dict = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # Check if the input month is valid (between 1 and 12)
    if 1 <= month <= 12:
        return month_dict[month]
    else:
        return "Invalid month"

data['NoMonth'] = data.index.month
data['Month'] = data['NoMonth'].apply(x)
last_month = data[data['NoMonth'] == data['NoMonth'].max()]
groupbymonth = data.groupby(data.Month).sum()
newgroup = groupbymonth

month_dict = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}
newgroup['Month_count'] = newgroup.index.map(month_dict)
newgroup.sort_values(by = 'Month_count', inplace=True)

# Define the last month data
last_month = data[data['NoMonth'] == data['NoMonth'].max()]

# Create traces for the last month's data
trace = []
columns = ['Open', 'High', 'Low', 'Close', 'Adj Close']
for column in columns:
    trace.append(
        go.Scatter(
            x=last_month.index,
            y=last_month[column],
            mode='lines+markers',
            name=column,
            text=last_month['Month'],
            marker={
                'size': 11,  # Adjust marker size
                'opacity': 0.7,  # Marker opacity
                'colorscale': 'YlGnBu',
                'line_width': 2
            }
        )
    )

# Define your content
content = ''' 
## Monthly Stock Data Visualization Dashboard

This dashboard is designed to provide an insightful and interactive visual analysis of monthly stock data. It is meticulously crafted by **Obaude Ayodeji** and centers around the financial performance of the American Tower Corporation, a prominent real estate investment trust in the United States. The company specializes in the ownership and operation of wireless and broadcast communication infrastructure, with a global presence that spans multiple countries and its headquarters based in Boston, Massachusetts.

For those seeking further details and real-time information, you can access the [American Tower Corporation Live Data](https://finance.yahoo.com/quote/AMT/) to explore and stay informed about the latest developments in the financial world.
'''

# Define your plot data for monthly volume analysis
new_plot = [
    go.Scattergl(
        x=newgroup['Volume'].index,
        y=newgroup['Volume'].values,
        mode='lines+markers',
        marker={
            'size': 14,  # Adjust marker size
            'opacity': 0.6,  # Marker opacity
            'colorscale': 'Jet',
            'line_width': 3
        }
    )
]

# Create a Dash app
app = dash.Dash()

# Define the layout
app.layout = html.Div([
    html.Div([
        html.H1("Monthly Stock Analysis", style={'text-align': 'center', 'margin-bottom': '20px'}),
        dcc.Markdown(id="brief_summary", children=content),
    ], style={'background-color': '#f7f7f7', 'padding': '20px', 'border-radius': '5px', 'box-shadow': '2px 2px 5px #888888'}),

    dcc.Graph(
        id="volume-per-month",
        figure={
            'data': new_plot,
            'layout': go.Layout(
                title="Analysis of Stock Volume for the Year 2023",  # Updated title
                xaxis={'title': 'Month'},
                yaxis={'title': 'Volume'},
                hovermode='closest'  # Show data on hover
            )
        }
    ),
    dcc.Graph(
        id='all_report',
        figure={
            'data': trace,
            'layout': go.Layout(
                title="Stock Data for the Present Month",
                xaxis={'title': 'Date'},
                yaxis={'title': 'Stock Value'},
                hovermode='closest'
            )
        }
    )
])

if __name__ == "__main__":
    app.run_server()

