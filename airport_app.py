import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from itertools import cycle
from dash.dependencies import Input,Output
from dash_bootstrap_components._components.Navbar import Navbar
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

### import prepared data
df_melt = pd.read_csv("df_melt.csv")

# re-format date column to date format
if 'date' in df_melt:
    df_melt['date'] = pd.to_datetime(df_melt['date'])

df_table = df_melt.copy()
df_table['latitude'] = df_table['latitude'].map('{:,.2f}'.format)
df_table['longitude'] = df_table['longitude'].map('{:,.2f}'.format)
df_table['date'] = df_table['date'].astype(str).str.strip('T00:00:00')

airports = df_melt['airport'].unique().tolist()
#print(airports)
type_of_traffic = df_melt['type of traffic'].unique().tolist()
#print(type_of_traffic)

years = df_melt['date'].dt.year.unique().tolist()
#print(years)

months = df_melt['date'].dt.month.unique().tolist()
months=sorted(months)
#print(months)

months_alpha = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

color_1 = "#3498db"
color_2 = "#2c3e50"
color_3 = "#000000"

pallette = cycle(px.colors.qualitative.Dark24)

#--------------------------------------------------------------------------
# Build the app
#--------------------------------------------------------------------------

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Norway Airport Passenger Traffic'
server = app.server

#--------------------------------------------------------------------------
# Define Graphs
#--------------------------------------------------------------------------
graph_bar = dcc.Graph(id='graph-bar',figure={},style={"height": "80vh", "width": "100%"})
graph_map = dcc.Graph(id='graph-map',figure={},style={"height": "80vh", "width": "100%"})
graph_line = dcc.Graph(id='graph-line',figure={},style={"height": "75vh", "width": "100%"})

#--------------------------------------------------------------------------
# Define Search Bar
#--------------------------------------------------------------------------
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(id='search-input',type='search',placeholder='Search')),
        dbc.Col(html.A
                        (dbc.Button('Search',id='search-button',color='primary',className='ml-1'),
                        href="https://upjoke.com/airport-jokes"
                        ),
                        width='auto',
                ),
    ],
    no_gutters=True,
    className='ml-auto flex-nowrap mt-3 mt-md-0',
    align='center',
)

#--------------------------------------------------------------------------
# Define navbar
#--------------------------------------------------------------------------
LOGO = ''
navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=LOGO,height='40px'),width='60px'),
                    dbc.Col(dbc.NavbarBrand('Norway Airport Passenger Traffic',className='ml-1')),
                ],
                align='center',
                no_gutters=True,
            ),

        ),
        dbc.NavbarToggler(id='navbar-toggler'),
        dbc.Collapse(search_bar,id='navbar-collapse',navbar=True),
    ],
    color='black',
    dark=True,
)

#--------------------------------------------------------------------------
# Define dropdowns
#--------------------------------------------------------------------------
traffic_dropdown = dcc.Dropdown(
    id="traffic-dropdown",
    options=[
        {"label": t, "value": t} for t in type_of_traffic
    ],
    value="All commercial flights",
    clearable=False,
    multi=False,
    style={"width": "100%"},
)

year_dropdown = dcc.Dropdown(
    id="year-dropdown",
    options=[
        {'label': y, 'value': y} for y in years
    ],
    value=[2020],
    multi=True,
    style={"width": "100%"},
)

month_dropdown = dcc.Dropdown(
    id="month-dropdown",
    options=[
        {'label': x, 'value': y} for x, y in zip(months_alpha, months)
    ],
    value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    multi=True,
    style={"width": "100%"},
)

airport_dropdown = dcc.Dropdown(
    id="airport-dropdown",
    options=[
        {"label": a, "value": a} for a in airports
    ],
    value=["Oslo Gardermoen", "Kristiansand Kjevik"],
    clearable=False,
    multi=True,
    style={"width": "100%"},
)

scale_dropdown = dcc.Dropdown(
    id="scale-dropdown",
    options=[{"label": "Linear", "value": "Linear"},
             {"label": "Logarithmic", "value": "Logarithmic"}],
    value="Linear",
    style={"width": "100%"},
)

################################################################################

time_traffic_dropdown = dcc.Dropdown(
    id="time-traffic-dropdown",
    options=[
        {"label": t, "value": t} for t in type_of_traffic
    ],
    value="All commercial flights",
    clearable=False,
    multi=False,
    style={"width": "100%"},
)

time_airport_dropdown = dcc.Dropdown(
    id="time-airport-dropdown",
    options=[
        {"label": a, "value": a} for a in airports
    ],
    value=["Oslo Gardermoen", "Kristiansand Kjevik"],
    clearable=False,
    multi=True,
    style={"width": "100%"},
)

time_scale_dropdown = dcc.Dropdown(
    id="time-scale-dropdown",
    options=[{"label": "Linear", "value": "Linear"},
             {"label": "Logarithmic", "value": "Logarithmic"}],
    value="Linear",
    clearable=False,
    multi=False,
    style={"width": "100%"},
)

# ------------------------------------------------------------------------------
# Define buttons
# ------------------------------------------------------------------------------
year_set_btn = dbc.ButtonGroup(
    [
        dbc.Button(
            "Select all",
            id="year-btn-all",
            # outline=True,
            color="primary",
            className="mr-1",
        ),
        dbc.Button(
            "Deselect",
            id="year-btn-none",
            # outline=True,
            color="primary",
            className="mr-1",
        ),
    ],
    id="year-set-btn",
    size="md",
)

month_set_btn = dbc.ButtonGroup(
    [
        dbc.Button(
            "Select all",
            id="month-btn-all",
            # outline=True,
            color="primary",
            className="mr-1",
        ),
        dbc.Button(
            "Deselect",
            id="month-btn-none",
            # outline=True,
            color="primary",
            className="mr-1",
        ),
    ],
    id="month-set-btn",
    size="md",
)

airport_set_btn = dbc.ButtonGroup(
    [
        dbc.Button(
            "Select all",
            id="airport-btn-all",
            # outline=True,
            color="primary",
            className="mr-1",
        ),
        dbc.Button(
            "Deselect",
            id="airport-btn-none",
            # outline=True,
            color="primary",
            className="mr-1",
        ),
    ],
    id="airport-set-btn", size="md",
)

# ------------------------------------------------------------------------------
# Define overview options
# ------------------------------------------------------------------------------
time_options = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col([dbc.Label("Select type of traffic"), time_traffic_dropdown]),
                dbc.Col([dbc.Label("Search and select airports"), time_airport_dropdown]),
                dbc.Col([dbc.Label("Select scale"), time_scale_dropdown]),
            ]
        )
    ], body=True
)

# ------------------------------------------------------------------------------
# Define overview options card
# ------------------------------------------------------------------------------
overview_options_card = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([dbc.Label("Select scale")]),
                        dbc.Row([scale_dropdown]),
                        html.Br(),
                        dbc.Row([dbc.Label("Select type of traffic")]),
                        dbc.Row([traffic_dropdown]),
                        html.Br(),
                        dbc.Row([dbc.Label("Search and select years")]),
                        dbc.Row([year_set_btn]),
                        dbc.Row([year_dropdown]),
                        html.Br(),
                        dbc.Row([dbc.Label("Search and select months")]),
                        dbc.Row([month_set_btn]),
                        dbc.Row([month_dropdown]),
                        html.Br(),
                        dbc.Row([dbc.Label("Search and select airports")]),
                        dbc.Row([airport_set_btn]),
                        dbc.Row([airport_dropdown]),
                    ], style={"width": "100%"},
                )
            ], style={"width": "100%"},
        ),
    ],
    body=True,
    style={"width": "100%"},
)

# ------------------------------------------------------------------------------
# Define table
# ------------------------------------------------------------------------------
table = dash_table.DataTable(
    id='table',
    columns = [{"name": i, "id": i} for i in df_table.columns],
    data = df_table.to_dict('records'),
    filter_action='native',
    sort_action='native',
    page_size=25,
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
        # 'textAlign': 'left',
    },
    style_cell_conditional=[
        {'if': {'column_id': 'airport'},
         'width': '18%', 'textAlign': 'left'},
        {'if': {'column_id': 'type of traffic'},
         'width': '17%', 'textAlign': 'left'},
        {'if': {'column_id': 'location'},
         'width': '32%', 'textAlign': 'left'},
        {'if': {'column_id': 'latitude'},
         'width': '5%'},
        {'if': {'column_id': 'longitude'},
         'width': '5%'},
        {'if': {'column_id': 'date'},
         'width': '7%'},
        {'if': {'column_id': 'passengers'},
         'width': '6%'},
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
)
# ------------------------------------------------------------------------------
# Define tabs
# ------------------------------------------------------------------------------
tab1_content = dbc.Row(
    [
        html.Div([
            html.Br(),
            html.Span('Airport Passenger Amount by Location', style={
                      "font-size": 22, "color": color_2, 'font-weight': 'bold'}),
            html.Br(),
            html.Span('Graphical representation of the amount of passenger in Norwegian airports summarized by the type of traffic, years, months, and airport', style={
                      "font-size": 14, "color": color_2}),
        ]
        ),
        graph_map,
    ],
    no_gutters=True,
)

tab2_content = dbc.Row(
    [
        html.Div([
            html.Br(),
            html.Span('Airport Passenger Amount by Category', style={
                      "font-size": 22, "color": color_2, 'font-weight': 'bold'}),
            html.Br(),
            html.Span('Categorical representation of the amount of passenger in Norwegian airports summarized by the type of traffic, years, months, and airport', style={
                      "font-size": 14, "color": color_2}),
        ]
        ),
        graph_bar,
    ],
    no_gutters=True,
)

tab3_content = dbc.Col(
    [
        time_options,
        html.Div([
            html.Br(),
            html.Span('Airport Passenger Amount Over Time', style={
                      "font-size": 22, "color": color_2, 'font-weight': 'bold'}),
            html.Br(),
            html.Span('Representation of the amount of passenger in Norwegian airports over time summarized by the type of traffic, and airport', style={
                      "font-size": 14, "color": color_2}),
        ]
        ),
        graph_line,

    ]
)

tab4_content = dbc.Col(
    [
        html.Div([
            html.Br(),
            html.Span('Table of Data', style={
                      "font-size": 22, "color": color_2, 'font-weight': 'bold'}),
            html.Br(),
            html.Span('Explore the date making the graphs by filtering and sorting', style={
                      "font-size": 14, "color": color_2}),
        ]
        ),
        dbc.Card(table, body=True)
    ]
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, tab_id="tab_map", label="Geographical"),  # style={"width": "100%"}),
        dbc.Tab(tab2_content, tab_id="tab_total", label="Categorical"),  # style={"width": "100%"}),
        dbc.Tab(tab3_content, tab_id="tab_time", label="Time"),  # style={"width": "100%"}),
        dbc.Tab(tab4_content, tab_id="tab_table", label="Table"),  # style={"width": "100%"}),
    ],
    id="tabs",
    active_tab="tab_map",
    style={"width": "100%"}
    # style={"height": "auto", "width": "auto"},
)

# ------------------------------------------------------------------------------
# Define layout
# ------------------------------------------------------------------------------
app.layout = html.Div(
    [
        navbar,
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Collapse(
                            overview_options_card,
                            id="menu_1",
                        )
                    ], id="menu_col_1", width=6, xs=6, sm=5, md=4, lg=3, xl=2
                ),
                dbc.Col([tabs]),
            ], style={"height": "auto", "width": "99%"},
        )
    ],
    # style={"height": "auto", "width": "auto"},
)

# ------------------------------------------------------------------------------
# Define callback to toggle tabs
# ------------------------------------------------------------------------------
@app.callback(
    [
        Output("scale-dropdown",'disabled'),
        Output("menu_1", "is_open"),
        Output("menu_col_1", "width"),
        Output("menu_col_1", "xs"),
        Output("menu_col_1", "sm"),
        Output("menu_col_1", "md"),
        Output("menu_col_1", "lg"),
        Output("menu_col_1", "xl")
    ],
        Input("tabs", "active_tab"),
)
def toggle_tabs(tab_id):
    if(tab_id == 'tab_time' or tab_id == 'tab_table'):
        return False,False,'0%',0,0,0,0,0
    elif tab_id == 'tab_map':
        return True,True,'0%',6,5,4,3,2
    elif tab_id == 'tab_total':
        return False,True,'0%',6,5,4,3,2

# ------------------------------------------------------------------------------
# Define callback to set year value
# ------------------------------------------------------------------------------

@app.callback(
    Output('year-dropdown','value'),
    [
        Input('year-btn-all','n_clicks'),
        Input('year-btn-none','n_clicks')
    ]
)
def set_selected_years(year_btn_all,year_btn_none):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'year-btn-all':
        return [year for year in years]
    
    if button_id == 'year-btn-none':
        return [2020]

# ------------------------------------------------------------------------------
# Define callback to set month value
# ------------------------------------------------------------------------------

@app.callback(
    Output('month-dropdown','value'),
    [
        Input('month-btn-all','n_clicks'),
        Input('month-btn-none','n_clicks')
    ]
)
def set_selected_months(month_btn_all,month_btn_none):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'month-btn-all':
        return [month for month in months]
    
    if button_id == 'month-btn-none':
        return [1]

# ------------------------------------------------------------------------------
# Define callback to set month value
# ------------------------------------------------------------------------------

@app.callback(
    Output('airport-dropdown','value'),
    [
        Input('airport-btn-all','n_clicks'),
        Input('airport-btn-none','n_clicks')
    ]
)
def set_selected_airport(airport_btn_all,airport_btn_none):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'airport-btn-all':
        return [airport for airport in airports]
    
    if button_id == 'airport-btn-none':
        return ["Oslo Gardermoen", "Kristiansand Kjevik"]


# ------------------------------------------------------------------------------
# Define callback to update graph
# ------------------------------------------------------------------------------

@app.callback(
    Output('graph-bar','figure'),
    Output('graph-map','figure'),
    Input("traffic-dropdown", "value"),
    Input("year-dropdown", "value"),
    Input("month-dropdown", "value"),
    Input("airport-dropdown", "value"),
    Input("scale-dropdown", "value"),
)
def update_figures(selected_traffic, selected_year, selected_month, selected_airport, selected_scale):
    if not isinstance(selected_year,list):
        temp: list = [selected_year]
    
    if selected_scale == "Linear":
        scale = False
    else:
        scale = True
    
    if len(selected_airport) <=5:
        bargap = .65
    elif 6 <= len(selected_airport) <= 10:
        bargap=.25
    else:
        bargap=0

    mapbox_style = "mapbox://styles/lewiuberg/cki0nrkmf3x6w19qrwb8rmgm1"

    current_df = df_melt.copy()

    current_df = current_df[current_df["type of traffic"] == selected_traffic]

    current_df = current_df[current_df['date'].dt.year.isin(selected_year)]

    current_df = current_df[current_df['date'].dt.month.isin(selected_month)]

    current_df = current_df[current_df["airport"].isin(selected_airport)]
    agg_current_df = current_df.groupby(
        ['airport'])['passengers'].agg('sum').to_frame().reset_index()

    agg_current_df = agg_current_df.sort_values(by="passengers")

    maplat = current_df["latitude"].unique()
    maplon = current_df["longitude"].unique()
    current_df_map = current_df.groupby(["airport"]).sum().copy().reset_index()
    current_df_map["latitude"] = maplat
    current_df_map["longitude"] = maplon

    fig_bar = px.bar(agg_current_df,
                     x="passengers",
                     y="airport",
                     orientation="h",
                     log_x=scale,
                     # hover_name="airport",
                     # color="airport",
                     # color_continuous_scale=["blue"],
                     # color_discrete_map=["blue"],
                     color_discrete_sequence=[color_2],
                     )
    fig_bar.update_traces(
        hovertemplate='Passengers: %{x:n}')
    fig_bar.update_traces(hovertemplate=None,
                          selector={"name": "airport"})
    fig_bar.update_traces(texttemplate='%{x:.2s}',
                          textposition='outside')
    fig_bar.update_layout(hovermode="y",
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          uniformtext_minsize=8,
                          uniformtext_mode='hide',
                          bargap=bargap,
                          modebar={'bgcolor': 'rgba(255,255,255,0.0)'},
                          xaxis_title="Amount of Passengers",
                          yaxis_title="Airports",)
    fig_bar.update_xaxes(showgrid=False)
    fig_bar.update_yaxes(showgrid=False)


#-----------------------------------------------------------------
    fig_map = px.scatter_mapbox(current_df_map,
                                    lat="latitude",
                                    lon="longitude",
                                    size="passengers",
                                    opacity=.8,
                                    size_max=35,
                                    color="passengers",
                                    text="airport",
                                    hover_name="airport",
                                    color_continuous_scale=[color_1, color_2, color_3],
                                    zoom=3.9,
                                    center={"lat": 65, "lon": 17},
                                    )

    fig_map.update_traces(
        hovertemplate='<b>%{text}</b><br><br>Passengers: %{marker.size:n} <br>Lat: %{lat:,.2f} <br>Lon: %{lon:,.2f}')
    fig_map.update_traces(hovertemplate=None, selector={"name": "airport"})

    fig_map.update_layout(mapbox_style=mapbox_style,
                          mapbox_accesstoken='pk.eyJ1Ijoia3Jpc2hoLW5haWR1IiwiYSI6ImNram9mZThoNzBtZXAyc3ByOG54a2ZuOGMifQ._3EFTyp5GGrSQ4Qf_lSPBg',
                          modebar={'bgcolor': 'rgba(255,255,255,0.0)'},
                          coloraxis_colorbar=dict(
                              title='<span style="font-size: 13px;">Passenger<br>Amount</span>',
                          ),
                          )
    fig_map.update_xaxes(showgrid=False)
    fig_map.update_yaxes(showgrid=False)

    return fig_bar, fig_map


# ------------------------------------------------------------------------------
# Define callback to update graph
# ------------------------------------------------------------------------------
@ app.callback(Output('graph-line', 'figure'),
               [Input("time-traffic-dropdown", "value"),
                Input("time-airport-dropdown", "value"),
                Input("time-scale-dropdown", "value")])
def update_figure(selected_traffic, selected_airport, selected_scale):

    df_airport = df_melt.copy()

    df_airport = df_melt[df_melt["type of traffic"] == selected_traffic]

    df_airport = df_airport[df_airport['airport'].isin(selected_airport)]

    airport_range = df_airport["airport"].unique().tolist()

    n_airports: list = []
    for a in airport_range:
        n_airports.append(df_airport[df_airport["airport"] == a])

    agg_airports: dict = {}
    for a in range(len(airport_range)):
        n_airports[a] = n_airports[a].groupby(['date'])['passengers'].agg('sum').to_frame().reset_index()
        agg_airports[airport_range[a]] = n_airports[a].sort_values(by="date")

    if selected_scale == "Linear":
        scale = 'linear'
    else:
        scale = 'log'

    fig_line = go.Figure()

    for i, (k, v) in enumerate(agg_airports.items()):
        fig_line.add_trace(go.Scatter(
            name=k,
            mode="lines", x=v["date"], y=v["passengers"],
            # line=dict(color=colors[i]),
            line=dict(color=next(pallette)),
        )
        )

    fig_line.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="Month", step="month", stepmode="backward"),
                dict(count=6, label="6 Months", step="month", stepmode="backward"),
                dict(count=1, label="Today", step="year", stepmode="todate"),
                dict(count=1, label="Year", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
    )

    fig_line.update_layout(hovermode="x",
                           yaxis_type=scale,
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           modebar={'bgcolor': 'rgba(255,255,255,0.0)'},
                           )

    fig_line.update_xaxes(showgrid=False)
    fig_line.update_yaxes(showgrid=False)

    return fig_line








app.run_server(debug=True)
#if __name__ == '__main__':
#    app.run_server(debug=True)