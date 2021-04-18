import requests
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlencode
from time import sleep
import os
import datetime as dt
from utils.configuracoes import Configuracoes

###
# UtilsG1: Classe de utilidades para lista de notícias.
###
class UtislG1:
    urlSiteMap = "https://g1.globo.com/sitemap/g1/sitemap.xml"
    
    def __init__(self):
        self.listaXMLDiario = self.getListaXmlDiarios()

    def getListaXmlDiarios(self):
        response = requests.get(self.urlSiteMap)
        xmlList = BeautifulSoup(response.content, "html.parser")
        listaNoticias = []
        listaBase = [i for i in xmlList.find_all("loc")]
        listaBase = [{"url":l.text, "ano":l.text.split("/")[5], "mes":l.text.split("/")[6], "dia":l.text.split("/")[7][:2]} for l in listaBase]
        return listaBase

    def filtraNoticiasPalavraChave(self, listaNoticias, palavrasChave):
        listaFiltrada = []
        palavrasChave  = [p.upper() for p in palavrasChave]
        for n in listaNoticias:
            if any(item in palavrasChave for item in n["url"].upper().replace("/", "-").replace(".","-").split("-")):
                listaFiltrada.append(n)
        return listaFiltrada

    def getListaNoticias(self, urlXmlDia):
        listaNoticias = []
        response = requests.get(urlXmlDia)
        for url in BeautifulSoup(response.content, "html.parser").find_all("url"):
            loc = url.find("loc")
            regiao = ""
            localidade = ""
            if (loc): 
                loc = loc.text
                regiao = loc.split("/")[3].upper()
                localidade = loc.split("/")[4].replace("-"," ").capitalize()
            image = url.find("image:loc")
            if (image): image = image.text
            dado = {
                    "url":loc,
                    "image":image,
                    "regiao": regiao,
                    "localidade": localidade
                   }
            listaNoticias.append(dado)        
        return listaNoticias

    def getListaNoticiasDia(self, data):
        listaNoticias = []
        for l in self.listaXMLDiario:
            if (int(l["ano"]) == data.year) and (int(l["mes"]) == data.month) and (int(l["dia"]) == data.day):
                listaNoticias += self.getListaNoticias(l["url"])
        return listaNoticias
    
    def getListaNoticiasHoje(self):
        return self.getListaNoticiasDia(dt.datetime.today())
    
    def getListaNoticiasUltimosDias(self, nDias):
        listaNoticias = []
        seq = []
        if nDias >= 0:
            seq = range(0, nDias)
        else: seq = range(nDias + 1, 1)
        for  d in seq:
            data = dt.datetime.today() + dt.timedelta(days=d)
            listaNoticias += self.getListaNoticiasDia(data)
        return listaNoticias

###
# CrawlerG1: Classe de captura de informações das notícias.
###
class CrawlerG1:

    ## url: do site G1 a ser coletada.
    def __init__(self, url):
        self.url = url
        self.feedback = True
        if not(os.environ.get("COVIDREPORT_HOME")):
            raise Exception("Variável de ambiente COVIDREPORT_HOME não esta configurada.")
        self.cfg = Configuracoes();
    
    def setUrlNoticia(self, url):
        self.url = url
    
    def setFeedback(self, value):
        self.feedback = value
    
    def getUrlComentarios(self):
        return "https://g1.comentarios.globo.com/embed/stream?{0}".format(urlencode({"storyURL":self.url}))
    
    def getLoadMoreCommentsButton(self, driver):
        btns = driver.find_elements_by_tag_name("button")
        for btn in reversed(btns):
            if (btn.text == "Carregar Mais"):
                return btn
                break
        return None
    
    def waitPageLoaded(self, driver):
        sleep(1)
        page_state = driver.execute_script('return document.readyState;')
        while (page_state != 'complete'):
            sleep(0.5)
            page_state = driver.execute_script('return document.readyState;')
    
    def getComentariosNoticia(self):
        if self.feedback: print("carregando comentarios...", self.url)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")        
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.binary_location = ""
        options.headless = True        
        driver = webdriver.Chrome(executable_path="{0}/coletores/driver/{1}".format(os.environ.get("COVIDREPORT_HOME"), self.cfg.config["chromeDriver"]), options=options)
        driver.minimize_window();
        driver.get(self.getUrlComentarios())
        self.waitPageLoaded(driver)          
        
        btnMais = self.getLoadMoreCommentsButton(driver)
        if (btnMais):
            while True:
                try:
                    if self.feedback: print("carregando mais comentarios...")
                    btnMais.click()
                    self.waitPageLoaded(driver)          
                except:
                    break
                    
        pageComment = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        comments = []
        
        for c in pageComment.find_all("div", attrs={"class":"coral-comment"}):
            usuario = c.find("button", attrs={"class":"coral-comment-username"})
            if (usuario):
                usuario = usuario.text
            else: usuario = ""
                
            texto = c.find("div", attrs={"class":"coral-comment-content"})
            if (texto):
                texto = texto.text
            else: texto = ""
            
            if not (texto == ""):
                comments.append({"usuario":usuario, "comentario":texto})
        if self.feedback: print(len(comments), " comentario(s) carregados")
        return comments
    
    def getNoticia(self):
        response = requests.get(self.url)        
        if (response.status_code == 200):
            if self.feedback: print("Recuperando notícia de ", self.url)
            
            page = BeautifulSoup(response.content, "html.parser")
            titulo = page.find("h1", attrs={"class":"content-head__title"})
            if (titulo):
                titulo = titulo.text
            else: titulo = ""
                
            subTitulo = page.find("h2", attrs={"class":"content-head__subtitle"})
            if (subTitulo):
                subTitulo = subTitulo.text
            else: subTitulo = ""
                
            dataPublicacao = page.find("time", attrs={"itemprop":"datePublished"})
            if (dataPublicacao):
                dataPublicacao = dataPublicacao.text.strip()
            else: dataPublicacao = ""
                
            localPublicacao = page.find("p", attrs={"class":"content-publication-data__from"})
            if (localPublicacao):
                if (localPublicacao.find("span")):
                    localPublicacao = localPublicacao.find("span").text
                else: localPublicacao = ""
            else: localPublicacao = ""
            noticia = page.find_all("p", attrs={"class":"content-text__container"})
            entidades = page.find_all("li", attrs={"class":"entities__list-item"})
            noticia = {"url":self.url,
                       "titulo":titulo,
                       "subTitulo":subTitulo,
                       "dataPublicacao": dataPublicacao,
                       "localPublicacao":localPublicacao,
                       "entidades": [n.text for n in entidades],
                       "noticia": [n.text for n in noticia]
                      }
            return noticia
        else:
            print("Erro ao recuperar dados da notícia.\nStatus Code: ", response.status_code)
            return None;