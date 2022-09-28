# Run with `python preprocessing.py` to preprocess csv files into dataframes.

# import packages
import pandas as pd
from datetime import date

# paths for csv files for each position
CB_DATA_PATH = 'Data/data_cb.csv'
FB_DATA_PATH = 'Data/data_fb.csv'
DM_DATA_PATH = 'Data/data_dm.csv'
M_DATA_PATH = 'Data/data_m.csv'
W_DATA_PATH = 'Data/data_w.csv'
CF_DATA_PATH = 'Data/data_cf.csv'

# load dataframes for each position
cb_full_df = pd.read_csv(CB_DATA_PATH)
fb_full_df = pd.read_csv(FB_DATA_PATH)
dm_full_df = pd.read_csv(DM_DATA_PATH)
m_full_df = pd.read_csv(M_DATA_PATH)
w_full_df = pd.read_csv(W_DATA_PATH)
cf_full_df = pd.read_csv(CF_DATA_PATH)

if __name__ == '__main__':
    # drop ord column
    cb_full_df = cb_full_df.drop(columns='Ord')
    fb_full_df = fb_full_df.drop(columns='Ord')
    dm_full_df = dm_full_df.drop(columns='Ord')
    m_full_df = m_full_df.drop(columns='Ord')
    w_full_df = w_full_df.drop(columns='Ord')
    cf_full_df = cf_full_df.drop(columns='Ord')

    # replace spaces with underscores and lowercase column names
    cb_full_df.columns = [col.replace(' ', '_').lower() for col in cb_full_df.columns]
    fb_full_df.columns = [col.replace(' ', '_').lower() for col in fb_full_df.columns]
    dm_full_df.columns = [col.replace(' ', '_').lower() for col in dm_full_df.columns]
    m_full_df.columns = [col.replace(' ', '_').lower() for col in m_full_df.columns]
    w_full_df.columns = [col.replace(' ', '_').lower() for col in w_full_df.columns]
    cf_full_df.columns = [col.replace(' ', '_').lower() for col in cf_full_df.columns]

    # rename `player_name` column to `player_details`
    cb_full_df = cb_full_df.rename(columns={'player_name': 'player_details'})
    fb_full_df = fb_full_df.rename(columns={'player_name': 'player_details'})
    dm_full_df = dm_full_df.rename(columns={'player_name': 'player_details'})
    m_full_df = m_full_df.rename(columns={'player_name': 'player_details'})
    w_full_df = w_full_df.rename(columns={'player_name': 'player_details'})
    cf_full_df = cf_full_df.rename(columns={'player_name': 'player_details'})

    # add a column `player_name`
    cb_player_names = [row.player_details.replace(row.team_id, '').replace(str(row.season), '').strip() for index, row
                       in cb_full_df.iterrows()]
    cb_full_df.insert(1, 'player_name', cb_player_names)
    fb_player_names = [row.player_details.replace(row.team_id, '').replace(str(row.season), '').strip() for index, row
                       in fb_full_df.iterrows()]
    fb_full_df.insert(1, 'player_name', fb_player_names)
    dm_player_names = [row.player_details.replace(row.team_id, '').replace(str(row.season), '').strip() for index, row
                       in dm_full_df.iterrows()]
    dm_full_df.insert(1, 'player_name', dm_player_names)
    m_player_names = [row.player_details.replace(row.team_id, '').replace(str(row.season), '').strip() for index, row in
                      m_full_df.iterrows()]
    m_full_df.insert(1, 'player_name', m_player_names)
    w_player_names = [row.player_details.replace(row.team_id, '').replace(str(row.season), '').strip() for index, row in
                      w_full_df.iterrows()]
    w_full_df.insert(1, 'player_name', w_player_names)
    cf_player_names = [row.player_details.replace(row.team_id, '').replace(str(row.season), '').strip() for index, row
                       in cf_full_df.iterrows()]
    cf_full_df.insert(1, 'player_name', cf_player_names)

    # add a column 'total_mins'
    cb_full_df.insert(10, 'total_mins', cb_full_df.apps * cb_full_df.mins)
    fb_full_df.insert(10, 'total_mins', fb_full_df.apps * fb_full_df.mins)
    dm_full_df.insert(10, 'total_mins', dm_full_df.apps * dm_full_df.mins)
    m_full_df.insert(10, 'total_mins', m_full_df.apps * m_full_df.mins)
    w_full_df.insert(10, 'total_mins', w_full_df.apps * w_full_df.mins)
    cf_full_df.insert(10, 'total_mins', cf_full_df.apps * cf_full_df.mins)

    # add a column 'age'
    cb_full_df.insert(8, 'age', date.today().year - cb_full_df.dob)
    fb_full_df.insert(8, 'age', date.today().year - fb_full_df.dob)
    dm_full_df.insert(8, 'age', date.today().year - dm_full_df.dob)
    m_full_df.insert(8, 'age', date.today().year - m_full_df.dob)
    w_full_df.insert(8, 'age', date.today().year - w_full_df.dob)
    cf_full_df.insert(8, 'age', date.today().year - cf_full_df.dob)

    # add a column 'position'
    cb_full_df.insert(5, 'position', 'CB')
    fb_full_df.insert(5, 'position', 'FB')
    dm_full_df.insert(5, 'position', 'DM')
    m_full_df.insert(5, 'position', 'M')
    w_full_df.insert(5, 'position', 'W')
    cf_full_df.insert(5, 'position', 'CF')

    # convert season from int to str
    cb_full_df.season = cb_full_df.season.map(str)
    fb_full_df.season = fb_full_df.season.map(str)
    dm_full_df.season = dm_full_df.season.map(str)
    m_full_df.season = m_full_df.season.map(str)
    w_full_df.season = w_full_df.season.map(str)
    cf_full_df.season = cf_full_df.season.map(str)

    # create a full dataframe for all positions
    all_dfs = [cb_full_df, fb_full_df, dm_full_df, m_full_df, w_full_df, cf_full_df]
    all_df = pd.concat(all_dfs)

    # aggregate full df
    SEASONS = ['2019', '2020', '2021']
    agg_all_df = pd.DataFrame(
        {'player_details': [], 'player_name': [], 'season': [], 'league': [], 'team': [], 'position': [],
         'primary_position': [], 'nationality': [], 'dob': [], 'age': [],
         'apps': [], 'mins': [], 'total_mins': [], 'rating': [], 'scoring': [], 'creating': [], 'passing': [],
         'defending': [], 'goals': [], 'shots': [], 'conversion': [],
         'positioning': [], 'assists': [], 'crossing': [], 'dribbling': [], 'carries': [], 'involvement': [],
         'accuracy': [], 'intent': [], 'receiving': [], 'aerial': [],
         'on_ball': [], 'off_ball': [], 'fouls': []})
    unique_ids = ['player_name', 'position', 'primary_position', 'nationality', 'dob', 'age']
    uniques = []

    for index, row in all_df[unique_ids].iterrows():
        # iterate through unique players
        if row[unique_ids].tolist() not in uniques:
            uniques.append(row[unique_ids].tolist())

            player_name = row.player_name
            position = row.position
            primary_position = row.primary_position
            nationality = row.nationality
            dob = row.dob
            age = row.age

            player_df = all_df[(all_df.player_name == player_name) &
                                (all_df.position == position) &
                                (all_df.primary_position == primary_position) &
                                (all_df.nationality == nationality) &
                                (all_df.dob == dob) &
                                (all_df.age == age)]

            # dict with all aggregated values for 2019, 2020, 2021, 2020-2021, 2019-2021, if present
            seasons_combined_dict = {'player_details': [],  #
                                     'player_name': [],  #
                                     'season': [],
                                     'league': [],  #
                                     'team': [],  #
                                     'position': [],  #
                                     'primary_position': [],  #
                                     'nationality': [],  #
                                     'dob': [],  #
                                     'age': [],  #
                                     'apps': [],  #
                                     'mins': [],  #
                                     'total_mins': [],  #
                                     'rating': [],  #
                                     'scoring': [],  #
                                     'creating': [],  #
                                     'passing': [],  #
                                     'defending': [],  #
                                     'goals': [],  #
                                     'shots': [],  #
                                     'conversion': [],  #
                                     'positioning': [],  #
                                     'assists': [],  #
                                     'crossing': [],  #
                                     'dribbling': [],  #
                                     'carries': [],  #
                                     'involvement': [],  #
                                     'accuracy': [],  #
                                     'intent': [],  #
                                     'receiving': [],  #
                                     'aerial': [],  #
                                     'on_ball': [],  #
                                     'off_ball': [],  #
                                     'fouls': [],  #
                                     }

            # indexed to 2019, 2020, 2021
            has_seasons = [False, False, False]
            for index, season in enumerate(SEASONS):
                season_df = player_df[player_df.season == season]
                if len(season_df) > 0:
                    has_seasons[index] = True
                else:
                    continue

                # compute aggregated values
                team_id = season_df.team_id.tolist()[0]
                player_details = player_name + ' ' + team_id + ' ' + season
                league = season_df.league.tolist()[0]
                apps = sum(season_df.apps.tolist())
                mins = sum(season_df.mins.tolist())
                total_mins = sum(season_df.total_mins.tolist())
                rating = sum(season_df.rating.tolist()) / len(season_df.rating.tolist())
                scoring = sum(season_df.scoring.tolist()) / len(season_df.scoring.tolist())
                creating = sum(season_df.creating.tolist()) / len(season_df.creating.tolist())
                passing = sum(season_df.passing.tolist()) / len(season_df.passing.tolist())
                defending = sum(season_df.defending.tolist()) / len(season_df.defending.tolist())
                goals = sum(season_df.goals.tolist()) / len(season_df.goals.tolist())
                shots = sum(season_df.shots.tolist()) / len(season_df.shots.tolist())
                conversion = sum(season_df.conversion.tolist()) / len(season_df.conversion.tolist())
                positioning = sum(season_df.positioning.tolist()) / len(season_df.positioning.tolist())
                assists = sum(season_df.assists.tolist()) / len(season_df.assists.tolist())
                crossing = sum(season_df.crossing.tolist()) / len(season_df.crossing.tolist())
                dribbling = sum(season_df.dribbling.tolist()) / len(season_df.dribbling.tolist())
                carries = sum(season_df.carries.tolist()) / len(season_df.carries.tolist())
                involvement = sum(season_df.involvement.tolist()) / len(season_df.involvement.tolist())
                accuracy = sum(season_df.accuracy.tolist()) / len(season_df.accuracy.tolist())
                intent = sum(season_df.intent.tolist()) / len(season_df.intent.tolist())
                receiving = sum(season_df.receiving.tolist()) / len(season_df.receiving.tolist())
                aerial = sum(season_df.aerial.tolist()) / len(season_df.aerial.tolist())
                on_ball = sum(season_df.on_ball.tolist()) / len(season_df.on_ball.tolist())
                off_ball = sum(season_df.off_ball.tolist()) / len(season_df.off_ball.tolist())
                fouls = sum(season_df.fouls.tolist()) / len(season_df.fouls.tolist())

                # add aggregated values to dictionary
                seasons_combined_dict['player_details'].append(player_details)
                seasons_combined_dict['player_name'].append(player_name)
                seasons_combined_dict['season'].append(season)
                seasons_combined_dict['league'].append(league)
                seasons_combined_dict['team'].append(team_id)
                seasons_combined_dict['position'].append(position)
                seasons_combined_dict['primary_position'].append(primary_position)
                seasons_combined_dict['nationality'].append(nationality)
                seasons_combined_dict['dob'].append(dob)
                seasons_combined_dict['age'].append(age)
                seasons_combined_dict['apps'].append(apps)
                seasons_combined_dict['mins'].append(mins)
                seasons_combined_dict['total_mins'].append(total_mins)
                seasons_combined_dict['rating'].append(rating)
                seasons_combined_dict['scoring'].append(scoring)
                seasons_combined_dict['creating'].append(creating)
                seasons_combined_dict['passing'].append(passing)
                seasons_combined_dict['defending'].append(defending)
                seasons_combined_dict['goals'].append(goals)
                seasons_combined_dict['shots'].append(shots)
                seasons_combined_dict['conversion'].append(conversion)
                seasons_combined_dict['positioning'].append(positioning)
                seasons_combined_dict['assists'].append(assists)
                seasons_combined_dict['crossing'].append(crossing)
                seasons_combined_dict['dribbling'].append(dribbling)
                seasons_combined_dict['carries'].append(carries)
                seasons_combined_dict['involvement'].append(involvement)
                seasons_combined_dict['accuracy'].append(accuracy)
                seasons_combined_dict['intent'].append(intent)
                seasons_combined_dict['receiving'].append(receiving)
                seasons_combined_dict['aerial'].append(aerial)
                seasons_combined_dict['on_ball'].append(on_ball)
                seasons_combined_dict['off_ball'].append(off_ball)
                seasons_combined_dict['fouls'].append(fouls)

            # for 2020-2021
            if all(has_seasons[1:]):
                season = '2020-2021'
                player_details = player_name + ' ' + seasons_combined_dict['team'][-1] + ' ' + season
                league = seasons_combined_dict['league'][-1]
                team_id = seasons_combined_dict['team'][-1]
                apps = sum(seasons_combined_dict['apps'][-2:]) / 2
                mins = sum(seasons_combined_dict['mins'][-2:]) / 2
                total_mins = sum(seasons_combined_dict['total_mins'][-2:]) / 2
                # weighted 2 for 2021 and 1 for 2020 for traits
                rating = (2 * seasons_combined_dict['rating'][-1] + seasons_combined_dict['rating'][-2]) / 3
                scoring = (2 * seasons_combined_dict['scoring'][-1] + seasons_combined_dict['scoring'][-2]) / 3
                creating = (2 * seasons_combined_dict['creating'][-1] + seasons_combined_dict['creating'][-2]) / 3
                passing = (2 * seasons_combined_dict['passing'][-1] + seasons_combined_dict['passing'][-2]) / 3
                defending = (2 * seasons_combined_dict['defending'][-1] + seasons_combined_dict['defending'][-2]) / 3
                goals = (2 * seasons_combined_dict['goals'][-1] + seasons_combined_dict['goals'][-2]) / 3
                shots = (2 * seasons_combined_dict['shots'][-1] + seasons_combined_dict['shots'][-2]) / 3
                conversion = (2 * seasons_combined_dict['conversion'][-1] + seasons_combined_dict['conversion'][-2]) / 3
                positioning = (2 * seasons_combined_dict['positioning'][-1] + seasons_combined_dict['positioning'][
                    -2]) / 3
                assists = (2 * seasons_combined_dict['assists'][-1] + seasons_combined_dict['assists'][-2]) / 3
                crossing = (2 * seasons_combined_dict['crossing'][-1] + seasons_combined_dict['crossing'][-2]) / 3
                dribbling = (2 * seasons_combined_dict['dribbling'][-1] + seasons_combined_dict['dribbling'][-2]) / 3
                carries = (2 * seasons_combined_dict['carries'][-1] + seasons_combined_dict['carries'][-2]) / 3
                involvement = (2 * seasons_combined_dict['involvement'][-1] + seasons_combined_dict['involvement'][
                    -2]) / 3
                accuracy = (2 * seasons_combined_dict['accuracy'][-1] + seasons_combined_dict['accuracy'][-2]) / 3
                intent = (2 * seasons_combined_dict['intent'][-1] + seasons_combined_dict['intent'][-2]) / 3
                receiving = (2 * seasons_combined_dict['receiving'][-1] + seasons_combined_dict['receiving'][-2]) / 3
                aerial = (2 * seasons_combined_dict['aerial'][-1] + seasons_combined_dict['aerial'][-2]) / 3
                on_ball = (2 * seasons_combined_dict['on_ball'][-1] + seasons_combined_dict['on_ball'][-2]) / 3
                off_ball = (2 * seasons_combined_dict['off_ball'][-1] + seasons_combined_dict['off_ball'][-2]) / 3
                fouls = (2 * seasons_combined_dict['fouls'][-1] + seasons_combined_dict['fouls'][-2]) / 3

                # add aggregated values to dictionary
                seasons_combined_dict['player_details'].append(player_details)
                seasons_combined_dict['player_name'].append(player_name)
                seasons_combined_dict['season'].append(season)
                seasons_combined_dict['league'].append(league)
                seasons_combined_dict['team'].append(team_id)
                seasons_combined_dict['position'].append(position)
                seasons_combined_dict['primary_position'].append(primary_position)
                seasons_combined_dict['nationality'].append(nationality)
                seasons_combined_dict['dob'].append(dob)
                seasons_combined_dict['age'].append(age)
                seasons_combined_dict['apps'].append(apps)
                seasons_combined_dict['mins'].append(mins)
                seasons_combined_dict['total_mins'].append(total_mins)
                seasons_combined_dict['rating'].append(rating)
                seasons_combined_dict['scoring'].append(scoring)
                seasons_combined_dict['creating'].append(creating)
                seasons_combined_dict['passing'].append(passing)
                seasons_combined_dict['defending'].append(defending)
                seasons_combined_dict['goals'].append(goals)
                seasons_combined_dict['shots'].append(shots)
                seasons_combined_dict['conversion'].append(conversion)
                seasons_combined_dict['positioning'].append(positioning)
                seasons_combined_dict['assists'].append(assists)
                seasons_combined_dict['crossing'].append(crossing)
                seasons_combined_dict['dribbling'].append(dribbling)
                seasons_combined_dict['carries'].append(carries)
                seasons_combined_dict['involvement'].append(involvement)
                seasons_combined_dict['accuracy'].append(accuracy)
                seasons_combined_dict['intent'].append(intent)
                seasons_combined_dict['receiving'].append(receiving)
                seasons_combined_dict['aerial'].append(aerial)
                seasons_combined_dict['on_ball'].append(on_ball)
                seasons_combined_dict['off_ball'].append(off_ball)
                seasons_combined_dict['fouls'].append(fouls)

            # for 2019-2021
            if all(has_seasons):
                season = '2019-2021'
                player_details = player_name + ' ' + seasons_combined_dict['team'][-1] + ' ' + season
                league = seasons_combined_dict['league'][-1]
                team_id = seasons_combined_dict['team'][-1]
                apps = sum(seasons_combined_dict['apps'][:3]) / 3
                mins = sum(seasons_combined_dict['mins'][:3]) / 3
                total_mins = sum(seasons_combined_dict['total_mins'][:3]) / 3
                # weighted 3 for 2021, 2 for 2020 and 1 for 2019 for traits
                rating = (3 * seasons_combined_dict['rating'][2] + 2 * seasons_combined_dict['rating'][1] +
                          seasons_combined_dict['rating'][0]) / 6
                scoring = (3 * seasons_combined_dict['scoring'][2] + 2 * seasons_combined_dict['scoring'][1] +
                           seasons_combined_dict['scoring'][0]) / 6
                creating = (3 * seasons_combined_dict['creating'][2] + 2 * seasons_combined_dict['creating'][1] +
                            seasons_combined_dict['creating'][0]) / 6
                passing = (3 * seasons_combined_dict['passing'][2] + 2 * seasons_combined_dict['passing'][1] +
                           seasons_combined_dict['passing'][0]) / 6
                defending = (3 * seasons_combined_dict['defending'][2] + 2 * seasons_combined_dict['defending'][1] +
                             seasons_combined_dict['defending'][0]) / 6
                goals = (3 * seasons_combined_dict['goals'][2] + 2 * seasons_combined_dict['goals'][1] +
                         seasons_combined_dict['goals'][0]) / 6
                shots = (3 * seasons_combined_dict['shots'][2] + 2 * seasons_combined_dict['shots'][1] +
                         seasons_combined_dict['shots'][0]) / 6
                conversion = (3 * seasons_combined_dict['conversion'][2] + 2 * seasons_combined_dict['conversion'][1] +
                              seasons_combined_dict['conversion'][0]) / 6
                positioning = (3 * seasons_combined_dict['positioning'][2] + 2 * seasons_combined_dict['positioning'][
                    1] + seasons_combined_dict['positioning'][0]) / 6
                assists = (3 * seasons_combined_dict['assists'][2] + 2 * seasons_combined_dict['assists'][1] +
                           seasons_combined_dict['assists'][0]) / 6
                crossing = (3 * seasons_combined_dict['crossing'][2] + 2 * seasons_combined_dict['crossing'][1] +
                            seasons_combined_dict['crossing'][0]) / 6
                dribbling = (3 * seasons_combined_dict['dribbling'][2] + 2 * seasons_combined_dict['dribbling'][1] +
                             seasons_combined_dict['dribbling'][0]) / 6
                carries = (3 * seasons_combined_dict['carries'][2] + 2 * seasons_combined_dict['carries'][1] +
                           seasons_combined_dict['carries'][0]) / 6
                involvement = (3 * seasons_combined_dict['involvement'][2] + 2 * seasons_combined_dict['involvement'][
                    1] + seasons_combined_dict['involvement'][0]) / 6
                accuracy = (3 * seasons_combined_dict['accuracy'][2] + 2 * seasons_combined_dict['accuracy'][1] +
                            seasons_combined_dict['accuracy'][0]) / 6
                intent = (3 * seasons_combined_dict['intent'][2] + 2 * seasons_combined_dict['intent'][1] +
                          seasons_combined_dict['intent'][0]) / 6
                receiving = (3 * seasons_combined_dict['receiving'][2] + 2 * seasons_combined_dict['receiving'][1] +
                             seasons_combined_dict['receiving'][0]) / 6
                aerial = (3 * seasons_combined_dict['aerial'][2] + 2 * seasons_combined_dict['aerial'][1] +
                          seasons_combined_dict['aerial'][0]) / 6
                on_ball = (3 * seasons_combined_dict['on_ball'][2] + 2 * seasons_combined_dict['on_ball'][1] +
                           seasons_combined_dict['on_ball'][0]) / 6
                off_ball = (3 * seasons_combined_dict['off_ball'][2] + 2 * seasons_combined_dict['off_ball'][1] +
                            seasons_combined_dict['off_ball'][0]) / 6
                fouls = (3 * seasons_combined_dict['fouls'][2] + 2 * seasons_combined_dict['fouls'][1] +
                         seasons_combined_dict['fouls'][0]) / 6

                # add aggregated values to dictionary
                seasons_combined_dict['player_details'].append(player_details)
                seasons_combined_dict['player_name'].append(player_name)
                seasons_combined_dict['season'].append(season)
                seasons_combined_dict['league'].append(league)
                seasons_combined_dict['team'].append(team_id)
                seasons_combined_dict['position'].append(position)
                seasons_combined_dict['primary_position'].append(primary_position)
                seasons_combined_dict['nationality'].append(nationality)
                seasons_combined_dict['dob'].append(dob)
                seasons_combined_dict['age'].append(age)
                seasons_combined_dict['apps'].append(apps)
                seasons_combined_dict['mins'].append(mins)
                seasons_combined_dict['total_mins'].append(total_mins)
                seasons_combined_dict['rating'].append(rating)
                seasons_combined_dict['scoring'].append(scoring)
                seasons_combined_dict['creating'].append(creating)
                seasons_combined_dict['passing'].append(passing)
                seasons_combined_dict['defending'].append(defending)
                seasons_combined_dict['goals'].append(goals)
                seasons_combined_dict['shots'].append(shots)
                seasons_combined_dict['conversion'].append(conversion)
                seasons_combined_dict['positioning'].append(positioning)
                seasons_combined_dict['assists'].append(assists)
                seasons_combined_dict['crossing'].append(crossing)
                seasons_combined_dict['dribbling'].append(dribbling)
                seasons_combined_dict['carries'].append(carries)
                seasons_combined_dict['involvement'].append(involvement)
                seasons_combined_dict['accuracy'].append(accuracy)
                seasons_combined_dict['intent'].append(intent)
                seasons_combined_dict['receiving'].append(receiving)
                seasons_combined_dict['aerial'].append(aerial)
                seasons_combined_dict['on_ball'].append(on_ball)
                seasons_combined_dict['off_ball'].append(off_ball)
                seasons_combined_dict['fouls'].append(fouls)

            # add to new_df
            seasons_combined_df = pd.DataFrame(seasons_combined_dict)
            agg_all_df = pd.concat([agg_all_df, seasons_combined_df], ignore_index=True)
            agg_full_df = agg_all_df.reset_index()

    # save dataframes as csv files
    # cb_full_df.to_csv('Data/df_cb.csv')
    # fb_full_df.to_csv('Data/df_fb.csv')
    # dm_full_df.to_csv('Data/df_dm.csv')
    # m_full_df.to_csv('Data/df_m.csv')
    # w_full_df.to_csv('Data/df_w.csv')
    # cf_full_df.to_csv('Data/df_cf.csv')
    # all_df.to_csv('Data/df_all.csv')
    agg_all_df.to_csv('Data/df_agg_all.csv')