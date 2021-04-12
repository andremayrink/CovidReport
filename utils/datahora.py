import datetime as dt
import time

class DataHoraUtils:
    
    def datetime_from_utc_to_local(self, utc_datetime):
        now_timestamp = time.time()
        offset = dt.datetime.fromtimestamp(now_timestamp) - dt.datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset

    def datetime_from_local_to_utc(self, utc_datetime):
        now_timestamp = time.time()
        offset = dt.datetime.utcfromtimestamp(now_timestamp) - dt.datetime.fromtimestamp(now_timestamp)
        return utc_datetime + offset

    def adicionaDiasData(self, data, dias):
        return data + dt.timedelta(days=dias)