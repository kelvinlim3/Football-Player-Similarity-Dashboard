# Run with `python dashboard.py` and visit http://127.0.0.1:8050/ in your web browser.

# import packages
from dash import Dash, dcc, dash_table, html, Input, Output, no_update
import dash_bootstrap_components as dbc
import similarity

# constants
ALL_PLAYER_DETAILS = similarity.get_all_player_details()
ALL_YEARS = similarity.get_all_seasons()
ALL_YEARS_OPTIONS = [{'label': year, 'value': year} for year in ALL_YEARS]
ALL_LEAGUES = similarity.get_all_leagues()
ALL_LEAGUES_OPTIONS = [{'label': league, 'value': league} for league in ALL_LEAGUES]
DARK_BLUE_HEX = '#4074B2'
LIGHT_BLUE_HEX = '#ADCDF0'
BACKGROUND_HEX = '#111111'

### build components
dashboard = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# query players
player_1_details = dcc.Dropdown(options=ALL_PLAYER_DETAILS, value=ALL_PLAYER_DETAILS[0], placeholder='Select player 1',
                                clearable=False, style={'font-size': 12, 'color': 'black'},
                                id='player_1_details_dropdown')
player_2_details = dcc.Dropdown(placeholder='Select player 2 (Optional)', style={'font-size': 12, 'color': 'black'},
                                id='player_2_details_dropdown')
# player weights
player_1_weight = dcc.Dropdown(clearable=False, style={'font-size': 12, 'color': 'black'},
                               id='player_1_weight_dropdown')
player_2_weight = dcc.Dropdown(clearable=False, style={'font-size': 12, 'color': 'black'},
                               id='player_2_weight_dropdown')
# top n
top_n = dcc.Input(min=1, max=30, step=1, value=10, type='number', placeholder='Select number of similar player to output',
                  style={'font-size': 12, 'color': 'black'}, id='top_n_input')
# traits weights
goals_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='goals_weight_slider')
shots_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='shots_weight_slider')
conversion_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='conversion_weight_slider')
positioning_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='positioning_weight_slider')
assists_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='assists_weight_slider')
crossing_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='crossing_weight_slider')
dribbling_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='dribbling_weight_slider')
carries_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='carries_weight_slider')
involvement_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='involvement_weight_slider')
accuracy_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='accuracy_weight_slider')
intent_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='intent_weight_slider')
receiving_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='receiving_weight_slider')
aerial_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='aerial_weight_slider')
on_ball_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='on_ball_weight_slider')
off_ball_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='off_ball_weight_slider')
fouls_weight = dcc.Slider(1, 5, 1, value=1, dots=True, id='fouls_weight_slider')
# filters
seasons_filter = dbc.Checklist(options=ALL_YEARS_OPTIONS, value=ALL_YEARS, switch=True,
                               label_style={'font-size': 12}, id='seasons_filter_checklist')
leagues_filter = dbc.Checklist(options=ALL_LEAGUES_OPTIONS, value=ALL_LEAGUES, switch=True,
                               label_style={'font-size': 12}, id='leagues_filter_checklist')
primary_positions_filter = dbc.Checklist(switch=True, label_style={'font-size': 12},
                                         id='primary_positions_filter_checklist')
age_range_filter = dcc.RangeSlider(step=1, id='age_range_filter_slider')
apps_range_filter = dcc.RangeSlider(step=1, id='apps_range_filter_slider')
# similar players table
table_similar_players = dash_table.DataTable(style_header={'textAlign': 'center', 'backgroundColor': '#375a7f', 'color': 'white', 'font-size': 18, 'fontWeight': 'bold', 'border': '2px white'},
                                             style_data={'backgroundColor': '#5181b4', 'color': 'white', 'font-size': 16, 'height': 'auto'},
                                             style_cell={'textAlign': 'left', 'padding': '10px'},
                                             style_cell_conditional=[{'if': {'column_id': 'Similarity'}, 'textAlign': 'center', 'color': '#375a7f', 'fontWeight': 'bold'}] + [{'if': {'column_id': col}, 'textAlign': 'center'} for col in ['Rank', 'Season', 'Age', 'Apps', 'Nationality']],
                                             style_as_list_view=True,
                                             style_table={'height': 500, 'overflowY': 'auto', 'overflowX': 'auto', 'minWidth': '100%'},
                                             fixed_columns={'headers': True},
                                             id='table_similar_players_graph')
# rating indicator
rating_indicator = dcc.Graph(id='rating_indicator_graph')
# traits radar chart
traits_radar_chart = dcc.Graph(id='traits_radar_chart_graph')
# difference bar chart
difference_bar_chart = dcc.Graph(id='difference_bar_chart_graph')

# list similar players
list_similar_players = dcc.Store(storage_type='memory', id='list_similar_players_store')



# # customise layout
# dashboard.layout = dbc.Container([dbc.Col([dbc.Row([dbc.Label('FOOTBALL PLAYER SIMILARITY', size='sm')], justify='center')], width=12),
#                                   dbc.Row([dbc.Col([dbc.Row([dbc.Col([dbc.Row([dbc.Label('Query player 1:', size='sm')], justify='left'),
#                                                                       dbc.Row([player_1_details], justify='center')
#                                                                       ],
#                                                                      width=6),
#                                                              dbc.Col([dbc.Row([dbc.Label('Query player 2 (Optional):', size='sm')], justify='left'),
#                                                                       dbc.Row([player_2_details], justify='center')
#                                                                       ],
#                                                                      width=6)
#                                                              ]
#                                                             ),
#                                                     dbc.Row([dbc.Col([dbc.Row([dbc.Label('Player 1 weight:', size='sm')], justify='left'),
#                                                                       dbc.Row([player_1_weight], justify='center')
#                                                                       ],
#                                                                      width=6),
#                                                              dbc.Col([dbc.Row([dbc.Label('Player 2 weight:', size='sm')], justify='left'),
#                                                                       dbc.Row([player_2_weight], justify='center')
#                                                                       ],
#                                                                      width=6)
#                                                              ]
#                                                             ),
#                                                     dbc.Row([dbc.Col([dbc.Row([dbc.Label('Number of similar players:', size='sm')], justify='left'),
#                                                                       dbc.Row([top_n], justify='center')
#                                                                       ],
#                                                                      width={'size': 6, 'offset': 3})
#                                                              ]
#                                                             ),
#                                                     dbc.Row([dbc.Col([dbc.Row([dbc.Label('Goals', size='sm')], justify='left'),
#                                                                       dbc.Row([goals_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Shots', size='sm')], justify='left'),
#                                                                       dbc.Row([shots_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Conversion', size='sm')], justify='left'),
#                                                                       dbc.Row([conversion_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Positioning', size='sm')], justify='left'),
#                                                                       dbc.Row([positioning_weight], justify='center')
#                                                                       ],
#                                                                      width=3),
#                                                              dbc.Col([dbc.Row([dbc.Label('Assists', size='sm')], justify='left'),
#                                                                       dbc.Row([assists_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Crossing', size='sm')], justify='left'),
#                                                                       dbc.Row([crossing_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Dribbling', size='sm')], justify='left'),
#                                                                       dbc.Row([dribbling_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Carries', size='sm')], justify='left'),
#                                                                       dbc.Row([carries_weight], justify='center')
#                                                                       ],
#                                                                      width=3),
#                                                              dbc.Col([dbc.Row([dbc.Label('Involvement', size='sm')], justify='left'),
#                                                                       dbc.Row([involvement_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Accuracy', size='sm')], justify='left'),
#                                                                       dbc.Row([accuracy_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Intent', size='sm')], justify='left'),
#                                                                       dbc.Row([intent_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Receiving', size='sm')], justify='left'),
#                                                                       dbc.Row([receiving_weight], justify='center')
#                                                                       ],
#                                                                      width=3),
#                                                              dbc.Col([dbc.Row([dbc.Label('Aerial', size='sm')], justify='left'),
#                                                                       dbc.Row([aerial_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('On-ball', size='sm')], justify='left'),
#                                                                       dbc.Row([on_ball_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Off-ball', size='sm')], justify='left'),
#                                                                       dbc.Row([off_ball_weight], justify='center'),
#                                                                       dbc.Row([dbc.Label('Fouls', size='sm')], justify='left'),
#                                                                       dbc.Row([fouls_weight], justify='center')
#                                                                       ],
#                                                                      width=3),
#                                                              ]
#                                                             ),
#                                                     dbc.Row([dbc.Col([dbc.Row([dbc.Label('Seasons', size='sm')], justify='left'),
#                                                                       dbc.Row([seasons_filter], justify='center')
#                                                                       ],
#                                                                      width=4),
#                                                              dbc.Col([dbc.Row([dbc.Label('Leagues', size='sm')], justify='left'),
#                                                                       dbc.Row([leagues_filter], justify='center')
#                                                                       ],
#                                                                      width=4),
#                                                              dbc.Col([dbc.Row([dbc.Label('Primary positions', size='sm')], justify='left'),
#                                                                       dbc.Row([primary_positions_filter], justify='center')
#                                                                       ],
#                                                                      width=4)
#                                                              ]
#                                                             ),
#                                                     dbc.Row([dbc.Col([dbc.Row([dbc.Label('Age range', size='sm')], justify='left'),
#                                                                       dbc.Row([age_range_filter], justify='center'),
#                                                                       dbc.Row([dbc.Label('Appearances range', size='sm')], justify='left'),
#                                                                       dbc.Row([apps_range_filter], justify='center')
#                                                                       ],
#                                                                      width=12)
#                                                              ]
#                                                             )
#                                                     ],
#                                                    width=4
#                                                    ),
#                                            dbc.Col([dbc.Row([dbc.Col([table_similar_players], width=8),
#                                                              dbc.Col([rating_indicator], width=4)]),
#                                                     dbc.Row([dbc.Col([traits_radar_chart], width=12)]),
#                                                     dbc.Row([dbc.Col([difference_bar_chart], width=12)])
#                                                     ],
#                                                    width=8
#                                                    )
#                                            ]
#                                           ),
#                                   list_similar_players
#                                   ],
#                                  style={'background-color': BACKGROUND_HEX},
#                                  fluid=True
#                                  )

# customise layout
dashboard.layout = dbc.Container([dbc.Col([dbc.Row([dbc.Label('FOOTBALL PLAYER SIMILARITY', size='l')], justify='center')], width={'size': 2, 'offset': 5}),
                                  dbc.Row([dbc.Col([dbc.Row([dbc.Col([dbc.Row([dbc.Label('Query player 1:', size='sm')], justify='left'),
                                                                      dbc.Row([player_1_details], justify='center')
                                                                      ],
                                                                     width=6),
                                                             dbc.Col([dbc.Row([dbc.Label('Query player 2 (Optional):', size='sm')], justify='left'),
                                                                      dbc.Row([player_2_details], justify='center')
                                                                      ],
                                                                     width=6)
                                                             ]
                                                            ),
                                                    dbc.Row([dbc.Col([dbc.Row([dbc.Label('Player 1 weight:', size='sm')], justify='left'),
                                                                      dbc.Row([player_1_weight], justify='center')
                                                                      ],
                                                                     width=6),
                                                             dbc.Col([dbc.Row([dbc.Label('Player 2 weight:', size='sm')], justify='left'),
                                                                      dbc.Row([player_2_weight], justify='center')
                                                                      ],
                                                                     width=6)
                                                             ]
                                                            ),
                                                    dbc.Row([dbc.Col([dbc.Row([dbc.Label('Number of similar players:', size='sm')], justify='left'),
                                                                      dbc.Row([top_n], justify='center')
                                                                      ],
                                                                     width={'size': 6, 'offset': 3})
                                                             ]
                                                            )
                                                    ],
                                                   width=4
                                                   ),
                                           dbc.Col([dbc.Row([dbc.Col([dbc.Row([dbc.Label('Goals', size='sm')], justify='left'),
                                                                      dbc.Row([goals_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Shots', size='sm')], justify='left'),
                                                                      dbc.Row([shots_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Conversion', size='sm')], justify='left'),
                                                                      dbc.Row([conversion_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Positioning', size='sm')], justify='left'),
                                                                      dbc.Row([positioning_weight], justify='center')
                                                                      ],
                                                                     width=3),
                                                             dbc.Col([dbc.Row([dbc.Label('Assists', size='sm')], justify='left'),
                                                                      dbc.Row([assists_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Crossing', size='sm')], justify='left'),
                                                                      dbc.Row([crossing_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Dribbling', size='sm')], justify='left'),
                                                                      dbc.Row([dribbling_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Carries', size='sm')], justify='left'),
                                                                      dbc.Row([carries_weight], justify='center')
                                                                      ],
                                                                     width=3),
                                                             dbc.Col([dbc.Row([dbc.Label('Involvement', size='sm')], justify='left'),
                                                                      dbc.Row([involvement_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Accuracy', size='sm')], justify='left'),
                                                                      dbc.Row([accuracy_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Intent', size='sm')], justify='left'),
                                                                      dbc.Row([intent_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Receiving', size='sm')], justify='left'),
                                                                      dbc.Row([receiving_weight], justify='center')
                                                                      ],
                                                                     width=3),
                                                             dbc.Col([dbc.Row([dbc.Label('Aerial', size='sm')], justify='left'),
                                                                      dbc.Row([aerial_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('On-ball', size='sm')], justify='left'),
                                                                      dbc.Row([on_ball_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Off-ball', size='sm')], justify='left'),
                                                                      dbc.Row([off_ball_weight], justify='center'),
                                                                      dbc.Row([dbc.Label('Fouls', size='sm')], justify='left'),
                                                                      dbc.Row([fouls_weight], justify='center')
                                                                      ],
                                                                     width=3),
                                                             ]
                                                            )
                                                    ],
                                                   width=4
                                                   ),
                                           dbc.Col([dbc.Row([dbc.Col([dbc.Row([dbc.Label('Seasons', size='sm')], justify='left'),
                                                                      dbc.Row([seasons_filter], justify='center')
                                                                      ],
                                                                     width=4),
                                                             dbc.Col([dbc.Row([dbc.Label('Leagues', size='sm')], justify='left'),
                                                                      dbc.Row([leagues_filter], justify='center')
                                                                      ],
                                                                     width=4),
                                                             dbc.Col([dbc.Row([dbc.Label('Primary positions', size='sm')], justify='left'),
                                                                      dbc.Row([primary_positions_filter], justify='center')
                                                                      ],
                                                                     width=4)
                                                             ]
                                                            ),
                                                    dbc.Row([dbc.Col([dbc.Row([dbc.Label('Age range', size='sm')], justify='left'),
                                                                      dbc.Row([age_range_filter], justify='center'),
                                                                      dbc.Row([dbc.Label('Appearances range', size='sm')], justify='left'),
                                                                      dbc.Row([apps_range_filter], justify='center')
                                                                      ],
                                                                     width=12)
                                                             ]
                                                            )
                                                    ],
                                                   width=4)
                                           ]
                                          ),
                                  dbc.Row(dbc.Col([table_similar_players],
                                                  width=12)),
                                  dbc.Row(dbc.Col([rating_indicator],
                                                  width={'size': 10, 'offset': 1})),
                                  dbc.Row([dbc.Col([dbc.Row([traits_radar_chart]),
                                                    dbc.Row([difference_bar_chart])
                                                    ],
                                                   width={'size': 10, 'offset': 1}
                                                   )
                                           ]
                                          ),
                                  list_similar_players
                                  ],
                                 style={'background-color': BACKGROUND_HEX},
                                 fluid=True
                                 )

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
    primary_positions_options = [{'label': position, 'value': position} for position in primary_positions]
    min_age = similarity.get_min_age(player_1_details)
    max_age = similarity.get_max_age(player_1_details)
    age_range = [min_age, max_age]
    min_apps = similarity.get_min_apps(player_1_details)
    max_apps = similarity.get_max_apps(player_1_details)
    apps_range = [min_apps, max_apps]

    return position_player_details, primary_positions_options, primary_positions, min_age, max_age, age_range, min_apps, max_apps, apps_range

@dashboard.callback(Output(player_1_weight, component_property='options'),
                    Output(player_1_weight, component_property='placeholder'),
                    Output(player_2_weight, component_property='options'),
                    Output(player_2_weight, component_property='placeholder'),
                    Input(player_2_details, component_property='value'))
def update_players_weight_dropdowns(player_2_details):
    if player_2_details is None:
        options = []
        placeholder_1 = '100%'
        placeholder_2 = '0%'
    else:
        options = [f'{i}%' for i in range(10, 91, 10)]
        placeholder_1 = 'Select weight for player 1'
        placeholder_2 = 'Select weight for player 2'

    return options, placeholder_1, options, placeholder_2

@dashboard.callback(Output(player_2_weight, component_property='value'),
                    Input(player_1_weight, component_property='value'))
def update_player_2_weight(player_1_weight):

    if player_1_weight is None:
        return None

    # convert to fraction
    fraction_1 = int(player_1_weight[:-1]) / 100
    fraction_2 = 1 - fraction_1

    return f'{fraction_2*100:.0f}%'

@dashboard.callback(Output(player_1_weight, component_property='value'),
                    Input(player_2_weight, component_property='value'))
def update_player_2_weight(player_2_weight):

    if player_2_weight is None:
        return None

    # convert to fraction
    fraction_2 = int(player_2_weight[:-1]) / 100
    fraction_1 = 1 - fraction_2

    return f'{fraction_1*100:.0f}%'

@dashboard.callback(Output(table_similar_players, component_property='data'),
                    Output(table_similar_players, component_property='columns'),
                    Output(list_similar_players, component_property='data'),
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
        if player_1_weight is None or player_2_weight is None:
            player_weights = None
        else:
            player_weights = [int(player_1_weight[:-1])/100, int(player_2_weight[:-1])/100]

        table_similar_players, similar_players = similarity.table_similar_players_2(player_1_details=player_1_details,
                                                                                    player_2_details=player_2_details,
                                                                                    df=df,
                                                                                    top_n=top_n,
                                                                                    player_weights=player_weights,
                                                                                    traits_weights=traits_weights,
                                                                                    filters=filters)
    df_dict = table_similar_players.to_dict('records')
    df_cols = [{'name': col, 'id': col} for col in table_similar_players.columns]

    return df_dict, df_cols, similar_players

@dashboard.callback(Output(rating_indicator, component_property='figure'),
                    Output(traits_radar_chart, component_property='figure'),
                    Output(difference_bar_chart, component_property='figure'),
                    Input(player_1_details, component_property='value'),
                    Input(player_2_details, component_property='value'),
                    Input(player_1_weight, component_property='value'),
                    Input(player_2_weight, component_property='value'),
                    Input(list_similar_players, component_property='data'),
                    Input(table_similar_players, component_property='active_cell'))
def update_charts(player_1_details, player_2_details, player_1_weight, player_2_weight, list_similar_players, active_cell):

    if active_cell is None:
        return similarity.blank_figure(), similarity.blank_figure(), similarity.blank_figure()

    compare_player = list_similar_players[active_cell['row']]

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
        if player_1_weight is None or player_2_weight is None:
            player_weights = None
        else:
            player_weights = [int(player_1_weight[:-1]) / 100, int(player_2_weight[:-1]) / 100]

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
