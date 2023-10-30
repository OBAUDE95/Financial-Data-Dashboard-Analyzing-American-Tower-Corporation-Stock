import dash
from dash import dcc, html
import plotly.graph_objs as go
import yfinance as yf
from dash.dependencies import Input, Output
import json

# Load your stock data
yf.pdr_override()
retrieved_data = yf.download('AMT', start='2023-01-01')
data = retrieved_data

# Define a function to convert month number to month name
def x(month):
    month_dict = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    if 1 <= month <= 12:
        return month_dict[month]
    else:
        return "Invalid month"

# Add a 'Month' column to the data
data['NoMonth'] = data.index.month
data['Month'] = data['NoMonth'].apply(x)
data['day'] = data.index.day
data['formatted'] = 'Day'  + ' ' + data['day'].astype('str')
last_month = data[data['NoMonth'] == data['NoMonth'].max()]
groupbymonth = data.groupby(data.Month).sum()
newgroup = groupbymonth

# Create a dictionary to map month names to month numbers
month_dict = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}
newgroup['Month_count'] = newgroup.index.map(month_dict)
newgroup.sort_values(by='Month_count', inplace=True)

# Define the last month data
last_month = data[data['NoMonth'] == data['NoMonth'].max()]

# Create traces for the last month's data
trace = []
columns = ['Open', 'High', 'Low', 'Close', 'Adj Close']

data_categories = ['Open', 'High', 'Low', 'Close', 'Adj Close']
symbols = ['circle', 'triangle-up', 'triangle-down', 'square', 'diamond']
color_scales = ['Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis']

for column, symboled, color in zip(columns, symbols, color_scales):
    trace.append(
        go.Scatter(
            x=last_month.index,
            y=last_month[column],
            mode='lines+markers',
            name=column,
            text=last_month['Month'],
            marker={
                'size': 8,
                'opacity': 1,
                'colorscale': color,
                'line_width': 2,
                'symbol': symboled,
            }
        )
    )

# Define your content
content = '''
**Monthly Stock Data Visualization**

Explore American Tower Corporation's monthly stock data. Crafted by **Obaude Ayodeji**, this dashboard provides interactive insights into the company's financial performance. For real-time updates, visit [American Tower Corporation Live Data](https://finance.yahoo.com/quote/AMT/).
'''

# Create a Dash app
app = dash.Dash(__name__)
server = app.server
# Define the layout
app.layout = html.Div([
    html.Div([
        html.H1("Monthly Stock Analysis", style={'text-align': 'center', 'margin-bottom': '20px'}),
        dcc.Markdown(id="brief_summary", children=content),
    ], style={'background-color': '#f7f7f7', 'padding': '20px', 'border-radius': '5px', 'box-shadow': '2px 2px 5px #888888'}),

    html.Div([dcc.Graph(
        id="volume-per-month",
        figure={
            'data': [
                go.Bar(
                    x=newgroup['Volume'].index,
                    y=newgroup['Volume'].values,
                    text=newgroup['Volume'].values,
                    textposition='outside',
                    marker_color='indianred'
               )
        ]
            ,
            'layout': go.Layout(
                title="Analysis of Stock Volume for the Year 2023",
                xaxis={'title': 'Month'},
                yaxis={'title': 'Volume'},
                hovermode='closest'
            )
        }, style=dict(width='65%',display='inline-block')
    ),  dcc.Graph(
            id='localgraph',
            figure={
                'data': [go.Scatter(
                    x=[],
                    y=[],
                    mode='markers+lines',
                    marker=dict(size=8, opacity=1, colorscale='Viridis'),
                    text=[]
                )],
                'layout': go.Layout(
                    title="Hover data output",
                    xaxis={'title': 'Volume'},
                    yaxis={'title': 'Open'},
                    hovermode='closest'
                )
            }, style=dict(width='35%',display='inline-block')
        )



             ]),
    html.Div([
        dcc.Graph(
            id='all_report',
            figure={
                'data': trace,
                'layout': go.Layout(
                    title="Stock Data for the Present Month",
                    xaxis={'title': 'Days'},
                    yaxis={'title': 'Stock Value'},
                    hovermode='closest'
                )
            }
        )
      ,
    ], style={'width': '70%'}),
])

@app.callback(Output('localgraph', 'figure'), Input('volume-per-month', 'clickData'))
def receive(hoverdata):
    data2 = json.loads(json.dumps(hoverdata))
    month = data2['points'][0]['x']

    # Output: "July"

    df3 = data[data['Month'] == month]
    trace2 = go.Scatter(
        x=df3['day'],
        y=df3['Volume'],
        mode='markers+lines',
        marker=dict(size=10, opacity=1, colorscale='Viridis'),
        text=df3['formatted'],name=month
    )

    return {
        'data': [trace2],
        'layout': go.Layout(
            title=f"{month} - Stock Volume per Day",
            xaxis={'title': 'day'},
            yaxis={'title': 'Volume'},
            hovermode='closest'
        )
    }

if __name__ == "__main__":
    app.run_server(port=85)
