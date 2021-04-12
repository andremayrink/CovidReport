import json
import os

class Configuracoes():

    def carregaDadosJson(self, fileName):
        with open(fileName) as json_file:
            data = json.load(json_file)
            return data

    def __init__(self):
        cfgFilePath = (os.path.join(os.environ.get("COVIDREPORT_HOME"), 'config/config.json'))
        self.config = self.carregaDadosJson(cfgFilePath)