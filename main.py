import os
import json
import csv
import requests
from datetime import datetime

def obtener_datos(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud web:", e)
        return None

def guardar_json(datos, ruta):
    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def procesar_paises(datos_crudos):
    paises_limpios = []
    for pais in datos_crudos:
        nombre = pais.get('name', {}).get('common', 'Desconocido')
        
        capitales = pais.get('capital', [])
        capital = capitales[0] if capitales else 'Sin capital'
        
        region = pais.get('region', 'Desconocida')
        poblacion = pais.get('population', 0)
        area = pais.get('area', 0)
        
        paises_limpios.append({
            'nombre': nombre,
            'capital': capital,
            'region': region,
            'poblacion': poblacion,
            'area': area
        })
    return paises_limpios

if __name__ == '__main__':
    carpeta = "datos_paises"
    os.makedirs(carpeta, exist_ok=True)
    
    url = "https://restcountries.com/v3.1/all?fields=name,capital,region,population,area,flags,languages,currencies,timezones,borders"
    ruta_json = os.path.join(carpeta, "paises.json")
    
    datos = obtener_datos(url)
    if datos:
        guardar_json(datos, ruta_json)
        datos_procesados = procesar_paises(datos)
        print(f"Se extrajeron y limpiaron los datos de {len(datos_procesados)} países.")
