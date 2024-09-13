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

stopwords_custom = ["the","of", "and"]  

''' 2. TF-IDF (Term Frequency-Inverse Document Frequency) es una técnica utilizada para evaluar la relevancia de una 
palabra en un documento dentro de un corpus. En este caso, se aplica a los títulos de las películas para 
representar cada título como un vector en un espacio multidimensional, donde cada dimensión corresponde a 
una palabra.'''

tfidf = TfidfVectorizer(stop_words=stopwords_custom)
tfidf_matrix = tfidf.fit_transform(data['title'])

# Calcular la similitud del coseno entre los títulos de las películas
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

''' 1. def cantidad_filmaciones_mes( Mes ): 
Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el
mes consultado en la totalidad del dataset.'''

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

@app.get("/cantidad_film_mes/{mes}")
def cantidad_film_mes(mes: str):
    # Convertir el mes a minúsculas para evitar problemas con las mayúsculas
    mes = mes.lower()

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

# Mapeao los nombres de los dias en español a los números de los dias

dias_semana = {"lunes": 0,"martes": 1,"miércoles": 2,"jueves": 3,
                   "viernes": 4,"sábado": 5,"domingo": 6}

# función
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str): # Devuelve la cantidad de filmaciones 
    contador = 0
    
     # Convertir el dia a minúsculas para evitar problemas con las mayusculas
    dia = dia.lower()
    
    # Verificar si el mes ingresado es válido
    if dia not in dias_semana:
        return {"error": "dia no válido"}
        
    #a continuacion el codigo cuenta el número de películas estrenadas en un día específico de la semana basado
    # en el campo release_date de un dataset.'''

    for fecha_estreno in data["release_date"]: #recorre cada fecha en la columna release_date del DataFrame data.
        fecha_estreno_obj = datetime.datetime.strptime(fecha_estreno, "%Y-%m-%d") #convierte una cadena de texto con formato "YYYY-MM-DD" en un objeto datetime. Esto permite manipular y comparar fechas fácilmente.

        if fecha_estreno_obj.weekday() == dias_semana[dia]: #Obtener el día de la semana y contar si coincide con el día especificado
            contador += 1 # Si el día de la semana coincide con el día consultado, incrementa el contador.

    #Retornar el resultado
    #dia.capitalize() convierte el primer carácter del día en mayúscula y el resto en minúscula.
    # Devuelve un diccionario con el nombre del día y el número total de películas estrenadas en ese día de la semana.
    return {'dia':dia.capitalize(), 'cantidad':contador} 

'''3. def score_titulo( titulo_de_la_filmación ): 
Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.'''

#funcion 
@app.get("/score_titulo/")
def score_titulo(titulo_de_la_filmación: str):
    
 # Buscar la fila en el DataFrame que coincide con el título proporcionado
    pelicula = data[data['title'] == titulo_de_la_filmación]

    # Verificar si se encontró alguna película con el título dado
    if not pelicula.empty: # El método empty devuelve True si el DataFrame está vacío.
        
        # Obtener el año de estreno y el score de la película encontrada
        titulo = pelicula['title'].values[0] 
        año_estreno = pelicula['release_year'].values[0]
        score = pelicula['vote_average'].values[0]
        # return f"La pelicula {titulo} fue estrenada en el año {año_estreno} con un score de {score}."
        return {'titulo':titulo, 'anio':año_estreno, 'popularidad':score}
    else:
        raise HTTPException(status_code=404, detail="Título no encontrado")

''' 4. def votos_titulo( titulo_de_la_filmación ):
Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor 
promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario,
debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''

@app.get("/votos_titulo/")
def votos_titulo(titulo_de_la_filmación: str):
    # Buscar la fila en el DataFrame que coincide con el título proporcionado
    pelicula = data[data['title'] == titulo_de_la_filmación]

 # Verificar si se encontró alguna película con el título dado
    if not pelicula.empty:
        cantidad_votos = pelicula['vote_count'].values[0]
        promedio_votos = pelicula['vote_average'].values[0]
        
         # Verificar si la película tiene al menos 2000 valoraciones
        if cantidad_votos >= 2000:
            return {
                'titulo': titulo_de_la_filmación,
                'cantidad_votos': cantidad_votos,
                'promedio_votos': promedio_votos
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="La película no cumple con la condición de tener al menos 2000 valoraciones."
            )
    else:
        raise HTTPException(status_code=404, detail="Título no encontrado")
        
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
        return {"message": f"No se encontró ninguna película con el título '{titulo}'."}

    # Crear una matriz TF-IDF para los títulos de las películas
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(data['title'])

    # Calcular la matriz de similitud de coseno
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Encontrar el índice de la película con el título dado
    idx = data[data['title'] == titulo].index[0]

    # Calcular las puntuaciones de similitud de todas las películas
    sim_scores = cosine_similarities[idx]

    # Obtener los índices de las 5 películas más similares, excluyendo la original
    sim_indices = sim_scores.argsort()[-6:-1][::-1]

    # Devolver los títulos de las películas más similares
    respuesta_recomendacion = data['title'].iloc[sim_indices].tolist()
    
    return {'lista_recomendada': respuesta_recomendacion}


# Ejecutar la aplicación con Uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)