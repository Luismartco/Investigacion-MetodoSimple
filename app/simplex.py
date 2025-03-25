import numpy as np

class SimplexSolver:
    def __init__(self, c, A, b, maximize=True):
        """
        Inicializa el problema de programación lineal
        
        :param c: Coeficientes de la función objetivo
        :param A: Matriz de restricciones
        :param b: Vector de términos independientes
        :param maximize: Indica si es un problema de maximización (True) o minimización (False)
        """
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.maximize = maximize
        
        self.iterations = []
        self.final_solution = None
        self.slack_variables = []
    
    def solve(self):
        """
        Resuelve el problema de programación lineal usando el método Simplex
        """
        # Preparar la tabla inicial
        m, n = self.A.shape
        
        # Crear variables de holgura
        slack_matrix = np.eye(m)
        
        # Crear tableau inicial
        tableau = np.zeros((m + 1, n + m + 1))
        
        # Colocar coeficientes de restricciones
        tableau[1:, :n] = self.A
        
        # Colocar matriz de holgura
        tableau[1:, n:n+m] = slack_matrix
        
        # Términos independientes
        tableau[1:, -1] = self.b
        
        # Función objetivo (ajustada para maximización o minimización)
        if self.maximize:
            # Para maximización, los coeficientes son negativos
            tableau[0, :n] = -self.c
        else:
            # Para minimización, los coeficientes son positivos
            tableau[0, :n] = self.c
        
        iteracion = 0
        while True:
            # Guardar estado actual de la tabla
            self.iterations.append(tableau.copy())
            
            # Encontrar columna pivote (variable que entra)
            pivot_col = self._find_entering_variable(tableau)
            
            # Si no hay columna pivote, hemos llegado a la solución óptima
            if pivot_col is None:
                break
            
            # Encontrar fila pivote (variable que sale)
            pivot_row = self._find_leaving_variable(tableau, pivot_col)
            
            # Si no hay fila pivote, el problema es no acotado
            if pivot_row is None:
                raise ValueError("Problema no acotado")
            
            # Realizar operación pivote
            tableau = self._pivot_operation(tableau, pivot_row, pivot_col)
            
            iteracion += 1
            
            # Límite de iteraciones para evitar bucles infinitos
            if iteracion > 100:
                raise ValueError("Demasiadas iteraciones. Posible problema de convergencia.")
        
        # Extraer solución final
        self._extract_solution(tableau)
        
        return self.final_solution
    
    def _find_entering_variable(self, tableau):
        """
        Encuentra la variable que entra (columna pivote)
        """
        # Para maximización, buscamos el coeficiente más negativo
        # Para minimización, buscamos el coeficiente más positivo
        candidates = tableau[0, :-1]
        
        if self.maximize:
            # Maximización: buscamos el valor más negativo
            if np.all(candidates >= 0):
                return None
            return np.argmin(candidates)
        else:
            # Minimización: buscamos el valor más positivo
            if np.all(candidates <= 0):
                return None
            return np.argmax(candidates)
    
    def _find_leaving_variable(self, tableau, pivot_col):
        """
        Encuentra la variable que sale (fila pivote)
        """
        m, n = tableau.shape
        ratios = []
        
        for i in range(1, m):
            if tableau[i, pivot_col] > 0:
                ratio = tableau[i, -1] / tableau[i, pivot_col]
                ratios.append((ratio, i))
        
        if not ratios:
            return None
        
        return min(ratios, key=lambda x: x[0])[1]
    
    def _pivot_operation(self, tableau, pivot_row, pivot_col):
        """
        Realiza la operación pivote en la tabla
        """
        pivot = tableau[pivot_row, pivot_col]
        tableau[pivot_row] /= pivot
        
        for i in range(tableau.shape[0]):
            if i != pivot_row:
                factor = tableau[i, pivot_col]
                tableau[i] -= factor * tableau[pivot_row]
        
        return tableau
    
    def _extract_solution(self, tableau):
        """
        Extrae la solución final del tableau
        """
        m, n = self.A.shape
        solution = np.zeros(n)
        slack_solution = np.zeros(m)
        
        # Encontrar variables básicas
        for j in range(n + m):
            col = tableau[:, j]
            if np.sum(col) == 1 and col[np.nonzero(col)[0][0]] == 1:
                row = np.nonzero(col)[0][0]
                if j < n:
                    # Variable de decisión original
                    solution[j] = tableau[row, -1]
                else:
                    # Variable de holgura
                    slack_solution[j - n] = tableau[row, -1]
        
        # Calcular valor objetivo Z
        if self.maximize:
            # Para maximización, el valor en la esquina superior derecha es negativo
            z_value = tableau[0, -1]
        else:
            # Para minimización, el valor es positivo
            z_value = -tableau[0, -1]
        
        self.final_solution = {
            'variables': solution,
            'slack_variables': slack_solution,
            'objective_value': z_value,
            'iterations': len(self.iterations)
        }