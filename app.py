from dash import dcc, html
import plotly.graph_objs as go
import yfinance as yf
import dash

# Load stock data
yf.pdr_override()
data = yf.download('AMT', start='2023-01-01')

# Process data
data['NoMonth'] = data.index.month
data['Month'] = data['NoMonth'].apply(lambda month: {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                                                      7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}.get(month, "Invalid month"))
last_month = data[data['NoMonth'] == data['NoMonth'].max()]
groupbymonth = data.groupby(data.Month).sum()
groupbymonth['Month_count'] = groupbymonth.index.map({'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                                                      'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12})
groupbymonth.sort_values(by='Month_count', inplace=True)

# Create traces for the last month's data
trace = []
columns = ['Open', 'High', 'Low', 'Close', 'Adj Close']
symbols = ['circle', 'triangle-up', 'triangle-down', 'square', 'diamond']
color_scales = ['Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis']

for column, symbol, color in zip(columns, symbols, color_scales):
    trace.append(go.Scatter(x=last_month.index, y=last_month[column], mode='lines+markers',
                            name=column, text=last_month['Month'], marker={'size': 8, 'opacity': 1, 'colorscale': color, 'line_width': 2, 'symbol': symbol}))

# Define content
content = '''
**Monthly Stock Data Visualization**

Explore American Tower Corporation's monthly stock data. Crafted by **Obaude Ayodeji**, this dashboard provides interactive insights into the company's financial performance. For real-time updates, visit [American Tower Corporation Live Data](https://finance.yahoo.com/quote/AMT/).
'''

# Define your plot data for monthly volume analysis
volume_plot = [go.Scattergl(x=groupbymonth['Volume'].index, y=groupbymonth['Volume'].values, mode='lines+markers',
                            marker={'size': 10, 'opacity': 0.6, 'colorscale': 'RdBu', 'line_width': 1})]

# Create a Dash app
app = dash.Dash()
server = app.server
# Define the layout
app.layout = html.Div([
    html.Div([html.H1("Monthly Stock Analysis", style={'text-align': 'center', 'margin-bottom': '20px'}),
              dcc.Markdown(id="brief_summary", children=content)],
             style={'background-color': '#f7f7f7', 'padding': '20px', 'border-radius': '5px', 'box-shadow': '2px 2px 5px #888888'}),

    dcc.Graph(id="volume-per-month", figure={'data': volume_plot,
                                              'layout': go.Layout(title="Stock Volume Analysis 2023", xaxis={'title': 'Month'},
                                                                  yaxis={'title': 'Volume'}, hovermode='closest')}),
    dcc.Graph(id='all_report', figure={'data': trace, 'layout': go.Layout(title="Stock Data for the Present Month", xaxis={'title': 'Days'},
                                                                       yaxis={'title': 'Stock Value'}, hovermode='closest')})
])

if __name__ == "__main__":
    app.run_server()
