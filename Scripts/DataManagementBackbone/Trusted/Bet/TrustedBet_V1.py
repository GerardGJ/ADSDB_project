import psycopg2
import pandas as pd
import numpy as np
import psycopg2.extras as extras

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
psycopg2.extensions.register_adapter(np.float64, psycopg2._psycopg.AsIs)

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

def trustedBet_V1():
    SELECT_2020_GAMES = """select * from tennis_data td where td."date" >= '01-01-2020' and td."date" <= '12-31-2020'"""

    with psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5) as conn:
        tennis2020 = pd.read_sql_query(SELECT_2020_GAMES, conn)

    columns_delete = tennis2020.columns[[36,37,38,39,40,41,42,43,44,45,47,48,49,50,52,53]]
    tennis2020_small = tennis2020.drop(columns_delete, axis=1) 

    rowsToDrop = tennis2020_small.index[(tennis2020_small['pl1_weight'] == 7) | (tennis2020_small['pl2_weight'] == 7)].tolist()
    tennis2020_small.drop(rowsToDrop,axis = 0,inplace=True)

    conn = psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5)
    execute_values(conn,tennis2020_small, "tennis_datav1")