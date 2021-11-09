import pandas as pd
import requests
import re
from io import StringIO

try:
    url = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04639PD-PD04640PD-PD04637PD-PD04638PD/csv/2020-01-01/2021-11-30"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
    req = requests.get(url, headers=headers)
    req_text=str(req.text).replace("<br>","\n")
    req_text=str(req_text).replace('"',"")

    dict_months = {
        "Ene": "01",
        "Feb": "02",
        "Mar": "03",
        "Abr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Ago": "08",
        "Set": "09",
        "Oct": "10",
        "Nov": "11",
        "Dic": "12"
    }

    pattern = re.compile(r'\b(' + '|'.join(dict_months.keys()) + r')\b')
    result = pattern.sub(lambda x: dict_months[x.group()], req_text)
    data = StringIO(result)

    df=pd.read_csv(data, names=["FECHA","TC_SBS_COMPRA","TC_SBS_VENTA","TC_INTERBANCARIO_COMPRA","TC_INTERBANCARIO_VENTA"],skiprows=1)
    df['FECHA']=pd.to_datetime(df['FECHA'], format='%d.%m.%y')
    df.to_csv("results/dolar.csv",index=False)

except ConnectionResetError:
    pass