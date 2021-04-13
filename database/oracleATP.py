import cx_Oracle
from utils.configuracoes import Configuracoes

class OracleATP:

    def _initializeClientLibrary(self):
        try:
            cx_Oracle.init_oracle_client(lib_dir=self._cfg.config["oracle"]["lib_dir"], 
                                     config_dir=self._cfg.config["oracle"]["config_dir"])
        except cx_Oracle.ProgrammingError  as e:
            if not (str(e) == "Oracle Client library has already been initialized"):
                raise

    def __init__(self):
        self._cfg = Configuracoes()
        self._initializeClientLibrary()
        self._con = cx_Oracle.connect(self._cfg.config["oracle"]["user"],
                                      self._cfg.config["oracle"]["password"], 
                                      self._cfg.config["oracle"]["databaseName"])

    def getCursor(self):
        return self._con.cursor()
    
    def execute(self, sql, params, cursor):
        if (cursor):
            cursor.execute(sql, params)
        else: 
            with self._con.cursor() as c:
                c.execute(sql, params)

    def executeFetchAll(self, sql, params, cursor):
        c = cursor
        if not (c):
            c = self._con.cursor()
        try:
            c.execute(sql, params)
            colName = [c[0] for c in c.description]
            dados = []
            for r in c.fetchall():
                dado = {}
                for i in range(len(colName)):
                    dado[colName[i]] = r[i]
                dados.append(dado)
            return dados
        finally:
            if not (cursor):
                c.close()

    def executeScalar(self, sql, params, cursor):
        c = cursor
        if not (c):
            c = self._con.cursor()
        try:
            c.execute(sql, params)
            colName = [c[0] for c in c.description]
            r = c.fetchone()
            dado = {}
            for i in range(len(colName)):
                dado[colName[i]] = r[i]

            return dado
        finally:
            if not (cursor):
                c.close()

    def getBlobVar(self, content, cursor):
        blobvar = cursor.var(cx_Oracle.BLOB)
        blobvar.setvalue(0,content)
        return blobvar

    def executeOnly(self, sql, params, cursor):
        c = cursor
        if not (c):
            c = self._con.cursor()
        try:
            c.execute(sql, params)
        finally:
            if not (cursor):
                c.close()