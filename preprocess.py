import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR


conn = sqlite3.connect('E:\CalamariHoops\database\player_stats.db')
cursor = conn.cursor()

'''
This function prepares dataset for training, it simplifies the position of players by 
replacing the position of versatile players with their primary position.
Players whose draft years are null are dropped from the database, These players were signed
to certain teams but never played a minute of basketball in the NBA.
The final data set is returned as a dataframe
'''
def preprocess_pos():
    static_data = pd.read_sql_query("SELECT * FROM players", conn)

    static_data['POSITION'] = static_data['POSITION'].replace(['Guard-Forward'], 'Guard')
    static_data['POSITION'] = static_data['POSITION'].replace(['Forward-Guard'], 'Forward')
    static_data['POSITION'] = static_data['POSITION'].replace(['Center-Forward'], 'Center')
    static_data['POSITION'] = static_data['POSITION'].replace(['Forward-Center'], 'Forward')

    filtered_static = static_data[static_data['DRAFT_YEAR'].notnull()]

    return filtered_static


'''
This function cleans the basic_stats and adv_stats table by dropping the rows without a CAREER_YEAR,
these players were either on a two-way contract or G-league callups.
It also drops stats for player_id 1682 (Reggie Hanson) and player_id 1872 (Randell Jackson) because
their draft/career stats information is inaccurate. 
Both processed tables are returned as dataframes
'''
def preprocess_stats():
    basic_stats = pd.read_sql_query("SELECT * FROM basic_stats", conn)
    adv_stats = pd.read_sql_query("SELECT * FROM adv_stats", conn)

    filtered_basic = basic_stats[basic_stats['CAREER_YEAR'].notnull()]
    filtered_adv = adv_stats[adv_stats['CAREER_YEAR'].notnull()]

    filtered_basic = filtered_basic[filtered_basic['CAREER_YEAR'] != 0]
    filtered_adv = filtered_adv[filtered_adv['CAREER_YEAR'] != 0]

    return filtered_adv, filtered_basic

'''
main method
'''
if __name__ == '__main__':
    static_data = preprocess_pos()
    adv_stats, basic_stats = preprocess_stats()

    #Extracting basic stats for all guards
    guards_static_data = static_data.loc[static_data['POSITION'] == 'Guard']
    guards_mask = basic_stats['PLAYER_ID'].isin(guards_static_data['PERSON_ID'])
    guards_basic_stats = basic_stats[guards_mask]
  
    #Extracting the PTS and CAREER_YEAR, MIN columns from all guards basic stats
    x = guards_basic_stats.loc[:,['CAREER_YEAR','MIN']].values
    y = guards_basic_stats.loc[:, 'PTS'].values

    #Feature scaling
    sc_x = StandardScaler()
    sc_y = StandardScaler()
    x = sc_x.fit_transform(x)
    # y = sc_y.fit_transform(y)

    #Fitting SVR to the dataset
    guard_regressor = SVR(kernel = 'rbf')
    guard_regressor.fit(x,y)
    
    #Predicting a guard at career_year 6, averaging 25 minutes a game
    y_pred = guard_regressor.predict(6, 25)
    y_pred = sc_y.inverse_transform(y_pred)
    print(y_pred) 

    # #Visualizing SVR results
    # x_grid = np.arange(min(x), max(x), 0.01) #this step required because data is feature scaled.
    # x_grid = x_grid.reshape((len(x_grid), 1))
    # plt.scatter(x, y, color = 'red')
    # plt.plot(x_grid, regressor.predict(x_grid), color = 'blue')
    # plt.title('PTS prediction (SVR)')
    # plt.xlabel('Position level')
    # plt.ylabel('Points per game')
    # plt.show()

    conn.close()