import pulp
from pulp import LpAffineExpression as Sum

def batalla_naval_lineal2(demandas_col: list, demandas_fil: list, long_barcos: list):
    
    problem = pulp.LpProblem("bn", pulp.LpMaximize)

    barcos_vars = []
    for b in range(len(long_barcos)):
        vars = {
            "Oh": pulp.LpVariable("oh"+str((b)),cat="Binary"),
            "Ov": pulp.LpVariable("ov"+str((b)),cat="Binary"),
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

    M = len(demandas_col)*len(demandas_fil)*max(long_barcos)
    # Ahora las restricciones
    for i in range(len(barcos_vars)):
        
        actual = barcos_vars[i]

        # Limites para que no se salga del tablero
        problem += actual["F"] >= 0
        problem += actual["F"] <= len(demandas_fil)-1
        problem += actual["C"] >= 0
        problem += actual["C"] <= len(demandas_col)-1
        problem += actual["Ov"] + actual["Oh"] <= actual["B"]

        # Para que entre todo el barco en el tablero
        problem += actual["F"] + long_barcos[i] <= len(demandas_fil) + M * (actual["Oh"])
        problem += actual["C"] + long_barcos[i] <= len(demandas_fil) + M * (actual["Ov"])

        # Ahora tengo que hacer que los barcos se respeten entre si
        for j in range(len(barcos_vars)):
            if j == i:
                continue
            aux = barcos_vars[j]

            # Fuerzo A2 y D2
            problem += actual["F"] >= aux["F"] + (long_barcos[j] - 1) * aux["Ov"] + 2 - M * (1 - actual["2A"][j])
            problem += actual["F"] <= aux["F"] + (long_barcos[j] - 1) * aux["Ov"] + 1 + M * (actual["2A"][j])
            problem += actual["C"] >= aux["C"] + (long_barcos[j] - 1) * (aux["Oh"]) + 2 - M * (1 - actual["2D"][j])
            problem += actual["C"] <= aux["C"] + (long_barcos[j] - 1) * (aux["Oh"]) + 1 + M * (actual["2D"][j])

            problem += actual["2D"][j] + actual["2A"][j] + aux["2D"][i] + aux["2A"][i] >= 1 - M * (1 - actual["B"]) - M * (1 - aux["B"])
        
        # Falta ver las demandas
        for c in range(len(demandas_col)):

            # Fuerzo infBcol para que me diga si el barco empieza antes de o en la columna c
            problem += actual["C"] <= c + M * (1 - actual["InfBCol"][c])
            problem += actual["C"] >= c + 1 - M * (actual["InfBCol"][c])
            
            # Fuerzo supBcol para que me diga si el barco termina despues de o en la columna c
            problem += actual["C"] + (long_barcos[i] - 1) * (1 - actual["O"]) >= c - M * (1 - actual["SupBCol"][c])
            problem += actual["C"] + (long_barcos[i] - 1) * (1 - actual["O"]) <= c - 1 + M * (actual["SupBCol"][c])

            # Consigo Bcol par ver si este barco afecta el tablero final
            problem += actual["B"] + actual["InfBCol"][c] + actual["SupBCol"][c] >= 3 - M * (1 - actual["BCol"][c])
            problem += actual["B"] + actual["InfBCol"][c] + actual["SupBCol"][c] <= 2 + M * (actual["BCol"][c])

            # problem += actual["ICol"][c] <= M * actual["BCol"][c]

            # B_y_O = pulp.LpVariable("B_and_O"+str((i,c)),cat="Binary")
            # problem += actual["BCol"][c] + actual["O"] >= 2 - M * (1 - B_y_O)
            # problem += actual["BCol"][c] + actual["O"] <= 1 + M * (B_y_O)            

            # problem += actual["ICol"][c] == 1 + B_y_O * (long_barcos[i] - 1) - 1 * (1 - actual["BCol"][c])

            problem += actual["ICol"][c] == actual["BCol"][c] + (long_barcos[i] - 1) * (actual["Oh"])
            bcols[c].append(actual["ICol"][c])
        
        for f in range(len(demandas_fil)):

            # Fuerzo infBcol para que me diga si el barco empieza antes de o en la fila f
            problem += actual["F"] <= f + M * (1 - actual["InfBFil"][f])
            problem += actual["F"] >= f + 1 - M * (actual["InfBFil"][f])
            
            # Fuerzo supBcol para que me diga si el barco termina antes de o en la fila f
            problem += actual["F"] + (long_barcos[i] - 1) * (actual["O"]) >= f - M * (1 - actual["SupBFil"][f])
            problem += actual["F"] + (long_barcos[i] - 1) * (actual["O"]) <= f - 1 + M * (actual["SupBFil"][f])

            # Consigo Bcol par ver si este barco afecta el tablero final
            problem += actual["B"] + actual["InfBFil"][f] + actual["SupBFil"][f] >= 3 - M * (1 - actual["BFil"][f])
            problem += actual["B"] + actual["InfBFil"][f] + actual["SupBFil"][f] <= 2 + M * (actual["BFil"][f])

            # problem += actual["IFil"][f] <= M * actual["BFil"][f]

            B_y_NoO = pulp.LpVariable("B_and_no_O"+str((i,f)),cat="Binary")
            problem += actual["BFil"][f] + (1 - actual["O"]) >= 2 - M * (1 - B_y_NoO)
            problem += actual["BFil"][f] + (1 - actual["O"]) <= 1 + M * (B_y_NoO)            

            problem += actual["IFil"][f] == 1 + B_y_NoO * (long_barcos[i] - 1) - 1 * (1 - actual["BFil"][f])

            # problem += actual["ICol"][c] == actual["BCol"][c] + (long_barcos[i] - 1) * (1 - algo)
            bfils[f].append(actual["IFil"][f])
        
    # Obtengo la demanda cumplida y le pongo tope
    for col in range(len(demandas_cumplidas_columnas)):
        problem += demandas_cumplidas_columnas[col] == Sum([(dem,1) for dem in bcols[col]])
        problem += demandas_cumplidas_columnas[col] <= demandas_col[col]
    
    for fil in range(len(demandas_cumplidas_filas)):
        problem += demandas_cumplidas_filas[fil] == Sum([(dem,1) for dem in bfils[fil]])
        problem += demandas_cumplidas_filas[fil] <= demandas_fil[fil]
    
    # Y maximizo la suma de las demandas
    problem += pulp.lpSum(demandas_cumplidas_columnas + demandas_cumplidas_filas)
    # problem += Sum([(barcos_vars[b]["B"],long_barcos[b]) for b in range(len(long_barcos))])

    # Resuelvo
    problem.writeLP("modelo.lp")
    problem.solve()
    problem.writeLP("modelo_reducido.lp")

    # Interpreto resultados
    solucion = [[0 for col in range(len(demandas_col))] for fil in range(len(demandas_fil))]

    for b in range(len(barcos_vars)):
        barco = barcos_vars[b]
        print(pulp.value(barco["B"]),pulp.value(barco["F"]), pulp.value(barco["C"]), pulp.value(barco["O"]))
        for c in range(len(demandas_col)):
            print(f"ICol barco {b} columna {c}",pulp.value(barco["ICol"][c]),end=" ")
            print(f"InfBCol barco {b} columna {c}",pulp.value(barco["InfBCol"][c]),end=" ")
            print(f"SupBCol barco {b} columna {c}",pulp.value(barco["SupBCol"][c]),end=" ")
            print(f"BCol barco {b} columna {c}",pulp.value(barco["BCol"][c]))
        for f in range(len(demandas_fil)):
            print(f"IFil barco {b} fila {f}",pulp.value(barco["IFil"][f]),end=" ")
            print(f"InfBFil barco {b} fila {f}",pulp.value(barco["InfBFil"][f]),end=" ")
            print(f"SupBFil barco {b} fila {f}",pulp.value(barco["SupBFil"][f]),end=" ")
            print(f"BFil barco {b} fila {f}",pulp.value(barco["BFil"][f]))
        if int(pulp.value(barco["B"])) == 1:
            f, c, o = int(pulp.value(barco["F"])), int(pulp.value(barco["C"])), int(pulp.value(barco["O"]))
            for _ in range(long_barcos[b]):
                solucion[f][c] = 1
                if o == 1:
                    f += 1
                else:
                    c += 1
    
    return solucion


l_barcos = [1,2,2,2,2,1]
restricciones_filas = [3,3,0,1,1]
restricciones_columnas = [3,1,0,3,3]
print(batalla_naval_lineal2(restricciones_columnas,restricciones_filas,l_barcos))