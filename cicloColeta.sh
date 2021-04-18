python3 ${COVIDREPORT_HOMO}/ColetarNoticiasG1Diaria.py -2
python3 ${COVIDREPORT_HOMO}/ColetarTweetsDiario.py 50000
python3 ${COVIDREPORT_HOMO}/EnviarNoticiasOracleATP.py -2
python3 ${COVIDREPORT_HOMO}/EnviarTweetsOracleATP.py -2
python3 ${COVIDREPORT_HOMO}/preencherNuvemPalavrasOracleATP.py
python3 ${COVIDREPORT_HOMO}/preencherSentimentosOracleATP.py
sh ${COVIDREPORT_HOMO}/cicloColeta.sh