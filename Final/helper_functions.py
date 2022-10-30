# Script containing functions necessary for 'launch_dashboard.py'.

# import packages
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# constants
RAW_TRAITS = ['goals', 'shots', 'conversion', 'positioning', 'assists', 'crossing', 'dribbling', 'carries',
              'involvement', 'accuracy', 'intent', 'receiving', 'aerial', 'on_ball', 'off_ball', 'fouls']
COMPOSITE_TRAITS = ['scoring', 'creating', 'passing', 'defending']
RAW_TRAITS_DISPLAY = ['Goals', 'Shots', 'Conversion', 'Positioning', 'Assists', 'Crossing', 'Dribbling', 'Carries',
                      'Involvement', 'Accuracy', 'Intent', 'Receiving', 'Aerial', 'On ball', 'Off ball', 'Fouls']
COMPOSITE_TRAITS_DISPLAY = ['Scoring', 'Creating', 'Passing', 'Defending']
SIMILARITY_TABLE_HEADERS = ['RANK', 'PLAYER NAME', 'NATIONALITY', 'AGE', 'TEAM', 'PRIMARY POSITION', 'SIMILARITY SCORE']
TOP_N = 20
MIN_AGE = 17
MAX_AGE = 45
MIN_TOTAL_MINS = 720
MAX_TOTAL_MINS = 3420
MIN_RATING = 0.6
MAX_RATING = 4.9
DARK_BLUE_HEX = '#4074B2'
DARK_ORANGE_HEX = '#E77052'

# paths to dataframe csv files
DF_FULL_PATH = 'Data/df_full.csv'

# load dataframes for each position
df_full = pd.read_csv(DF_FULL_PATH, index_col=0)

def get_position(player_details):

    df_full_copy = df_full.copy()

    # get player position
    try:
        position = df_full_copy[df_full_copy.player_details==player_details].position.tolist()[0]

        return position

    except:
        raise Exception('Player not in database')

def get_all_player_details():

    # sort df by rating in descending order
    df_full_sorted = df_full.copy()
    df_full_sorted = df_full_sorted[(df_full_sorted.season=='2019') | (df_full_sorted.season=='2020') | (df_full_sorted.season=='2021')]
    df_full_sorted = df_full_sorted.sort_values(by='rating', ascending=False)

    return df_full_sorted.player_details.tolist()

def get_position_player_details(player_details):

    # get player position
    df_full_copy = df_full.copy()
    position = get_position(player_details)

    # sort df by rating in descending order
    position_df_sorted = df_full_copy[df_full_copy.position==position]
    position_df_sorted = position_df_sorted[(position_df_sorted.season=='2019') | (position_df_sorted.season=='2020') | (position_df_sorted.season=='2021')]
    position_df_sorted = position_df_sorted.sort_values(by='rating', ascending=False)

    return position_df_sorted.player_details.tolist()

def get_all_leagues():

    df_full_copy = df_full.copy()

    return sorted(set(df_full_copy.league))

def get_primary_positions(player_details):

    # get player position
    df_full_copy = df_full.copy()
    position = get_position(player_details)

    return sorted(set(df_full_copy[df_full_copy.position==position].primary_position))

def get_min_age():

    df_full_copy = df_full.copy()

    return int(df_full_copy.age.min())

def get_max_age():

    df_full_copy = df_full.copy()

    return int(df_full_copy.age.max())

def get_min_total_mins():

    df_full_copy = df_full.copy()

    return int(df_full_copy.total_mins.min())

def get_max_total_mins():

    df_full_copy = df_full.copy()

    return int(df_full_copy.total_mins.max())

def get_min_rating():

    df_full_copy = df_full.copy()

    return df_full_copy.rating.min()

def get_max_rating():

    df_full_copy = df_full.copy()

    return df_full_copy.rating.max()

def blank_figure():

    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template='plotly_dark')
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig

def weighted_cosine_similarity_score(vec1, vec2, weights=None):

    # asserts that vec1 and vec2 have same length
    assert len(vec1) == len(vec2), f'Vectors have distinct shapes ({len(vec1)},), ({len(vec2)},)'

    # asserts that weights have same length as vec1 and vec2
    if weights is None:
        weights = [1] * len(vec1)
    else:
        assert len(weights) == len(vec1), f'Weights have distinct shape ({len(weights)},) from vectors ({len(vec1)},)'

    # return 1 if two arrays are identical
    if np.array_equal(vec1, vec2):
        return 1

    # return 0 if either arrays is full of zeros
    if not (vec1.any() and vec2.any()):
        return 0

    # compute weighted dot product and length of vectors
    dot_product = 0
    weighted_squared_length_vec1 = 0
    weighted_squared_length_vec2 = 0
    for i in range(len(vec1)):
        dot_product += vec1[i] * vec2[i] * weights[i]
        weighted_squared_length_vec1 += vec1[i] ** 2 * weights[i]
        weighted_squared_length_vec2 += vec2[i] ** 2 * weights[i]
    weighted_length_vec1 = weighted_squared_length_vec1 ** 0.5
    weighted_length_vec2 = weighted_squared_length_vec2 ** 0.5

    # compute cosine similarity scores
    score = dot_product / (weighted_length_vec1 * weighted_length_vec2)

    return score

def get_scores(player_traits, others_traits, weights):

    # compute similarity scores
    similarity_scores = np.zeros([others_traits.shape[0]])
    for i in range(others_traits.shape[0]):
        similarity_scores[i] = weighted_cosine_similarity_score(player_traits, others_traits[i], weights)

    # rescale similarity scores as per afl metric
    similarity_scores = 1 - (2 / np.pi) * np.arccos(similarity_scores)

    # normalise similarity scores
    similarity_scores = (similarity_scores - similarity_scores.min()) / (1 - similarity_scores.min())

    return similarity_scores

def filter_df(df, filters):

    if filters['seasons'] is None:
        seasons = '2021'
    else:
        seasons = filters['seasons']

    if filters['leagues'] is None:
        leagues = df.league.unique()
    else:
        leagues = filters['leagues']

    if filters['primary_positions'] is None:
        primary_positions = df.primary_position.unique()
    else:
        primary_positions = filters['primary_positions']

    if filters['min_age'] is None:
        min_age = MIN_AGE
    else:
        min_age = filters['min_age']

    if filters['max_age'] is None:
        max_age = MAX_AGE
    else:
        max_age = filters['max_age']

    if filters['min_total_mins'] is None:
        min_total_mins = MIN_TOTAL_MINS
    else:
        min_total_mins = filters['min_total_mins']

    if filters['min_rating'] is None:
        min_rating = MIN_RATING
    else:
        min_rating = filters['min_rating']

    # get filtered df
    filtered_df = df[(df.season==seasons) &
                     (df.league.isin(leagues)) &
                     (df.primary_position.isin(primary_positions)) &
                     (df.age>=min_age) &
                     (df.age<=max_age) &
                     (df.total_mins>=min_total_mins) &
                     (df.rating>=min_rating)]

    return filtered_df

def get_similar_players_df(results, df):

    # get all player details
    all_player_details = list(results.keys())

    # trim dataframe to similar players
    similar_players_df = df[df.player_details.isin(all_player_details)]

    # add new column for similarity scores
    similar_players_df['similarity_score'] = similar_players_df.player_details.map(results)

    # rearrange columns
    temp_cols = similar_players_df.columns.tolist()
    new_cols = temp_cols[1:2] + temp_cols[7:8] + temp_cols[9:10] + temp_cols[4:5] + temp_cols[6:7] + temp_cols[-1:]
    similar_players_df = similar_players_df[new_cols]

    # sort dataframe by similarity score
    similar_players_df = similar_players_df.sort_values(by='similarity_score', ascending=False)

    # insert a rank column
    rank_list = list(range(1, len(all_player_details)+1))
    similar_players_df.insert(0, 'Rank', rank_list)

    # convert similarity scores into percentage
    similar_players_df['similarity_score'] = similar_players_df['similarity_score'].mul(100).round(1).astype(str).add(' %')

    # rename dataframe columns
    similar_players_df.columns = SIMILARITY_TABLE_HEADERS

    return similar_players_df

def similar_players_df_1(player_details, position, top_n=TOP_N, traits_weights=None, filters=None):

    # get position df
    df = df_full[df_full.position==position]
    df = df.reset_index(drop=True)

    # get all player details
    all_player_details = df.player_details.tolist()

    # get matrix of raw traits only
    raw_traits_df = df[RAW_TRAITS]
    raw_traits_np = raw_traits_df.to_numpy()

    # assert that player details is in dataframe
    assert player_details in all_player_details, 'Player details not in dataframe'

    # asserts that matrix has 2 dimensions
    assert raw_traits_np.ndim == 2, 'Matrix should have 2 dimensions'

    # asserts that matrix is not ragged
    ragged = False
    for i in range(1, raw_traits_np.shape[0]):
        if len(raw_traits_np[i - 1]) != len(raw_traits_np[i]):
            ragged = True
            break
    assert ragged == False, 'Ragged matrix is not allowed'

    # asserts that traits weights have same length as matrix rows
    if traits_weights is not None:
        assert len(traits_weights) == len(raw_traits_np[0]), f'Weights have distinct shape ({len(traits_weights)},) ' \
                                                             f'from matrix rows ({len(raw_traits_np[0])},)'

    # get indices of queried player names
    player_index = all_player_details.index(player_details)
    player_name = df.iloc[player_index]['player_name']
    duplicate_indices = df.index[df.player_name == player_name].tolist()

    # get which indices to keep if filters are prompted
    if filters is not None:
        filtered_df = filter_df(df, filters)
        keep_indices = filtered_df.index.tolist()

        # assert that filters does not empty dataframe
        assert len(set(keep_indices) - set(duplicate_indices)) > 0, 'Filters result in an empty dataframe'
    else:
        keep_indices = []

    # set indices to be deleted
    all_indices = list(range(len(df)))
    delete_indices = list((set(all_indices) - set(keep_indices)).union(set(duplicate_indices)))

    # get queried player raw traits
    player_raw_traits = raw_traits_np[player_index]

    # get similarity scores
    similarity_scores = get_scores(player_raw_traits, raw_traits_np, traits_weights)

    if filters is not None:
        # remove necessary rows from similarity_scores and all_player_details
        similarity_scores = np.delete(similarity_scores, delete_indices, axis=0)
        all_player_details = np.delete(all_player_details, delete_indices, axis=0)
    else:
        # remove rows of queried player name from similarity_scores and all_player_details
        similarity_scores = np.delete(similarity_scores, duplicate_indices, axis=0)
        all_player_details = np.delete(all_player_details, duplicate_indices, axis=0)

    # set top_n to the number of players if too large
    if top_n > similarity_scores.shape[0]:
        top_n = similarity_scores.shape[0]
        print(f'There is only {top_n} players after filtering!\n')

    # get indices of top n scores
    top_n_indices = np.argpartition(similarity_scores, -top_n)[-top_n:]
    top_n_indices = np.flip(top_n_indices[np.argsort(similarity_scores[top_n_indices])])

    # dictionary of player details as keys and similarity scores as values
    top_n_dict = {all_player_details[ind]: similarity_scores[ind] for ind in top_n_indices}

    # create table of similar players
    similar_players_df = get_similar_players_df(top_n_dict, df)

    return similar_players_df, top_n_dict

def similar_players_df_2(player_1_details, player_2_details, position, top_n=TOP_N, player_weights=None, traits_weights=None, filters=None):

    # get position df
    df = df_full[df_full.position == position]
    df = df.reset_index(drop=True)

    # get all player details
    all_player_details = df.player_details.tolist()

    # get matrix of raw traits only
    raw_traits_df = df[RAW_TRAITS]
    raw_traits_np = raw_traits_df.to_numpy()

    # assert that player details are in dataframe
    assert player_1_details in all_player_details, 'Player 1 details not in dataframe'
    assert player_2_details in all_player_details, 'Player 2 details not in dataframe'

    # asserts that matrix has 2 dimensions
    assert raw_traits_np.ndim == 2, 'Matrix should have 2 dimensions'

    # asserts that matrix is not ragged
    ragged = False
    for i in range(1, raw_traits_np.shape[0]):
        if len(raw_traits_np[i - 1]) != len(raw_traits_np[i]):
            ragged = True
            break
    assert ragged == False, 'Ragged matrix is not allowed'

    # asserts that traits weights have same length as matrix rows
    if traits_weights is not None:
        assert len(traits_weights) == len(raw_traits_np[0]), f'Weights have distinct shape ({len(traits_weights)},) ' \
                                                             f'from matrix rows ({len(raw_traits_np[0])},)'

    if player_weights is not None:
        # assert that player weights sum up to 1
        assert sum(player_weights) == 1, f'Player weights do not sum up to 1'
    else:
        player_weights = [0.5, 0.5]

    # get indices of queried player names
    player_1_index = all_player_details.index(player_1_details)
    player_1_name = df.iloc[player_1_index]['player_name']
    player_1_indices = df.index[df.player_name == player_1_name].tolist()
    player_2_index = all_player_details.index(player_2_details)
    player_2_name = df.iloc[player_2_index]['player_name']
    player_2_indices = df.index[df.player_name == player_2_name].tolist()
    duplicate_indices = player_1_indices + player_2_indices

    # get which indices to keep if filters are prompted
    if filters is not None:
        filtered_df = filter_df(df, filters)
        keep_indices = filtered_df.index.tolist()

        # assert that filters does not empty dataframe
        assert len(set(keep_indices) - set(duplicate_indices)) > 0, 'Filters result in an empty dataframe'
    else:
        keep_indices = []

    # set indices to be deleted
    all_indices = list(range(len(df)))
    delete_indices = list((set(all_indices) - set(keep_indices)).union(set(duplicate_indices)))

    # get queried player raw traits
    player_1_raw_traits = raw_traits_np[player_1_index]
    player_2_raw_traits = raw_traits_np[player_2_index]

    # combined traits
    combined_raw_traits = np.average(np.array([player_1_raw_traits, player_2_raw_traits]), axis=0,
                                     weights=player_weights)

    # combined player details
    combined_player_details = f'{player_1_details} ({player_weights[0] * 100:.0f}%) + {player_2_details} ' \
                              f'({player_weights[1] * 100:.0f}%)'

    # get similarity scores
    similarity_scores = get_scores(combined_raw_traits, raw_traits_np, traits_weights)

    if filters is not None:
        # remove necessary rows from similarity_scores and all_player_details
        similarity_scores = np.delete(similarity_scores, delete_indices, axis=0)
        all_player_details = np.delete(all_player_details, delete_indices, axis=0)
    else:
        # remove rows of queried player name from similarity_scores and all_player_details
        similarity_scores = np.delete(similarity_scores, duplicate_indices, axis=0)
        all_player_details = np.delete(all_player_details, duplicate_indices, axis=0)

    # set top_n to the number of players if too large
    if top_n > similarity_scores.shape[0]:
        top_n = similarity_scores.shape[0]
        print(f'There is only {top_n} players filtering!\n')

    # get indices of top n scores
    top_n_indices = np.argpartition(similarity_scores, -top_n)[-top_n:]
    top_n_indices = np.flip(top_n_indices[np.argsort(similarity_scores[top_n_indices])])

    # dictionary of player details as keys and similarity scores as values
    top_n_dict = {all_player_details[ind]: similarity_scores[ind] for ind in top_n_indices}

    # create table of similar players
    similar_players_df = get_similar_players_df(top_n_dict, df)

    return similar_players_df, top_n_dict

def rating_indicators_1(query_player_details, similar_player_details, position):

    # get position df
    df = df_full[df_full.position == position]
    df = df.reset_index(drop=True)

    # get query player rating
    query_player_rating = df[df.player_details == query_player_details].rating.tolist()[0]

    # get similar player rating
    similar_player_rating = df[df.player_details == similar_player_details].rating.tolist()[0]

    # create rating indicator cards
    fig = go.Figure()

    # rating of query player
    fig.add_trace(go.Indicator(mode='number',
                               value=query_player_rating,
                               title=query_player_details,
                               domain={'row': 0, 'column': 0}))

    # rating of similar player
    fig.add_trace(go.Indicator(mode='number+delta',
                               value=similar_player_rating,
                               delta=dict(reference=query_player_rating),
                               title=similar_player_details,
                               domain={'row': 1, 'column': 0}))

    # card details
    fig.update_layout(height=800,
                      width=1200,
                      grid={'rows': 2, 'columns': 1},
                      template='plotly_dark',
                      font={'size': 18}
    )

    return fig

def rating_indicators_2(query_player_1_details, query_player_2_details, similar_player_details, position, player_weights=None):

    if player_weights is not None:
        # assert that player weights sum up to 1
        assert sum(player_weights) == 1, f'Player weights do not sum up to 1'
    else:
        player_weights = [0.5, 0.5]

    # get position df
    df = df_full[df_full.position == position]
    df = df.reset_index(drop=True)

    # get query players ratings
    query_player_1_rating = df[df.player_details == query_player_1_details].rating.tolist()[0]
    query_player_2_rating = df[df.player_details == query_player_2_details].rating.tolist()[0]

    # combine ratings
    combined_player_rating = np.average(np.array([query_player_1_rating, query_player_2_rating]), axis=0,
                                        weights=player_weights)

    # combined player details
    combined_player_details = f'{query_player_1_details} ({player_weights[0] * 100:.0f}%) + {query_player_2_details} ' \
                              f'({player_weights[1] * 100:.0f}%)'

    # get similar player rating
    similar_player_rating = df[df.player_details == similar_player_details].rating.tolist()[0]

    # create rating indicator cards
    fig = go.Figure()

    # rating of query player
    fig.add_trace(go.Indicator(mode='number',
                               value=combined_player_rating,
                               title=combined_player_details,
                               domain={'row': 0, 'column': 0}))

    # rating of similar player
    fig.add_trace(go.Indicator(mode='number+delta',
                               value=similar_player_rating,
                               delta=dict(reference=combined_player_rating),
                               title=similar_player_details,
                               domain={'row': 1, 'column': 0}))

    # card details
    fig.update_layout(height=800,
                      width=1200,
                      grid={'rows': 2, 'columns': 1},
                      template='plotly_dark',
                      font={'size': 18}
    )

    return fig

def composite_traits_charts_1(query_player_details, similar_player_details, position):

    # get position df
    df = df_full[df_full.position == position]
    df = df.reset_index(drop=True)

    # get values for query player traits
    composite_trait_values_1 = df[df.player_details == query_player_details][COMPOSITE_TRAITS].values[0].tolist()
    circ_composite_trait_values_1 = composite_trait_values_1 + composite_trait_values_1[:1]

    # get values for similar player traits
    composite_trait_values_2 = df[df.player_details == similar_player_details][COMPOSITE_TRAITS].values[0].tolist()
    circ_composite_trait_values_2 = composite_trait_values_2 + composite_trait_values_2[:1]

    # get difference in traits values
    composite_traits_diff = [composite_trait_1 - composite_trait_2 for composite_trait_1, composite_trait_2 in zip(composite_trait_values_1, composite_trait_values_2)]

    # get positive and negative lists for composite traits differences
    composite_traits_pos_diff = []
    composite_traits_neg_diff = []
    pos_composite_traits = []
    neg_composite_traits = []
    for diff, trait in zip(composite_traits_diff, COMPOSITE_TRAITS_DISPLAY):
        if diff >= 0:
            composite_traits_pos_diff.append(diff)
            pos_composite_traits.append(trait)
        else:
            composite_traits_neg_diff.append(diff)
            neg_composite_traits.append(trait)

    # adjust composite traits lists
    circ_composite_traits = COMPOSITE_TRAITS_DISPLAY + COMPOSITE_TRAITS_DISPLAY[:1]

    # create radar charts
    fig = make_subplots(rows=1,
                        cols=2,
                        specs=[[{'type': 'polar'}, {'type': 'bar'}]],
                        subplot_titles=('Radar Chart', 'Difference Bar Chart'))

    # plot radar chart
    fig.add_trace(go.Scatterpolar(r=circ_composite_trait_values_1,
                                  theta=circ_composite_traits,
                                  fill='toself',
                                  name=query_player_details,
                                  marker=dict(color=DARK_BLUE_HEX)),
                  row=1,
                  col=1
                  )
    fig.add_trace(go.Scatterpolar(r=circ_composite_trait_values_2,
                                  theta=circ_composite_traits,
                                  fill='toself',
                                  name=similar_player_details,
                                  marker=dict(color=DARK_ORANGE_HEX)),
                  row=1,
                  col=1
                  )

    # plot difference bar chart
    fig.add_trace(go.Bar(x=pos_composite_traits,
                         y=composite_traits_pos_diff,
                         name=query_player_details,
                         marker=dict(color=DARK_BLUE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )
    fig.add_trace(go.Bar(x=neg_composite_traits,
                         y=composite_traits_neg_diff,
                         name=similar_player_details,
                         marker=dict(color=DARK_ORANGE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )

    # plot details
    fig.update_layout(height=800,
                      width=1200,
                      margin=dict(l=90, r=90, t=90, b=10),
                      polar={'radialaxis': {'visible': True}},
                      showlegend=True,
                      legend=dict(x=0, y=-0.3),
                      template='plotly_dark',
                      font={'size': 14}
                      )
    # fig.update_polars(radialaxis=dict(range=[0, max(circ_composite_trait_values_1)]))
    fig.update_xaxes(categoryorder='array', categoryarray=COMPOSITE_TRAITS_DISPLAY, row=1, col=2)
    fig.update_yaxes(range=[-4, 4])

    return fig

def composite_traits_charts_2(query_player_1_details, query_player_2_details, similar_player_details, position, player_weights=None):

    if player_weights is not None:
        # assert that player weights sum up to 1
        assert sum(player_weights) == 1, f'Player weights do not sum up to 1'
    else:
        player_weights = [0.5, 0.5]

    # get position df
    df = df_full[df_full.position == position]
    df = df.reset_index(drop=True)

    # get values for query players traits
    composite_trait_values_1 = df[df.player_details == query_player_1_details][COMPOSITE_TRAITS].values[0].tolist()
    composite_trait_values_2 = df[df.player_details == query_player_2_details][COMPOSITE_TRAITS].values[0].tolist()

    # combine traits for query players traits
    composite_trait_values_combined = np.average(np.array([composite_trait_values_1, composite_trait_values_2]), axis=0,
                                           weights=player_weights).tolist()
    circ_composite_trait_values_combined = composite_trait_values_combined + composite_trait_values_combined[:1]

    # get values for similar player traits
    composite_trait_values_3 = df[df.player_details == similar_player_details][COMPOSITE_TRAITS].values[0].tolist()
    circ_composite_trait_values_3 = composite_trait_values_3 + composite_trait_values_3[:1]

    # create traits difference in traits values
    composite_traits_diff = [composite_trait_1 - composite_trait_2 for composite_trait_1, composite_trait_2 in
                       zip(composite_trait_values_combined, composite_trait_values_3)]

    # get positive and negative lists for composite traits differences
    composite_traits_pos_diff = []
    composite_traits_neg_diff = []
    pos_composite_traits = []
    neg_composite_traits = []
    for diff, trait in zip(composite_traits_diff, COMPOSITE_TRAITS_DISPLAY):
        if diff >= 0:
            composite_traits_pos_diff.append(diff)
            pos_composite_traits.append(trait)
        else:
            composite_traits_neg_diff.append(diff)
            neg_composite_traits.append(trait)

    # adjust composite traits lists
    circ_composite_traits = COMPOSITE_TRAITS_DISPLAY + COMPOSITE_TRAITS_DISPLAY[:1]

    # combined player details
    combined_player_details = f'{query_player_1_details} ({player_weights[0] * 100:.0f}%) + {query_player_2_details} ' \
                              f'({player_weights[1] * 100:.0f}%)'

    # create radar charts
    fig = make_subplots(rows=1,
                        cols=2,
                        specs=[[{'type': 'polar'}, {'type': 'bar'}]],
                        subplot_titles=('Radar Chart', 'Difference Bar Chart'))

    # plot radar chart
    fig.add_trace(go.Scatterpolar(r=circ_composite_trait_values_combined,
                                  theta=circ_composite_traits,
                                  fill='toself',
                                  name=combined_player_details,
                                  marker=dict(color=DARK_BLUE_HEX)),
                  row=1,
                  col=1
                  )
    fig.add_trace(go.Scatterpolar(r=circ_composite_trait_values_3,
                                  theta=circ_composite_traits,
                                  fill='toself',
                                  name=similar_player_details,
                                  marker=dict(color=DARK_ORANGE_HEX)),
                  row=1,
                  col=1
                  )

    # plot difference bar chart
    fig.add_trace(go.Bar(x=pos_composite_traits,
                         y=composite_traits_pos_diff,
                         name=combined_player_details,
                         marker=dict(color=DARK_BLUE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )
    fig.add_trace(go.Bar(x=neg_composite_traits,
                         y=composite_traits_neg_diff,
                         name=similar_player_details,
                         marker=dict(color=DARK_ORANGE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )

    # plot details
    fig.update_layout(height=800,
                      width=1200,
                      margin=dict(l=90, r=90, t=90, b=10),
                      polar={'radialaxis': {'visible': True}},
                      showlegend=True,
                      legend=dict(x=0, y=-0.3),
                      template='plotly_dark',
                      font={'size': 14}
                      )
    # fig.update_polars(radialaxis=dict(range=[0, max(circ_composite_trait_values_combined)]))
    fig.update_xaxes(categoryorder='array', categoryarray=COMPOSITE_TRAITS_DISPLAY, row=1, col=2)
    fig.update_yaxes(range=[-4, 4])

    return fig

def raw_traits_charts_1(query_player_details, similar_player_details, position):

    # get position df
    df = df_full[df_full.position == position]
    df = df.reset_index(drop=True)

    # get values for query player traits
    raw_trait_values_1 = df[df.player_details == query_player_details][RAW_TRAITS].values[0].tolist()
    circ_raw_trait_values_1 = raw_trait_values_1 + raw_trait_values_1[:1]

    # get values for similar player traits
    raw_trait_values_2 = df[df.player_details == similar_player_details][RAW_TRAITS].values[0].tolist()
    circ_raw_trait_values_2 = raw_trait_values_2 + raw_trait_values_2[:1]

    # get difference in traits values
    raw_traits_diff = [raw_trait_1 - raw_trait_2 for raw_trait_1, raw_trait_2 in
                       zip(raw_trait_values_1, raw_trait_values_2)]

    # get positive and negative lists for raw traits differences
    raw_traits_pos_diff = []
    raw_traits_neg_diff = []
    pos_raw_traits = []
    neg_raw_traits = []
    for diff, trait in zip(raw_traits_diff, RAW_TRAITS_DISPLAY):
        if diff >= 0:
            raw_traits_pos_diff.append(diff)
            pos_raw_traits.append(trait)
        else:
            raw_traits_neg_diff.append(diff)
            neg_raw_traits.append(trait)

    # adjust raw and composite traits lists
    circ_raw_traits = RAW_TRAITS_DISPLAY + RAW_TRAITS_DISPLAY[:1]

    # create radar charts
    fig = make_subplots(rows=1,
                        cols=2,
                        specs=[[{'type': 'polar'}, {'type': 'bar'}]],
                        subplot_titles=('Radar Chart', 'Difference Bar Chart'))

    # plot radar chart
    fig.add_trace(go.Scatterpolar(r=circ_raw_trait_values_1,
                                  theta=circ_raw_traits,
                                  fill='toself',
                                  name=query_player_details,
                                  marker=dict(color=DARK_BLUE_HEX)),
                  row=1,
                  col=1
                  )
    fig.add_trace(go.Scatterpolar(r=circ_raw_trait_values_2,
                                  theta=circ_raw_traits,
                                  fill='toself',
                                  name=similar_player_details,
                                  marker=dict(color=DARK_ORANGE_HEX)),
                  row=1,
                  col=1
                  )

    # plot difference bar chart
    fig.add_trace(go.Bar(x=pos_raw_traits,
                         y=raw_traits_pos_diff,
                         name=query_player_details,
                         marker=dict(color=DARK_BLUE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )
    fig.add_trace(go.Bar(x=neg_raw_traits,
                         y=raw_traits_neg_diff,
                         name=similar_player_details,
                         marker=dict(color=DARK_ORANGE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )

    # plot details
    fig.update_layout(height=800,
                      width=1200,
                      margin=dict(l=90, r=90, t=90, b=10),
                      polar={'radialaxis': {'visible': True}},
                      showlegend=True,
                      legend=dict(x=0, y=-0.3),
                      template='plotly_dark',
                      font={'size': 14}
                      )
    # fig.update_polars(radialaxis=dict(range=[0, max(circ_raw_trait_values_1)]))
    fig.update_xaxes(categoryorder='array', categoryarray=RAW_TRAITS_DISPLAY, row=1, col=2)
    fig.update_yaxes(range=[-4, 4])

    return fig

def raw_traits_charts_2(query_player_1_details, query_player_2_details, similar_player_details, position, player_weights=None):

    if player_weights is not None:
        # assert that player weights sum up to 1
        assert sum(player_weights) == 1, f'Player weights do not sum up to 1'
    else:
        player_weights = [0.5, 0.5]

    # get position df
    df = df_full[df_full.position == position]
    df = df.reset_index(drop=True)

    # get values for query players traits
    raw_trait_values_1 = df[df.player_details == query_player_1_details][RAW_TRAITS].values[0].tolist()
    raw_trait_values_2 = df[df.player_details == query_player_2_details][RAW_TRAITS].values[0].tolist()

    # combine traits for query players traits
    raw_trait_values_combined = np.average(np.array([raw_trait_values_1, raw_trait_values_2]), axis=0,
                                           weights=player_weights).tolist()
    circ_raw_trait_values_combined = raw_trait_values_combined + raw_trait_values_combined[:1]

    # get values for similar player traits
    raw_trait_values_3 = df[df.player_details == similar_player_details][RAW_TRAITS].values[0].tolist()
    circ_raw_trait_values_3 = raw_trait_values_3 + raw_trait_values_3[:1]

    # create traits difference in traits values
    raw_traits_diff = [raw_trait_1 - raw_trait_2 for raw_trait_1, raw_trait_2 in
                       zip(raw_trait_values_combined, raw_trait_values_3)]

    # get positive and negative lists for raw traits differences
    raw_traits_pos_diff = []
    raw_traits_neg_diff = []
    pos_raw_traits = []
    neg_raw_traits = []
    for diff, trait in zip(raw_traits_diff, RAW_TRAITS_DISPLAY):
        if diff >= 0:
            raw_traits_pos_diff.append(diff)
            pos_raw_traits.append(trait)
        else:
            raw_traits_neg_diff.append(diff)
            neg_raw_traits.append(trait)

    # adjust raw and composite traits lists
    circ_raw_traits = RAW_TRAITS_DISPLAY + RAW_TRAITS_DISPLAY[:1]

    # combined player details
    combined_player_details = f'{query_player_1_details} ({player_weights[0] * 100:.0f}%) + {query_player_2_details} ' \
                              f'({player_weights[1] * 100:.0f}%)'

    # create radar charts
    fig = make_subplots(rows=1,
                        cols=2,
                        specs=[[{'type': 'polar'}, {'type': 'bar'}]],
                        subplot_titles=('Radar Chart', 'Difference Bar Chart'))

    # plot radar chart
    fig.add_trace(go.Scatterpolar(r=circ_raw_trait_values_combined,
                                  theta=circ_raw_traits,
                                  fill='toself',
                                  name=combined_player_details,
                                  marker=dict(color=DARK_BLUE_HEX)),
                  row=1,
                  col=1
                  )
    fig.add_trace(go.Scatterpolar(r=circ_raw_trait_values_3,
                                  theta=circ_raw_traits,
                                  fill='toself',
                                  name=similar_player_details,
                                  marker=dict(color=DARK_ORANGE_HEX)),
                  row=1,
                  col=1
                  )

    # plot difference bar chart
    fig.add_trace(go.Bar(x=pos_raw_traits,
                         y=raw_traits_pos_diff,
                         name=combined_player_details,
                         marker=dict(color=DARK_BLUE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )
    fig.add_trace(go.Bar(x=neg_raw_traits,
                         y=raw_traits_neg_diff,
                         name=similar_player_details,
                         marker=dict(color=DARK_ORANGE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )

    # plot details
    fig.update_layout(height=800,
                      width=1200,
                      margin=dict(l=90, r=90, t=90, b=10),
                      polar={'radialaxis': {'visible': True}},
                      showlegend=True,
                      legend=dict(x=0, y=-0.3),
                      template='plotly_dark',
                      font={'size': 14}
                      )
    fig.update_polars(radialaxis=dict(range=[0, max(circ_raw_trait_values_combined)]))
    fig.update_xaxes(categoryorder='array', categoryarray=RAW_TRAITS_DISPLAY, row=1, col=2)
    fig.update_yaxes(range=[-4, 4])

    return fig

if __name__ == '__main__':
    print('This file should not be called directly!')