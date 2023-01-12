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

def trustedATP_V2():
    SELECT_ATP = "select * from atpdatav1"
    with psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5) as conn:
        ATPdata = pd.read_sql_query(SELECT_ATP, conn)

    x=[ATPdata.pop(x) for x in ['winner_seed','winner_entry','loser_seed','loser_entry']]

    ATPdata['first_set'] = ATPdata.score.str.split(" ",expand=True)[0]
    ATPdata['second_set'] = ATPdata.score.str.split(" ",expand=True)[1]
    ATPdata['third_set'] = ATPdata.score.str.split(" ",expand=True)[2]
    ATPdata['fourth_set'] = ATPdata.score.str.split(" ",expand=True)[3]
    ATPdata['fifth_set'] = ATPdata.score.str.split(" ",expand=True)[4]
    x=[ATPdata.pop(x) for x in ['score']]

    conn = psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5)
    execute_values(conn,ATPdata, "atpdatav2")