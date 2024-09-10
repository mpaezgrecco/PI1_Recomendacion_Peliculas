from typing import Union
from fastapi import FastAPI
import uvicorn 
import pandas as pd
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


app = FastAPI()

# Cargamos el dataframe
data = pd.read_csv('data_preparada_ML.csv')


# Mapeo de los meses en español a números
meses = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12
}

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    # Convertir el mes a minúsculas para evitar problemas con las mayúsculas
    mes = mes.lower()

    # Verificar si el mes ingresado es válido
    if mes not in meses:
        return {"error": "Mes no válido"}

    # Filtrar el DataFrame por el mes especificado
    mes_numero = meses[mes]
    data['release_date'] = pd.to_datetime(df['release_date'])
    filmaciones_mes = data[data['release_date'].dt.month == mes_numero]

    # Obtener la cantidad de películas estrenadas en el mes consultado
    cantidad = filmaciones_mes.shape[0]

    return {"mensaje": f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"}