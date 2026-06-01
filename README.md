# Proyecto_web_requests-y-stdlib
Proyecto orientado al uso y aplicación de peticiones en la web y librerías estándar de Python.
# Cliente de Datos Abiertos con Python

Proyecto de la asignatura Programación de Computadores 2026-1 — Universidad Nacional de Colombia.

El programa consulta la API pública de países [restcountries.com](https://restcountries.com), descarga la información de 250 países y genera tres archivos locales: un JSON con la respuesta completa, un CSV con los datos limpios y un reporte de texto con estadísticas básicas.

## Requisitos

- Python 3.x
- Librería `requests`:

```
pip install requests
```

## Uso

```
python main.py
```

Al ejecutarlo se crea automáticamente la carpeta `datos_paises/` con los siguientes archivos:

```
datos_paises/
├── paises.json   ← respuesta completa de la API
├── paises.csv    ← campos relevantes de cada país
└── reporte.txt   ← país más poblado y de mayor área
```

## Estructura del código

| Función | Descripción |
|---|---|
| `obtener_datos(url)` | Hace la petición GET con manejo de errores |
| `guardar_json(datos, ruta)` | Guarda la respuesta cruda en JSON |
| `procesar_paises(datos_crudos)` | Extrae nombre, capital, región, población y área |
| `guardar_csv(datos, ruta)` | Exporta los datos limpios a CSV |
| `calcular_estadisticas(datos_procesados)` | Determina el país más poblado y el de mayor área |
| `generar_reporte(estadisticas, ruta)` | Escribe el reporte con fecha de generación |
