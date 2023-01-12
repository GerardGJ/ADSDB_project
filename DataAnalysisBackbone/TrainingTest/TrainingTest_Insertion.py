import pandas as pd
import numpy as np
import os 
import csv
import datetime
from sqlalchemy import create_engine

def trainingValidation():
    SELECT_ATP = "select * from final_table"

    conn_string = 'postgresql://biel.caballero:DB130201@postgresfib.fib.upc.edu:6433/ADSDBbiel.caballero'
    db = create_engine(conn_string)

    with db.connect() as conn:
        merged = pd.read_sql_query(SELECT_ATP, conn)

    train = merged.sample(frac=0.8,random_state=0)
    test = merged.drop(train.index)

    conn = db.connect()
    train.to_sql('trainingtable', con=conn, if_exists='replace', index = False)
    test.to_sql('testingtable', con=conn, if_exists='replace', index = False)

