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

def trustedAtp_V3():
    SELECT_ATP = "select * from atpdatav2"
    with psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5) as conn:
        atp = pd.read_sql_query(SELECT_ATP, conn)

    def formatingName(name):
        mod_name = name.split(' ')
        temp = '.'.join([mod_name[i][0] for i in range (0, len(mod_name) - 1)])
        if temp == '':
            return mod_name[-1]
        else:
            return mod_name[-1] + ' ' + temp + '.'

    atp["winner_name"] = atp["winner_name"].apply(formatingName)
    atp["loser_name"] = atp["loser_name"].apply(formatingName)

    atp["tourney_name"] = atp["tourney_name"].astype("category")
    dic_changeTournaments = {"ATP Rio de Janeiro" : "Rio Open",
                            "Adelaide" : "Adelaide Internacional",
                            "Acapulco" : "Abierto Mexicano",
                            "Antwerp" : "European Open",
                            "Auckland" : "ASB Classic",
                            "Buenos Aires" : "Argentina Open",
                            "Cinncinati Masters" : "Western & Sourthern Financial Group Masters",
                            "Cologne 1" : "bett1HULKS Indoors",
                            "Cologne 2" : "bett2HULKS Championship",
                            "Cordoba" : "Cordoba Open",
                            "Delray Beach" : "Delray Beach Open",
                            "Doha" : "Qatar Exxon Mobile Open",
                            "Dubai" : "Dubai Tennis Championship",
                            "Hamburg" : "German Tennis Championship",
                            "Kitzbuhel" : "Generali Open",
                            "Marseille" : "Open 13",
                            "Montpellier" : "Open Sud de France",
                            "New York" : "New York Open",
                            "Nur-Sultan" : "Astana Open",
                            "Paris Masters" : "BNP Paribas Masters",
                            "Pune" : "Maharashtra Open",
                            "Roland Garros" : "French Open",
                            "Roma Masters" : "Internazionali BNL d'Italia",
                            "Rotterdam" : "ABN AMRO World Tennis Tournament",
                            "Santiago" : "Chile Open",
                            "Sardinia" : "Forte Village Sardegna Open",
                            "Sofia" : "Sofia Open",
                            "St Petersburg" : "St. Petersburg Open",
                            "Tour Finals" : "Masters Cup",
                            "Us Open" : "US Open",
                            "Vienna" : "Erste Bank Open"}
    atp["tourney_name"] = atp["tourney_name"].cat.rename_categories(dic_changeTournaments)

    atp = atp.replace({np.NaN: None})

    conn = psycopg2.connect(host='postgresfib.fib.upc.edu', dbname='ADSDBbiel.caballero', user='biel.caballero', password='DB130201', port=6433, connect_timeout=5)
    execute_values(conn,atp,"atpdatav3")