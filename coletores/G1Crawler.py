import requests
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlencode
from time import sleep
import os

class CrawlerG1:
    def __init__(self, url):
        self.url = url
        self.feedback = True
        self.chormeDriverPath= os.path.abspath(os.path.join('.', 'driver')) + ""

    def setChromeDriverPath(self, value):
        self.chormeDriverPath = value
    
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
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.binary_location = ""
        options.headless = True
        driver = webdriver.Chrome(executable_path="{0}\chromedriver.exe".format(self.chormeDriverPath), options=options)
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