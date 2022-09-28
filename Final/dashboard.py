# Run with `python dashboard.py` and visit http://127.0.0.1:8050/ in your web browser.

# import packages
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, dash_table, no_update
import dash_bootstrap_components as dbc
import similarity

# constants
ALL_PLAYER_DETAILS = similarity.get_all_player_details()
ALL_PERIODS = ['2021', '2020-2021', '2019-2021']
ALL_PERIODS_OPTIONS = [{'label': year, 'value': year} for year in ALL_PERIODS]
ALL_LEAGUES = similarity.get_all_leagues()
ALL_LEAGUES_OPTIONS = [{'label': league, 'value': league} for league in ALL_LEAGUES]
MIN_AGE = 18 #similarity.get_min_age()
MAX_AGE = 46 # similarity.get_max_age()
MIN_TOTAL_MINS = 720 # similarity.get_min_total_mins()
MAX_TOTAL_MINS = 3420 # similarity.get_max_total_mins()
MIN_RATING = 0.6 # similarity.get_min_rating()
MAX_RATING = 4.9 # similarity.get_max_rating()
TOP_N = 20
DARK_BLUE_HEX = '#4074B2'
DARK_ORANGE_HEX = '#E77052'
BACKGROUND_HEX = '#111111'
SUBBACKGROUND_HEX = '#222222'
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '30%',
    'margin-top': '65px',
    'textAlign': 'center',
    'padding': '20px 10px',
    'background-color': SUBBACKGROUND_HEX
}
PARAGRAPH_STYLE = {
    'textAlign': 'left',
    'color': 'white',
    'font-size': '20px',
}
CONTENT_STYLE = {
    'position': 'fixed',
    'top': 0,
    'right': 0,
    'bottom': 0,
    'margin-left': '30%',
    'margin-top': '65px',
    'width': '70%',
    'padding': '20px 10px',
    'background-color': BACKGROUND_HEX
}
TABLE_STYLE = {
    'background-color': BACKGROUND_HEX,
    'margin-top': '-10px',
    'textAlign': 'center',
    'font-size': '16px'
}

### COMPONENTS
dashboard = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# query players
player_1_details = dcc.Dropdown(options=ALL_PLAYER_DETAILS, placeholder='Player 1', className='dropdown', id='player_1_details_dropdown')
player_2_details = dcc.Dropdown(placeholder='Player 2 [Optional]', className='dropdown', id='player_2_details_dropdown')

# player weights
player_1_weight = dcc.Dropdown(clearable=False, className='dropdown', placeholder='Weightage', id='player_1_weight_dropdown')
player_2_weight = dcc.Dropdown(clearable=False, className='dropdown', placeholder='Weightage', id='player_2_weight_dropdown')

# traits weights
goals_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='goals_weight_slider')
shots_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='shots_weight_slider')
conversion_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='conversion_weight_slider')
positioning_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='positioning_weight_slider')
assists_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='assists_weight_slider')
crossing_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='crossing_weight_slider')
dribbling_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='dribbling_weight_slider')
carries_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='carries_weight_slider')
involvement_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='involvement_weight_slider')
accuracy_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='accuracy_weight_slider')
intent_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='intent_weight_slider')
receiving_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='receiving_weight_slider')
aerial_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='aerial_weight_slider')
on_ball_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='on_ball_weight_slider')
off_ball_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='off_ball_weight_slider')
fouls_weight = dcc.Slider(1, 9, 2, value=1, dots=True, className='slider', id='fouls_weight_slider')

# filters
seasons_filter = dcc.Dropdown(options=ALL_PERIODS_OPTIONS, className='dropdown', placeholder='Season(s)', id='seasons_filter_dropdown')
leagues_filter = dcc.Dropdown(options=ALL_LEAGUES_OPTIONS, multi=True, className='dropdown', placeholder='League(s)', id='leagues_filter_dropdown')
primary_positions_filter = dcc.Dropdown(multi=True, className='dropdown', placeholder='Primary Position(s)', id='primary_positions_filter_dropdown')
age_range_filter = dcc.RangeSlider(min=MIN_AGE, max=MAX_AGE, step=2, value=[MIN_AGE, MAX_AGE], className='range_slider', id='age_range_filter_slider')
min_total_mins_filter = dcc.Input(min=MIN_TOTAL_MINS, max=MAX_TOTAL_MINS, step=90, value=MIN_TOTAL_MINS, type='number', className='input', id='min_total_mins_filter_input')
min_rating_filter = dcc.Input(min=MIN_RATING, max=MAX_RATING, step=0.1, value=MIN_RATING, type='number', className='input', id='min_rating_filter_input')

# charts
rating_indicators = dcc.Graph(figure=similarity.blank_figure(), id='rating_indicators_graph', config={'displayModeBar': False})
composite_traits_charts = dcc.Graph(figure=similarity.blank_figure(), id='composite_traits_charts_graph', config={'displayModeBar': False})
raw_traits_charts = dcc.Graph(figure=similarity.blank_figure(), id='raw_traits_charts_graph', config={'displayModeBar': False})

# storage
button_clicks = dcc.Store(data=0, storage_type='memory', id='button_clicks_store')

### LAYOUT
# players input
players = html.Div([dbc.Row([dbc.Col([player_1_details], width=8),
                             dbc.Col([player_1_weight], width=4)],
                            style={'margin-bottom': '5px'}),
                    dbc.Row([dbc.Col([player_2_details], width=8),
                             dbc.Col([player_2_weight], width=4)],
                            style={'margin-bottom': '5px'})
                    ])

# traits weights input
traits_weights = dbc.Row([dbc.Col([dbc.Label('Goals', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                   goals_weight,
                                   dbc.Label('Shots', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                   shots_weight,
                                   dbc.Label('Conversion', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                   conversion_weight,
                                   dbc.Label('Positioning', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                   positioning_weight],
                                  width=3),
                               dbc.Col([dbc.Label('Assists', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        assists_weight,
                                        dbc.Label('Crossing', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        crossing_weight,
                                        dbc.Label('Dribbling', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        dribbling_weight,
                                        dbc.Label('Carries', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        carries_weight],
                                       width=3),
                               dbc.Col([dbc.Label('Involvement', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        involvement_weight,
                                        dbc.Label('Accuracy', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        accuracy_weight,
                                        dbc.Label('Intent', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        intent_weight,
                                        dbc.Label('Receiving', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        receiving_weight],
                                       width=3),
                               dbc.Col([dbc.Label('Aerial', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        aerial_weight,
                                        dbc.Label('On-ball', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        on_ball_weight,
                                        dbc.Label('Off-ball', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        off_ball_weight,
                                        dbc.Label('Fouls', size='sm', style={'margin-top': '-5px', 'margin-bottom': '-5px'}),
                                        fouls_weight],
                                       width=3)
                               ])

# filters input
filters = html.Div([dbc.Row([seasons_filter], style={'margin-bottom': '5px'}),
                    dbc.Row([leagues_filter], style={'margin-bottom': '5px'}),
                    dbc.Row([primary_positions_filter], style={'margin-bottom': '5px'}),
                    dbc.Row([dbc.Label('Age Range', size='m')]),
                    dbc.Row([age_range_filter], justify='center', style={'margin-bottom': '5px'}),
                    dbc.Row([dbc.Col([dbc.Label('Min. Minutes Played', size='m')], width=4),
                             dbc.Col([min_total_mins_filter], width=2),
                             dbc.Col([dbc.Label('Min. Overall Rating', size='m')], width=4),
                             dbc.Col([min_rating_filter], width=2)],
                            align='center',
                            justify='between'
                            )
                    ])

# submit button input
submit_button = dbc.Button(id='submit_button', n_clicks=0, children='Submit', color='primary', outline=True)

# all query inputs
query_inputs = dbc.Form([html.P('Query Player(s)', style=PARAGRAPH_STYLE),
                         players,
                         html.Br(),
                         html.P('Traits Importance', style=PARAGRAPH_STYLE),
                         traits_weights,
                         html.Br(),
                         html.P('Filters', style=PARAGRAPH_STYLE),
                         filters,
                         html.Br(),
                         submit_button
                         ]
                        )

# components in find tab
find_sidebar = html.Div([query_inputs],style=SIDEBAR_STYLE)
find_table = html.Div(style=CONTENT_STYLE)

# query player display
query_player_table = dash_table.DataTable(data=pd.DataFrame(['']).to_dict('records'),
                                          style_data={'backgroundColor': DARK_BLUE_HEX, 'textAlign': 'center', 'font-size': '17px', 'height': 'auto', 'whiteSpace': 'normal'},
                                          style_cell={'padding': '5px 5px'},
                                          style_table={'margin-top':'-30px'},
                                          style_as_list_view=True,
                                          style_header={'display': 'none'},
                                          cell_selectable=False,
                                          id='query_player_table_datatable')

# similar player display/input
similar_players_table = dash_table.DataTable(data=pd.DataFrame(['']*TOP_N).to_dict('records'),
                                             style_data={'backgroundColor': DARK_ORANGE_HEX, 'textAlign': 'center', 'font-size': '17px', 'height': 'auto', 'whiteSpace': 'normal'},
                                             style_cell={'padding': '5px 5px'},
                                             style_table={'margin-top': '-10px'},
                                             style_as_list_view=True,
                                             style_header={'display': 'none'},
                                             id='similar_players_table_datatable')

# compare inputs
compare_inputs = dbc.Form([html.Br(),
                           query_player_table,
                           html.Br(),
                           html.P('and', style={'textAlign': 'center', 'color': 'white', 'font-size': '20px'}),
                           similar_players_table
                           ]
                          )

# components in compare tab
compare_sidebar = html.Div([compare_inputs], style=SIDEBAR_STYLE)
compare_charts = html.Div([dbc.Tabs([dbc.Tab([rating_indicators], label='OVERALL RATING'),
                                     dbc.Tab([composite_traits_charts], label='COMPOSITE MEASURES'),
                                     dbc.Tab([raw_traits_charts], label='DERIVED METRICS')
                                     ],
                                    style={'line-height': '30px', 'margin-top': '-15px', 'margin-left': '-5px', 'margin-right': '-5px'}
                                    )
                           ],
                          style=CONTENT_STYLE
                          )

# general tab format
tabs = dbc.Tabs([dbc.Tab([find_sidebar, find_table], label='1. FIND SIMILAR PLAYERS'),
                 dbc.Tab([compare_sidebar, compare_charts], label='2. COMPARE PLAYERS')
                 ],
                style={'line-height': '40px', 'margin-top': '5px'}
                )

# final layout
dashboard.layout = html.Div([tabs, button_clicks], style={'background-color': BACKGROUND_HEX})


### CALLBACKS
# updates filters when player 1 is input
@dashboard.callback(Output(player_2_details, component_property='options'),
                    Output(primary_positions_filter, component_property='options'),
                    Input(player_1_details, component_property='value')
                    )
def update_filters(player_1_details):
    if player_1_details is None:
        position_player_details = []
        primary_positions = []
    else:
        position_player_details = similarity.get_position_player_details(player_1_details)
        position_player_details.remove(player_1_details)
        primary_positions = [{'label': position, 'value': position} for position in similarity.get_primary_positions(player_1_details)]

    return position_player_details, primary_positions

# prevents player 2 to come back when player 1 is input again
@dashboard.callback(Output(player_2_details, component_property='value'),
                    Input(player_1_details, component_property='value')
                    )
def update_player_2(player_1_details):
    if player_1_details is None:
        return None
    else:
        return no_update

# updates dropdown list of weights when both players 1 and 2 are input
@dashboard.callback(Output(player_1_weight, component_property='options'),
                    Output(player_1_weight, component_property='placeholder'),
                    Output(player_2_weight, component_property='options'),
                    Output(player_2_weight, component_property='placeholder'),
                    Input(player_1_details, component_property='value'),
                    Input(player_2_details, component_property='value'))
def update_players_weight_dropdowns(player_1_details, player_2_details):
    if player_1_details is None:
        options = []
        placeholder_1 = 'Weightage'
        placeholder_2 = 'Weightage'
    elif player_2_details is None:
        options = []
        placeholder_1 = '100%'
        placeholder_2 = ''
    else:
        options = [f'{i}%' for i in range(10, 91, 10)]
        placeholder_1 = '50%'
        placeholder_2 = '50%'

    return options, placeholder_1, options, placeholder_2

# updates player 2's weight when player 1 weight is input
@dashboard.callback(Output(player_2_weight, component_property='value'),
                    Input(player_1_weight, component_property='value'))
def update_player_2_weight(player_1_weight):

    if player_1_weight is None:
        return None

    # convert to fraction
    fraction_1 = int(player_1_weight[:-1]) / 100
    fraction_2 = 1 - fraction_1

    return f'{fraction_2*100:.0f}%'

# updates player 1's weight when player 2 weight is input
@dashboard.callback(Output(player_1_weight, component_property='value'),
                    Input(player_2_weight, component_property='value'))
def update_player_1_weight(player_2_weight):

    if player_2_weight is None:
        return None

    # convert to fraction
    fraction_2 = int(player_2_weight[:-1]) / 100
    fraction_1 = 1 - fraction_2

    return f'{fraction_1*100:.0f}%'

# builds tables when submit button is pressed
@dashboard.callback(Output(find_table, component_property='children'),
                    Output(query_player_table, component_property='data'),
                    Output(similar_players_table, component_property='data'),
                    Output(similar_players_table, component_property='active_cell'),
                    Output(button_clicks, component_property='data'),
                    State(player_1_details, component_property='value'),
                    State(player_2_details, component_property='value'),
                    State(player_1_weight, component_property='value'),
                    State(player_2_weight, component_property='value'),
                    State(goals_weight, component_property='value'),
                    State(shots_weight, component_property='value'),
                    State(conversion_weight, component_property='value'),
                    State(positioning_weight, component_property='value'),
                    State(assists_weight, component_property='value'),
                    State(crossing_weight, component_property='value'),
                    State(dribbling_weight, component_property='value'),
                    State(carries_weight, component_property='value'),
                    State(involvement_weight, component_property='value'),
                    State(accuracy_weight, component_property='value'),
                    State(intent_weight, component_property='value'),
                    State(receiving_weight, component_property='value'),
                    State(aerial_weight, component_property='value'),
                    State(on_ball_weight, component_property='value'),
                    State(off_ball_weight, component_property='value'),
                    State(fouls_weight, component_property='value'),
                    State(seasons_filter, component_property='value'),
                    State(leagues_filter, component_property='value'),
                    State(primary_positions_filter, component_property='value'),
                    State(age_range_filter, component_property='value'),
                    State(min_total_mins_filter, component_property='value'),
                    State(min_rating_filter, component_property='value'),
                    State(button_clicks, component_property='data'),
                    Input(submit_button, component_property='n_clicks'),
                    )
def build_tables(player_1_details, player_2_details, player_1_weight, player_2_weight, #top_n,
                 goals_weight, shots_weight, conversion_weight, positioning_weight, assists_weight, crossing_weight, dribbling_weight,
                 carries_weight, involvement_weight, accuracy_weight, intent_weight, receiving_weight, aerial_weight,
                 on_ball_weight, off_ball_weight, fouls_weight, seasons_filter, leagues_filter, primary_positions_filter,
                 age_range_filter, min_total_mins_filter, min_rating_filter, button_clicks, submit_button):

    if submit_button <= button_clicks:
        return no_update, no_update, no_update, no_update, no_update
    else:
        position = similarity.get_position(player_1_details)
        traits_weights = [goals_weight, shots_weight, conversion_weight, positioning_weight, assists_weight,
                          crossing_weight, dribbling_weight, carries_weight, involvement_weight, accuracy_weight,
                          intent_weight, receiving_weight, aerial_weight, on_ball_weight, off_ball_weight, fouls_weight]
        if seasons_filter == '':
            seasons_filter = None
        if leagues_filter == []:
            leagues_filter = None
        if primary_positions_filter == []:
            primary_positions_filter = None

        filters = {'seasons': seasons_filter,
                   'leagues': leagues_filter,
                   'primary_positions': primary_positions_filter,
                   'min_age': age_range_filter[0],
                   'max_age': age_range_filter[1],
                   'min_total_mins': min_total_mins_filter,
                   'min_rating': min_rating_filter}

        # when one player is queried
        if player_2_details is None:
            query_player = player_1_details

            table_similar_players, similar_players_list = similarity.table_similar_players_1(player_details=player_1_details,
                                                                                        position=position,
                                                                                        top_n=TOP_N,
                                                                                        traits_weights=traits_weights,
                                                                                        filters=filters)

        # when two players are queried
        else:
            if player_1_weight is None or player_2_weight is None:
                player_weights = None
                query_player = f'{player_1_details} (50%) + {player_2_details} (50%)'
            else:
                player_weights = [int(player_1_weight[:-1])/100, int(player_2_weight[:-1])/100]
                query_player = f'{player_1_details} ({player_1_weight}) + {player_2_details} ({player_2_weight})'

            table_similar_players, similar_players_list = similarity.table_similar_players_2(player_1_details=player_1_details,
                                                                                        player_2_details=player_2_details,
                                                                                        position=position,
                                                                                        top_n=TOP_N,
                                                                                        player_weights=player_weights,
                                                                                        traits_weights=traits_weights,
                                                                                        filters=filters)

        table_similar_players = dbc.Table.from_dataframe(df=table_similar_players, bordered=True, color='primary', hover=True,
                                                         striped=True, style=TABLE_STYLE)
        query_player_df = pd.DataFrame([query_player]).to_dict('records')
        similar_players_df = pd.DataFrame(similar_players_list).to_dict('records')

        return table_similar_players, query_player_df, similar_players_df, None, submit_button

# updates charts when similar player is pressed
@dashboard.callback(Output(rating_indicators, component_property='figure'),
                    Output(composite_traits_charts, component_property='figure'),
                    Output(raw_traits_charts, component_property='figure'),
                    State(player_1_details, component_property='value'),
                    State(player_2_details, component_property='value'),
                    State(player_1_weight, component_property='value'),
                    State(player_2_weight, component_property='value'),
                    State(similar_players_table, component_property='data'),
                    Input(similar_players_table, component_property='active_cell'))
def update_charts(player_1_details, player_2_details, player_1_weight, player_2_weight, similar_players_data, active_cell):

    if active_cell is None:
        return no_update, no_update, no_update
    else:
        compare_player = similar_players_data[active_cell['row']]['0']

        position = similarity.get_position(player_1_details)

        # when one player is queried
        if player_2_details is None:
            rating_indicators = similarity.rating_indicators_1(query_player_details=player_1_details,
                                                             similar_player_details=compare_player,
                                                             position=position)

            composite_traits_charts = similarity.composite_traits_charts_1(query_player_details=player_1_details,
                                                                 similar_player_details=compare_player,
                                                                 position=position)

            raw_traits_charts = similarity.raw_traits_charts_1(query_player_details=player_1_details,
                                                               similar_player_details=compare_player,
                                                               position=position)
        # when two players are queried
        else:
            if player_1_weight is None or player_2_weight is None:
                player_weights = None
            else:
                player_weights = [int(player_1_weight[:-1]) / 100, int(player_2_weight[:-1]) / 100]

            rating_indicators = similarity.rating_indicators_2(query_player_1_details=player_1_details,
                                                             query_player_2_details=player_2_details,
                                                             similar_player_details=compare_player,
                                                             position=position,
                                                             player_weights=player_weights)

            composite_traits_charts = similarity.composite_traits_charts_2(query_player_1_details=player_1_details,
                                                                 query_player_2_details=player_2_details,
                                                                 similar_player_details=compare_player,
                                                                 position=position,
                                                                 player_weights=player_weights)

            raw_traits_charts = similarity.raw_traits_charts_2(query_player_1_details=player_1_details,
                                                               query_player_2_details=player_2_details,
                                                               similar_player_details=compare_player,
                                                               position=position,
                                                               player_weights=player_weights)

        return rating_indicators, composite_traits_charts, raw_traits_charts

if __name__ == '__main__':
    dashboard.run_server(debug=True)
