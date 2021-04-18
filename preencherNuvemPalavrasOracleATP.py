from database.oracleATP import OracleATP
from processadores.nuvemPalavras import NuvemPalavras
import cx_Oracle
import os

def getFileContent(fileName):
    file = open (fileName,"rb") 
    content = file.read()
    file.close ()
    return content

o = OracleATP()

sqlConsultaNoticias = """select n.id, count(1) total
                        from comentarios c 
                        inner join noticias n
                        on n.id = c.id_noticia
                        where n.np_comentarios is null
                        group by n.id
                        order by total desc"""

sqlConsultaComentarios = """select c.texto 
                            from comentarios c 
                            where c.id_noticia = :id"""

sqlUpdateNoticia = """Update Noticias N
                      Set N.Np_Comentarios = :blobData
                      Where N.Id = :Id """


listaIdsNoticas = o.executeFetchAll(sqlConsultaNoticias, [], None)
listaIdsNoticas = [l["ID"] for l in listaIdsNoticas]

np = NuvemPalavras("")
cursor = o.getCursor()
commitCount = 0

for idNoticia in listaIdsNoticas:
    comentarios = o.executeFetchAll(sqlConsultaComentarios, [idNoticia], cursor)
    comentarios = [str(c["TEXTO"]) for c in comentarios]
    np.setTexto(" ".join(comentarios))

    fileName = "{1}dados/temp/np_{0}.jpg".format(idNoticia, os.environ.get("COVIDREPORT_HOME"))
    print(fileName)
    np.salvarNuvemPalavras(fileName)
    content = getFileContent(fileName)
    blobvar = o.getBlobVar(content, cursor)
    cursor.setinputsizes(blobData = cx_Oracle.BLOB)
    o.executeOnly(sqlUpdateNoticia, {'blobData': blobvar, "Id":idNoticia}, cursor)    
    commitCount += 1
    
    if commitCount >= 10:
        cursor.connection.commit()
        commitCount = 0

cursor.connection.commit()
print("Geração de núvem de palavras concluída.\n===================================\n\n")