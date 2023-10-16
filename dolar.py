import re
from datetime import datetime
from io import StringIO

import pandas as pd
import requests


def round_half_up(number, decimals):
    if round((number * 10 ** (decimals + 1)) % 10) == 5:
        new_number = number+1/(10**(decimals+1))
        return round(new_number, decimals)
    else:
        return round(number, decimals)


try:

    url = f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04639PD-PD04640PD-PD04637PD-PD04638PD/csv/2020-01-01/{datetime.today().strftime('%Y-%m-%d')}"

    print(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
    req = requests.get(url, headers=headers)
    req_text = str(req.text).replace("<br>", "\n")
    req_text = str(req_text).replace('"', "")

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

    df = pd.read_csv(data)
    df["TC_INTERBANCARIO_COMPRA"]=df["Tipo de cambio - TC Interbancario (S/ por US$) - Compra"]
    df["TC_INTERBANCARIO_VENTA"]=df["Tipo de cambio - TC Interbancario (S/ por US$) - Venta"]
    df["TC_SBS_COMPRA"]=df["Tipo de cambio - TC Sistema bancario SBS (S/ por US$) - Compra"]
    df["TC_SBS_VENTA"]=df["Tipo de cambio - TC Sistema bancario SBS (S/ por US$) - Venta"]
    df["FECHA"]=df["D&iacute;a/Mes/A&ntilde;o"]
    df=df[["FECHA", "TC_INTERBANCARIO_COMPRA", "TC_INTERBANCARIO_VENTA", "TC_SBS_COMPRA", "TC_SBS_VENTA"]]
    

    df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d.%m.%y')

    df['TC_SBS_COMPRA'] = df['TC_SBS_COMPRA'].apply(round_half_up, decimals=3)
    df['TC_SBS_VENTA'] = df['TC_SBS_VENTA'].apply(round_half_up, decimals=3)

    df['AÑO'] = df['FECHA'].dt.year.astype(str)

    df.to_csv("results/dolar.csv", index=False)

    df_5d = df.tail(5)
    df.to_csv("results/dolar_5d.csv", index=False)

    df_sbs_com = df[["FECHA", "TC_SBS_COMPRA"]]
    df_sbs_ven = df[["FECHA", "TC_SBS_VENTA"]]
    df_int_com = df[["FECHA", "TC_INTERBANCARIO_COMPRA"]]
    df_int_ven = df[["FECHA", "TC_INTERBANCARIO_VENTA"]]

    df_sbs_com.columns = ['time', 'value']
    df_sbs_ven.columns = ['time', 'value']
    df_int_com.columns = ['time', 'value']
    df_int_ven.columns = ['time', 'value']

    df_sbs_com['time'] = df_sbs_com['time'].dt.strftime('%Y-%m-%d')
    df_sbs_ven['time'] = df_sbs_ven['time'].dt.strftime('%Y-%m-%d')
    df_int_com['time'] = df_int_com['time'].dt.strftime('%Y-%m-%d')
    df_int_ven['time'] = df_int_ven['time'].dt.strftime('%Y-%m-%d')

    df_sbs_com.to_json("results/timeseries_by_tc/TC_SBS_COMPRA.json", orient="records")
    df_sbs_ven.to_json("results/timeseries_by_tc/TC_SBS_VENTA.json", orient="records")
    df_int_com.to_json("results/timeseries_by_tc/TC_INTERBANCARIO_COMPRA.json", orient="records")
    df_int_ven.to_json("results/timeseries_by_tc/TC_INTERBANCARIO_VENTA.json", orient="records")

except ConnectionResetError:
    pass
