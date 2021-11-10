[![dolar-daily](https://github.com/annaabsi/USDPEN/actions/workflows/main.yml/badge.svg)](https://github.com/annaabsi/USDPEN/actions/workflows/main.yml)

<!-- PROJECT HEADER -->
<br />
<p align="center">
  <a href="#">
    <img src="https://data.larepublica.pe/avance-vacunacion-covid-19-peru/logo.png" alt="Logo" width="30%" >
  </a>

  <h3 align="center">Tipo de cambio USDPEN</h3>

  <p align="center">
    <a href="#">Publicación</a>
  </p>
</p>

<hr>

## Instalación 

### Linux (Probado en Python 3.8.1+)

Automatizado con [Github Actions](.github/workflows/main.yml)

Instalación
```bash
# Instala requerimientos de Python
pip3 install -r requirements.txt

```

Obtener resultados
```bash
# Obtener tipos de cambio del día
python3 dolar.py
```


## Descripción

El programa consta de los siguientes scripts:
- dolar: obtiene [tipos de cambio](https://estadisticas.bcrp.gob.pe/estadisticas/series/diarias/tipo-de-cambio) a partir de endpoints del BCRP

<!-- https://www.bcrp.gob.pe/index.php -->

### *dolar.py*

Genera distintas tablas y jsons de salida con sus respetivas columnas que se encuentran dentro de la carpeta [results/](results/)

1. [dolar.csv](results/dolar.csv): FECHA,TC_SBS_COMPRA,TC_SBS_VENTA,TC_INTERBANCARIO_COMPRA,TC_INTERBANCARIO_VENTA
2. [dolar.json](results/dolar.json)

Series de tiempo:

3. [TC_INTERBANCARIO_COMPRA.json](results/timeseries_by_tc/TC_INTERBANCARIO_COMPRA.json)
4. [TC_INTERBANCARIO_VENTA.json](results/timeseries_by_tc/TC_INTERBANCARIO_VENTA.json)
5. [TC_SBS_COMPRA.json](results/timeseries_by_tc/TC_SBS_COMPRA.json)
6. [TC_SBS_VENTA.json](results/timeseries_by_tc/TC_SBS_VENTA.json)
