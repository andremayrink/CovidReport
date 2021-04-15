import nltk
from nltk.corpus import stopwords
import regex as re
import string
from unidecode import unidecode 
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import os

class NuvemPalavras:
    _extraStopWords = []
    _extraStopWords = " ".join([e.lower() for e in _extraStopWords]).split()
    _stopWords = set(stopwords.words('portuguese') + _extraStopWords)
    _negativeWords = []

    def __init__(self, texto):
        nltk.download('stopwords')
        self._texto = texto
        self._imageMask = "{0}content/mask.jpg".format(os.environ.get("COVIDREPORT_HOME"))
    
    def pre_processamento_texto(self, corpus):
        corpus_alt = re.findall(r"\w+(?:'\w+)?|[^\w\s]", corpus.lower())
        corpus_alt = [t for t in corpus_alt if t not in self._stopWords]
        corpus_alt = [re.sub("\d", "", t) for t in corpus_alt]
        corpus_alt =  [s.translate(str.maketrans('', '', string.punctuation)) for s in corpus_alt]
        corpus_alt = [unidecode(t) for t in corpus_alt]
        corpus_alt = [t for t in corpus_alt if t!=""]
        return corpus_alt

    def setTexto(self, value):
        self._texto = " ".join(self.pre_processamento_texto(value))

    def _color_func(self, word, font_size, position,orientation,random_state=None, **kwargs):
        if word in self._negativeWords:
            return (255,0,0)
        else:
            return (0,255,0)

    def salvarNuvemPalavras(self, nomeArquivo, minWLen=2, col=2):
        _mask = np.array(Image.open(self._imageMask))
        wordcloud = WordCloud(stopwords=self._stopWords, 
                                width=700, 
                                height=700, 
                                mask=_mask,
                                max_font_size=200, 
                                max_words=500, 
                                background_color="white", 
                                min_word_length=minWLen,
                                color_func = self._color_func)
        wordcloud.generate(self._texto)
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(nomeArquivo)
        plt.close('all')