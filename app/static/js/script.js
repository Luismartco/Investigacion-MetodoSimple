document.addEventListener('DOMContentLoaded', function() {
    // Validaciones de formulario
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const objectiveCoefficients = document.getElementById('objective_coefficients');
            const restrictionsMatrix = document.getElementById('restrictions_matrix');
            const independentTerms = document.getElementById('independent_terms');

            // Validar que los campos no estén vacíos
            if (!objectiveCoefficients.value.trim()) {
                alert('Por favor, ingrese los coeficientes de la función objetivo');
                event.preventDefault();
                return;
            }

            if (!restrictionsMatrix.value.trim()) {
                alert('Por favor, ingrese la matriz de restricciones');
                event.preventDefault();
                return;
            }

            if (!independentTerms.value.trim()) {
                alert('Por favor, ingrese los términos independientes');
                event.preventDefault();
                return;
            }

            // Validar formato de entrada
            try {
                const coeffs = objectiveCoefficients.value.split(',').map(x => parseFloat(x.trim()));
                const matrix = restrictionsMatrix.value.split(';').map(row => 
                    row.split(',').map(x => parseFloat(x.trim()))
                );
                const terms = independentTerms.value.split(',').map(x => parseFloat(x.trim()));

                // Validar que sean números válidos
                if (coeffs.some(isNaN) || matrix.some(row => row.some(isNaN)) || terms.some(isNaN)) {
                    alert('Por favor, ingrese solo valores numéricos');
                    event.preventDefault();
                    return;
                }
            } catch (error) {
                alert('Error en el formato de entrada. Verifique los datos.');
                event.preventDefault();
            }
        });
    }
});