# Run with `python dashboard.py` and visit http://127.0.0.1:8050/ in your web browser.

# import packages
from dash import Dash, dcc, Input, Output
import dash_bootstrap_components as dbc
import similarity

# constants
ALL_PLAYER_DETAILS = similarity.get_all_player_details()
ALL_YEARS = similarity.get_all_seasons()
ALL_LEAGUES = similarity.get_all_leagues()

### build components
dashboard = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# query players
player_1_details = dcc.Dropdown(options=ALL_PLAYER_DETAILS, value=ALL_PLAYER_DETAILS[0], style={'color': 'black'},
                              id='player_1_details_dropdown')
player_2_details = dcc.Dropdown(style={'color': 'black'}, id='player_2_details_dropdown')
# top n
top_n = dcc.Dropdown(options=list(range(1, 21)), value=10, style={'color': 'black'}, id='top_n_dropdown')
# player weights
player_1_weight = dcc.Dropdown(value='50%', style={'color': 'black'}, id='player_1_weight_dropdown')
player_2_weight = dcc.Dropdown(value='50%', style={'color': 'black'}, id='player_2_weight_dropdown')
# traits weights
goals_weight = dcc.Slider(1, 5, 1, value=1, id='goals_weight_slider')
shots_weight = dcc.Slider(1, 5, 1, value=1, id='shots_weight_slider')
conversion_weight = dcc.Slider(1, 5, 1, value=1, id='converesion_weight_slider')
positioning_weight = dcc.Slider(1, 5, 1, value=1, id='positioning_weight_slider')
assists_weight = dcc.Slider(1, 5, 1, value=1, id='assists_weight_slider')
crossing_weight = dcc.Slider(1, 5, 1, value=1, id='crossing_weight_slider')
dribbling_weight = dcc.Slider(1, 5, 1, value=1, id='dribbling_weight_slider')
carries_weight = dcc.Slider(1, 5, 1, value=1, id='carries_weight_slider')
involvement_weight = dcc.Slider(1, 5, 1, value=1, id='involvement_weight_slider')
accuracy_weight = dcc.Slider(1, 5, 1, value=1, id='accuracy_weight_slider')
intent_weight = dcc.Slider(1, 5, 1, value=1, id='intent_weight_slider')
receiving_weight = dcc.Slider(1, 5, 1, value=1, id='receiving_weight_slider')
aerial_weight = dcc.Slider(1, 5, 1, value=1, id='aerial_weight_slider')
on_ball_weight = dcc.Slider(1, 5, 1, value=1, id='on_ball_weight_slider')
off_ball_weight = dcc.Slider(1, 5, 1, value=1, id='off_ball_weight_slider')
fouls_weight = dcc.Slider(1, 5, 1, value=1, id='fouls_weight_slider')
# filters
seasons_filter = dcc.Checklist(options=ALL_YEARS, value=ALL_YEARS, inline=True, id='seasons_filter_checklist')
leagues_filter = dcc.Checklist(options=ALL_LEAGUES, value=ALL_LEAGUES, inline=True, id='leagues_filter_checklist')
primary_positions_filter = dcc.Checklist(inline=True, id='primary_positions_filter_checklist')
age_range_filter = dcc.RangeSlider(step=1, id='age_range_filter_slider')
apps_range_filter = dcc.RangeSlider(step=1, id='apps_range_filter_slider')
# compare player dropdown
compare_player = dcc.Dropdown(style={'color': 'black'}, id='compare_player_dropdown')
# similar players table
table_similar_players = dcc.Graph(figure={}, id='table_similar_players_graph')
# rating indicator
rating_indicator = dcc.Graph(figure={}, id='rating_indicator_graph')
# traits radar chart
traits_radar_chart = dcc.Graph(figure={}, id='traits_radar_chart_graph')
# difference bar chart
difference_bar_chart = dcc.Graph(figure={}, id='difference_bar_chart_graph')

# customise layout
dashboard.layout = dbc.Container([dbc.Row([dbc.Col([dbc.Row(['Query player 1:'], justify='left'),
                                                    dbc.Row([player_1_details], justify='center')
                                                    ],
                                                   width=2),
                                          dbc.Col([dbc.Row(['Query player 2:'], justify='left'),
                                                   dbc.Row([player_2_details], justify='center')
                                                   ],
                                                  width=2)
                                           ]
                                          ),
                                  dbc.Row([dbc.Col([dbc.Row(['Player 1 weight:'], justify='left'),
                                                    dbc.Row([player_1_weight], justify='center')
                                                    ],
                                                   width=2),
                                          dbc.Col([dbc.Row(['Player 2 weight:'], justify='left'),
                                                   dbc.Row([player_2_weight], justify='center')
                                                   ],
                                                  width=2)
                                           ]
                                          ),
                                  dbc.Row([dbc.Col([dbc.Row(['Number of similar players:'], justify='left'),
                                                    dbc.Row([top_n], justify='center')
                                                    ],
                                                   width=2)
                                           ]
                                          ),
                                  dbc.Row([dbc.Col([dbc.Row(['Goals:'], justify='left'),
                                                    dbc.Row([goals_weight], justify='center'),
                                                    dbc.Row(['Shots:'], justify='left'),
                                                    dbc.Row([shots_weight], justify='center'),
                                                    dbc.Row(['Conversion:'], justify='left'),
                                                    dbc.Row([conversion_weight], justify='center'),
                                                    dbc.Row(['Positioning:'], justify='left'),
                                                    dbc.Row([positioning_weight], justify='center')
                                                    ],
                                                   width=1),
                                           dbc.Col([dbc.Row(['Assists:'], justify='left'),
                                                    dbc.Row([assists_weight], justify='center'),
                                                    dbc.Row(['Crossing:'], justify='left'),
                                                    dbc.Row([crossing_weight], justify='center'),
                                                    dbc.Row(['Dribbling:'], justify='left'),
                                                    dbc.Row([dribbling_weight], justify='center'),
                                                    dbc.Row(['Carries:'], justify='left'),
                                                    dbc.Row([carries_weight], justify='center')
                                                    ],
                                                   width=1),
                                           dbc.Col([dbc.Row(['Involvement:'], justify='left'),
                                                    dbc.Row([involvement_weight], justify='center'),
                                                    dbc.Row(['Accuracy:'], justify='left'),
                                                    dbc.Row([accuracy_weight], justify='center'),
                                                    dbc.Row(['Intent:'], justify='left'),
                                                    dbc.Row([intent_weight], justify='center'),
                                                    dbc.Row(['Receiving:'], justify='left'),
                                                    dbc.Row([receiving_weight], justify='center')
                                                    ],
                                                   width=1),
                                           dbc.Col([dbc.Row(['Aerial:'], justify='left'),
                                                    dbc.Row([aerial_weight], justify='center'),
                                                    dbc.Row(['On-ball:'], justify='left'),
                                                    dbc.Row([on_ball_weight], justify='center'),
                                                    dbc.Row(['Off-ball:'], justify='left'),
                                                    dbc.Row([off_ball_weight], justify='center'),
                                                    dbc.Row(['Fouls:'], justify='left'),
                                                    dbc.Row([fouls_weight], justify='center')
                                                    ],
                                                   width=1),
                                           ]
                                          ),
                                  dbc.Row([dbc.Col([dbc.Row(['Seasons filter:'], justify='left'),
                                                    dbc.Row([seasons_filter], justify='center'),
                                                    dbc.Row(['Leagues filter:'], justify='left'),
                                                    dbc.Row([leagues_filter], justify='center'),
                                                    dbc.Row(['Primary positions filter:'], justify='left'),
                                                    dbc.Row([primary_positions_filter], justify='center'),
                                                    dbc.Row(['Age filter:'], justify='left'),
                                                    dbc.Row([age_range_filter], justify='center'),
                                                    dbc.Row(['Number of appearances filter:'], justify='left'),
                                                    dbc.Row([apps_range_filter], justify='center')
                                                    ],
                                                   width=4)
                                           ]
                                          ),
                                  dbc.Row([dbc.Col([table_similar_players], width=6)]),
                                  dbc.Row([dbc.Col([dbc.Row(['Compare player:'], justify='left'),
                                                    dbc.Row([compare_player], justify='center')
                                                    ],
                                                   width=4)
                                           ]
                                          ),
                                  dbc.Row([dbc.Col([rating_indicator], width={'size': 9, 'offset':3})]),
                                  dbc.Row([dbc.Col([traits_radar_chart], width={'size': 9, 'offset':3})]),
                                  dbc.Row([dbc.Col([difference_bar_chart], width={'size': 9, 'offset':3})])
                                  ],
                                 fluid=True)

# interacting components
@dashboard.callback(Output(player_2_details, component_property='options'),
                    Output(primary_positions_filter, component_property='options'),
                    Output(primary_positions_filter, component_property='value'),
                    Output(age_range_filter, component_property='min'),
                    Output(age_range_filter, component_property='max'),
                    Output(age_range_filter, component_property='value'),
                    Output(apps_range_filter, component_property='min'),
                    Output(apps_range_filter, component_property='max'),
                    Output(apps_range_filter, component_property='value'),
                    Input(player_1_details, component_property='value')
                    )
def update_filters(player_1_details):
    position_player_details = similarity.get_position_player_details(player_1_details)
    position_player_details.remove(player_1_details)
    primary_positions = similarity.get_primary_positions(player_1_details)
    min_age = similarity.get_min_age(player_1_details)
    max_age = similarity.get_max_age(player_1_details)
    age_range = [min_age, max_age]
    min_apps = similarity.get_min_apps(player_1_details)
    max_apps = similarity.get_max_apps(player_1_details)
    apps_range = [min_apps, max_apps]

    return position_player_details, primary_positions, primary_positions, min_age, max_age, age_range, min_apps, \
           max_apps, apps_range

@dashboard.callback(Output(player_1_weight, component_property='options'),
                    Output(player_2_weight, component_property='options'),
                    Input(player_2_details, component_property='value'))
def update_players_weight_dropdowns(player_2_details):
    if player_2_details is None:
        options = []
    else:
        options = [f'{i}%' for i in range(10, 91, 10)]

    return options, options

@dashboard.callback(Output(player_2_weight, component_property='value'),
                    Input(player_1_weight, component_property='value'))
def update_player_2_weight(player_1_weight):
    # convert to fraction
    fraction_1 = int(player_1_weight[:-1]) / 100
    fraction_2 = 1 - fraction_1

    return f'{fraction_2*100:.0f}%'

@dashboard.callback(Output(player_1_weight, component_property='value'),
                    Input(player_2_weight, component_property='value'))
def update_player_2_weight(player_2_weight):
    # convert to fraction
    fraction_2 = int(player_2_weight[:-1]) / 100
    fraction_1 = 1 - fraction_2

    return f'{fraction_1*100:.0f}%'

@dashboard.callback(Output(table_similar_players, component_property='figure'),
                    Output(compare_player, component_property='options'),
                    Output(compare_player, component_property='value'),
                    Input(player_1_details, component_property='value'),
                    Input(player_2_details, component_property='value'),
                    Input(player_1_weight, component_property='value'),
                    Input(player_2_weight, component_property='value'),
                    Input(top_n, component_property='value'),
                    Input(goals_weight, component_property='value'),
                    Input(shots_weight, component_property='value'),
                    Input(conversion_weight, component_property='value'),
                    Input(positioning_weight, component_property='value'),
                    Input(assists_weight, component_property='value'),
                    Input(crossing_weight, component_property='value'),
                    Input(dribbling_weight, component_property='value'),
                    Input(carries_weight, component_property='value'),
                    Input(involvement_weight, component_property='value'),
                    Input(accuracy_weight, component_property='value'),
                    Input(intent_weight, component_property='value'),
                    Input(receiving_weight, component_property='value'),
                    Input(aerial_weight, component_property='value'),
                    Input(on_ball_weight, component_property='value'),
                    Input(off_ball_weight, component_property='value'),
                    Input(fouls_weight, component_property='value'),
                    Input(seasons_filter, component_property='value'),
                    Input(leagues_filter, component_property='value'),
                    Input(primary_positions_filter, component_property='value'),
                    Input(age_range_filter, component_property='value'),
                    Input(apps_range_filter, component_property='value'),
                    )
def update_table(player_1_details, player_2_details, player_1_weight, player_2_weight, top_n, goals_weight,
                 shots_weight, conversion_weight, positioning_weight, assists_weight, crossing_weight, dribbling_weight,
                 carries_weight, involvement_weight, accuracy_weight, intent_weight, receiving_weight, aerial_weight,
                 on_ball_weight, off_ball_weight, fouls_weight, seasons_filter, leagues_filter,
                 primary_positions_filter, age_range_filter, apps_range_filter):

    df = similarity.get_position_df(player_1_details)
    traits_weights = [goals_weight, shots_weight, conversion_weight, positioning_weight, assists_weight,
                      crossing_weight, dribbling_weight, carries_weight, involvement_weight, accuracy_weight,
                      intent_weight, receiving_weight, aerial_weight, on_ball_weight, off_ball_weight, fouls_weight]
    filters = {'seasons': seasons_filter,
               'leagues': leagues_filter,
               'primary_positions': primary_positions_filter,
               'min_age': age_range_filter[0],
               'max_age': age_range_filter[1],
               'min_apps': apps_range_filter[0],
               'max_apps': apps_range_filter[1]}

    # when one player is queried
    if player_2_details is None:
        table_similar_players, similar_players = similarity.table_similar_players_1(player_details=player_1_details,
                                                                                    df=df,
                                                                                    top_n=top_n,
                                                                                    traits_weights=traits_weights,
                                                                                    filters=filters)
    # when two players are queried
    else:
        player_weights = [player_1_weight, player_2_weight]

        table_similar_players, similar_players = similarity.table_similar_players_2(player_1_details=player_1_details,
                                                                                    player_2_details=player_2_details,
                                                                                    df=df,
                                                                                    top_n=top_n,
                                                                                    player_weights=player_weights,
                                                                                    traits_weights=traits_weights,
                                                                                    filters=filters)

    return table_similar_players, similar_players, similar_players[0]

@dashboard.callback(Output(rating_indicator, component_property='figure'),
                    Output(traits_radar_chart, component_property='figure'),
                    Output(difference_bar_chart, component_property='figure'),
                    Input(player_1_details, component_property='value'),
                    Input(player_2_details, component_property='value'),
                    Input(player_1_weight, component_property='value'),
                    Input(player_2_weight, component_property='value'),
                    Input(compare_player, component_property='value'))
def update_charts(player_1_details, player_2_details, player_1_weight, player_2_weight, compare_player):

    df = similarity.get_position_df(player_1_details)

    # when one player is queried
    if player_2_details is None:
        rating_indicator = similarity.rating_indicator_1(query_player_details=player_1_details,
                                                         similar_player_details=compare_player,
                                                         df=df)

        traits_radar_chart = similarity.traits_radar_chart_1(query_player_details=player_1_details,
                                                             similar_player_details=compare_player,
                                                             df=df)

        difference_bar_chart = similarity.difference_bar_chart_1(query_player_details=player_1_details,
                                                                 similar_player_details=compare_player,
                                                                 df=df)
    # when two players are queried
    else:
        player_weights = [player_1_weight, player_2_weight]

        rating_indicator = similarity.rating_indicator_2(query_player_1_details=player_1_details,
                                                         query_player_2_details=player_2_details,
                                                         similar_player_details=compare_player,
                                                         df=df,
                                                         player_weights=player_weights)

        traits_radar_chart = similarity.traits_radar_chart_2(query_player_1_details=player_1_details,
                                                             query_player_2_details=player_2_details,
                                                             similar_player_details=compare_player,
                                                             df=df,
                                                             player_weights=player_weights)

        difference_bar_chart = similarity.difference_bar_chart_2(query_player_1_details=player_1_details,
                                                                 query_player_2_details=player_2_details,
                                                                 similar_player_details=compare_player,
                                                                 df=df,
                                                                 player_weights=player_weights)

    return rating_indicator, traits_radar_chart, difference_bar_chart

if __name__ == '__main__':
    dashboard.run_server(debug=True)
