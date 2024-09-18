# **PROYECTO INDIVIDUAL Nº1**

## Machine Learning Operations (MLOps)
### **Descripción**
#### El Proyecto Individual 1 es una API desarrollada con FastAPI que ofrece datos estadísticos, consultas, y recomendaciones personalizadas de películas. Permite explorar información detallada de filmaciones, actores y directores, con un sistema de recomendación basado en puntajes, géneros y títulos.

### **Tabla de contenido**
#### 
1. Introduccion 
2. Instalación y Requisitos
3. Estructura del Proyecto
4. Uso y Ejecución
5. Datos y Fuentes
6. Metodología
7. Funciones desarrolladas
8. Resultados y Conclusiones
9. Pagina Web API
10. Video 
11. Autor 

### **1. Introduccion**
#### Este proyecto presenta una aplicación basada en una API que ofrece información detallada sobre películas y funcionalidades, como consultas y recomendaciones. Desarrollada utilizando el framework FastAPI, la aplicación permite a los usuarios acceder a datos estadísticos, como la cantidad de filmaciones en un mes, puntajes y número de votaciones, así como explorar información relacionada con actores y directores. Incluye un sistema de recomendación basado en la similitud de puntuaciones, géneros y títulos. Se llevó a cabo un análisis exploratorio de los datos y la aplicación fue desplegada en Render. Al final, se incluye un video que demuestra su funcionamiento y las consultas implementadas.

### *2.Instalación y Requisitos*
#### Requisitos:
- Python 3.11 
- pandas
- numpy
- matplotlib
- scikit-learn
- FastApi
- uvicorn 

#### *Pasos de instalación:*

- Clonar el repositorio: git clone https://github.com/mpaezgrecco/PI1_Recomendacion_Peliculas.git
- Crear un entorno virtual: python -m venv venv
- Activar el entorno virtual:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
- Instalar las dependencias: pip install -r requirements.txt

### *3. Estructura del Proyecto*
####
- data/: Contiene los archivos de datos utilizados en el proyecto 
- README.md: Archivo de documentación del proyecto.
- PI1_preparacion : Archivo donde se encuentra el proceso de ETL 
- PI1_EDA : Archivo donde se encuentra el analisis exploratorio de los datos
- main : Archivo donde se encuentra el codigo para crear la API de forma local utilizando fastAPI.
- sistema_de_recomendacion_ML: En este archivo se encuentra el modelo de machine learning con un sistema de recomendación de películas.

### *4. Uso y Ejecución*
#### Antes de comenzar a ejecutar este proyecto es necesario descargar los datos completos, para eso descarga en la misma carpeta donde ejecutaras el proyecto los archivos "movies_dataset.csv" y "credits.csv. 
sigue los pasos que te indico acontinuacion: 
1. Ejecutar: PI1_Preparacion_los_datos.ipynb
Este notebook contiene el proceso detallado de preparación de datos y el flujo ETL. Genera los archivos "movies_dataset_parte1.csv" y "movies_dataset_parte2.csv", divididos para cumplir con el límite de 25MB de GitHub, y "dataset_ML.csv", que contiene 9000 registros para minimizar el uso de memoria RAM, adaptándose al límite de 512MB de la versión gratuita de Render.

2. Ejecutar: PI1_EDA.ipynb
En este notebook se realiza el análisis exploratorio de los datos (EDA), con visualizaciones gráficas y algunas de palabras de los títulos que nos ayudaran a investigar las relaciones que hay entre las variables de los datasets

3. Ejecutar: main.py
Este script contiene el código para crear y ejecutar la API localmente utilizando FastAPI.

4. Deployment
Para realizar el deployment utilice Render para poder utilizar la API en una pagina web. 

### *5. Datos y Fuentes*

#### Los datos utilizados en este proyecto provienen de la base de datos proporcionada por Henry. Los datos incluyen información sobre peliculas, directores, actores, entre otros. Los archivos de datos se encuentran en la carpeta [data/](https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5) en formato CSV.

### *6. Metodología*

####
- *Preparación y exploracion de Datos* 
Se llevó a cabo un proceso de preparación de los datos, generando el archivo dataset_ML.csv que contiene 9000 registros para minimizar el uso de memoria RAM y ajustarse al límite de 512MB de la versión gratuita de Render. El conjunto de datos fue limpiado y preparado para su uso, implementando técnicas de análisis exploratorio para identificar relaciones entre variables y detectar posibles outliers o anomalías.

- *Creación de la API*
Para la creación de la API, se siguieron los siguientes pasos clave:
 1. Carga y Transformación de Datos:
 - El archivo dataset_ML.csv se cargó en un DataFrame de pandas
 - Se transformaron columnas relevantes, como 'name_genres', en un formato adecuado para el procesamiento,convirtiendo listas de géneros en cadenas de texto concatenadas.

 2. Ingeniería de Características para Recomendaciones:
 - Se implementó un sistema de recomendación utilizando un vectorizador TF-IDF para los títulos de las películas.
 - Se utilizaron palabras clave personalizadas para mejorar el procesamiento del texto.
 - Se aplicó la similitud del coseno para calcular puntajes de similitud entre títulos y generar recomendaciones.

 3. Desarrollo de Endpoints:
 Utilizando FastAPI, se crearon endpoints que ofrecen distintas funcionalidades:
 - Cantidad de películas: Endpoints para consultar la cantidad de películas estrenadas por mes o día.
 - Puntajes y votos: Recuperar el puntaje, cantidad de votos y promedio de votaciones para un título.
 - Consultas de actores y directores: Proveer estadísticas como número total de películas y retorno promedio.
 - Recomendaciones: Un endpoint que proporciona una lista de películas recomendadas basadas en similitud de títulos.

 4. Manejo de Errores y Validación:
 - Se integró el manejo básico de errores para gestionar entradas inválidas, garantizando un funcionamiento fluido.
 - Validación de entradas, como nombres de meses y días en español, para asegurar respuestas precisas.

#### *Despliegue*
#### La API se configuró para ejecutarse localmente con Uvicorn, permitiendo pruebas y desarrollo antes del despliegue en un entorno de producción, como la plataforma Render. Esta metodología estructurada garantiza una API eficiente y capaz de manejar diversas consultas relacionadas con películas, preservando la integridad de los datos y proporcionando respuestas claras ante errores.

### *7. Funciones desarrolladas*
####
1. Función: Cantidad de filmaciones estrenadas por mes
Recibe un mes en español como parámetro, lo convierte a minúsculas y verifica su validez. Luego, mapea el mes al formato en inglés, filtra las películas estrenadas en dicho mes y devuelve la cantidad en un mensaje formateado.
2. Función: Cantidad de filmaciones estrenadas por día de la semana
Recibe un día en español, lo valida y convierte a minúsculas. Cuenta las películas estrenadas en ese día comparando la fecha de estreno en el DataFrame con el día consultado. Devuelve el total en un mensaje formateado.
3. Función: Puntaje de la filmación
Recibe el título de una película, lo busca en el DataFrame y, si existe, obtiene el título, año de estreno y puntaje. Devuelve esta información formateada. Si la película no se encuentra, indica "Película no encontrada".
4. Función: Cantidad de votos y promedio de votaciones de la filmación
Recibe el título de una película, lo busca en el DataFrame y obtiene la cantidad de votos, promedio de votaciones y año de estreno. Si tiene al menos 2000 votos, devuelve esta información; si no, indica que no cumple con la condición.
5. Función: Éxito de un actor
Recibe el nombre de un actor, busca las películas en las que ha participado, y calcula el número de películas, retorno total y promedio de retorno. Devuelve un diccionario con esta información. Si el actor no aparece en el dataset, devuelve un mensaje indicándolo.
6. Función: Éxito de un director
Recibe el nombre de un director, busca sus películas en el DataFrame y calcula el retorno total. Para cada película, obtiene el título, fecha de lanzamiento, retorno individual, costo y ganancia, y lo almacena en una lista. Devuelve un diccionario con el retorno total y la información de cada película. Si el director no se encuentra, lo indica.
7. Función: Recomendación de películas
Recibe el título de una película y recomienda 5 películas similares. Verifica la existencia del título, calcula la similitud utilizando TF-IDF y la similitud del coseno, y devuelve una lista de las 5 películas más similares.


### *8.Resultados y Conclusiones* 

#### 
- El analisis de los resultados revelo que la mayoría de las películas se estrenan a principios y finales de semana, especialmente los viernes, alineándose con las estrategias de marketing para maximizar la audiencia durante el fin de semana.
- En términos de meses, enero y los meses de otoño son épocas populares para los estrenos, mientras que los meses de verano muestran una disminución, posiblemente debido a las vacaciones y menor asistencia al cine.
- Estos patrones pueden ser útiles para estudios de mercado y planificación estratégica de estrenos en la industria cinematográfica.
- La API proporciona puntajes de popularidad y cantidades de votos para películas individuales. Esto puede llevar a conclusiones sobre qué tipos de películas tienden a ser más populares.
- La API permite obtener el retorno total y promedio de un actor en función de las películas en las que ha participado. Los resultados podrían mostrar qué actores tienen mayor impacto en la taquilla, lo cual puede ser útil para estudios de mercado y estrategias de casting
- La API proporciona estadísticas sobre directores, incluyendo el retorno total y detalles de cada película dirigida. Esto puede ayudar a identificar a los directores más exitosos en términos de retorno de inversión y determinar si ciertos directores tienden a trabajar en películas más rentables.
-  La capacidad de la API para recomendar películas basadas en similitudes puede ser una herramienta valiosa para personalizar experiencias de usuario. Las recomendaciones efectivas pueden mejorar el compromiso del usuario en plataformas de contenido.

### *9. Pagina Web API*

#### https://pi1-recomendacion-peliculas.onrender.com/docs#/

### *10. Video*

#### https://www.youtube.com/watch?v=9PZ-XpwXByo

####

### *11. Autor*

#### Este proyecto fue realizado por: Maria Jose Paez Grecco 
#### Mail: mpaezgrecco@gmail.com
#### Linkedin: [Linkedin_MariaJosePaezGrecco](https://www.linkedin.com/in/maria-jose-paez-grecco-78a155192/)