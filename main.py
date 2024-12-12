import sys
from aproximacion_bn import extraer_listas, aproximacion_john_jellicoe
from batalla_naval_backtracking import batalla_naval_bt
from batalla_naval_lineal import batalla_naval_lineal

def main():
    """
    Lee un archivo en el formato especificado y ejecuta los algoritmos de solucion de batalla naval dependiendo el segundo parametro dado.
    
    El segundo parametro puede ser:
    - `aproximacion` para ejecutar la aproximacion de la batalla naval.
    - `aproximacion_mod` para ejecutar la aproximacion modificada de la batalla naval.
    - `lineal` para ejecutar la solucion lineal de la batalla naval.
    - `backtracking` para ejecutar la solucion de backtracking de la batalla naval.
    """
    path = sys.argv[1]
    demandas_col, demandas_fil, long_barcos = extraer_listas(path)

    tipo = sys.argv[2]
    if tipo == 'aproximacion':
        tablero = aproximacion_john_jellicoe(demandas_col, demandas_fil, long_barcos)
    elif tipo == 'lineal':
        tablero = batalla_naval_lineal(demandas_col, demandas_fil, long_barcos)
    elif tipo == 'backtracking':
        tablero, _ = batalla_naval_bt(len(demandas_fil), len(demandas_col), demandas_fil, demandas_col, long_barcos)
    elif tipo == 'aproximacion_mod':
        tablero = aproximacion_john_jellicoe(demandas_col, demandas_fil, long_barcos, True)
    else:
        print(f"No implementamos {tipo} jeje, elegi uno de estos --> ['aproximacion', 'aproximacion_mod', 'lineal', 'backtracking']")
        return
    print(tablero)

if __name__ == "__main__":
    main()