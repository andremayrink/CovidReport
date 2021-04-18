python3 ${COVIDREPORT_HOME}/ColetarNoticiasG1Diaria.py -2
python3 ${COVIDREPORT_HOME}/ColetarTweetsDiario.py 50000
python3 ${COVIDREPORT_HOME}/EnviarNoticiasOracleATP.py -2
python3 ${COVIDREPORT_HOME}/EnviarTweetsOracleATP.py -2
python3 ${COVIDREPORT_HOME}/preencherNuvemPalavrasOracleATP.py
python3 ${COVIDREPORT_HOME}/preencherSentimentosOracleATP.py
python3 ${COVIDREPORT_HOME}/preencherEntidadesNoticiasOracleATP.py -7
date; echo ciclo concluído
echo ======================================
echo novo ciclo em 30 minutos; sleep 30m
date; echo iniciando novo ciclo
echo ======================================
sh ${COVIDREPORT_HOME}/cicloColeta.sh