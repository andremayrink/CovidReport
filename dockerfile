FROM ubuntu

COPY ./requirements.txt /covidReport/requirements.txt
COPY ./coletores /covidReport/coletores
COPY ./processadores /covidReport/processadores
COPY ./content /covidReport/content
COPY ./database /covidReport/database
COPY ./utils /covidReport/utils
COPY ./ColetarNoticiasG1Diaria.py /covidReport/ColetarNoticiasG1Diaria.py
COPY ./ColetarTweetsDiario.py /covidReport/ColetarTweetsDiario.py
COPY ./EnviarNoticiasOracleATP.py /covidReport/EnviarNoticiasOracleATP.py
COPY ./EnviarTweetsOracleATP.py /covidReport/EnviarTweetsOracleATP.py
COPY ./preencherNuvemPalavrasOracleATP.py /covidReport/preencherNuvemPalavrasOracleATP.py
COPY ./preencherSentimentosOracleATP.py /covidReport/preencherSentimentosOracleATP.py
COPY ./cicloColeta.sh /covidReport/cicloColeta.sh

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99

RUN apt-get update
RUN apt-get -y install python3 python3-pip libaio1 wget
# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Updating apt to see and install Google Chrome
RUN apt-get -y update
# Magic happens
RUN apt-get install -y google-chrome-stable

RUN pip3 install --upgrade pip
RUN pip3 install -r /covidReport/requirements.txt
RUN python3 -m spacy download pt_core_news_sm
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader rslp
RUN python3 -m nltk.downloader stopwords

ENV COVIDREPORT_HOME=/covidReport/
ENV PATH=${PATH}:${COVIDREPORT_HOME}
ENV LD_LIBRARY_PATH=${COVIDREPORT_HOME}database/oracle/instantclient_19_6/
ENV PATH=${PATH}:${LD_LIBRARY_PATH}

CMD sh /covidReport/cicloColeta.sh