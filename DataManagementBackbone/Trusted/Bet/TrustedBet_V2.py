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

def trustedBet_V2():

    SELECT_2020_GAMES = """select * from tennis_datav1"""
    with psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5) as conn:
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

    conn = psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5)
    execute_values(conn,tennisv1,"tennis_datav2")
