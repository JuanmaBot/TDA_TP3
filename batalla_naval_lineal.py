import pulp
from pulp import LpAffineExpression as Sum
"""
def adyacentes(matriz, fila, columna, direcciones):
    
    elementos = []
    
    for dr, dc in direcciones:
        nr, nc = fila + dr, columna + dc
        
        if 0 <= nr < len(matriz) and 0 <= nc < len(matriz[0]):
            elementos.append(matriz[nr][nc])
    
    return elementos

def batalla_naval_lineal(demandas_col: list, demandas_fil: list, long_barcos: list):
    
    problem = pulp.LpProblem("bn", pulp.LpMaximize)

    casilleros = []
    for b in range(len(long_barcos)):
        barco = []
        for f in range(len(demandas_fil)):
            fila = []
            for c in range(len(demandas_col)):
                variables = {
                    "C": pulp.LpVariable("c"+str((f,c,b)),cat="Binary"),
                    "A2": pulp.LpVariable("a2"+str((f,c,b)),cat="Binary"),
                    "VRC": pulp.LpVariable("vrc"+str((f,c,b)),cat="Binary")
                }
                fila.append(variables)
            barco.append(fila)
        casilleros.append(barco)

    barcos = []
    for b in range(len(long_barcos)):
        variables = {
            "L1": pulp.LpVariable("l1"+str(b),cat="Binary"),
            "B": pulp.LpVariable("b"+str(b),cat="Binary"),
            "O": pulp.LpVariable("o"+str(b),cat="Binary")
        }
        barcos.append(variables)

    variables_por_fila = [[] for _ in range(len(demandas_fil))]
    variables_por_columna = [[] for _ in range(len(demandas_col))]

    M = len(demandas_col)*len(demandas_fil)

    # Ahora a definir las restricciones
    for i_barco in range(len(long_barcos)): # Por cada barco k...

        # Fuerzo L1
        problem += long_barcos[i_barco] >= 2 - M * barcos[i_barco]["L1"]
        problem += long_barcos[i_barco] <= 1 + M * (1 - barcos[i_barco]["L1"])

        tablero_k = casilleros[i_barco]
        todos_los_casilleros = []
        for fil in range(len(tablero_k)):

            todos_los_casilleros += tablero_k[fil]
            for col in range(len(tablero_k[fil])): # Para cada casillero...
                
                actual = tablero_k[fil][col]
                barco_actual = barcos[i_barco]
                
                # Lo meto a los arreglos correspondientes para despues
                variables_por_columna[col].append(actual)
                variables_por_fila[fil].append(actual)
                
                # Le saco los adyacentes
                horizontales = pulp.lpSum([a["C"] for a in adyacentes(tablero_k, fil, col, [(0,1),(0,-1)])])
                verticales = pulp.lpSum([a["C"] for a in adyacentes(tablero_k, fil, col, [(1,0),(-1,0)])])
                
                # Restricciones de orientacion
                problem += actual["C"] >= 1 + verticales - M * (1 - actual["C"]) - M * barco_actual["O"]
                problem += actual["C"] >= 1 + horizontales - M * (1 - actual["C"]) - M * (1 - barco_actual["O"])

                # De ser usados, deben tener un adyacente (A menos que sea un barco de tamaño 1)
                problem += verticales + horizontales >= 1 - M * barco_actual["L1"] - M * (1 - actual["C"])

                # Fuerzo A2
                problem += actual["C"] + verticales + horizontales >= 3 - M * (1 - actual["A2"])
                problem += actual["C"] + verticales + horizontales <= 2 + M * actual["A2"]

                # Fuerzo Vrc
                problem += actual["C"] + barco_actual["B"] >= 2 - M * (1 - actual["VRC"])
                problem += actual["C"] + barco_actual["B"] <= 1 + M * actual["VRC"]

                # Falta ver que en los otros tablero de barco, nadie se ponga cerca de los casilleros que se usan en este tablero
                ady = []
                for j_barco in range(i_barco + 1,len(long_barcos)):
                    ady += adyacentes(casilleros[j_barco], fil, col, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)])
                
                problem += Sum([(a["VRC"],1) for a in ady]) <= 0 + M * (1 - actual["VRC"])

        # Solo tiene que haber Lk casilleros ocupados
        problem += Sum([(c["C"],1) for c in todos_los_casilleros]) == long_barcos[i_barco]
        
        # Debe haber Lk - 2 casilleros con A2 en 1
        problem += Sum([(c["A2"],1) for c in todos_los_casilleros]) >= long_barcos[i_barco] - 2
    
    # Solo faltan las demandas
    demandas_cumplidas_col = [pulp.LpVariable("dcc"+str(c),cat="Integer") for c in range(len(demandas_col))]
    demandas_cumplidas_fil = [pulp.LpVariable("dcf"+str(f),cat="Integer") for f in range(len( demandas_fil))]
    
    for i in range(len(demandas_cumplidas_col)):
        problem += demandas_cumplidas_col[i] == Sum([(c["VRC"],1) for c in variables_por_columna[i]])
        problem += demandas_cumplidas_col[i] <= demandas_col[i]

    for i in range(len(demandas_cumplidas_fil)):
        problem += demandas_cumplidas_fil[i] == Sum([(f["VRC"],1) for f in variables_por_fila[i]])
        problem += demandas_cumplidas_fil[i] <= demandas_fil[i]
    
    # Y maximizo las demandas cumplidas
    problem += Sum([(dem,1) for dem in demandas_cumplidas_col] + [(dem,1) for dem in demandas_cumplidas_fil])
    problem.writeLP("modelo.lp")

    # Hago que se resuelva el problema
    problem.solve()
    problem.writeLP("modelo_reducido.lp")

    # Formo la matriz solucion
    solucion = [[0 for c in range(len(demandas_col))] for f in range(len(demandas_fil))]
    for b in range(len(casilleros)):
        for f in range(len(casilleros[b])):
            for c in range(len(casilleros[b][f])):
                if int(pulp.value(casilleros[b][f][c]["VRC"])) == 1:
                    solucion[f][c] = 1
    
    return solucion
"""


def batalla_naval_lineal2(demandas_col: list, demandas_fil: list, long_barcos: list):
    
    problem = pulp.LpProblem("bn", pulp.LpMaximize)

    barcos_vars = []
    for b in range(len(long_barcos)):
        vars = {
            "O": pulp.LpVariable("o"+str((b)),cat="Binary"),
            "B": pulp.LpVariable("b"+str((b)),cat="Binary"),
            "C": pulp.LpVariable("c"+str((b)),cat="Integer"),
            "F": pulp.LpVariable("f"+str((b)),cat="Integer"),
            "2A": [pulp.LpVariable("2a"+str((b,b2)),cat="Binary") for b2 in range(len(long_barcos))],
            "2D": [pulp.LpVariable("2d"+str((b,b2)),cat="Binary") for b2 in range(len(long_barcos))],
            "InfBCol": [pulp.LpVariable("infBcol"+str((b,c)),cat="Binary") for c in range(len(demandas_col))],
            "SupBCol": [pulp.LpVariable("supBcol"+str((b,c)),cat="Binary") for c in range(len(demandas_col))],
            "BCol": [pulp.LpVariable("Bcol"+str((b,c)),cat="Binary") for c in range(len(demandas_col))],
            "ICol": [pulp.LpVariable("Icol"+str((b,c)),cat="Integer") for c in range(len(demandas_col))],
            "InfBFil": [pulp.LpVariable("infBfil"+str((b,f)),cat="Binary") for f in range(len(demandas_fil))],
            "SupBFil": [pulp.LpVariable("supBfil"+str((b,f)),cat="Binary") for f in range(len(demandas_fil))],
            "BFil": [pulp.LpVariable("Bfil"+str((b,f)),cat="Binary") for f in range(len(demandas_fil))],
            "IFil": [pulp.LpVariable("IFil"+str((b,f)),cat="Integer") for f in range(len(demandas_fil))]
        }
        barcos_vars.append(vars)
    
    demandas_cumplidas_columnas = [pulp.LpVariable("dcc"+str((c)),cat="Integer") for c in range(len(demandas_col))]
    demandas_cumplidas_filas = [pulp.LpVariable("dcf"+str((f)),cat="Integer") for f in range(len(demandas_fil))]
    bcols = [[] for col in range(len(demandas_col))]
    bfils = [[] for fil in range(len(demandas_fil))]

    M = len(demandas_col)*len(demandas_fil)
    # Ahora las restricciones
    for i in range(len(barcos_vars)):
        
        actual = barcos_vars[i]

        # Limites para que no se salga del tablero
        problem += actual["F"] >= 0
        problem += actual["F"] >= len(demandas_fil)-1
        problem += actual["C"] >= 0
        problem += actual["C"] >= len(demandas_col)-1

        # Para que entre todo el barco en el tablero
        problem += actual["F"] + long_barcos[i] <= len(demandas_fil) + M * (1 - actual["O"])
        problem += actual["C"] + long_barcos[i] <= len(demandas_fil) + M * (actual["O"])

        # Ahora tengo que hacer que los barcos se respeten entre si
        for j in range(len(barcos_vars)):
            if j == i:
                continue
            aux = barcos_vars[j]

            # Fuerzo A2 y D2
            problem += actual["F"] >= aux["F"] + (long_barcos[j] - 1) * aux["O"] + 2 - M * (1 - actual["2A"][j])
            problem += actual["F"] <= aux["F"] + (long_barcos[j] - 1) * aux["O"] + 1 + M * (actual["2A"][j])
            problem += actual["C"] >= aux["C"] + (long_barcos[j] - 1) * (1 - aux["O"]) + 2 - M * (1 - actual["2D"][j])
            problem += actual["C"] <= aux["C"] + (long_barcos[j] - 1) * (1 - aux["O"]) + 1 + M * (actual["2D"][j])

            problem += actual["2D"][j] + actual["2A"][j] + aux["2D"][i] + aux["2A"][i] >= 2 - M * (1 - actual["B"]) - M * (1 - aux["B"])
        
        # Falta ver las demandas
        for c in range(len(demandas_col)):

            # Fuerzo infBcol para que me diga si el barco empieza antes de la columna c o despues
            problem += actual["C"] <= c + M * (1 - actual["InfBCol"][c])
            problem += actual["C"] >= c + 1 - M * (actual["InfBCol"][c])
            
            # Fuerzo supBcol para que me diga si el barco termina antes de la columna c o justo en c
            problem += actual["C"] + (long_barcos[i] - 1) * (1 - actual["O"]) >= c - M * (actual["SupBCol"][c])
            problem += actual["C"] + (long_barcos[i] - 1) * (1 - actual["O"]) <= c - 1 + M * (1 - actual["SupBCol"][c])

            # Consigo Bcol par ver si este barco afecta el tablero final
            problem += actual["B"] + actual["InfBCol"][c] + actual["SupBCol"][c] >= 3 - M * (1 - actual["BCol"][c])
            problem += actual["B"] + actual["InfBCol"][c] + actual["SupBCol"][c] <= 2 + M * (actual["BCol"][c])
        
            problem += actual["ICol"] == actual["BCol"][c] + (long_barcos[i] - 1) * (1 - actual["O"])
            bcols[c].append(actual["ICol"])
        for f in range(len(demandas_fil)):

            # Fuerzo infBcol para que me diga si el barco empieza antes de la columna c o despues
            problem += actual["F"] <= f + M * (1 - actual["InfBFil"][f])
            problem += actual["F"] >= f + 1 - M * (actual["InfBFil"][f])
            
            # Fuerzo supBcol para que me diga si el barco termina antes de la columna c o justo en c
            problem += actual["F"] + (long_barcos[i] - 1) * (actual["O"]) >= f - M * (actual["SupBFil"][f])
            problem += actual["F"] + (long_barcos[i] - 1) * (actual["O"]) <= f - 1 + M * (1 - actual["SupBFil"][f])

            # Consigo Bcol par ver si este barco afecta el tablero final
            problem += actual["B"] + actual["InfBFil"][f] + actual["SupBFil"][f] >= 3 - M * (1 - actual["BFil"][f])
            problem += actual["B"] + actual["InfBFil"][f] + actual["SupBFil"][f] <= 2 + M * (actual["BFil"][f])

            problem += actual["IFil"] == actual["BFil"][f] + (long_barcos[i] - 1) * (actual["O"])
            bcols[c].append(actual["IFil"])
        
    # Obtengo la demanda cumplida y le pongo tope
    for col in range(len(demandas_cumplidas_columnas)):
        problem += demandas_cumplidas_columnas[col] == Sum([(dem,1) for dem in bcols[col]])
        problem += demandas_cumplidas_columnas[col] <= demandas_col[col]
    
    for fil in range(len(demandas_cumplidas_filas)):
        problem += demandas_cumplidas_filas[fil] == Sum([(dem,1) for dem in bfils[fil]])
        problem += demandas_cumplidas_filas[fil] <= demandas_fil[fil]
    
    # Y maximizo la suma de las demandas
    problem += Sum([(dem,1) for dem in demandas_cumplidas_columnas] + [(dem,1) for dem in demandas_cumplidas_filas])

    # Resuelvo
    problem.writeLP("modelo.lp")
    problem.solve()
    problem.writeLP("modelo_reducido.lp")

    # Interpreto resultados
    solucion = [[0 for col in range(len(demandas_col))] for fil in range(len(demandas_fil))]

    for b in range(len(barcos_vars)):
        barco = barcos_vars[b]
        if int(pulp.value(barco["B"])) == 1:
            f, c, o = int(pulp.value(barco["F"])), int(pulp.value(barco["C"])), int(pulp.value(barco["O"]))
            for _ in range(long_barcos[b]):
                solucion[f][c] = 1
                if o == 1:
                    f += 1
                else:
                    c += 1
    
    return solucion


l_barcos = [3,1,1,2,4,2]
restricciones_filas = [3,2,2,4,3,0]
restricciones_columnas = [2,2,3,1,5,0]
print(batalla_naval_lineal2(restricciones_columnas,restricciones_filas,l_barcos))