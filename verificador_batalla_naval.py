def verificador_batalla_naval(solucion, long_barcos, restricciones_col, restricciones_fil):
    aux_r_col = [0]*(len(restricciones_col)-1)
    aux_r_fil = [0]*(len(restricciones_fil)-1)
    barcos_visitados = set()
    for n_fil in range(len(solucion)):
        for n_col in range(len(solucion[0])):
            if not solucion[n_fil][n_col]: # Si no hay barco paso de largo
                continue
            if (n_fil,n_col) in barcos_visitados: # Si ya vi este barco antes paso de largo
                continue
            # Tengo que encontrar el resto del barco
            tam_barco_valido = descubrir_barco(solucion, barcos_visitados, aux_r_col, aux_r_fil, n_fil, n_col)


def descubrir_barco(solucion, barcos_visitados, aux_r_col, aux_r_fil, n_fil, n_col):
    tam = 0
    horizontal = n_fil == len(solucion)-1 or not solucion[n_fil+1][n_col]

    # Ciclo para encontrar tamaño, guardarlos en visitados, y actualizar restricciones de columnas
    while True:
        tam += 1
        barcos_visitados.add((n_fil,n_col))
        aux_r_col[n_col] += 1
        aux_r_fil[n_fil] += 1

        if horizontal:
            if n_col + 1 == len(solucion[0]) or not solucion[n_fil][n_col+1]: # Si a su derecha no hay un barco termino
                break
            n_col += 1
        else:
            if n_fil + 1 == len(solucion) or not solucion[n_fil+1][n_col]: # Si abajo no hay un barco termino
                break
            n_fil += 1
    
    

    return True