import random as rd
import time
from aproximacion_bn import aproximacion_john_jellicoe
from batalla_naval_backtracking import batalla_naval_bt
from batalla_naval_lineal import batalla_naval_lineal

# Configuración inicial
SEED = "SUPER_RANDOM_SEED"
rd.seed(SEED)

# Función para medir el tiempo de ejecución de un algoritmo
def medir_tiempo(algoritmo, nombre, demandas_col, demandas_fil, long_barcos):
    inicio = time.time()

    if nombre == 'Backtracking':
        resultado, _ = algoritmo(len(demandas_col), len(demandas_fil), demandas_col, demandas_fil, long_barcos)
    else:
        resultado = algoritmo(demandas_col, demandas_fil, long_barcos)

    duracion = time.time() - inicio
    return duracion, resultado

# Función principal para ejecutar pruebas con volumen creciente
def pruebas_volumen():
    resultados = []
    
    # Tamaños crecientes para probar
    tamaños = [(100, 100, 10), (500, 500, 50), (1000, 1000, 200)]
    
    for max_col, max_fil, max_bar in tamaños:
        # Generar datos específicos para el tamaño
        demandas_col = [rd.randint(0, max_fil) for _ in range(max_col)]
        demandas_fil = [rd.randint(0, max_col) for _ in range(max_fil)]
        long_barcos = [rd.randint(0, max(max_fil, max_col)) for _ in range(max_bar)]
        
        # Probar cada algoritmo
        tiempos = {}
        
        for algoritmo, nombre in [
            (aproximacion_john_jellicoe, "Aproximación"),
            (batalla_naval_bt, "Backtracking"),
            (batalla_naval_lineal, "Lineal")
        ]:
            duracion, _ = medir_tiempo(algoritmo, nombre, demandas_col, demandas_fil, long_barcos)
            tiempos[nombre] = duracion
        
        # Guardar resultados
        resultados.append({
            "tamaño": (max_col, max_fil, max_bar),
            "tiempos": tiempos
        })
    
    return resultados

# Ejecutar las pruebas
resultados = pruebas_volumen()

# Imprimir resultados
print("Resultados de las pruebas:")
for resultado in resultados:
    tamaño = resultado["tamaño"]
    print(f"\nTamaño (Columnas: {tamaño[0]}, Filas: {tamaño[1]}, Barcos: {tamaño[2]})")
    for nombre, tiempo in resultado["tiempos"].items():
        print(f"  {nombre}: {tiempo:.4f} segundos")