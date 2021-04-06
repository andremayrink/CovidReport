import spacy
import pt_core_news_sm

class NLP:
    def __init__(self, texto):
        self._nlp = pt_core_news_sm.load()
        self._text = texto
    
    def setTexto(self, value):
        self._text = value

    def getEntidades(self):
        nlp = self._nlp(self._text)
        entidades = {}
        for e in nlp.ents:
            entidades[e.text.strip()] = e.label_
        return [{"entidade":k, "tag":entidades[k]} for k in entidades.keys()]