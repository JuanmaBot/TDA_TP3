import time

def batalla_naval_bt(n: int, m: int, row_demand: list[int], col_demand: list[int], ships: list, board=None, best_solution=None):
    """
    Resuelve el problema de batalla naval usando backtracking con podas.
    Retorna el mejor tablero encontrado y su demanda incumplida.
    """
    # Inicializar mejor solución
    if best_solution is None:
        best_solution = {
            'board': None,
            'unmet': float('inf')
        }
    
    # Inicializar tablero
    if board is None:
        board = [[0] * m for _ in range(n)]
        ships.sort()
    
    # Calcular demanda incumplida actual
    current_unmet = sum(max(0, d) for d in row_demand) + sum(max(0, d) for d in col_demand)
    
    # Si encontramos una mejor solución, actualizarla
    if current_unmet < best_solution['unmet']:
        best_solution['unmet'] = current_unmet
        best_solution['board'] = [row[:] for row in board]
    
    # Si no quedan barcos o ya cumplimos toda la demanda, retornar
    if not ships or current_unmet == 0:
        return best_solution['board'], best_solution['unmet']
    
    # === Poda 1: Si la demanda actual ya es peor que la mejor encontrada === #
    # if current_unmet >= best_solution['unmet']:
    #     return best_solution['board'], best_solution['unmet']
    
    original_ships = ships.copy()
    tried_ships = set()

    while ships and len(tried_ships) < len(ships):
        # Seleccionar el barco más grande restante
        ship = ships.pop()

        print("Barco:", ship)
        print("Demanda incumplida:", current_unmet)
        print("Tablero:")
        for row in board:
            print(row)

        if ship in tried_ships:
            continue
        
        tried_ships.add(ship)
        
        # Probar todas las posiciones posibles, priorizando la mayor demanda
        positions = []
        
        # Agregar todas las posiciones horizontales válidas
        for i in range(n):
            if row_demand[i] > 0:
                for j in range(m - ship + 1):
                    positions.append((i, j, "horizontal"))
        
        # Agregar todas las posiciones verticales válidas
        for j in range(m):
            if col_demand[j] > 0:
                for i in range(n - ship + 1):
                    positions.append((i, j, "vertical"))
        
        # Ordenar posiciones por demanda total afectada
        def position_score(pos):
            i, j, direction = pos
            if direction == "horizontal":
                return row_demand[i] + sum(col_demand[j+k] for k in range(ship))
            else:
                return col_demand[j] + sum(row_demand[i+k] for k in range(ship))
        
        positions.sort(key=position_score, reverse=True)
        
        # Probar cada posición
        for i, j, direction in positions:
            if se_puede_colocar(board, i, j, ship, direction, row_demand, col_demand):
                # Colocar barco
                colocar_barco(board, i, j, ship, direction, row_demand, col_demand)
                
                # Recursión
                batalla_naval_bt(n, m, row_demand, col_demand, ships, board, best_solution)
                
                # Retroceso
                quitar_barco(board, i, j, ship, direction, row_demand, col_demand)

    # Restaurar lista de barcos
    ships.clear()
    ships.extend(original_ships)

    return best_solution['board'], best_solution['unmet']

# =========== Utilidades de Barcos =========== #

def se_puede_colocar(board, i, j, ship, direction, row_demand, col_demand):
    """Verifica si es válido colocar un barco en la posición dada."""

    if direction == "horizontal":
        # Verificar si la fila tiene suficiente demanda
        if row_demand[i] < ship:
            return False
        
        # Verificar si el barco cabe en la fila y no hay conflictos con la demanda de columnas
        for k in range(ship):
            if board[i][j + k] != 0 or col_demand[j + k] <= 0:
                return False
            
        # Verificar adyacencias (incluyendo diagonales)
        return all(board[x][y] == 0 for x, y in obtener_adyacentes(board, i, j, ship, "horizontal"))
    
    elif direction == "vertical":
        # Verificar si la columna tiene suficiente demanda
        if col_demand[j] < ship:
            return False
        
        # Verificar si el barco cabe en la columna y no hay conflictos con la demanda de filas
        for k in range(ship):
            if board[i + k][j] != 0 or row_demand[i + k] <= 0:
                return False
            
        # Verificar adyacencias (incluyendo diagonales)
        return all(board[x][y] == 0 for x, y in obtener_adyacentes(board, i, j, ship, "vertical"))
    
    return False

def colocar_barco(board, i, j, ship, direction, row_demand, col_demand):
    """Coloca un barco en el tablero, actualizando las demandas."""

    if direction == "horizontal":
        for k in range(ship):
            board[i][j + k] = 1
            row_demand[i] -= 1
            col_demand[j + k] -= 1

    elif direction == "vertical":
        for k in range(ship):
            board[i + k][j] = 1
            row_demand[i + k] -= 1
            col_demand[j] -= 1


def quitar_barco(board, i, j, ship, direction, row_demand, col_demand):
    """Elimina un barco del tablero, restaurando las demandas."""

    if direction == "horizontal":
        for k in range(ship):
            board[i][j + k] = 0
            row_demand[i] += 1
            col_demand[j + k] += 1

    elif direction == "vertical":
        for k in range(ship):
            board[i + k][j] = 0
            row_demand[i + k] += 1
            col_demand[j] += 1

# =========== Utilidades de Adyacencias =========== #

def obtener_adyacentes(board, i, j, ship, direction):
    """Obtiene las posiciones vecinas para verificar restricciones."""
    neighbors = []

    if direction == "horizontal":
        # Fila superior e inferior para todo el barco
        neighbors += [(i - 1, j + dy) for dy in range(-1, ship + 1)]
        neighbors += [(i + 1, j + dy) for dy in range(-1, ship + 1)]

        # Extremos izquierdo y derecho en la misma fila
        neighbors.append((i, j - 1))
        neighbors.append((i, j + ship)) 

    elif direction == "vertical":
        # Columna izquierda y derecha para todo el barco
        neighbors += [(i + dx, j - 1) for dx in range(-1, ship + 1)]
        neighbors += [(i + dx, j + 1) for dx in range(-1, ship + 1)]

        # Extremos superior e inferior en la misma columna
        neighbors.append((i - 1, j))
        neighbors.append((i + ship, j))

    return [(x, y) for x, y in neighbors if 0 <= x < len(board) and 0 <= y < len(board[0])]

# =========== Ejemplo de Uso =========== #

if __name__ == "__main__":
    # Ejemplo 3 3 2
    n, m = 3,3
    row_demand = [3,1,2]
    col_demand = [3,2,0]
    ships = [1,1]

    # Ejemplo 5 5 6
    n, m = 5,5
    row_demand = [3,3,0,1,1]
    col_demand = [3,1,0,3,3]
    ships = [1,2,2,2,2,1]

    # Ejemplo 8 7 10
    n, m = 8,7
    row_demand = [1,4,4,4,3,3,4,4]
    col_demand = [6,5,3,0,6,3,3]
    ships = [2,1,2,2,1,3,2,7,7,7]

    # # Ejemplo 10 3 3
    # n, m = 10,3
    # row_demand = [1,0,1,0,1,0,0,1,1,1]
    # col_demand = [1,4,3]
    # ships = [3,3,4]

    # # Ejemplo 10 10 10
    # n, m = 10,10
    # row_demand = [3,2,2,4,2,1,1,2,3,0]
    # col_demand = [1,2,1,3,2,2,3,1,5,0]
    # ships = [4,3,3,2,2,2,1,1,1,1]

    # # Ejemplo 12 12 21
    # n, m = 12,12
    # row_demand = [3,6,1,2,3,6,5,2,0,3,0,3]
    # col_demand = [3,0,1,1,3,1,0,3,3,4,1,4]
    # ships = [4,3,7,4,3,2,2,5,5,5,4,4,5,5,7,6,4,1,7,4,4]

    total_demand = sum(row_demand) + sum(col_demand)

    start_time = time.time()
    board, unmet = batalla_naval_bt(n, m, row_demand, col_demand, ships)
    elapsed_time = time.time() - start_time

    print("Tiempo de ejecución:", elapsed_time)
    print("Demanda incumplida mínima:", unmet)
    print("Demanda cumplida:", total_demand - unmet)
    print("Demanda total:", total_demand)
    for row in board:
        print(row)