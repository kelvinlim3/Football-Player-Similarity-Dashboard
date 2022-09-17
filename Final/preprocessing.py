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

    # create a full dataframe for all positions
    all_dfs = [cb_full_df, fb_full_df, dm_full_df, m_full_df, w_full_df, cf_full_df]
    all_df = pd.concat(all_dfs)

    # save dataframes as csv files
    cb_full_df.to_csv('Data/df_cb.csv')
    fb_full_df.to_csv('Data/df_fb.csv')
    dm_full_df.to_csv('Data/df_dm.csv')
    m_full_df.to_csv('Data/df_m.csv')
    w_full_df.to_csv('Data/df_w.csv')
    cf_full_df.to_csv('Data/df_cf.csv')
    all_df.to_csv('Data/df_all.csv')