import os
import json
import csv
import requests
from datetime import datetime

def obtener_datos(url):
    """ 
    Me encargo de realizar la petición a la API pública. Decidí implementar
    un bloque de manejo de errores porque confiar a ciegas en la conexión a
    internet es una mala práctica.
    """
    try:
        respuesta = requests.get(url)
        # Esta línea valida la conexión de forma mucho más eficiente que un if manual
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud web:", e)
        return None

def guardar_json(datos, ruta):
    """
    Tomo la información descargada y la respaldo en un documento de texto.
    Mi prioridad aquí fue asegurar que los caracteres especiales se guarden
    correctamente.
    """
    # Abro el archivo normalmente en modo escritura.
    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def procesar_paises(datos_crudos):
    """
    Filtro la inmensa cantidad de datos crudos para extraer únicamente los campos
    solicitados.
    """
    paises_limpios = []
    for pais in datos_crudos:
        # Busco el nombre común anidado, si la estructura falla, devuelvo Desconocido
        nombre = pais.get('name', {}).get('common', 'Desconocido')
        
        # Extraigo la lista de capitales y me quedo con la primera si es que hay alguna
        capitales = pais.get('capital', [])
        capital = capitales[0] if capitales else 'Sin capital'
        # Aquí preferí reemplazar para los datos de tipo numérico (población y área), en caso de que no haya algún número, por 0, aunque Desconocida también funciona
        region = pais.get('region', 'Desconocida')
        poblacion = pais.get('population', 0)
        area = pais.get('area', 0)
        # Empaqueto la información filtrada y la agrego a mi lista final
        paises_limpios.append({
            'nombre': nombre,
            'capital': capital,
            'region': region,
            'poblacion': poblacion,
            'area': area
        })
    return paises_limpios

if __name__ == '__main__':
    # Defino la estructura inicial usando una instrucción que ignora si la carpeta ya existe
    carpeta = "datos_paises"
    os.makedirs(carpeta, exist_ok=True)
    
    # Almaceno la ruta de la API y construyo la ruta del archivo uniendo los nombres
    url = "https://restcountries.com/v3.1/all?fields=name,capital,region,population,area,flags,languages,currencies,timezones,borders"
    ruta_json = os.path.join(carpeta, "paises.json")
    print("Iniciando petición web...")
    # Ejecuto el flujo de trabajo comprobando que los datos realmente existan antes de guardar
    datos = obtener_datos(url)
    if datos:
        guardar_json(datos, ruta_json)
        datos_procesados = procesar_paises(datos)
        print(f"Se extrajeron y limpiaron los datos de {len(datos_procesados)} países.")
