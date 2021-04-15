import spacy
import pt_core_news_sm
import nltk
from nltk.corpus import stopwords
import regex as re
import string
from unidecode import unidecode 
import os

class NLP:
    _extraStopWords = []
    _extraStopWords = " ".join([e.lower() for e in _extraStopWords]).split()
    _stopWords = set(stopwords.words('portuguese') + _extraStopWords)
    _negativeWords = []

    def __init__(self, texto):
        self._nlp = pt_core_news_sm.load()
        self._text = texto
        self.dic_palavra = {}
        self._carregarDicionario()
        nltk.download('rslp') 
        nltk.download('stopwords')
        nltk.download('punkt')
    
    def _carregarDicionario(self):
        with open("{0}content/SentiLex-flex-PT02_mod3.txt".format(os.environ.get("COVIDREPORT_HOME")), 'r', encoding="utf8") as sentilex:
            for i in sentilex.readlines():
                pos_ponto = i.find(',')
                palavra = (i[:pos_ponto])
                pol_pos = i.find('POL')
                polaridade = (i[pol_pos+7:pol_pos+9]).replace(';','')
                self.dic_palavra[palavra] = polaridade

    def setTexto(self, value):
        self._text = value

    def pre_processamento_texto(self, corpus):
        corpus_alt = re.findall(r"\w+(?:'\w+)?|[^\w\s]", corpus.lower())
        corpus_alt = [t for t in corpus_alt if t not in self._stopWords]
        corpus_alt = [re.sub("\d", "", t) for t in corpus_alt]
        corpus_alt =  [s.translate(str.maketrans('', '', string.punctuation)) for s in corpus_alt]
        corpus_alt = [unidecode(t) for t in corpus_alt]
        corpus_alt = [t for t in corpus_alt if t!=""]
        return corpus_alt

    def getEntidades(self):
        nlp = self._nlp(self._text)
        entidades = {}
        for e in nlp.ents:
            entidades[e.text.strip()] = e.label_
        return [{"entidade":k, "tag":entidades[k]} for k in entidades.keys()]

    def Score_sentimento(self):
        l_sentimento = []
        for p in self.pre_processamento_texto(self._text):
            l_sentimento.append(int(self.dic_palavra.get(p, 0)))
        score = sum(l_sentimento)
        if score > 0:
            return ["P", score]
        elif score == 0:
            return ["E",score]
        else:
            return ["N", score]