from database.oracleATP import OracleATP
from processadores.nlp import NLP
import cx_Oracle
import os, sys
from utils.datahora import DataHoraUtils
from utils.jsonutils import JsonUtils
import datetime as dt

print("Preenchimento de entidades  iniciado.\n===================================\n\n")

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


o = OracleATP()
nlp = NLP("")


sqlRecuperaNoticiasSemEntidade = """SELECT N.ID, N.URL
FROM NOTICIAS N
LEFT JOIN ENTIDADES_NOTICIA E ON E.ID_NOTICIA = N.ID
WHERE E.ID_NOTICIA IS NULL"""

sqlInserirEntidadesNoticia = """INSERT INTO ENTIDADES_NOTICIA 
(ID_NOTICIA, ENTIDADE, TIPO)
VALUES 
(:ID_NOTICIA, :ENTIDADE, :TIPO)"""

print("Carregando noticias...")
listaNoticiasNuvem = o.executeFetchAll(sqlRecuperaNoticiasSemEntidade, [], None)


def retornaIdNoticia(url):
    for n in listaNoticiasNuvem:
        if (n["URL"] == url):
            return int(n["ID"])
            break
    return 0

for database in getListaDatas():
    notiticaFileName = "{1}dados/noticias/noticiasCovid_{0}.json".format(database.strftime("%d_%m_%Y"), os.environ.get("COVIDREPORT_HOME"))
    print(database, notiticaFileName)

    ju = JsonUtils()
    noticias = ju.carregaDadosJson(notiticaFileName)

    inserir = 0
    ignorar = 0

    cursor = o.getCursor()

    for noticia in noticias:
        idNoticia = retornaIdNoticia(noticia["url"])
        if (idNoticia > 0):
            inserir += 1
            nlp.setTexto(" ".join(noticia["noticia"]))    
            for e in nlp.getEntidades():
                o.executeOnly(sqlInserirEntidadesNoticia, [idNoticia, e["entidade"], e["tag"]], cursor)
            if inserir >= 100:
                cursor.connection.commit()
                inserir = 0
        else: 
            ignorar += 1

    cursor.connection.commit()    
    cursor.close()

print("Preenchimento de entidades  concluída.\n===================================\n\n")