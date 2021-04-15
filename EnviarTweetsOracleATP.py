from database.oracleATP import OracleATP
from utils.jsonutils import JsonUtils
import datetime as dt
import os, sys
import random
from processadores.nlp import NLP
o = OracleATP()
ju = JsonUtils()
nlp = NLP("")

def getListaDatas():
    dias = [0]

    if (len(sys.argv) > 1):
        d = int(sys.argv[1])
        if d >= 0:
            dias = range(0, d)
        else: dias = range(d + 1, 1)

    datas = []
    for d in dias:
        data = dt.datetime.today() + dt.timedelta(days=d)
        datas.append(data)
    return datas

def getTweetDate(dtime):
    new_datetime = dt.datetime.strptime(dtime,'%d/%m/%Y %H:%M%S')
    return new_datetime

def inserirTweet(id, texto, data, sentimento, c):
    sqlInsert = """INSERT INTO TWEETS
    (id, texto, sentimento, data) 
    VALUES (:id, :texto, :sentimento, :data)"""
    try:
        o.executeOnly(sqlInsert, [id, texto, sentimento, data], c)
    except:
        print("erro ", sqlInsert, [id, texto, sentimento, data])
        raise
    


for database in getListaDatas():
    fileName = "{1}dados/tweets/Tweets_{0}.json".format(database.strftime("%d_%m_%Y"), os.environ.get("COVIDREPORT_HOME"))
    novo = 0
    ignorado = 0
    commitCount = 0
    if os.path.exists(fileName):
        tweets = ju.carregaDadosJson(fileName)
        
        print(database, len(tweets), "carregados")
        idsNuvem = [str(r["ID"]) for r in o.executeFetchAll("select id from tweets order by id", [], None)]
        print(len(idsNuvem), "na nuvem")
        cursor = o.getCursor()
        for t in tweets:
            if t["id"] not in idsNuvem:
                novo +=1
                data = getTweetDate(t["data"])
                nlp.setTexto(t["texto"])
                sentimento = nlp.Score_sentimento()[0]
                inserirTweet(t["id"], t["texto"], data, sentimento, cursor)
                commitCount += 1
                if commitCount >= 100:
                    commitCount = 0
                    cursor.connection.commit()
            else: ignorado += 1
        cursor.connection.commit()
    print("novos:", novo, "ignorados:", ignorado)