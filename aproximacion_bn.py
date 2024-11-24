
def meter_barco_en_col(tablero, barco, col, demandas_col, demandas_fil): # O(Filas)
    "Mete el barco en la columna provista si encuentra un lugar valido"
    i = -1
    contador = 0
    for f in range(len(tablero)): # O(F)
        if tablero[f][col] + tablero[f][max(0,col-1)] + tablero[f][min(col+1,len(demandas_col)-1)] == 0 and demandas_fil[f] > 0:
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
        if contador == barco + 2 or (i == 0 and contador == barco+1) or (c == len(tablero[0])-1 and contador == barco + 1):
            for c in range(barco):
                tablero[fil][i+1] = 1
                demandas_col[i+1] -= 1
                i += 1
            demandas_fil[fil] -= barco
            return True
    return False


def aproximacion_john_jellicoe(demandas_col: list,demandas_fil: list,long_barcos: list):
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
            if es_col:
                columnas.remove(index)
            else:
                filas.remove(index)
    
    return tablero
