import pandas as pd
import numpy as np
import os
import datetime
import csv
from sqlalchemy import create_engine

def formated():
    
    conn_string = 'postgresql://biel.caballero:DB130201@postgresfib.fib.upc.edu:6433/ADSDBbiel.caballero'
    db = create_engine(conn_string)
    conn = db.connect()
    
    dataATP_path = os.getcwd()[0:-7] + "Landing_Zone\\Persistent_Landing\\ATPdata.csv"
    dataATP = pd.read_csv(dataATP_path)
    dataATP.to_sql('atpdata', con=conn, if_exists='replace', index = False)

    tennis_data_path = os.getcwd()[0:-7] + "Landing_Zone\\Persistent_Landing\\tennis_data.csv"
    tennis_data = pd.read_csv(tennis_data_path, sep = ";")
    tennis_data.to_sql('tennis_data', con=conn, if_exists='replace', index = False)  

