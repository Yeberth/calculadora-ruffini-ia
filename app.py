#!/usr/bin/env python3
"""
Servidor Flask para la Calculadora de Ruffini con IA
Proporciona tanto la interfaz web como una API REST
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from src.ruffini_calculator import RuffiniCalculator

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Cambiar en producción
app.config['DEBUG'] = True

# Instancia global del calculador
calculator = RuffiniCalculator()

@app.route('/')
def index():
    """Página principal de la aplicación"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    API endpoint para realizar cálculos de Ruffini
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos JSON'
            }), 400
        
        polynomial = data.get('polynomial', '').strip()
        root = data.get('root')
        
        if not polynomial:
            return jsonify({
                'success': False,
                'error': 'El polinomio es requerido'
            }), 400
        
        try:
            root = float(root)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'La raíz debe ser un número válido'
            }), 400
        
        # Realizar el cálculo
        result = calculator.calculate(polynomial, root)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route('/validate', methods=['POST'])
def validate_polynomial():
    """
    API endpoint para validar polinomios con ayuda de IA
    """
    try:
        data = request.get_json()
        polynomial = data.get('polynomial', '').strip()
        
        if not polynomial:
            return jsonify({
                'valid': False,
                'error': 'Polinomio vacío',
                'suggestions': generate_format_suggestions()
            })
        
        # Intentar parsear el polinomio
        try:
            coefficients = calculator.parse_polynomial(polynomial)
            
            # Generar análisis con IA
            analysis = generate_polynomial_analysis(polynomial, coefficients)
            
            return jsonify({
                'valid': True,
                'polynomial': polynomial,
                'coefficients': coefficients,
                'analysis': analysis,
                'degree': len(coefficients) - 1,
                'formatted': calculator.format_polynomial(coefficients)
            })
            
        except Exception as e:
            return jsonify({
                'valid': False,
                'error': str(e),
                'suggestions': generate_error_suggestions(polynomial, str(e))
            })
            
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': f'Error interno: {str(e)}'
        }), 500

@app.route('/examples')
def get_examples():
    """
    API endpoint que proporciona ejemplos de polinomios
    """
    examples = [
        {
            'title': 'Polinomio cúbico simple',
            'polynomial': 'x^3 + 2x^2 - 5x + 6',
            'root': 2,
            'description': 'Un polinomio de grado 3 con coeficientes mixtos',
            'difficulty': 'Intermedio'
        },
        {
            'title': 'Diferencia de cuadrados',
            'polynomial': 'x^4 - 1',
            'root': 1,
            'description': 'Factorización de diferencia de potencias',
            'difficulty': 'Fácil'
        },
        {
            'title': 'Polinomio con coeficiente principal',
            'polynomial': '2x^3 - 3x^2 + x - 2',
            'root': 2,
            'description': 'Polinomio con coeficiente principal diferente de 1',
            'difficulty': 'Avanzado'
        },
        {
            'title': 'Polinomio cuadrático',
            'polynomial': 'x^2 - 5x + 6',
            'root': 3,
            'description': 'Un polinomio cuadrático clásico',
            'difficulty': 'Fácil'
        },
        {
            'title': 'Polinomio con raíz negativa',
            'polynomial': 'x^3 + x^2 - 2x',
            'root': -2,
            'description': 'División por un binomio con raíz negativa',
            'difficulty': 'Intermedio'
        }
    ]
    
    return jsonify(examples)

@app.route('/ai-tutor', methods=['POST'])
def ai_tutor():
    """
    Endpoint para el tutor de IA que responde preguntas sobre Ruffini
    """
    try:
        data = request.get_json()
        question = data.get('question', '').strip().lower()
        context = data.get('context', {})
        
        # Generar respuesta del tutor basada en la pregunta
        response = generate_tutor_response(question, context)
        
        return jsonify({
            'success': True,
            'response': response,
            'type': 'tutor_help'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error en el tutor: {str(e)}'
        }), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir archivos estáticos"""
    return send_from_directory('static', filename)

# Funciones auxiliares para IA
def generate_format_suggestions():
    """Genera sugerencias de formato para polinomios"""
    return [
        "Usa ^ para exponentes: x^3, x^2",
        "Incluye signos: +, -",
        "Ejemplos válidos: x^3 + 2x^2 - 5x + 6",
        "Para términos lineales: 3x o -2x",
        "Para constantes: +5 o -3"
    ]

def generate_error_suggestions(polynomial, error):
    """Genera sugerencias específicas basadas en errores"""
    suggestions = []
    
    if "invalid" in error.lower():
        suggestions.append("Verifica la sintaxis del polinomio")
        suggestions.append("Asegúrate de usar ^ para exponentes")
    
    if "x" not in polynomial:
        suggestions.append("¿Olvidaste incluir la variable 'x'?")
        suggestions.append("Para constantes, solo escribe el número")
    
    if "^" not in polynomial and "x" in polynomial:
        suggestions.append("Para exponentes, usa ^ (ejemplo: x^2)")
    
    suggestions.extend([
        "Ejemplos correctos:",
        "• x^3 + 2x^2 - 5x + 6",
        "• 2x^4 - x^3 + 3x - 1",
        "• x^2 - 4"
    ])
    
    return suggestions

def generate_polynomial_analysis(polynomial, coefficients):
    """Genera análisis detallado del polinomio con IA"""
    degree = len(coefficients) - 1
    
    analysis = f"""🤖 ANÁLISIS DEL POLINOMIO

📊 Información básica:
• Grado: {degree}
• Número de términos: {sum(1 for c in coefficients if c != 0)}
• Coeficiente principal: {coefficients[0]}

🔍 Características:
"""
    
    # Análisis de grado
    if degree == 1:
        analysis += "• Polinomio lineal - gráfica es una línea recta\n"
    elif degree == 2:
        analysis += "• Polinomio cuadrático - gráfica es una parábola\n"
    elif degree == 3:
        analysis += "• Polinomio cúbico - puede tener hasta 2 extremos locales\n"
    elif degree >= 4:
        analysis += f"• Polinomio de grado {degree} - comportamiento complejo\n"
    
    # Análisis de coeficientes
    if coefficients[0] > 0:
        analysis += "• Coeficiente principal positivo\n"
    elif coefficients[0] < 0:
        analysis += "• Coeficiente principal negativo\n"
    
    # Análisis del término independiente
    if len(coefficients) > 0 and coefficients[-1] != 0:
        analysis += f"• Término independiente: {coefficients[-1]}\n"
        analysis += "• La gráfica interseca el eje Y en este punto\n"
    
    analysis += f"""
💡 Consejos para Ruffini:
• Prueba con divisores del término independiente
• Usa el teorema del resto para verificar
• Si el resto es 0, encontraste un factor
"""
    
    return analysis

def generate_tutor_response(question, context):
    """Genera respuesta del tutor basada en la pregunta"""
    
    # Respuestas predefinidas del tutor
    responses = {
        'que es ruffini': """🎓 ¿Qué es el método de Ruffini?

El método de Ruffini es una técnica simplificada para dividir polinomios por binomios de la forma (x - a).

🔧 ¿Cómo funciona?
1. Se escriben los coeficientes del polinomio en una fila
2. Se coloca la raíz 'a' a la izquierda
3. Se baja el primer coeficiente
4. Se multiplica por 'a' y se suma al siguiente coeficiente
5. Se repite hasta completar todos los coeficientes

✅ Ventajas:
• Más rápido que la división larga
• Menos propenso a errores
• Útil para factorizar polinomios""",

        'como usar': """📚 ¿Cómo usar esta calculadora?

1️⃣ **Ingresa tu polinomio**
   • Formato: x^3 + 2x^2 - 5x + 6
   • Usa ^ para exponentes
   • Incluye signos + y -

2️⃣ **Especifica la raíz**
   • Para dividir por (x - 2), usa raíz = 2
   • Para dividir por (x + 3), usa raíz = -3

3️⃣ **¡Calcula!**
   • Ve el resultado paso a paso
   • Obtén explicaciones detalladas
   • Verifica el resultado automáticamente""",

        'errores comunes': """⚠️ Errores comunes y cómo evitarlos

❌ **Error de formato**
• Malo: x3 + 2x2 - 5x + 6
• Bueno: x^3 + 2x^2 - 5x + 6

❌ **Olvidar signos**
• Malo: x^3 2x^2 5x 6
• Bueno: x^3 + 2x^2 - 5x + 6

❌ **Raíz incorrecta**
• Para (x - 2): usa 2, no -2
• Para (x + 3): usa -3, no 3

💡 **Consejo**: Usa el botón "Ejemplo" para ver formatos correctos!""",

        'interpretar resultado': """🧠 ¿Cómo interpretar el resultado?

📋 **El resultado tiene dos partes:**

🎯 **Cociente**
• Es el polinomio resultado de la división
• Tiene grado menor al original
• Representa el "factor" multiplicativo

🔢 **Resto**
• Si es 0: división exacta
• Si no es 0: división con residuo

✅ **Verificación**
(Cociente) × (x - raíz) + Resto = Polinomio original

💡 **Interpretación geométrica**
• Si resto = 0, la raíz es una solución del polinomio
• Si resto ≠ 0, la raíz no es solución exacta""",

        'ejemplo paso a paso': """📖 Ejemplo paso a paso

**Problema:** Dividir x³ + 2x² - 5x + 6 entre (x - 2)

**Paso 1:** Coeficientes del polinomio
[1, 2, -5, 6]

**Paso 2:** Colocamos la raíz a = 2

**Paso 3:** Proceso Ruffini
```
    |  1   2  -5   6
  2 |      2   8   6
    |  1   4   3  12
```

**Paso 4:** Interpretación
• Cociente: x² + 4x + 3
• Resto: 12

**Verificación:**
(x² + 4x + 3)(x - 2) + 12 = x³ + 2x² - 5x + 6 ✓"""
    }
    
    # Buscar respuesta más relevante
    for keyword, response in responses.items():
        if keyword in question:
            return response
    
    # Respuesta por defecto
    return """🤖 ¡Hola! Soy tu tutor de IA para el método de Ruffini.

💬 Puedes preguntarme sobre:
• "¿Qué es Ruffini?"
• "¿Cómo usar la calculadora?"
• "Errores comunes"
• "¿Cómo interpretar el resultado?"
• "Ejemplo paso a paso"

¡Escribe tu pregunta y te ayudo! 😊"""

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    print("🧮 Iniciando Calculadora de Ruffini con IA...")
    print("🌐 Servidor disponible en: http://localhost:5000")
    print("📚 Presiona Ctrl+C para detener el servidor")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
