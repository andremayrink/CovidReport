import json

class JsonUtils:

    def gravarJson(self, fileName,  dados):
        with open(fileName, 'w') as outfile:
            json.dump(dados, outfile, indent=3)

    def carregaDadosJson(self, fileName):
        with open(fileName) as json_file:
            data = json.load(json_file)
            return data