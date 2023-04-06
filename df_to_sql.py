import pandas as pd
import sqlite3
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import playerestimatedmetrics
from nba_api.stats.endpoints import commonplayerinfo
import time

conn = sqlite3.connect('E:\CalamariHoops\database\player_stats.db')
cursor = conn.cursor()


'''
Filter the desired columns from static team information, then insert into local sqlite database
'''
def load_team_info():
    all_teams = teams.get_teams()
    req_keys = ['id', 'full_name', 'abbreviation', 'city']
    all_teams = [{k:v for k, v in i.items() if k in req_keys} for i in all_teams]

    for i in range(0,30):
        cursor.execute("INSERT INTO teams VALUES(:id, :full_name, :abbreviation, :city)", all_teams[i])
        conn.commit()


'''
Access all player basic statistics from the leaguedashplayerstats endpoint from 1996-97 to the current season. 
Desired columns are filtered. Data in the df is inserted into local sqlite database
'''
def load_basic_stats():
    seasons = ["1996-97", "1997-98", "1998-99", 
               "1999-00", "2000-01", "2001-02", "2002-03", "2003-04", "2004-05", "2005-06", "2006-07", "2007-08", 
               "2008-09", "2009-10", "2010-11", "2011-12", "2012-13", "2013-14", "2014-15", "2015-16", "2016-17",
               "2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23"]
    c_bas_full = pd.DataFrame(columns=['PLAYER_ID', 'PTS', 'FG_PCT', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'MIN', 'PLUS_MINUS', 'SEASON'])
    
    for s in seasons:
        c_bas = leaguedashplayerstats.LeagueDashPlayerStats(rank='N', measure_type_detailed_defense='Base', season=s, per_mode_detailed='PerGame')
        c_bas_df = c_bas.get_data_frames()[0]
        c_bas_df = c_bas_df[['PLAYER_ID', 'PTS', 'FG_PCT', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'MIN', 'PLUS_MINUS']]
        c_bas_df['SEASON'] = s
        frames = [c_bas_full, c_bas_df]
        c_bas_full = pd.concat(frames)
        time.sleep(2)
    c_bas_full.to_sql('basic_stats', conn, if_exists='replace')


'''
Access all player advanced statistics from the playerestimatedmetrics endpoint from 1996-97 to the current season. 
Desired columns are filtered. Data in the df is inserted into local sqlite database
'''
def load_adv_stats():
    seasons = ["1996-97", "1997-98", "1998-99", 
               "1999-00", "2000-01", "2001-02", "2002-03", "2003-04", "2004-05", "2005-06", "2006-07", "2007-08", 
               "2008-09", "2009-10", "2010-11", "2011-12", "2012-13", "2013-14", "2014-15", "2015-16", "2016-17",
               "2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23"]
    c_adv_full = pd.DataFrame(columns=['PLAYER_ID', 'E_OFF_RATING', 'E_DEF_RATING', 'E_NET_RATING', 'E_AST_RATIO', 'E_REB_PCT', 'E_USG_PCT', 'E_PACE', 'SEASON'])
    
    for s in seasons:
        c_adv = playerestimatedmetrics.PlayerEstimatedMetrics(league_id='00', season=s)
        c_adv_df = c_adv.get_data_frames()[0]
        c_adv_df = c_adv_df[['PLAYER_ID', 'E_OFF_RATING', 'E_DEF_RATING', 'E_NET_RATING', 'E_AST_RATIO', 'E_REB_PCT', 'E_USG_PCT', 'E_PACE']]
        c_adv_df['SEASON'] = s
        frames = [c_adv_full, c_adv_df]
        c_adv_full = pd.concat(frames)
        time.sleep(2)
    c_adv_full.to_sql('adv_stats', conn, if_exists='replace')


'''
Filter the desired columns from static player information using players endpoint to
access all the player IDs
*Need to add a try/except in case of error
There are ids from the players endpoint that does not exist in commonplayerinfo endpoint
those players are returned as a list
'''
def load_static_player_info():
    nba_players = players.get_players()
    res = [d.get('id', None) for d in nba_players]
    static_info = pd.DataFrame()
    missing_data = []

    for i in res:
        try:
            c_info = commonplayerinfo.CommonPlayerInfo(player_id=i)
        except ValueError:
            missing_data.append(players.find_player_by_id(i))
            continue
        static_info_temp = c_info.get_data_frames()[0]
        time.sleep(0.5)
        frames = [static_info_temp, static_info]
        static_info = pd.concat(frames)

    static_info = static_info[['PERSON_ID', 'DISPLAY_FIRST_LAST', 'HEIGHT', 'WEIGHT', 'POSITION', 'TEAM_ID', 'DRAFT_YEAR', 'DRAFT_NUMBER']]
    static_info.to_sql('players', conn, if_exists='replace')
    return missing_data


'''
Main method
'''
if __name__ == '__main__':
    print()
#    missing_data = load_static_player_info()
#    print(missing_data)
#    load_adv_stats()
#    load_basic_stats()
#    load_team_info()
    conn.close()