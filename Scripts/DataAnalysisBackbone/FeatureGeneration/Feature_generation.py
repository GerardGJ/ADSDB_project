import pandas as pd
import numpy as np
import os 
import csv
import datetime
from sqlalchemy import create_engine

def fetaure_generation():
    SELECT_ATP = """select * from analyticalsandbox n order by n."date" """

    conn_string = 'postgresql://biel.caballero:DB130201@postgresfib.fib.upc.edu:6433/ADSDBbiel.caballero'
    db = create_engine(conn_string)

    with db.connect() as conn:
        new_merged = pd.read_sql_query(SELECT_ATP, conn)

    new_merged.info()


    # ## BMI calculation

    new_merged[["pl1_weight", "pl2_weight","winner_ht","loser_ht","winner_age","loser_age","winner_rank_points","loser_rank_points"]] = new_merged[["pl1_weight", "pl2_weight","winner_ht","loser_ht","winner_age","loser_age","winner_rank_points","loser_rank_points"]].apply(pd.to_numeric)
    new_merged['winner_bmi']=new_merged['pl1_weight']/(new_merged['winner_ht']/100)**2
    new_merged['loser_bmi']=new_merged['pl2_weight']/(new_merged['loser_ht']/100)**2


    # ## Differences between players

    # Secondly we will calculate the differences for physical traits for each pair of players (players involved in each match)

    new_merged['diff_rank_points']= new_merged['winner_rank_points'] - new_merged['loser_rank_points']


    #Height difference:
    new_merged['diff_height']=new_merged['winner_ht']-new_merged['loser_ht']

    #Weight difference:
    new_merged['diff_weight']=new_merged['pl1_weight']-new_merged['pl2_weight']

    #Age difference:
    new_merged['diff_age']=new_merged['winner_age']-new_merged['loser_age']

    #BMI difference:
    new_merged['diff_bmi']=new_merged['winner_bmi']-new_merged['loser_bmi']

    # ## Player's streak
    # Next we will calculate the winning streaks and loosing streaks of the players, as this are statistics that could be important when calculating the odds of a player winning

    losingStreak = dict.fromkeys(tuple(new_merged['loser_id']),0)
    winningStreak = dict.fromkeys(tuple(new_merged['winner_id']),0)
    losingList = []
    winningList = []
    for index,row in new_merged.iterrows():
        winner = row['winner_id']
        loser = row['loser_id']
        
        #Winner:
        winningList.append(winningStreak[winner])
        winningStreak[winner] += 1
        losingStreak[winner] = 0
        
        #Loser
        losingList.append(losingStreak[loser])
        losingStreak[loser] += 1
        winningStreak[loser] = 0

    new_merged['winningstreak'] = winningList
    new_merged['losingstreak'] = losingList

    conn = db.connect()
    new_merged.to_sql('final_table', con=conn, if_exists='replace', index = False)

