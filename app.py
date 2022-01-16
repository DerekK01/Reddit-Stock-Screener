from pickle import TRUE
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import pandas_datareader.data as web
from datetime import date as dt
import time

tesla = {}
for i in range(1,31):
    date = '2021_11_' + str(i)
    df = pd.read_csv('TestData/Reddit Raw Data/mention_'+date+'.csv')
    #tesla.append(int(df.loc[df['Stock'] == 'TSLA']['Num_of_mention']))
    tesla[date] =  int(df.loc[df['Stock'] == 'TSLA']['Num_of_mention'])
tesla_df = pd.DataFrame.from_dict(tesla, orient='index',columns=["Mention"])






app = Dash(__name__)
server = app.server
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(children="Stock Reddit Screener"),
                html.P(
                    id="description",
                    children="Screener for reddit",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the year:",
                                ),
                                    dcc.Dropdown(id="stock_dropdown",
                                                options=[
                                                    {"label": "TSLA", "value": 'TSLA'},
                                                    {"label": "AAPL", "value": 'AAPL'},
                                                    {"label": "GOOGL", "value": 'GOOGL'},
                                                    {"label": "GME", "value": 'GME'},
                                                    {"label": "SE", "value": 'SE'},
                                                    {"label": "NVDA", "value": 'NVDA'},
                                                    {"label": "AMC", "value": 'AMC'}],
                                                multi=False,
                                                value='TSLA',
                                                style={'width': "60%"}
                                                ),
                                    dcc.RadioItems(id='stock_radio',
                                    options=[
                                        {'label': 'Line (close)', 'value': 'LINE'},
                                        {'label': 'CandleStick', 'value': 'CS'},
                                    ],
                                    value='LINE'
                                    ),
                                    html.Br(),
                                    dcc.DatePickerRange(
                                        id='stock_date_range',
                                        min_date_allowed=dt(1995, 8, 5),
                                        max_date_allowed=dt.today(),
                                        initial_visible_month=dt.today(),
                                        updatemode='bothdates',
                                        style={'color': "#7fafdf"}

                                    ),
                            ],
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    "Stock Screener",
                                    id="heatmap-title",
                                ),
                                dcc.Graph(id='stock_graph', figure={}),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select chart:"),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "TSLA",
                                    "value": "TSLA",
                                },
                                {
                                    "label": "(coming soon)",
                                    "value": "absolute_deaths_all_time",
                                },
                                {
                                    "label": "(coming soon)",
                                    "value": "show_death_rate_single_year",
                                },
                                {
                                    "label": "(coming soon)",
                                    "value": "death_rate_all_time",
                                },
                            ],
                            value="TSLA",
                            id="chart-dropdown",
                        ),
                        dcc.Graph(id='stock_reddit_mention', figure={}),
                    ],
                ),
            ],
        ),
    ],
)






#     html.Div([

#     html.H1("Stock Reddit Screener", style={'text-align': 'center'}),

#     dcc.Dropdown(id="stock_dropdown",
#                  options=[
#                      {"label": "TSLA", "value": 'TSLA'},
#                      {"label": "AAPL", "value": 'AAPL'},
#                      {"label": "GOOGL", "value": 'GOOGL'},
#                      {"label": "GME", "value": 'GME'},
#                      {"label": "SE", "value": 'SE'},
#                      {"label": "NVDA", "value": 'NVDA'},
#                      {"label": "AMC", "value": 'AMC'}],
#                  multi=False,
#                  value='TSLA',
#                  style={'width': "40%"}
#                  ),
#     dcc.RadioItems(id='stock_radio',
#     options=[
#         {'label': 'Line (close)', 'value': 'LINE'},
#         {'label': 'CandleStick', 'value': 'CS'},
#     ],
#     value='LINE'
#     ),

#     html.Div(id='output_container', children=[]),
#     html.Br(),
#     dcc.Graph(id='stock_graph', figure={})

# ])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    #Output(component_id='output_container', component_property='children'),
    Output(component_id='stock_graph', component_property='figure'),
    Output(component_id='stock_reddit_mention', component_property='figure'),
    Input(component_id='stock_dropdown', component_property='value'),
    Input(component_id='stock_radio', component_property='value'),
    Input(component_id='stock_date_range', component_property='start_date'),
    Input(component_id='stock_date_range', component_property='end_date')
)

def update_graph(stock_dropdown_values, radio_values,start_date,end_date):

    container = "The stock chosen: {}".format(stock_dropdown_values)
    if start_date is None:
        sd=dt(2016,1,1)
    else:
        sd = dt.fromisoformat(start_date)
    if end_date is None:
        ed=dt.today()
    else:
        ed = dt.fromisoformat(end_date)

    df = web.DataReader(
        stock_dropdown_values,'yahoo',
        start=sd, end=ed
    )
    #print(df)
    if radio_values == 'LINE':
        fig = px.line(df, x=df.index, y=df['Close'], title="{} Graph".format(stock_dropdown_values))
        fig.update_layout(plot_bgcolor="#1f2630",paper_bgcolor="#1f2630",xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(26, 135, 237)',),yaxis=dict(
        showgrid=False),
        font=dict(
        size=18,
        color="white"
        ))
    else:
        fig = go.Figure(
            data=[go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])
        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.update_layout(plot_bgcolor="#1f2630",paper_bgcolor="#1f2630",xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(26, 135, 237)',),yaxis=dict(
        showgrid=False),
        font=dict(
        size=18,
        color="white"
        ))



    fig2 = px.line(tesla_df, x=tesla_df.index, y=tesla_df['Mention'], title="{} Reddit Mention Graph".format(stock_dropdown_values))
    fig2.update_layout(plot_bgcolor="#1f2630",paper_bgcolor="#1f2630",xaxis=dict(
    showline=True,
    showgrid=False,
    showticklabels=True,
    linecolor='rgb(26, 135, 237)',),yaxis=dict(
    showgrid=True),
    font=dict(
    size=18,
    color="white"
    ))
    return fig, fig2

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)