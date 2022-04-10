from typing import List

import pandas as pd
from pandas import DataFrame

import wspra1 as ws


def genera_conjunto_datos(anio, mes_inicial, mes_final):
    datos_lista: list[DataFrame] = []

    for mes in range(mes_inicial, mes_final + 1):
        webscraping = ws.Wspra1()
        webscraping.genera_boletin_fecha(anio=anio, mes=mes, dia=25)
        datos_temp = webscraping.descarga_precios()
        if datos_temp is not None:
            datos_lista.append(datos_temp)

    if len(datos_lista) > 0:
        datos_anio = pd.concat(datos_lista)
        return datos_anio
    else:
        return None


if __name__ == '__main__':

    conjunto_datos = []
    # Generación de lista de precios de los años 2011 a 2021
    for i in range(2016, 2022):
        conjunto_datos.append(genera_conjunto_datos(anio=i, mes_inicial=1, mes_final=12))

    datos = pd.concat(conjunto_datos)

    datos.to_csv('precios.csv', index=False)
