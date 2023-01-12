import psycopg2
import pandas as pd
import psycopg2.extras as extras
import numpy as np
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

def execute_values(conn, df, table):
  
    tuples = [tuple(x) for x in df.to_numpy()]
  
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()

def insertTennisData(records):
    try:
        connection = psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5)
        cursor = connection.cursor()
        postgres_insert_query = " INSERT INTO tennis_data (ATP, Location, Tournament, Date, Series, Court, Surface, Round, Best_of, Winner, Loser, WRank, LRank, WPts, LPts, W1, L1, W2, L2, W3, L3, W4, L4, W5, L5, Wsets, Lsets, Comment, B365W, B365L, PSW, PSL, MaxW, MaxL, AvgW, AvgL, EXW, EXL, LBW, LBL, SJW, SJL, UBW, UBL, pl1_flag, pl1_year_pro, pl1_weight, pl1_height, pl1_hand, pl2_flag, pl2_year_pro, pl2_weight, pl2_height, pl2_hand) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        result = cursor.executemany(postgres_insert_query, records)
        connection.commit()
        print(cursor.rowcount, "Record inserted succesfully into tennis_data table")
    
    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into tennis_data table {}".format(error))

    finally:
        # closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def formated():
    conn = psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5)
    #Insetion of the ATP data
    dataATP = pd.read_csv("/Users/Gerard/Downloads/ATPdata.csv")
    dataATP = dataATP.replace({np.NaN: None})
    execute_values(conn,dataATP,"atpdata")

    #Insertion of the Bet data
    dataTennis = pd.read_csv("/Users/Gerard/Downloads/tennis_data.csv")
    dataTennis = dataTennis.replace({np.NaN: None})
    tupleTennis = list(dataTennis.to_records(index=False))
    insertTennisData(tupleTennis)
