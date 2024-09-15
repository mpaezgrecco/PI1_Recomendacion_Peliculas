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
7. Resultados y Conclusiones
8. Contribución y Colaboración
9. Licencia

### **Introduccion**
#### Este proyecto presenta una aplicación basada en una API que ofrece información detallada sobre películas y funcionalidades, como consultas y recomendaciones. Desarrollada utilizando el framework FastAPI, la aplicación permite a los usuarios acceder a datos estadísticos, como la cantidad de filmaciones en un mes, puntajes y número de votaciones, así como explorar información relacionada con actores y directores. Incluye un sistema de recomendación basado en la similitud de puntuaciones, géneros y títulos. Se llevó a cabo un análisis exploratorio de los datos y la aplicación fue desplegada en Render. Al final, se incluye un video que demuestra su funcionamiento y las consultas implementadas.

### Instalación y Requisitos
#### Requisitos:
- Python 3.11 
- pandas
- numpy
- matplotlib
- scikit-learn
- FastApi
- uvicorn 

#### Pasos de instalación:

- Clonar el repositorio: git clone https://github.com/mpaezgrecco/PI1_Recomendacion_Peliculas.git
- Crear un entorno virtual: python -m venv venv
- Activar el entorno virtual:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
- Instalar las dependencias: pip install -r requirements.txt

### Estructura del Proyecto
####
- data/: Contiene los archivos de datos utilizados en el proyecto 
- README.md: Archivo de documentación del proyecto.
- PI1_preparacion : Archivo donde se encuentra el proceso de ETL 
- PI1_EDA : Archivo donde se encuentra el analisis exploratorio de los datos
- main : Archivo donde se encuentra el codigo para crear la API de forma local utilizando fastAPI.
- sistema_de_recomendacion_ML: En este archivo se encuentra el 