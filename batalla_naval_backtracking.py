import time

# def batalla_naval_bt(n: int, m: int, row_demand: list[int], col_demand: list[int], ships: list, board=None, unmet_demand=None, best_unmet=float("inf")):
#     """
#         n: Cantidad de Filas
#         m: Cantidad de Columnas
#         row_demand: Lista con la demanda de barcos por fila
#         col_demand: Lista con la demanda de barcos por columna
#         ships: Lista con los tamaños de los barcos (el indice representa el tamaño)
#         board: Tablero actual
#         unmet_demand: Demanda incumplida actual
#     """
#     # Inicializar tablero y demandas incumplidas
#     if board is None:
#         board = [[0] * m for _ in range(n)]
#         unmet_demand = sum(row_demand) + sum(col_demand)

#         # Ordenar barcos de menor a mayor tamaño
#         ships.sort()

#     # Si no quedan barcos, evaluar solución
#     if not ships:
#         return board, unmet_demand

#     # Variables para la mejor solución encontrada
#     best_board = None

#     # Seleccionar el barco más grande restante (el ultimo de la lista)
#     ship = ships.pop()

#     # =========== Podas =========== #

#     # === Poda 1: Verificar si la demanda de barcos es suficiente para llenar el tablero === #

#     # # Calcular la suma de la demanda de barcos restante
#     # required_demand = sum(row_demand) + sum(col_demand)

#     # # Si la demanda restante con la configuracion actual es mayor a la mejor demanda incumplida encontrada, podar
#     # if unmet_demand + required_demand >= best_unmet:
#     #     ships.append(ship)
#     #     return None, float("inf")
    
#     # ====================== #

#     # Determinar fila o columna con mayor demanda 
#     # Esto es para intentar colocar el barco en la fila o columna con mayor demanda, removiendo los casos mas dificiles primero
#     max_row_index = max(range(n), key=lambda i: row_demand[i])
#     max_col_index = max(range(m), key=lambda j: col_demand[j])

#     if row_demand[max_row_index] >= col_demand[max_col_index]:
#         priority = "row"
#         priority_index = max_row_index
#     else:
#         priority = "col"
#         priority_index = max_col_index

#     # Intentar colocar el barco en cada fila y columna
#     if priority == "row":
#         for j in range(m - ship + 1):
#             # Analizar espacios para el barco en esta fila
#             if se_puede_colocar(board, priority_index, j, ship, "horizontal", row_demand, col_demand):
#                 # Colocar el barco horizontalmente
#                 colocar_barco(board, priority_index, j, ship, "horizontal", row_demand, col_demand)

#                 # Recursión
#                 new_board, new_unmet = batalla_naval_bt(n, m, row_demand, col_demand, ships, board, unmet_demand, best_unmet)
#                 if new_unmet < best_unmet:
#                     best_unmet = new_unmet
#                     best_board = [row[:] for row in new_board]

#                 # Retroceso (quitar el barco)
#                 quitar_barco(board, priority_index, j, ship, "horizontal", row_demand, col_demand)

#     elif priority == "col":
#         for j in range(n - ship + 1):
#             # Analizar espacios para el barco en esta columna
#             if se_puede_colocar(board, j, priority_index, ship, "vertical", row_demand, col_demand):
#                 # Colocar el barco verticalmente
#                 colocar_barco(board, j, priority_index, ship, "vertical", row_demand, col_demand)

#                 # Recursión
#                 new_board, new_unmet = batalla_naval_bt(n, m, row_demand, col_demand, ships, board, unmet_demand, best_unmet)
#                 if new_unmet < best_unmet:
#                     best_unmet = new_unmet
#                     best_board = [row[:] for row in new_board]

#                 # Retroceso (quitar el barco)
#                 quitar_barco(board, j, priority_index, ship, "vertical", row_demand, col_demand)

#     # Devolver la mejor solución encontrada
#     ships.append(ship)
#     return best_board, best_unmet

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
    if current_unmet > best_solution['unmet']:
        return best_solution['board'], best_solution['unmet']
    
    original_ships = ships.copy()
    while ships:
        # Seleccionar el barco más grande restante
        ship = ships.pop()
        can_place = False
        
        # Encontrar fila/columna con mayor demanda
        max_row_idx = max(range(n), key=lambda i: row_demand[i])
        max_col_idx = max(range(m), key=lambda j: col_demand[j])
        
        # Probar todas las posiciones posibles, priorizando la mayor demanda
        positions = []
        
        # Agregar posiciones horizontales
        if row_demand[max_row_idx] > 0:
            positions.extend((max_row_idx, j, "horizontal") 
                            for j in range(m - ship + 1))
        
        # Agregar posiciones verticales
        if col_demand[max_col_idx] > 0:
            positions.extend((i, max_col_idx, "vertical") 
                            for i in range(n - ship + 1))
        
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
                can_place = True

                # Colocar barco
                colocar_barco(board, i, j, ship, direction, row_demand, col_demand)
                
                # Recursión
                batalla_naval_bt(n, m, row_demand, col_demand, ships, board, best_solution)
                
                # Retroceso
                quitar_barco(board, i, j, ship, direction, row_demand, col_demand)
        
        if can_place:
            ships.append(ship)
            break

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
    n, m = 10,10
    row_demand = [3,2,2,4,2,1,1,2,3,0]
    col_demand = [1,2,1,3,2,2,3,1,5,0]
    total_demand = sum(row_demand) + sum(col_demand)
    ships = [4,3,3,2,2,2,1,1,1,1]

    start_time = time.time()
    board, unmet = batalla_naval_bt(n, m, row_demand, col_demand, ships)
    elapsed_time = time.time() - start_time

    print("Tiempo de ejecución:", elapsed_time)
    print("Demanda incumplida mínima:", unmet)
    print("Demanda cumplida:", total_demand - unmet)
    print("Demanda total:", total_demand)
    for row in board:
        print(row)