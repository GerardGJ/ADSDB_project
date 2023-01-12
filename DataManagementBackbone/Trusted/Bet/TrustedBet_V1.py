import pandas as pd
import numpy as np
import psycopg2.extras as extras
import os
import csv
import datetime
from sqlalchemy import create_engine

def trustedBet_V1():
    SELECT_2020_GAMES = """select * from tennis_data td where td."Date" >= '01-01-2020' and td."Date" <= '12-31-2020'"""

    conn_string = 'postgresql://biel.caballero:DB130201@postgresfib.fib.upc.edu:6433/ADSDBbiel.caballero'
    db = create_engine(conn_string)

    with db.connect() as conn:
        tennis2020 = pd.read_sql_query(SELECT_2020_GAMES, conn)

    columns_delete = tennis2020.columns[[36,37,38,39,40,41,42,43,44,45,47,48,49,50,52,53]]

    tennis2020_small = tennis2020.drop(columns_delete, axis=1) 

    columnNames = {'ATP':'atp', 'Location':'location', 'Tournament':'tournament','Date':'date','Series':'series','Court':'court',
                'Surface':'Surface','Round':'round','Best_of':'best_of', 'Winner':'winner', 'Loser':'loser','WRank' :'wrank',
                'LRank':'lrank', 'WPts':'wpts', 'LPts':'lpts', 'W1':'w1', 'L1':'l1', 'W2':'w2', 'L2':'l2', 'W3':'w3','L3':'l3',
                'W4':'w4', 'L4':'l4', 'W5':'w5', 'L5':'l5', 'Wsets':'wsets', 'Lsets':'lsets','Comment':'comment','B365W':'b365w',
                'B365L':'b365l', 'PSW':'psw', 'PSL':'psl','MaxW':'maxw', 'MaxL':'maxl','AvgW':'avgw','AvgL':'avgl'}
    tennis2020_small=tennis2020_small.rename(columns = columnNames) 

    rowsToDrop = tennis2020_small.index[(tennis2020_small['pl1_weight'] == 7) | (tennis2020_small['pl2_weight'] == 7)].tolist()
    tennis2020_small.drop(rowsToDrop,axis = 0,inplace=True)

    conn = db.connect()
    tennis2020_small.to_sql('tennis_datav1', con=conn, if_exists='replace', index = False)

