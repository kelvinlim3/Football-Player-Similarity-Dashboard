# Run with `python dashboard.py` and visit http://127.0.0.1:8050/ in your web browser.

# import packages
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import similarity

# constants
DARK_GREY_HEX = '#111111'
ALL_PLAYER_DETAILS = similarity.get_all_player_details()

# build components
dashboard = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
query_player_details = dcc.Dropdown(options=ALL_PLAYER_DETAILS,
                                    value=ALL_PLAYER_DETAILS[0])
top_n = dcc.Slider(1, 20, 1, value=10)
table = dcc.Graph(figure={})


# customise layout
dashboard.layout = dbc.Container([query_player_details, top_n, table])

# interacting components
@dashboard.callback(Output(table, component_property='figure'),
                    Input(query_player_details, component_property='value'),
                    Input(top_n, component_property='value')
                    )
def create_table(query_player_details, top_n):
    table_similar_players_1, similar_players_list_1_ = similarity.table_similar_players_1(
        player_details=query_player_details,
        df=similarity.get_position_df(query_player_details),
        top_n=top_n,
        traits_weights=None,
        filters=None)

    return table_similar_players_1


# table_similar_players_1, similar_players_list_1_ = similarity.table_similar_players_1(player_details='Robert Lewandowski Bayern Munich 2020',
#                                                                                       df=similarity.get_position_df('Robert Lewandowski Bayern Munich 2020'),
#                                                                                       top_n=10,
#                                                                                       traits_weights=None,
#                                                                                       filters=None)
#
# rating_indicator_1 = similarity.rating_indicator_1(query_player_details='Robert Lewandowski Bayern Munich 2020',
#                                                    similar_player_details=similar_players_list_1_[0],
#                                                    df=similarity.get_position_df('Robert Lewandowski Bayern Munich 2020'))
#
# traits_radar_chart_1 = similarity.traits_radar_chart_1(query_player_details='Robert Lewandowski Bayern Munich 2020',
#                                                        similar_player_details=similar_players_list_1_[0],
#                                                        df=similarity.get_position_df('Robert Lewandowski Bayern Munich 2020'))
#
# difference_bar_chart_1 = similarity.difference_bar_chart_1(query_player_details='Robert Lewandowski Bayern Munich 2020',
#                                                            similar_player_details=similar_players_list_1_[0],
#                                                            df=similarity.get_position_df('Robert Lewandowski Bayern Munich 2020'))


# dashboard.layout = html.Div(style={'backgroundColor': DARK_GREY_HEX},
#                             children=[html.H1(children='Hello Dash'),
#                                       html.Div(children='''Dash: A web application framework for your data.'''),
#                                       dcc.Graph(id='table_similar_players_1',
#                                                 figure=table_similar_players_1),
#                                       dcc.Graph(id='rating_indicator_1',
#                                                 figure=rating_indicator_1),
#                                       dcc.Graph(id='traits_radar_chart_1',
#                                                 figure=traits_radar_chart_1),
#                                       dcc.Graph(id='difference_bar_chart_1',
#                                                 figure=difference_bar_chart_1)
#                                       ]
#                             )

if __name__ == '__main__':
    dashboard.run_server(debug=True)
