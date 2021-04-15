from database.oracleATP import OracleATP
from utils.jsonutils import JsonUtils
import datetime as dt
import os, sys
import random
from utils.datahora import DataHoraUtils
from processadores.nlp import NLP

o = OracleATP()
UFs = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
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

def trataData(value):
    if (value):
        try:
            return dt.datetime.strptime(value.replace("h", ":"), '%d/%m/%Y %H:%M')
        except:
            return ""
    return ""

def getNext(seq):
    r = o.executeScalar("select {0}.nextval value from dual".format(seq), [], None)
    return r["VALUE"]

def inserirNoticia(noticia, cursor):
    if (noticia["titulo"]):
        sqlInsertNoticia = """INSERT INTO NOTICIAS 
        (ID, TITULO, URL, DATA, URL_IMAGEM, UF) 
        VALUES (:ID, :TITULO, :URL, :DATA, :URL_IMAGEM, :UF)"""

        sqlInsertComentario = """INSERT INTO COMENTARIOS
        (ID, TEXTO, SENTIMENTO, ID_NOTICIA)
        VALUES
        (:ID, :TEXTO, :SENTIMENTO, :ID_NOTICIA)
        """

        data = trataData(noticia["dataPublicacao"])

        idNoticia = getNext("SQ_NOTICIAS")
        try:
            UF = "BR"
            if noticia["regiao"].upper() in UFs:
                UF = noticia["regiao"].upper()
            o.executeOnly(sqlInsertNoticia, 
                    [idNoticia,
                    noticia["titulo"],
                    noticia["url"], 
                    data,
                    noticia["image"],
                    UF], cursor)

            for cm in noticia["comentarios"]:
                nlp.setTexto(cm["comentario"])
                sentimento = nlp.Score_sentimento()[0]
                o.executeOnly(sqlInsertComentario,
                        [getNext("SQ_COMENTARIOS"),
                        cm["comentario"],
                        sentimento,
                        idNoticia], cursor)
        except Exception as e:
            print("print falha ao inserir notícia:", e)

for database in getListaDatas():
    notiticaFileName = "{1}dados/noticias/noticiasCovid_{0}.json".format(database.strftime("%d_%m_%Y"), os.environ.get("COVIDREPORT_HOME"))
    print(database, notiticaFileName)

    urlsNuvem = [r["URL"] for r in o.executeFetchAll("Select URL from noticias", [], None)]

    ju = JsonUtils()
    noticias = ju.carregaDadosJson(notiticaFileName)

    inserir = 0
    ignorar = 0

    cursor = o.getCursor()

    for noticia in noticias:
        if not (noticia["url"] in urlsNuvem):
            inserirNoticia(noticia, cursor)
            inserir += 1
            if inserir >= 100:
                cursor.connection.commit()
                inserir = 0
        else: ignorar += 1

    cursor.connection.commit()    
    cursor.close()

    print(database, "ignorados: ", ignorar)