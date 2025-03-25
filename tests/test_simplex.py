import pytest
import numpy as np
from app.simplex import SimplexSolver

def test_simplex_solver():
    # Ejemplo de un problema de maximización
    c = [3, 5]  # Coeficientes de la función objetivo
    A = [[2, 1], [1, 3]]  # Matriz de restricciones
    b = [100, 150]  # Términos independientes
    
    solver = SimplexSolver(c, A, b)
    solution = solver.solve()
    
    # Verificaciones básicas
    assert solution is not None
    assert 'variables' in solution
    assert 'objective_value' in solution
    assert 'iterations' in solution
    
    # Verificar que las variables sean no negativas
    assert all(x >= 0 for x in solution['variables'])