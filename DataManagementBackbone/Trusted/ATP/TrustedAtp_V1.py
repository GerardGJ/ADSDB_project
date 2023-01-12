import pandas as pd
import numpy as np
import os
import csv
import datetime
from sqlalchemy import create_engine


def trustedAtp_V1():
    SELECT_ATP = "select * from atpdata"

    conn_string = 'postgresql://biel.caballero:DB130201@postgresfib.fib.upc.edu:6433/ADSDBbiel.caballero'
    db = create_engine(conn_string)

    with db.connect() as conn:
        ATPdata = pd.read_sql_query(SELECT_ATP, conn)

    conversionDic = {"tourney_id":"string", "tourney_name":"string", "surface":"string", "tourney_level":"string", "winner_name":"string", 
                    "winner_hand":"category", "winner_ioc":"category", "loser_name":"string", "loser_hand":"category", "loser_ioc":"category", 
                    "round":"category", "tourney_level":"category", "surface":"category", "best_of":"category"}
    ATPdata=ATPdata.astype(conversionDic)

    conn = db.connect()
    ATPdata.to_sql('atpdatav1', con=conn, if_exists='replace', index = False)

