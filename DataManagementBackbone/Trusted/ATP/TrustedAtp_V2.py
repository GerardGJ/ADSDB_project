import pandas as pd
import numpy as np
import os
import csv
import datetime
from sqlalchemy import create_engine

def trustedATP_V2():

    SELECT_ATP = "select * from atpdatav1"

    conn_string = 'postgresql://biel.caballero:DB130201@postgresfib.fib.upc.edu:6433/ADSDBbiel.caballero'
    db = create_engine(conn_string)

    with db.connect() as conn:
        ATPdata = pd.read_sql_query(SELECT_ATP, conn)

    x=[ATPdata.pop(x) for x in ['winner_seed','winner_entry','loser_seed','loser_entry']]

    ATPdata['first_set'] = ATPdata.score.str.split(" ",expand=True)[0]
    ATPdata['second_set'] = ATPdata.score.str.split(" ",expand=True)[1]
    ATPdata['third_set'] = ATPdata.score.str.split(" ",expand=True)[2]
    ATPdata['fourth_set'] = ATPdata.score.str.split(" ",expand=True)[3]
    ATPdata['fifth_set'] = ATPdata.score.str.split(" ",expand=True)[4]
    x=[ATPdata.pop(x) for x in ['score']]

    conn = db.connect()
    ATPdata.to_sql('atpdatav2', con=conn, if_exists='replace', index = False)

