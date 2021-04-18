from utils.configuracoes import Configuracoes
from coletores.tweeter import Tweeter
import datetime as dt
from utils.datahora import DataHoraUtils
from utils.jsonutils import JsonUtils
import sys, os

print("Inicializando coleta de tweets...\n===================================")

du = DataHoraUtils()
cfg = Configuracoes()
numTweets = 1000 #número de tweets para coletar
if (len(sys.argv) > 1):
    numTweets = int(sys.argv[1])

idioma = "pt"
dataBase = du.adicionaDiasData(dt.datetime.today(), -7)
dataBase = dt.datetime(dataBase.year, dataBase.month, dataBase.day)
print("Iniciando coleta para data base:", dataBase)
palavrasChave = ["Covid", "Coronavirus", "Pandemia", "Vacina"]
print ("Palavras chave: ", " ou ".join(palavrasChave))

t = Tweeter(cfg.config["tweeter"]["con_key"], 
            cfg.config["tweeter"]["con_sec"], 
            cfg.config["tweeter"]["a_token"], 
            cfg.config["tweeter"]["a_secret"])

t.setLang(idioma)

t.setDataInicial(dataBase)

print("iniciando coletas dos tweets...")
c = t.getSeachCursor(numTweets, palavrasChave)
listaTweets = t.getTweetsFromCursor(c)
print("coleta concluída.")

ju = JsonUtils()
for k in listaTweets.keys():
    fileName = "{0}dados/tweets/Tweets_{1}.json".format(os.environ.get("COVIDREPORT_HOME"), k)
    print("processando gravação {0}".format(fileName))
    dados = []
    if os.path.exists(fileName):
        dados = ju.carregaDadosJson(fileName)
    ids = [d["id"] for d in dados]
    for t in listaTweets[k]:
        if t["id"] not in ids:
            dados.append(t)
    ju.gravarJson(fileName, dados)

print("Coleta de tweets concluída.\n===================================\n\n")