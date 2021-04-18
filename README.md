# CovidReport
Projeto Final - Pós graduação   Ciencia de dados e Big Data - IEC - PUC Minas

É necessários criar a variável de ambiente **COVIDRREPORT_HOME** apontando para o diretório raiz da da aplicação

Ex.: *"c:\app\CovidReport"* ou *"/home/app/CovidReport"*

Pastas:
* coletores:
    - Classes python dos coletores
* dados:
    - Dados coletados zipados
* notebooks:
    - jupyter notebooks das coletas e provas de conceito
    
# Docker
O projeto de extração e procesamentos foi estruturado pra ser executado em um containter docker. 
Para criação da imagem e execução do container utilize os comandos abaixo.

## Criar imagem docker file.
docker build -t ubuntu/covidreport .

## Criar container docker rodando ciclo de coleta.
docker run -d -v "C:\Projeto Final\Python\CovidReport\dados":/covidReport/dados -v "C:\Projeto Final\Python\CovidReport\config":/covidReport/config --name covidreport-back ubuntu/covidreport