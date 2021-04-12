from  coletores.G1Crawler import CrawlerG1, UtislG1
from utils.jsonutils import JsonUtils
import sys
import datetime as dt
import json
import os

palavrasChave = ["COVID", "PANDEMIA", "CORONAVIRUS", "VACINA"]

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
            return datetime.strptime(value.replace("h", ":"), '%d/%m/%Y %H:%M')
        except:
            return datetime(1900,1,1)
    return datetime(1900,1,1)

util = UtislG1()
jutil = JsonUtils()
coleta = CrawlerG1("")
coleta.setFeedback(False)

for data in getListaDatas():
    fileName = "{1}dados\\noticias\\noticiasCovid_{0}.json".format(data.strftime('%d_%m_%Y'), os.environ.get("COVIDREPORT_HOME"))
    dados = []
    if os.path.exists(fileName):
        dados = jutil.carregaDadosJson(fileName)
    listaNoticias = util.filtraNoticiasPalavraChave(util.getListaNoticiasDia(data), palavrasChave)
    auxUrls = [n["url"] for n in dados]
    novas = 0
    for n in listaNoticias:
        if not(n["url"] in auxUrls):
            dados.append(n)
            novas +=1

    coletados = 0
    ignorados = 0
    gravar = 0
    for i in range(0,len(dados)):
        capturar = not ("noticia" in dados[i].keys())
        capturar = capturar or not (dados[i]["noticia"])
        if capturar:
            try:
                coleta.setUrlNoticia(dados[i]["url"])
                noticia = coleta.getNoticia()
                noticia["comentarios"] = coleta.getComentariosNoticia()
                dados[i].update(noticia)
                coletados += 1
                gravar += 1
                if gravar >= 100:
                    gravar = 0
                    jutil.gravarJson(fileName, dados)
            except:
                ignorados += 1
                print(dados[i]["url"])
    jutil.gravarJson(fileName, dados)                        
    print("Atualizado: ", fileName, " - ", len(dados), " novas: ", novas)