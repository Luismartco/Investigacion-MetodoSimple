from flask import Blueprint, render_template, request, jsonify
from .simplex import SimplexSolver
import traceback
import numpy as np

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página de inicio"""
    return render_template('index.html')

@main.route('/input', methods=['GET', 'POST'])
def input_problem():
    """Página para ingresar datos del problema de programación lineal"""
    return render_template('input.html')

@main.route('/solve', methods=['POST'])
def solve_problem():
    """Resolver el problema de programación lineal"""
    try:
        # Convertir datos
        objective_coefficients = [float(x.strip()) for x in request.form['objective_coefficients'].split(',')]
        restrictions_matrix = [
            [float(x.strip()) for x in row.split(',')] 
            for row in request.form['restrictions_matrix'].split(';')
        ]
        independent_terms = [float(x.strip()) for x in request.form['independent_terms'].split(',')]

        # Verificaciones adicionales
        if len(objective_coefficients) != len(restrictions_matrix[0]):
            raise ValueError("Las dimensiones de los coeficientes objetivo no coinciden con las restricciones")
        
        if len(restrictions_matrix) != len(independent_terms):
            raise ValueError("El número de filas de restricciones no coincide con los términos independientes")

        # Resolver usando Simplex (por defecto maximización)
        solver = SimplexSolver(objective_coefficients, restrictions_matrix, independent_terms, maximize=True)
        solution = solver.solve()
        
        # Convertir numpy arrays a listas para serialización
        solution_data = {
            'variables': solution['variables'].tolist() if isinstance(solution['variables'], np.ndarray) else solution['variables'],
            'slack_variables': solution['slack_variables'].tolist() if isinstance(solution['slack_variables'], np.ndarray) else solution['slack_variables'],
            'objective_value': float(solution['objective_value']),
            'iterations': solution.get('iterations', 0)
        }
        
        iterations_data = [iter_table.tolist() for iter_table in solver.iterations]
        
        return render_template('results.html', 
                               solution=solution_data, 
                               iterations=iterations_data)
    
    except Exception as e:
        # Imprimir error completo para diagnóstico
        print("Error completo:", traceback.format_exc())
        
        return render_template('error.html', 
                               error_message=str(e), 
                               error_details=traceback.format_exc()), 400