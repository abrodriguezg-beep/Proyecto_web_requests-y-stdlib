# Informe — Proyecto: Cliente de Datos Abiertos con Python
**Programación de Computadores 2026-1**  
**Universidad Nacional de Colombia**

---

## 1. Descripción del programa

El programa se conecta a la API pública de países `restcountries.com` y descarga información de 250 países. A partir de esa respuesta construye tres archivos: un JSON con los datos crudos, un CSV con los campos que nos interesan y un reporte de texto con estadísticas básicas.

La organización del código sigue una lógica de etapas: primero se hace la petición, luego se guarda lo que llegó, después se filtra lo que necesitamos, se exporta al CSV y finalmente se calculan estadísticas y se genera el reporte. Cada etapa está encapsulada en su propia función para que sea más fácil encontrar dónde falla algo si hay un error. El programa principal vive dentro del bloque `if __name__ == '__main__'`, lo que significa que las funciones se pueden importar desde otro archivo sin que se ejecute todo automáticamente.

La carpeta `datos_paises/` se crea con `os.makedirs(carpeta, exist_ok=True)`, que tiene la ventaja de no lanzar un error si la carpeta ya existe — algo que aprendimos que pasa seguido cuando se corre el programa más de una vez.

---

## 2. Explicación de las funciones

### `obtener_datos(url)`

Recibe la URL de la API y devuelve los datos en formato de lista de diccionarios Python (ya deserializados). Internamente usa `requests.get()` y luego llama a `.raise_for_status()` antes de devolver nada. Esa línea es la que detecta los errores HTTP como un 404 o un 500 sin tener que revisar el código de estado manualmente. Si algo falla, el `except` atrapa el error y devuelve `None` en lugar de detener el programa.

### `guardar_json(datos, ruta)`

Toma la lista de países que devolvió `obtener_datos` y la escribe en el archivo `paises.json` usando `json.dump`. El parámetro `indent=4` genera el archivo con sangría para que sea legible si alguien lo abre directamente. El parámetro `ensure_ascii=False` fue importante porque sin él los caracteres como tildes o la `ñ` se guardaban como secuencias de escape (`ó` en lugar de `ó`), que tecnicamente son equivalentes pero hacen el archivo muy difícil de leer.

### `procesar_paises(datos_crudos)`

Esta es la función más importante del procesamiento. Recorre la lista completa de países y de cada uno extrae únicamente cinco campos: nombre, capital, región, población y área.

El nombre no se obtiene directamente sino que está anidado dentro de un diccionario `name` como `name.common`. Para manejarlo usamos `.get('name', {}).get('common', 'Desconocido')`, que encadena dos `.get()` para no lanzar un `KeyError` si algún país no trae esa estructura.

La capital viene como lista en la API porque algunos países tienen más de una. Decidimos quedarnos solo con la primera: `capitales[0] if capitales else 'Sin capital'`. Esto cubre el caso de territorios sin capital oficial, que sí existen en los datos.

Para población y área, si el campo no existe en el diccionario del país, se reemplaza por `0` en lugar de un texto como `'Desconocido'` porque más adelante `calcular_estadisticas` necesita comparar esos valores numéricamente.

### `guardar_csv(datos, ruta)`

Recibe la lista de diccionarios limpios que generó `procesar_paises` y los escribe en `paises.csv`. Usamos `csv.DictWriter` porque ya tenemos los datos como diccionarios, entonces es más directo que usar `csv.writer` y armar cada fila a mano. El `newline=''` al abrir el archivo evita que en Windows se inserte una línea en blanco entre cada fila.

### `calcular_estadisticas(datos_procesados)`

Recorre la lista de países procesados y encuentra el de mayor población y el de mayor área usando `max()` con una función `lambda` como criterio de comparación. El resultado es un diccionario con dos entradas que se pasa directamente a `generar_reporte`.

### `generar_reporte(estadisticas, ruta)`

Toma el diccionario de estadísticas, construye un texto con los resultados y la fecha y hora actuales, y lo escribe en `reporte.txt`. La fecha se obtiene con `datetime.now().strftime('%Y-%m-%d %H:%M:%S')`. Los números se formatean con `:,` para que aparezcan con separadores de miles (por ejemplo `1,417,492,000`) y el área con `:.0f` para no mostrar decimales innecesarios.

---

## 3. Manejo de errores

El único punto donde el programa puede fallar de forma externa — es decir, por algo que está fuera de nuestro control — es la petición a la API. Eso lo manejamos con un bloque `try/except` dentro de `obtener_datos`. Capturamos `requests.exceptions.RequestException`, que es la clase base de todos los errores de la librería `requests`, así que cubre tanto problemas de conexión (sin internet, timeout) como errores del servidor (4xx, 5xx).

Si la petición falla, la función imprime el error y devuelve `None`. En el programa principal, antes de continuar con cualquier otra etapa, se verifica que `datos` no sea `None` con un `if datos:`. Si es `None`, el programa simplemente no entra al bloque y termina sin generar archivos a medias.

Para las operaciones de escritura de archivos no pusimos `try/except` adicionales porque en ese punto ya tenemos los datos en memoria y el único fallo posible sería de permisos del sistema operativo, que es un problema del entorno más que del programa.

---

## 4. Dificultades y conclusiones

La primera dificultad fue entender la estructura del JSON que devuelve la API. Al principio asumimos que los campos vendrían todos al mismo nivel, pero al explorarlo nos dimos cuenta de que el nombre del país está dentro de un diccionario `name`, y la capital viene como lista. Eso nos obligó a revisar la documentación de `restcountries.com` y a usar el doble `.get()` encadenado para acceder de forma segura a campos anidados.

Otro problema que nos tomó tiempo fue el archivo CSV con saltos de línea dobles. Al principio no teníamos el `newline=''` al abrir el archivo y en Windows cada fila terminaba con una línea en blanco. Revisando la documentación de Python sobre el módulo `csv` encontramos que ese parámetro es el que controla ese comportamiento.

También nos costó entender la diferencia entre `json.dump` (para escribir en un archivo) y `json.dumps` (para obtener un string). Al principio usamos el incorrecto y el programa fallaba porque intentaba escribir un string en lugar de serializar el objeto directamente.

En general el proyecto nos ayudó a ver que trabajar con APIs no es solo hacer un `requests.get()` y listo — hay que entender la estructura de lo que llega, manejar los casos en que faltan campos y pensar en qué pasa si la conexión falla. El uso de `os.path.join` para construir rutas también fue algo nuevo; antes hubiéramos concatenado los strings directamente con `/`, que no funciona igual en todos los sistemas operativos.
