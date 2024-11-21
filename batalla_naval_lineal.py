import pulp
from pulp import LpAffineExpression as Sum

def batalla_naval_lineal(demandas_col: list,demandas_fil: list,long_barcos: list):
    
    problem = pulp.LpProblem("bn", pulp.LpMaximize)

    casilleros = []
    for b in range(len(long_barcos)):
        barco = []
        for f in range(len(demandas_fil)):
            fila = []
            for c in range(len(demandas_col)):
                variables = {
                    "C": pulp.LpVariable("c"+str((f,c)),cat="Binary"),
                    "A2": pulp.LpVariable("a2"+str((f,c)),cat="Binary"),
                    "VRC": pulp.LpVariable("vrc"+str((f,c)),cat="Binary")
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

    demandas_cumplidas_col = [pulp.LpVariable("dcc"+str(c),cat="Integer") for c in demandas_col]
    demandas_cumplidas_fil = [pulp.LpVariable("dcf"+str(f),cat="Integer") for f in demandas_fil]
    M = len(demandas_col)*len(demandas_fil)

    # Ahora a definir las restricciones
    for i_barco in range(len(long_barcos)): # Por cada barco k...

        # Fuerzo L1
        problem += long_barcos[i_barco] > 1 - M * barcos[i_barco]["L1"]
        problem += long_barcos[i_barco] <= 1 + M * (1 - barcos[i_barco]["L1"])

        tablero_k = casilleros[i_barco]
        todos_los_casilleros = []
        for fil in range(len(tablero_k)):

            todos_los_casilleros += tablero_k[fil]
            for col in range(len(tablero_k[fil])): # Para cada casillero...
                actual = tablero_k[fil][col]
                horizontales = adyacentes_horizontales(tablero_k, fil, col)
                verticales = adyacentes_verticales(tablero_k, fil, col)
                
                # Restricciones de orientacion
                problem += actual["C"] > verticales - M * (1 - actual["C"]) - M * actual["O"]
                problem += actual["C"] > horizontales - M * (1 - actual["C"]) - M * (1 - actual["O"])

                # De ser usados, deben tener un adyacente (A menos que sea un barco de tamaño 1)
                problem += verticales + horizontales >= 1 - M * barcos[i_barco]["L1"] - M * (1 - actual["C"])

                # Fuerzo A2
                problem += actual["C"] + verticales + horizontales > 2 - M * (1 - actual["A2"])
                problem += actual["C"] + verticales + horizontales <= 2 + M * actual["A2"]

                # Fuerzo Vrc
                problem += actual["C"] + barco[i_barco]["B"] > 1 - M * (1 - actual["VRC"])
                problem += actual["C"] + barco[i_barco]["B"] <= 1 + M * actual["VRC"]

                # Falta ver que en los otros tablero de barco, nadie se ponga cerca de los casilleros que se usan en este tablero
                for j_barco in range(len(long_barcos)):
                    if j_barco == i_barco:
                        continue
                    

        # Solo tiene que haber Lk casilleros ocupados
        problem += Sum([(c["C"],1) for c in todos_los_casilleros]) == long_barcos[i_barco]
        
        # Debe haber Lk - 2 casilleros con A2 en 1
        problem += Sum([(c["A2"],1) for c in todos_los_casilleros]) >= long_barcos[i_barco] - 2

        

def adyacentes_horizontales(tablero_k, fil, col):
    if len(tablero_k[fil]) == 1:
        return 0
    elif col == 0:
        return tablero_k[fil][col+1]["C"]
    elif col == len(tablero_k[0])-1:
        return tablero_k[fil][col-1]["C"]
    return tablero_k[fil][col-1]["C"] + tablero_k[fil][col+1]["C"]

def adyacentes_verticales(tablero_k, fil, col):
    if len(tablero_k) == 1:
        return 0
    elif fil == 0:
        return tablero_k[fil+1][col]["C"]
    elif fil == len(tablero_k)-1:
        return tablero_k[fil-1][col]["C"]
    return tablero_k[fil-1][col]["C"] + tablero_k[fil+1][col]["C"]
"""
def vertex_cover_min(grafo):

    problem = pulp.LpProblem("vc", pulp.LpMinimize)
    vertices = {v:pulp.LpVariable(str(v),cat="Binary") for v in grafo.obtener_vertices()}
    
    for v in grafo.obtener_vertices():
        v1 = vertices[v]
        for ady in grafo.adyacentes(v):
            v2 = vertices[ady]
            problem += v1 + v2 >= 1
    problem += Sum([(v,1) for v in vertices.values()])
    problem.solve()

    solution = []
    for v in vertices:
        if pulp.value(vertices[v]) == 1:
            solution.append(v)
    return solution
"""