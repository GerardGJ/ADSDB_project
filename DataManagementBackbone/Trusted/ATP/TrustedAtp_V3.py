import pandas as pd
import numpy as np
import os
import csv
import datetime
from sqlalchemy import create_engine

def trustedAtp_V3():

    SELECT_ATP = "select * from atpdatav2"

    conn_string = 'postgresql://biel.caballero:DB130201@postgresfib.fib.upc.edu:6433/ADSDBbiel.caballero'
    db = create_engine(conn_string)

    with db.connect() as conn:
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

    conn = db.connect()
    atp.to_sql('atpdatav3', con=conn, if_exists='replace', index = False)

