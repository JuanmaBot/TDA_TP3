import random as rd
import time
from aproximacion_bn import aproximacion_john_jellicoe
from batalla_naval_backtracking import batalla_naval_bt
from batalla_naval_lineal import batalla_naval_lineal
import matplotlib.pyplot as plt

# Configuración inicial
SEED = 42
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

def aprox_mod(demandas_col, demandas_fil, long_barcos):
    return aproximacion_john_jellicoe(demandas_col, demandas_fil, long_barcos, True)

def medir_y_graficar_tiempos():
    algoritmos = [
        (aproximacion_john_jellicoe, "Aproximacion"),
        (aprox_mod, "Aproximacion_mod"),
        (batalla_naval_bt, "Backtracking"),
        (batalla_naval_lineal, "Lineal")
    ]
    max_dim = 150
    demandas_col = [rd.randint(0, max_dim) for _ in range(max_dim)]
    demandas_fil = [rd.randint(0, max_dim) for _ in range(max_dim)]
    long_barcos = [rd.randint(1, max_dim) for _ in range(max_dim)]

    print(demandas_col)
    print(demandas_fil)
    print(long_barcos)

    resultados_tamanos = {alg[1]: [] for alg in algoritmos}
    resultados_barcos = {alg[1]: [] for alg in algoritmos}

    # Variar columnas
    for cols in range(1, max_dim + 1):
        
        for algoritmo, nombre in algoritmos:
            print(f"Probando {nombre} con {cols} columnas")
            duracion, _ = medir_tiempo(algoritmo, nombre, demandas_col[0:cols].copy(), demandas_fil[0:cols].copy(), long_barcos.copy())
            resultados_tamanos[nombre].append(duracion)

    # Variar barcos
    for barcos in range(1, max_dim + 1):
        
        for algoritmo, nombre in algoritmos:
            print(f"Probando {nombre} con {barcos} barcos")
            duracion, _ = medir_tiempo(algoritmo, nombre, demandas_col.copy(), demandas_fil.copy(), long_barcos[0:barcos].copy())
            resultados_barcos[nombre].append(duracion)

    # Graficar resultados
    x = list(range(1, max_dim + 1))

    # Gráfico 1: Tiempo vs Tamaños
    plt.figure(figsize=(10, 6))
    for nombre, tiempos in resultados_tamanos.items():
        plt.plot(x, tiempos, label=nombre)
        plt.title("Tiempo vs Cantidad de Columnas")
        plt.xlabel("Cantidad de Columnas")
        plt.ylabel("Tiempo (s)")
        plt.legend()
        plt.grid()
        plt.savefig(f"graficos/{nombre}/tiempo_vs_tam.png")
        plt.close()

    # Gráfico 2: Tiempo vs Barcos
    plt.figure(figsize=(10, 6))
    for nombre, tiempos in resultados_barcos.items():
        plt.plot(x, tiempos, label=nombre)
        plt.title("Tiempo vs Cantidad de Barcos")
        plt.xlabel("Cantidad de Barcos")
        plt.ylabel("Tiempo (s)")
        plt.legend()
        plt.grid()
        plt.savefig(f"graficos/{nombre}/tiempo_vs_barcos.png")
        plt.close()


# Llamar a la función
medir_y_graficar_tiempos()