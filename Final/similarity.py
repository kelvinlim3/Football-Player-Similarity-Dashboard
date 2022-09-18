# Script containing functions necessary for 'dashboard.py'.

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
SIMILARITY_TABLE_HEADERS = ['Player details', 'Similarity score', 'Rating', 'Player name', 'Season', 'League', 'Team',
                            'Position', 'Nationality', 'Age', 'Total minutes']
DARK_BLUE_HEX = '#4074B2'
LIGHT_BLUE_HEX = '#ADCDF0'
DARK_ORANGE_HEX = '#E77052'

# paths to dataframe csv files
CB_DF_PATH = 'Data/df_cb.csv'
FB_DF_PATH = 'Data/df_fb.csv'
DM_DF_PATH = 'Data/df_dm.csv'
M_DF_PATH = 'Data/df_m.csv'
W_DF_PATH = 'Data/df_w.csv'
CF_DF_PATH = 'Data/df_cf.csv'
ALL_DF_PATH = 'Data/df_all.csv'

# load dataframes for each position
cb_full_df = pd.read_csv(CB_DF_PATH, index_col=0)
fb_full_df = pd.read_csv(FB_DF_PATH, index_col=0)
dm_full_df = pd.read_csv(DM_DF_PATH, index_col=0)
m_full_df = pd.read_csv(M_DF_PATH, index_col=0)
w_full_df = pd.read_csv(W_DF_PATH, index_col=0)
cf_full_df = pd.read_csv(CF_DF_PATH, index_col=0)
all_df = pd.read_csv(ALL_DF_PATH, index_col=0)

def get_all_player_details():
    # sort df by rating in descending order
    all_df_sorted = all_df.copy()
    all_df_sorted = all_df_sorted.sort_values(by='rating', ascending=False)

    return all_df_sorted.player_details.tolist()

def get_position_player_details(player_details):
    # get player position
    all_df_copy = all_df.copy()
    position = all_df_copy[all_df_copy.player_details==player_details].position.tolist()[0]

    # sort df by rating in descending order
    position_df_sorted = all_df_copy[all_df_copy.position==position].sort_values(by='rating', ascending=False)

    return position_df_sorted.player_details.tolist()

def get_all_seasons():
    all_df_copy = all_df.copy()

    return sorted(set(all_df_copy.season), reverse=True)

def get_all_leagues():
    all_df_copy = all_df.copy()

    return sorted(set(all_df_copy.league))

def get_primary_positions(player_details):
    # get player position
    all_df_copy = all_df.copy()
    position = all_df_copy[all_df_copy.player_details==player_details].position.tolist()[0]

    return sorted(set(all_df_copy[all_df_copy.position==position].primary_position))

def get_min_age(player_details):
    # get player position
    all_df_copy = all_df.copy()
    position = all_df_copy[all_df_copy.player_details==player_details].position.tolist()[0]

    return int(all_df_copy[all_df_copy.position==position].age.min())

def get_max_age(player_details):
    # get player position
    all_df_copy = all_df.copy()
    position = all_df_copy[all_df_copy.player_details==player_details].position.tolist()[0]

    return int(all_df_copy[all_df_copy.position==position].age.max())

def get_min_apps(player_details):
    # get player position
    all_df_copy = all_df.copy()
    position = all_df_copy[all_df_copy.player_details == player_details].position.tolist()[0]

    return int(all_df_copy[all_df_copy.position == position].apps.min())

def get_max_apps(player_details):
    # get player position
    all_df_copy = all_df.copy()
    position = all_df_copy[all_df_copy.player_details == player_details].position.tolist()[0]

    return int(all_df_copy[all_df_copy.position == position].apps.max())

def get_position_df(player_details):

    all_df_copy = all_df.copy()

    # get player position
    try:
        position = all_df_copy[all_df_copy.player_details==player_details].position.tolist()[0]

        if position == 'CB':
            return cb_full_df
        elif position == 'FB':
            return fb_full_df
        elif position == 'DM':
            return dm_full_df
        elif position == 'M':
            return m_full_df
        elif position == 'W':
            return w_full_df
        elif position == 'CF':
            return cf_full_df

    except:
        raise Exception('Player not in database')

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
    similarity_scores = (similarity_scores - similarity_scores.min()) / (similarity_scores.max() -
                                                                         similarity_scores.min())

    return similarity_scores

def filter_df(df, filters):

    if filters['seasons'] is None:
        seasons = df.season.unique()
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
        min_age = 18
    else:
        min_age = filters['min_age']

    if filters['max_age'] is None:
        max_age = 45
    else:
        max_age = filters['max_age']

    if filters['min_apps'] is None:
        min_apps = 12
    else:
        min_apps = filters['min_apps']

    if filters['max_apps'] is None:
        max_apps = 38
    else:
        max_apps = filters['max_apps']

    filtered_df = df[(df.season.isin(seasons)) &
                     (df.league.isin(leagues)) &
                     (df.primary_position.isin(primary_positions)) &
                     (df.age>=min_age) &
                     (df.age<=max_age) &
                     (df.apps>=min_apps) &
                     (df.apps<=max_apps)]

    return filtered_df

def get_nontraits_table_similar_players(results, df, player_details, top_n):

    # get all player details
    all_player_details = list(results.keys())

    # trim dataframe to similar players
    similar_players_df = df[df.player_details.isin(all_player_details)]

    # add new column for similarity scores
    similar_players_df['similarity_score'] = similar_players_df.player_details.map(results)

    # rearrange columns
    temp_cols = similar_players_df.columns.tolist()
    new_cols = temp_cols[:1] + temp_cols[-1:] + temp_cols[13:14] + temp_cols[1:5] + temp_cols[6:8] + temp_cols[9:10] + \
               temp_cols[12:13]
    similar_players_df = similar_players_df[new_cols]

    # sort dataframe by similarity score
    similar_players_df = similar_players_df.sort_values(by='similarity_score', ascending=False)

    # convert similarity scores into percentage
    similar_players_df['similarity_score'] = similar_players_df['similarity_score'].mul(100).round(2).astype(str).\
        add('%')

    # rename dataframe columns
    similar_players_df.columns = SIMILARITY_TABLE_HEADERS

    # create table of similar players
    fig = go.Figure(data=[go.Table(header=dict(values=SIMILARITY_TABLE_HEADERS,
                                               fill_color=DARK_BLUE_HEX,
                                               align='center',
                                               font=dict(color='white', size=12)),
                                   cells=dict(
                                       values=[similar_players_df[header] for header in SIMILARITY_TABLE_HEADERS],
                                       fill_color=LIGHT_BLUE_HEX,
                                       align=['left', 'center', 'center', 'left', 'left', 'left', 'left', 'left',
                                              'left', 'center', 'center'],
                                       font=dict(color='white', size=12)))
                          ])

    # table details
    fig.update_layout(# height=500,
                      # width=1000,
                      title=f'Top {top_n} similar players to {player_details}',
                      template='plotly_dark'
                      )
    fig.layout.title.update(y=0.85)

    # fig.show()

    return fig

def table_similar_players_1(player_details, df, top_n, traits_weights=None, filters=None):

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

    # get list of similar players
    similar_players = list(top_n_dict.keys())

    # create table of similar players
    fig = get_nontraits_table_similar_players(top_n_dict, df, player_details, top_n)

    return fig, similar_players

def table_similar_players_2(player_1_details, player_2_details, df, top_n, player_weights=None, traits_weights=None,
                            filters=None):

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

    # get list of similar players
    similar_players = list(top_n_dict.keys())

    # create table of similar players
    fig = get_nontraits_table_similar_players(top_n_dict, df, combined_player_details, top_n)

    return fig, similar_players

def rating_indicator_1(query_player_details, similar_player_details, df):

    # get query player rating
    query_player_rating = df[df.player_details == query_player_details].rating.tolist()[0]

    # get similar player rating
    similar_player_rating = df[df.player_details == similar_player_details].rating.tolist()[0]

    # create rating indicator cards
    fig = go.Figure()

    # rating of query player
    fig.add_trace(go.Indicator(mode='number',
                               value=query_player_rating,
                               title=dict(font=dict(size=12), text=query_player_details),
                               domain={'row': 0, 'column': 0}))

    # rating of similar player
    fig.add_trace(go.Indicator(mode='number+delta',
                               value=similar_player_rating,
                               delta=dict(reference=query_player_rating),
                               title=dict(font=dict(size=12), text=similar_player_details),
                               domain={'row': 1, 'column': 0}))

    # card details
    fig.update_layout(#height=500,
                      #width=500,
                      title={'text': 'Rating', 'x': 0.5},
                      grid={'rows': 2, 'columns': 1},
                      template='plotly_dark')

    # fig.show()

    return fig

def rating_indicator_2(query_player_1_details, query_player_2_details, similar_player_details, df, player_weights=None):

    if player_weights is not None:
        # assert that player weights sum up to 1
        assert sum(player_weights) == 1, f'Player weights do not sum up to 1'
    else:
        player_weights = [0.5, 0.5]

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
                               title=dict(font=dict(size=12), text=combined_player_details),
                               domain={'row': 0, 'column': 0}))

    # rating of similar player
    fig.add_trace(go.Indicator(mode='number+delta',
                               value=similar_player_rating,
                               delta=dict(reference=combined_player_rating),
                               title=dict(font=dict(size=12), text=similar_player_details),
                               domain={'row': 1, 'column': 0}))

    # card details
    fig.update_layout(#height=500,
                      #width=500,
                      title={'text': 'Rating', 'x': 0.5},
                      grid={'rows': 2, 'columns': 1},
                      template='plotly_dark')

    # fig.show()

    return fig

def traits_radar_chart_1(query_player_details, similar_player_details, df):

    # get values for query player traits
    raw_trait_values_1 = df[df.player_details == query_player_details][RAW_TRAITS].values[0].tolist()
    raw_trait_values_1 += raw_trait_values_1[:1]
    composite_trait_values_1 = df[df.player_details == query_player_details][COMPOSITE_TRAITS].values[0].tolist()
    composite_trait_values_1 += composite_trait_values_1[:1]

    # get values for similar player traits
    raw_trait_values_2 = df[df.player_details == similar_player_details][RAW_TRAITS].values[0].tolist()
    raw_trait_values_2 += raw_trait_values_2[:1]
    composite_trait_values_2 = df[df.player_details == similar_player_details][COMPOSITE_TRAITS].values[0].tolist()
    composite_trait_values_2 += composite_trait_values_2[:1]

    # adjust raw and composite traits lists
    circ_raw_traits = RAW_TRAITS_DISPLAY + RAW_TRAITS_DISPLAY[:1]
    circ_composite_traits = COMPOSITE_TRAITS_DISPLAY + COMPOSITE_TRAITS_DISPLAY[:1]

    # create radar charts
    fig = make_subplots(rows=1,
                        cols=2,
                        horizontal_spacing=0.05,
                        specs=[[{'type': 'polar'}, {'type': 'polar'}]],
                        subplot_titles=('Raw Traits Comparison', 'Composite Traits Comparison'))

    # plot raw traits radar chart
    fig.add_trace(go.Scatterpolar(r=raw_trait_values_1,
                                  theta=circ_raw_traits,
                                  fill='toself',
                                  name=query_player_details,
                                  marker=dict(color=DARK_BLUE_HEX)),
                  row=1,
                  col=1
                  )
    fig.add_trace(go.Scatterpolar(r=raw_trait_values_2,
                                  theta=circ_raw_traits,
                                  fill='toself',
                                  name=similar_player_details,
                                  marker=dict(color=DARK_ORANGE_HEX)),
                  row=1,
                  col=1
                  )

    # plot composite traits radar chart
    fig.add_trace(go.Scatterpolar(r=composite_trait_values_1,
                                  theta=circ_composite_traits,
                                  fill='toself',
                                  name=query_player_details,
                                  marker=dict(color=DARK_BLUE_HEX),
                                  showlegend=False),
                  row=1,
                  col=2
                  )
    fig.add_trace(go.Scatterpolar(r=composite_trait_values_2,
                                  theta=circ_composite_traits,
                                  fill='toself',
                                  name=similar_player_details,
                                  marker=dict(color=DARK_ORANGE_HEX),
                                  showlegend=False),
                  row=1,
                  col=2
                  )

    # plot details
    fig.update_layout(#height=500,
                      #width=1000,
                      polar={'radialaxis': {'visible': True}},
                      showlegend=True,
                      legend=dict(x=0, y=-0.5),
                      template='plotly_dark'
                      )
    # fig.update_polars(radialaxis=dict(range=[0, 10]))
    fig.layout.annotations[0].update(y=1.1)
    fig.layout.annotations[1].update(y=1.1)

    # fig.show()

    return fig

def traits_radar_chart_2(query_player_1_details, query_player_2_details, similar_player_details, df,
                         player_weights=None):

    if player_weights is not None:
        # assert that player weights sum up to 1
        assert sum(player_weights) == 1, f'Player weights do not sum up to 1'
    else:
        player_weights = [0.5, 0.5]

    # get values for query players traits
    raw_trait_values_1 = df[df.player_details == query_player_1_details][RAW_TRAITS].values[0].tolist()
    raw_trait_values_2 = df[df.player_details == query_player_2_details][RAW_TRAITS].values[0].tolist()
    composite_trait_values_1 = df[df.player_details == query_player_1_details][COMPOSITE_TRAITS].values[0].tolist()
    composite_trait_values_2 = df[df.player_details == query_player_2_details][COMPOSITE_TRAITS].values[0].tolist()

    # combine traits for query players traits
    raw_trait_values_combined = np.average(np.array([raw_trait_values_1, raw_trait_values_2]), axis=0,
                                           weights=player_weights).tolist()
    raw_trait_values_combined += raw_trait_values_combined[:1]
    composite_trait_values_combined = np.average(np.array([composite_trait_values_1, composite_trait_values_2]), axis=0,
                                                 weights=player_weights).tolist()
    composite_trait_values_combined += composite_trait_values_combined[:1]

    # get values for similar player traits
    raw_trait_values_3 = df[df.player_details == similar_player_details][RAW_TRAITS].values[0].tolist()
    raw_trait_values_3 += raw_trait_values_3[:1]
    composite_trait_values_3 = df[df.player_details == similar_player_details][COMPOSITE_TRAITS].values[0].tolist()
    composite_trait_values_3 += composite_trait_values_3[:1]

    # combined player details
    combined_player_details = f'{query_player_1_details} ({player_weights[0] * 100:.0f}%) + {query_player_2_details} ' \
                              f'({player_weights[1] * 100:.0f}%)'

    # adjust raw and composite traits lists
    circ_raw_traits = RAW_TRAITS_DISPLAY + RAW_TRAITS_DISPLAY[:1]
    circ_composite_traits = COMPOSITE_TRAITS_DISPLAY + COMPOSITE_TRAITS_DISPLAY[:1]

    # create radar charts
    fig = make_subplots(rows=1,
                        cols=2,
                        horizontal_spacing=0.05,
                        specs=[[{'type': 'polar'}, {'type': 'polar'}]],
                        subplot_titles=('Raw Traits Comparison', 'Composite Traits Comparison'))

    # plot raw traits radar chart
    fig.add_trace(go.Scatterpolar(r=raw_trait_values_combined,
                                  theta=circ_raw_traits,
                                  fill='toself',
                                  name=combined_player_details,
                                  marker=dict(color=DARK_BLUE_HEX)),
                  row=1,
                  col=1
                  )
    fig.add_trace(go.Scatterpolar(r=raw_trait_values_3,
                                  theta=circ_raw_traits,
                                  fill='toself',
                                  name=similar_player_details,
                                  marker=dict(color=DARK_ORANGE_HEX)),
                  row=1,
                  col=1
                  )

    # plot composite traits radar chart
    fig.add_trace(go.Scatterpolar(r=composite_trait_values_combined,
                                  theta=circ_composite_traits,
                                  fill='toself',
                                  name=combined_player_details,
                                  marker=dict(color=DARK_BLUE_HEX),
                                  showlegend=False),
                  row=1,
                  col=2
                  )
    fig.add_trace(go.Scatterpolar(r=composite_trait_values_3,
                                  theta=circ_composite_traits,
                                  fill='toself',
                                  name=similar_player_details,
                                  marker=dict(color=DARK_ORANGE_HEX),
                                  showlegend=False),
                  row=1,
                  col=2
                  )

    # plot details
    fig.update_layout(#height=500,
                      #width=1000,
                      polar={'radialaxis': {'visible': True}},
                      showlegend=True,
                      legend=dict(x=0, y=-0.5),
                      template='plotly_dark'
                      )
    # fig.update_polars(radialaxis=dict(range=[0, 10]))
    fig.layout.annotations[0].update(y=1.1)
    fig.layout.annotations[1].update(y=1.1)

    # fig.show()

    return fig

def difference_bar_chart_1(query_player_details, similar_player_details, df):

    # get values for query player traits
    raw_trait_values_1 = df[df.player_details == query_player_details][RAW_TRAITS].values[0].tolist()
    composite_trait_values_1 = df[df.player_details == query_player_details][COMPOSITE_TRAITS].values[0].tolist()

    # get values for similar player traits
    raw_trait_values_2 = df[df.player_details == similar_player_details][RAW_TRAITS].values[0].tolist()
    composite_trait_values_2 = df[df.player_details == similar_player_details][COMPOSITE_TRAITS].values[0].tolist()

    # get difference in traits values
    raw_traits_diff = [raw_trait_1 - raw_trait_2 for raw_trait_1, raw_trait_2 in zip(raw_trait_values_1,
                                                                                     raw_trait_values_2)]
    composite_traits_diff = [composite_trait_1 - composite_trait_2 for composite_trait_1, composite_trait_2 in
                             zip(composite_trait_values_1, composite_trait_values_2)]

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

    # create traits difference bar charts
    fig = make_subplots(rows=1,
                        cols=2,
                        horizontal_spacing=0.05,
                        specs=[[{'type': 'bar'}, {'type': 'bar'}]],
                        subplot_titles=('Raw Traits Difference', 'Composite Traits Difference'))

    # plot raw traits difference bar chart
    fig.add_trace(go.Bar(x=pos_raw_traits,
                         y=raw_traits_pos_diff,
                         name=f'{query_player_details} > {similar_player_details}',
                         marker=dict(color=DARK_BLUE_HEX)),
                  row=1,
                  col=1
                  )
    fig.add_trace(go.Bar(x=neg_raw_traits,
                         y=raw_traits_neg_diff,
                         name=f'{similar_player_details} > {query_player_details}',
                         marker=dict(color=DARK_ORANGE_HEX)),
                  row=1,
                  col=1
                  )

    # plot composite traits difference bar chart
    fig.add_trace(go.Bar(x=pos_composite_traits,
                         y=composite_traits_pos_diff,
                         marker=dict(color=DARK_BLUE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )
    fig.add_trace(go.Bar(x=neg_composite_traits,
                         y=composite_traits_neg_diff,
                         marker=dict(color=DARK_ORANGE_HEX),
                         showlegend=False),
                  row=1,
                  col=2
                  )

    # plot details
    fig.update_layout(#height=500,
                      #width=1000,
                      showlegend=True,
                      legend=dict(x=0, y=-0.5),
                      template='plotly_dark'
                      )
    fig.update_xaxes(categoryorder='array', categoryarray=RAW_TRAITS, row=1, col=1)
    fig.update_xaxes(categoryorder='array', categoryarray=COMPOSITE_TRAITS, row=1, col=2)
    fig.update_yaxes(range=[-4, 4])
    fig.layout.annotations[0].update(y=1.05)
    fig.layout.annotations[1].update(y=1.05)

    # fig.show()

    return fig

def difference_bar_chart_2(query_player_1_details, query_player_2_details, similar_player_details, df,
                           player_weights=None):

    if player_weights is not None:
        # assert that player weights sum up to 1
        assert sum(player_weights) == 1, f'Player weights do not sum up to 1'
    else:
        player_weights = [0.5, 0.5]

    # get values for query players traits
    raw_trait_values_1 = df[df.player_details == query_player_1_details][RAW_TRAITS].values[0].tolist()
    raw_trait_values_2 = df[df.player_details == query_player_2_details][RAW_TRAITS].values[0].tolist()
    composite_trait_values_1 = df[df.player_details == query_player_1_details][COMPOSITE_TRAITS].values[0].tolist()
    composite_trait_values_2 = df[df.player_details == query_player_2_details][COMPOSITE_TRAITS].values[0].tolist()

    # combine traits for query players traits
    raw_trait_values_combined = np.average(np.array([raw_trait_values_1, raw_trait_values_2]), axis=0,
                                           weights=player_weights).tolist()
    composite_trait_values_combined = np.average(np.array([composite_trait_values_1, composite_trait_values_2]), axis=0,
                                                 weights=player_weights).tolist()

    # get values for similar player traits
    raw_trait_values_3 = df[df.player_details == similar_player_details][RAW_TRAITS].values[0].tolist()
    composite_trait_values_3 = df[df.player_details == similar_player_details][COMPOSITE_TRAITS].values[0].tolist()

    # create traits difference in traits values
    raw_traits_diff = [raw_trait_1 - raw_trait_2 for raw_trait_1, raw_trait_2 in zip(raw_trait_values_combined,
                                                                                     raw_trait_values_3)]
    composite_traits_diff = [composite_trait_1 - composite_trait_2 for composite_trait_1, composite_trait_2 in
                             zip(composite_trait_values_combined, composite_trait_values_3)]

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

    # combined player details
    combined_player_details = f'{query_player_1_details} ({player_weights[0] * 100:.0f}%) + {query_player_2_details} ' \
                              f'({player_weights[1] * 100:.0f}%)'

    # create traits difference bar charts
    fig = make_subplots(rows=1,
                        cols=2,
                        horizontal_spacing=0.05,
                        specs=[[{'type': 'bar'}, {'type': 'bar'}]],
                        subplot_titles=('Raw Traits Difference', 'Composite Traits Difference'))

    # plot raw traits difference bar chart
    fig.add_trace(go.Bar(x=pos_raw_traits,
                         y=raw_traits_pos_diff,
                         name=f'{combined_player_details} > {similar_player_details}',
                         marker=dict(color=DARK_BLUE_HEX)),
                  row=1,
                  col=1
                  )
    fig.add_trace(go.Bar(x=neg_raw_traits,
                         y=raw_traits_neg_diff,
                         name=f'{similar_player_details} > {combined_player_details}',
                         marker=dict(color=DARK_ORANGE_HEX)),
                  row=1,
                  col=1
                  )

    # plot composite traits difference bar chart
    fig.add_trace(go.Bar(x=pos_composite_traits,
                         y=composite_traits_pos_diff,
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
    fig.update_layout(#height=500,
                      #width=1000,
                      showlegend=True,
                      legend=dict(x=0, y=-0.5),
                      template='plotly_dark'
                      )
    fig.update_xaxes(categoryorder='array', categoryarray=RAW_TRAITS, row=1, col=1)
    fig.update_xaxes(categoryorder='array', categoryarray=COMPOSITE_TRAITS, row=1, col=2)
    fig.update_yaxes(range=[-4, 4])
    fig.layout.annotations[0].update(y=1.05)
    fig.layout.annotations[1].update(y=1.05)

    # fig.show()

    return fig