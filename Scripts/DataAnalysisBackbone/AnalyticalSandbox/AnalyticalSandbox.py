import pandas as pd
import os 
import csv
import datetime
from sqlalchemy import create_engine

def analyticalSandbox():
    
    SELECT_ATP = "select * from mergedtables"

    conn_string = 'postgresql://biel.caballero:DB130201@postgresfib.fib.upc.edu:6433/ADSDBbiel.caballero'
    db = create_engine(conn_string)

    with db.connect() as conn:
        merged = pd.read_sql_query(SELECT_ATP, conn)

    merged= merged[merged['minutes'] != '0.0']

    merged = merged.drop(['w_ace','w_df','w_svpt','w_1stIn','w_1stWon','w_2ndWon','w_SvGms','w_bpSaved','w_bpFaced',
                        'l_ace','l_df','l_svpt','l_1stIn','l_1stWon','l_2ndWon','l_SvGms','l_bpSaved','l_bpFaced',
                        'w1','w2','w3','w4','w5','l1','l2','l3','l4','l5','wsets','lsets','comment'],axis = 1)

    conn = db.connect()
    merged.to_sql('analyticalsandbox', con=conn, if_exists='replace', index = False)

