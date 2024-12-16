
from os import path


def meter_barco_en_col(tablero, barco, col, demandas_col, demandas_fil): # O(Filas)
    "Mete el barco en la columna provista si encuentra un lugar valido"
    i = -1
    contador = 0
    for f in range(len(tablero)): # O(F)
        if tablero[f][col] + tablero[f][max(0,col-1)] + tablero[f][min(col+1,len(demandas_col)-1)] == 0:
            if demandas_fil[f] == 0:
                i = f
                contador = 0
            contador += 1
        else:
            contador = 0
            i = f+1
        if contador == barco + 2 or (i == 0 and contador == barco+1) or (f == len(tablero)-1 and contador == barco + 1):
            for f in range(barco): # O(b)
                tablero[i+1][col] = 1
                demandas_fil[i+1] -= 1
                i += 1
            demandas_col[col] -= barco
            return True
    return False

def meter_barco_en_fil(tablero, barco, fil, demandas_col, demandas_fil): # O(Columnas)
    "Mete el barco en la fila provista si encuentra un lugar valido"
    
    i = -1
    contador = 0
    for c in range(len(tablero[0])):
        if tablero[fil][c] + tablero[max(fil-1,0)][c] + tablero[min(fil+1, len(demandas_fil)-1)][c] == 0 and demandas_col[c] > 0:
            contador += 1
        else:
            contador = 0
            i = c+1
        if contador == barco + 2 or (i == -1 and contador == barco+1) or (c == len(tablero[0])-1 and contador == barco + 1):
            for c in range(barco):
                tablero[fil][i+1] = 1
                demandas_col[i+1] -= 1
                i += 1
            demandas_fil[fil] -= barco
            return True
    return False

def aproximacion_john_jellicoe(demandas_col: list,demandas_fil: list,long_barcos: list, modified = False):
    long_barcos.sort(reverse=True) # O(B*log(B))
    tablero = [[0 for c in range(len(demandas_col))] for f in range(len(demandas_fil))] # O(F*C)
    
    filas, columnas = list(range(len(demandas_fil))), list(range(len(demandas_col))) # O(F + C)
    
    while filas or columnas: # O(Min(F+C, B))
        es_col = True
        max_dem, index = 0, 0
        for f in filas: # O(Filas)
            if demandas_fil[f] > max_dem:
                max_dem, index = demandas_fil[f], f
                es_col = False
        for c in columnas: # O(Columnas)
            if demandas_col[c] > max_dem:
                max_dem, index = demandas_col[c], c
                es_col = True
        if max_dem == 0:
            return tablero
        
        entro = False
        for barco in long_barcos: # O(Barcos)
            if barco > max_dem: 
                continue
            
            # O( Max(F,C) )
            entro = meter_barco_en_col(tablero, barco, index, demandas_col, demandas_fil) if es_col else meter_barco_en_fil(tablero, barco, index,demandas_col, demandas_fil)
            
            # O(Barcos)
            if entro:
                long_barcos.remove(barco) 
                if len(long_barcos) == 0:
                    return tablero
                break

        # O(Max(F,C))
        if not entro:
            if not modified: return tablero
            if es_col:
                columnas.remove(index)
            else:
                filas.remove(index)
    
    return tablero

### Mediciones de aproximación

def extraer_listas(path):
    """
    Lee un archivo en el formato especificado y extrae tres listas de enteros.
    
    :param path: Ruta al archivo.
    :return: Tres listas de enteros.
    """
    with open(path, 'r') as archivo:
        # Saltar las dos primeras líneas irrelevantes
        next(archivo)
        next(archivo)
        
        # Leer todas las líneas restantes
        lineas = archivo.readlines()
    
    # Eliminar caracteres de salto de línea y espacios adicionales
    lineas = [linea.strip() if linea.strip() else '' for linea in lineas]
    
    # Separar las líneas en las tres listas
    listas = []
    temp_lista = []
    
    for linea in lineas:
        if linea == '':  # Línea en blanco
            if temp_lista:
                listas.append(temp_lista)
                temp_lista = []
        else:
            temp_lista.append(int(linea))
    
    # Agregar la última lista, si no se agregó aún
    if temp_lista:
        listas.append(temp_lista)
    
    # Retornar las tres listas
    if len(listas) != 3:
        raise ValueError("El archivo no tiene exactamente tres listas separadas por líneas en blanco.")
    
    return listas[0], listas[1], listas[2]



def medir_aproximacion_a_optimos():
    resultados_optimos = [4,12,26,6,40,46,40,104,172,202]
    paths = "TDA_TP3/archivos_catedra/3_3_2.txt TDA_TP3/archivos_catedra/5_5_6.txt TDA_TP3/archivos_catedra/8_7_10.txt TDA_TP3/archivos_catedra/10_3_3.txt TDA_TP3/archivos_catedra/10_10_10.txt TDA_TP3/archivos_catedra/12_12_21.txt TDA_TP3/archivos_catedra/15_10_15.txt TDA_TP3/archivos_catedra/20_20_20.txt TDA_TP3/archivos_catedra/20_25_30.txt TDA_TP3/archivos_catedra/30_25_25.txt".split()
    rs = []
    for i, p in enumerate(paths):
        filas, columnas, barcos = extraer_listas(p)
        solucion_aproximada = aproximacion_john_jellicoe(columnas, filas, barcos)
        demanda_cubierta = sum([sum(fila) for fila in solucion_aproximada])*2
        opt = resultados_optimos[i]
        r = opt/demanda_cubierta 
        rs.append(r)
        print(f"El algoritmo logró cubrir {demanda_cubierta} puntos de {opt} de la demanda del {path.basename(p)}, hay una relacion de {r}")
    mean = sum(rs)/len(rs)
    print(f"En promedio, se logró una aproximacion a los óptimos de {mean}")

if __name__ == "__main__":
    import random as rd
    def prueba_volumen_random(seed, n_col, n_fil, n_bar):
        rd.seed(seed)
        demandas_col = [rd.randint(0,n_fil) for _ in range(n_col)]
        demandas_fil = [rd.randint(0,n_col) for _ in range(n_fil)]
        long_barcos = [rd.randint(0,max(n_fil,n_col)) for _ in range(n_bar)]
        solucion_aprox1 = aproximacion_john_jellicoe(demandas_col.copy(),demandas_fil.copy(),long_barcos.copy(),True)
        solucion_aprox2 = aproximacion_john_jellicoe(demandas_col,demandas_fil,long_barcos,False)
        demanda_cubierta1 = sum([sum(fila) for fila in solucion_aprox1])*2
        demanda_cubierta2 = sum([sum(fila) for fila in solucion_aprox2])*2
        demanda_total = sum(demandas_col) + sum(demandas_fil)
        print(f"El algoritmo aproximado modificado pudo cubrir {demanda_cubierta1} de {demanda_total} de demanda total")
        print(f"El algoritmo aproximado pudo cubrir {demanda_cubierta2} de {demanda_total} de demanda total")


    # prueba_volumen_random(42, 1000, 1000, 200)