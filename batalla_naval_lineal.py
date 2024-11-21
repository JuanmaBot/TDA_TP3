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
