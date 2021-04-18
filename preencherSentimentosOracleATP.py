from database.oracleATP import OracleATP
from processadores.nlp import NLP
import cx_Oracle
import os

def getFileContent(fileName):
    file = open (fileName,"rb") 
    content = file.read()
    file.close ()
    return content

o = OracleATP()
nlp = NLP("")

sqlConsultaComentarios = "select ID, TEXTO from comentarios where sentimento is null"
sqlUpdateComentarios   = "Update comentarios set sentimento = :sentimento where id = :id"
sqlConsultaTweets      = "select ID, TEXTO from tweets where sentimento is null"
sqlUpdateTweets        = "Update tweets set sentimento = :sentimento where id = :id"

print("Carregando comentários...")
listaComentarios = o.executeFetchAll(sqlConsultaComentarios, [], None)
commitCount = 0
inseridos = {"P":0,"E":0,"N":0}
cursor = o.getCursor()
print("Atualizando Sentimentos...")
for c in listaComentarios:
    id = c["ID"]
    texto = str(c["TEXTO"])
    nlp.setTexto(texto)
    sentimento = nlp.Score_sentimento()[0]
    o.executeOnly(sqlUpdateComentarios, [sentimento, id], cursor)
    commitCount += 1
    inseridos[sentimento] += 1
    if commitCount >= 500:
        print (inseridos)
        cursor.connection.commit()
        commitCount = 0
cursor.connection.commit()

print("Carregando tweets...")
listaTweets = o.executeFetchAll(sqlConsultaTweets, [], None)
commitCount = 0
inseridos = {"P":0,"E":0,"N":0}
cursor = o.getCursor()
print("Atualizando Sentimentos...")
for c in listaTweets:
    id = c["ID"]
    texto = str(c["TEXTO"])
    nlp.setTexto(texto)
    sentimento = nlp.Score_sentimento()[0]
    o.executeOnly(sqlUpdateTweets, [sentimento, id], cursor)
    commitCount += 1
    inseridos[sentimento] += 1
    if commitCount >= 500:
        print (inseridos)
        cursor.connection.commit()
        commitCount = 0
cursor.connection.commit()

cursor.close()
print("Preenchimento de sentimentos concluída.\n===================================\n\n")