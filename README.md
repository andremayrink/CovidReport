# CovidReport

Projeto Final - Pós graduação   Ciencia de dados e Big Data - IEC - PUC Minas

## O que é o Covid Report?

    O CovidReport é uma ferramenta que fornece um “termômetro” dos sentimentos e do engajamento da população em relação às ações do governo no enfrentamento da pandemia, por meio de notícias coletadas nos principais portais e suas repercussões em comentários e no Twitter gerando reports, dashboards e análises automatizados.

## Componentes

* Alessandra Gomes Cioletti
* André Dutra Mayrink
* Claudio Lobenwein Resende
* Flávia Maria Dugulin Castro
* Ivana Villefort de Bessa Porto
* Késia Moreira Alves
* Laura Rodrigues Vieira
* Lucas Fernandes
* Raniere Christian Anastácio

## Variáveis de ambiente

É necessários criar a variável de ambiente **COVIDRREPORT_HOME** apontando para o diretório raiz da da aplicação

Ex.: *"c:\app\CovidReport"* ou *"/home/app/CovidReport"*

## Estrutura de diretórios

Pastas:
* coletores:
    - Classe python dos coletores de notícias do site G1.
    - Classe python para coleta de tweets.

* config:
    - Nesta pasta são armazenadas as configurações da aplicação para coleta de tweets, conexão ao banco de dados Oracle ATP e configurações para coleta de notícias.

* content:
    - Nesta pasta fica a mascara para geração da núvem de palavras e o arquivo do dicionário de polaridades para a análise de sentimentos.

* database:
    - Classe para conexão ao banco de dados  Oracle Autonomous Transaction Processing (ATP)
    - local de instalação do client oracle de conexão.

* processadores:
    - Classe de processamento de linguagem natural. (Análise de sentimento e Extração de entidades)
    - Classe de geração de núvem de palavras.

* utils:    
    - Classe de centralização das configurações da aplicação (lê as configurações do diretório /config)
    - Classe com funções facilitadoras para conversões e operações de data e hora
    - Classe para leitura e escrita dos arquivos em formato Json.

* dados:
    Neste diretório ficam armazendos os dados coletados e/ou gerados.
    - noticias: noticias em arquivo json separados por dia.
    - temp: Diretório de geração de arquivos temporários.
    - tweets: tweets em formato json separados por dia.


# Docker
O projeto de extração e procesamentos foi estruturado pra ser executado em um containter docker. 
Para criação da imagem e execução do container utilize os comandos abaixo.

## Criar imagem docker file.
docker build -t ubuntu/covidreport .

## Criar container docker rodando ciclo de coleta.
docker run -d -v "C:\Projeto Final\Python\CovidReport\dados":/covidReport/dados -v "C:\Projeto Final\Python\CovidReport\config":/covidReport/config --name covidreport-back ubuntu/covidreport