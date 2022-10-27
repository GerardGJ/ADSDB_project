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

def trustedAtp_V1():
    SELECT_ATP = "select * from atpdata"
    with psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5) as conn:
        ATPdata = pd.read_sql_query(SELECT_ATP, conn)

    conversionDic = {"tourney_id":"string", "tourney_name":"string", "surface":"string", "tourney_level":"string", "winner_name":"string", 
                    "winner_hand":"category", "winner_ioc":"category", "loser_name":"string", "loser_hand":"category", "loser_ioc":"category", 
                    "round":"category", "tourney_level":"category", "surface":"category", "best_of":"category"}
    ATPdata=ATPdata.astype(conversionDic)

    conn = psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5)
    execute_values(conn,ATPdata, "atpdatav1")
