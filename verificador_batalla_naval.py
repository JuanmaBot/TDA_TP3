def verificador_batalla_naval(solucion, long_barcos, restricciones_col, restricciones_fil):
    if len(long_barcos) > len(solucion)*len(solucion[0]):
        return False
    aux_r_col = [0]*(len(restricciones_col)) # O(col)
    aux_r_fil = [0]*(len(restricciones_fil)) # O(fil)
    barcos_visitados = set()
    tamanos = []
    for n_fil in range(len(solucion)): # O(fil)
        for n_col in range(len(solucion[0])): # O(col)
            if not solucion[n_fil][n_col]: # Si no hay barco paso de largo
                continue
            if (n_fil,n_col) in barcos_visitados: # Si ya vi este barco antes paso de largo
                continue
            # Tengo que encontrar el resto del barco
            tam_barco_valido = descubrir_barco(solucion, barcos_visitados, aux_r_col, aux_r_fil, n_fil, n_col) # O(long_barco_i + cant_barcos)
            if not tam_barco_valido:
                return False
            tamanos.append(tam_barco_valido)
    
    if aux_r_col != restricciones_col or aux_r_fil != restricciones_fil: # O(col + fil)
        return False
    
    barcos = {}
    for b in long_barcos: # O(barcos)
        barcos[b] = 1 if b not in barcos else barcos[b] + 1
    
    for t in tamanos: # O(barcos)
        if t not in barcos:
            return False
        elif barcos[t] == 1:
            del barcos[t]
        else:
            barcos[t] -= 1

    if len(barcos) != 0:
        return False
    
    return True

def descubrir_barco(solucion, barcos_visitados, aux_r_col, aux_r_fil, n_fil, n_col):
    ult_columna, ult_fila = len(solucion[0])-1, len(solucion)-1
    tam = 0
    horizontal = n_fil == ult_fila or not solucion[n_fil+1][n_col]

    # Ciclo para encontrar tamaño, guardarlos en visitados, y actualizar restricciones de columnas
    while True:
        tam += 1
        barcos_visitados.add((n_fil,n_col))
        aux_r_col[n_col] += 1
        aux_r_fil[n_fil] += 1

        if horizontal:
            if (n_fil > 0 and solucion[n_fil-1][n_col] == 1) or (n_fil < ult_fila and solucion[n_fil+1][n_col]):
                # Si hay un barco arriba o abajo la solucion es invalida
                return 0
            if n_col == ult_columna or not solucion[n_fil][n_col+1]: # Si a su derecha no hay un barco termino
                break
            n_col += 1
        else:
            if (n_col > 0 and solucion[n_fil][n_col-1] == 1) or (n_col < ult_columna and solucion[n_fil][n_col+1] == 1):
                # Si hay un barco a alguno de sus lados la solucion es invalida
                return 0
            if n_fil == ult_fila or not solucion[n_fil+1][n_col]: # Si abajo no hay un barco termino
                break
            n_fil += 1
    
    # Falta ver si se toca con otro barco en los extremos
    if horizontal:
        if n_col < ult_columna and (solucion[n_fil][n_col+1] or solucion[min(n_fil+1,ult_fila)][n_col+1] or solucion[max(n_fil-1,0)][n_col+1]):
            return 0
        if n_col - tam >= 0 and (solucion[n_fil][n_col-tam] or solucion[min(n_fil+1,ult_fila)][n_col-tam] or solucion[max(n_fil-1,0)][n_col-tam]):
            return 0
    else:
        if n_fil < ult_fila and (solucion[n_fil+1][n_col] or solucion[n_fil+1][min(ult_columna,n_col+1)] or solucion[n_fil+1][max(0,n_col-1)]):
            return 0
        if n_fil - tam >= 0 and (solucion[n_fil-tam][n_col] or solucion[n_fil-tam][min(ult_columna,n_col+1)] or solucion[n_fil+1][max(0,n_col-1)]):
            return 0
    
    return tam


solucion = [
    [0,0,0,0,1,1,1,0,0,0],
    [1,0,0,0,0,0,0,0,1,0],
    [0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,0],
    [0,1,0,1,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,1,0,1,0],
    [0,0,0,1,1,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0],
]
# l_barcos = [3,1,1,2,4,2,1,2,1,3]
# restricciones_filas = [3,2,2,4,2,1,1,2,3,0]
# restricciones_columnas = [1,2,1,3,2,2,3,1,5,0]
# print(verificador_batalla_naval(solucion,l_barcos,restricciones_columnas,restricciones_filas))


"""
La complejidad de este algoritmo es polinomica sobre los parametros que toma ya que chequea todos los casilleros de la solucion 1 o como mucho 2 veces
cuando forman parte de un barco y luego cuenta la cantidad de barcos que debe haber y chequea que sea el mismo dato obtenido. Luego hace otras operaciones 
lineales como construir y comparar los arreglos de restricciones de columnas y filas.

Por lo tanto la complejidad de este algoritmo seria O( K*(col + fil) + K'*col*fil + K''*(barcos) ) pero las constantes desaparecen, barcos nunca puede ser 
mas grande que col*fil, y tendiendo a infinito col*fil es mucho mas grande que col+fil, por lo tanto queda en O(col*fil) polinomial.

Al implementar este verificador eficiente, se demuestra que batalla naval infividual es un problema NP.
"""