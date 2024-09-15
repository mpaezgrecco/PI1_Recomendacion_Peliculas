from typing import Union
from fastapi import FastAPI,HTTPException
import uvicorn 
import pandas as pd
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from pydantic import BaseModel


app = FastAPI()

# Cargamos el dataframe
data = pd.read_csv('dataset_ML.csv')

# A continuacion comenzaremos con algunos pasos fundamentales para construir un sistema de recomendación de 
# películas basado en similitud de títulos. 

''' Preparacion de los datos '''
'''Convertir los valores de 'name_genres' en cadenas de texto: Es necesario para manipular y analizar los datos
de género de las películas. Si la columna 'name_genres' contiene listas o diccionarios en formato de texto, 
convertirlos en cadenas concatenadas permite trabajar con estos datos de forma más directa.'''

data['name_genres'] = data['name_genres'].apply(lambda x: ' '.join(eval(x)))

''' Matriz TF-IDF para los títulos de las películas:
1. Stopwords personalizadas: Se eliminan palabras comunes que no aportan valor semántico relevante, 
como "the","of", "and" lo que ayuda a mejorar la precisión del modelo de recomendación.'''

custom_stop_words = [
    'the', 'and', 'to', 'of', 'in', 'a', 'for', 'on', 'with', 'as', 'is', 'at', 'this'
]  

''' 2. TF-IDF (Term Frequency-Inverse Document Frequency) es una técnica utilizada para evaluar la relevancia de una 
palabra en un documento dentro de un corpus. En este caso, se aplica a los títulos de las películas para 
representar cada título como un vector en un espacio multidimensional, donde cada dimensión corresponde a 
una palabra.'''

# Vectorización de texto con eliminación de stopwords
vectorizer = TfidfVectorizer(stop_words=custom_stop_words)
tfidf_matrix = vectorizer.fit_transform(data['title'])

# Calcular la similitud del coseno entre los títulos de las películas
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

''' 1. def cantidad_filmaciones_mes( Mes ): 
Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el
mes consultado en la totalidad del dataset.'''
@app.get("/cantidad_film_mes/{mes}")
def cantidad_film_mes(mes: str):
    # Convertir el mes a minúsculas para evitar problemas con las mayúsculas
    mes = mes.lower()
    
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

    # Verificar si el mes ingresado es válido
    if mes not in meses:
        return {"error": "Mes no válido"}

    # Filtrar el DataFrame por el mes especificado
    mes_numero = meses[mes]
    data['release_date'] = pd.to_datetime(data['release_date'])
    filmaciones_mes = data[data['release_date'].dt.month == mes_numero]

    # Obtener la cantidad de películas estrenadas en el mes consultado
    cantidad = filmaciones_mes.shape[0]

    return {"mensaje": f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"}

''' 2. def cantidad_filmaciones_dia( Dia ):
Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas
en día consultado en la totalidad del dataset.'''

#Función
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str): # Devuelve la cantidad de filmaciones 
    contador = 0

    # Mapear los nombres de los dias en español a los números de los dias
    dias_semana = {"lunes": 0,"martes": 1,"miercoles": 2,"jueves": 3,
                   "viernes": 4,"sabado": 5,"domingo": 6}

    # Convertir el dia a minúsculas
    dia = dia.lower()

    # Verificar si el dia ingresado es válido
    if dia not in dias_semana:
        return f"Dia inválido: {dia}"
    
    # Aquí deberías tener la lógica para obtener los datos del dataset y contar las películas estrenadas en el día consultado
    # Asegúrate de tener la estructura adecuada del dataset y ajusta el código según tus necesidades
    for fecha_estreno in data["release_date"]:
        fecha_estreno_obj = datetime.datetime.strptime(fecha_estreno, "%Y-%m-%d") # strptime se utiliza para convertir una cadena de texto en un objeto de fecha y hora (datetime).

        if fecha_estreno_obj.weekday() == dias_semana[dia]: # La función weekday() se utiliza para obtener el día de la semana correspondiente a un objeto datetime. Retorna un número entero que representa el día de la semana, donde el lunes es el día 0 y el domingo es el día 6.
            contador += 1

    # return f"{contador} películas fueron estrenadas en los días {dia.capitalize()}" # capitalize() convierte el primer carácter de una cadena en mayúscula y el resto de los caracteres en minúscula.
    return {'dia':dia.capitalize(), 'cantidad':contador}


'''3. def score_titulo( titulo_de_la_filmación ): 
Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.'''

#funcion
@app.get("/score_titulo/")
def score_titulo(titulo_de_la_filmación: str):
    
    # Normalizar el título de entrada: convertir a minúsculas y eliminar espacios extra
    titulo_de_la_filmación = titulo_de_la_filmación.strip().lower()
    
    # Buscar la fila en el DataFrame que coincide con el título proporcionado
    pelicula = data[data['title'].str.lower().str.strip() == titulo_de_la_filmación]

    # Verificar si se encontró alguna película con el título dado
    if pelicula.empty:  # El método empty devuelve True si el DataFrame está vacío
        return {"error": "Película no encontrada"}
        
    # Obtener el año de estreno y el score de la película encontrada
    titulo = pelicula['title'].iloc[0]  # iloc[0] sirve para acceder al primer registro
    año_estreno = str(pelicula['release_year'].iloc[0])
    score = str(pelicula['popularity'].iloc[0])
    
    return {'titulo': titulo, 'anio': año_estreno, 'popularidad': score}

''' 4. def votos_titulo( titulo_de_la_filmación ):
Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor 
promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario,
debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''

@app.get("/votos_titulo/")
def votos_titulo(titulo_de_la_filmación: str):
    #buscar la fila en el DataFrame que coincide con el título proporcionado
    pelicula = data[data['title'] == titulo_de_la_filmación]
    #Verificar si se encontró alguna película con el título dado
    if pelicula.empty:
        return "Pelicula no encontrada."    
    # Verificar si la película tiene al menos 2000 valoraciones
    votos = pelicula['vote_count'].iloc[0]
    titulo =pelicula['title'].iloc[0] 
    promedio_votos= pelicula['vote_average'].iloc[0]
    año_estreno= str(pelicula['release_year'].iloc[0])
        
    if votos < 2000:
        return f"La película no cumple con la condición de tener al menos 2000 valoraciones, esta pelicula cuenta con {int(votos)} votos"
    else:
        return {'titulo':titulo, 'anio':año_estreno, 'voto_total':votos, 'voto_promedio':promedio_votos}
    
''' def get_actor( nombre_actor ): 
Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del
mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el
promedio de retorno. La definición no deberá considerar directores.'''

# Definir la función con el decorador
@app.get("/get_actor/{nombre_del_actor}")
def get_actor(nombre_del_actor: str):
    
    # Filtrar las filas donde se encuentra el actor que buscamos 
    actor_film = data[data['names_actors'].apply(lambda x: nombre_del_actor in x)]
    
    # Verificar si el actor existe
    if actor_film.empty:
        return {"message": f"No se encontro relacion del actor con ninguna pelicula: {nombre_del_actor}"}
    
    # Obtener la cantidad de películas y el promedio de retorno del actor
    cantidad_peliculas = len(actor_film)
    promedio_retorno = actor_film['return'].mean()
    retorno = sum(actor_film['return'])
    return {'actor':nombre_del_actor, 'cantidad_filmaciones':cantidad_peliculas, 'retorno_total':retorno, 'retorno_promedio':promedio_retorno}

''' def get_director( nombre_director ): 
Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del
mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de 
lanzamiento, retorno individual, costo y ganancia de la misma.'''

@app.get('/get_director/{nombre_del_director}')
def get_director(nombre_del_director: str):
    
    # Filtrar las películas del director
    peliculas_director = data[data['name_director'] == nombre_del_director]

    # Verificar si se encontraron películas
    if peliculas_director.empty:
        return {"message": f"No se encontraron películas para el director: {nombre_del_director}"}

    # Calcular el retorno total (más eficiente usando .sum() en una sola línea)
    retorno_total = peliculas_director['return'].sum()

    # Seleccionar columnas de interés y convertir el DataFrame resultante a diccionario
    peliculas_info = peliculas_director[['title', 'release_year', 'return', 'budget', 'revenue']].to_dict(orient='records')

    # Crear la respuesta
    respuesta = {
        'director': nombre_del_director,
        'retorno_total': retorno_total,
        'peliculas': peliculas_info
    }

    return respuesta

@app.get('/recomendacion/{titulo}')
def recomendacion(titulo: str):    
     # Verificar si el título está en el DataFrame
    if titulo not in data['title'].values:
        return {'error': f"No se encontró el título '{titulo}'."}

    # Encontrar el índice de la película con el título dado
    idx = data.index[data['title'] == titulo].tolist()[0]

    # Calcular las puntuaciones de similitud de todas las películas con la película dada
    sim_scores = cosine_similarities[idx]

    # Ordenar las películas por puntaje de similitud en orden descendente
    sim_scores = sim_scores.argsort()[::-1]  # Índices ordenados en orden descendente

    # Obtener los índices de las películas más similares 
    sim_scores = sim_scores[sim_scores != idx][:6]  # Excluyendo la película buscada y tomando las 5 mejores puntajes

    # Devolver los títulos de las películas más similares
    respuesta_recomendacion = data['title'].iloc[sim_scores].tolist()
    return {'lista recomendada': respuesta_recomendacion}

# Ejecutar la aplicación con Uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)