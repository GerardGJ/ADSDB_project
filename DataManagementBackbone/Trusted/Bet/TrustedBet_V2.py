import pandas as pd
import numpy as np
import os 
import csv
import datetime
from sqlalchemy import create_engine

def trustedBet_V2():
    SELECT_2020_GAMES = """select * from tennis_datav1"""

    conn_string = 'postgresql://biel.caballero:DB130201@postgresfib.fib.upc.edu:6433/ADSDBbiel.caballero'
    db = create_engine(conn_string)

    with db.connect() as conn:
        tennisv1 = pd.read_sql_query(SELECT_2020_GAMES, conn)

    convert_dict = {'wrank': 'Int64', 'lrank': 'Int64',
                    'wpts' : 'Int64', 'lpts' : 'Int64',
                    'w1'   : 'Int64', 'l1'   : 'Int64',
                    'w2'   : 'Int64', 'l2'   : 'Int64',
                    'w3'   : 'Int64', 'l3'   : 'Int64',
                    'w4'   : 'Int64', 'l4'   : 'Int64',
                    'w5'   : 'Int64', 'l5'   : 'Int64',
                    'wsets': 'Int64', 'lsets': 'Int64',
                    'pl1_weight' : 'Int64', 'pl2_weight' : 'Int64'
                    }
    tennisv1 = tennisv1.astype(convert_dict)

    tennisv1 = tennisv1.replace({np.NaN: None})

    conn = db.connect()
    tennisv1.to_sql('tennis_datav2', con=conn, if_exists='replace', index = False)

