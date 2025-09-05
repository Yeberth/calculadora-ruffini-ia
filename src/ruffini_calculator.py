"""
Calculadora de Ruffini con integración de IA
Implementa el método de Ruffini para división polinómica con explicaciones detalladas
"""

import json
from typing import List, Tuple, Dict, Any
import re

class RuffiniCalculator:
    """
    Calculadora que implementa el método de Ruffini para división polinómica
    """
    
    def __init__(self):
        self.steps = []  # Para almacenar pasos del proceso
        self.explanation = []  # Para explicaciones de IA
        
    def parse_polynomial(self, poly_str: str) -> List[float]:
        """
        Convierte una cadena de polinomio en lista de coeficientes
        Ejemplo: "x^3 + 2x^2 - 5x + 6" -> [1, 2, -5, 6]
        """
        # Remover espacios y normalizar
        poly_str = poly_str.replace(' ', '').replace('-', '+-')
        
        # Encontrar el grado máximo
        degrees = re.findall(r'x\^(\d+)', poly_str)
        if not degrees:
            # Si no hay x^n, buscar x solo
            if 'x' in poly_str:
                max_degree = 1
            else:
                max_degree = 0
        else:
            max_degree = max(map(int, degrees))
        
        # Inicializar coeficientes en cero
        coefficients = [0] * (max_degree + 1)
        
        # Encontrar todos los términos
        terms = re.findall(r'[+-]?[^+-]+', poly_str)
        
        for term in terms:
            term = term.strip()
            if not term:
                continue
                
            # Término constante
            if 'x' not in term:
                coefficients[max_degree] = float(term)
            else:
                # Extraer coeficiente
                coef_match = re.match(r'([+-]?\d*)', term)
                coef_str = coef_match.group(1) if coef_match else '1'
                
                if coef_str == '' or coef_str == '+':
                    coef = 1
                elif coef_str == '-':
                    coef = -1
                else:
                    coef = float(coef_str)
                
                # Extraer grado
                if '^' in term:
                    degree_match = re.search(r'x\^(\d+)', term)
                    degree = int(degree_match.group(1)) if degree_match else 1
                else:
                    degree = 1
                
                coefficients[max_degree - degree] = coef
        
        return coefficients
    
    def ruffini_division(self, coefficients: List[float], root: float) -> Tuple[List[float], float]:
        """
        Realiza la división de Ruffini
        
        Args:
            coefficients: Lista de coeficientes del polinomio
            root: Valor por el que se divide (x - root)
            
        Returns:
            Tupla con (coeficientes del cociente, resto)
        """
        self.steps = []
        n = len(coefficients)
        
        # Primera fila: coeficientes originales
        self.steps.append({
            'step': 0,
            'description': 'Coeficientes del polinomio original',
            'row1': coefficients.copy(),
            'row2': [0] * n,
            'row3': [coefficients[0]]
        })
        
        result = [coefficients[0]]  # El primer coeficiente se copia
        
        for i in range(1, n):
            # Multiplicar el resultado anterior por la raíz
            product = result[i-1] * root
            
            # Sumar al coeficiente actual
            new_coef = coefficients[i] + product
            result.append(new_coef)
            
            # Guardar paso
            row2 = [0] * n
            row2[i] = product
            
            self.steps.append({
                'step': i,
                'description': f'Paso {i}: Multiplicar {result[i-1]} × {root} = {product}, luego sumar {coefficients[i]} + {product} = {new_coef}',
                'row1': coefficients.copy(),
                'row2': row2,
                'row3': result.copy()
            })
        
        # El último elemento es el resto
        remainder = result[-1]
        quotient = result[:-1]
        
        return quotient, remainder
    
    def format_polynomial(self, coefficients: List[float]) -> str:
        """
        Convierte lista de coeficientes a representación polinómica
        """
        if not coefficients:
            return "0"
        
        terms = []
        degree = len(coefficients) - 1
        
        for i, coef in enumerate(coefficients):
            if coef == 0:
                continue
                
            current_degree = degree - i
            
            # Formato del coeficiente
            if coef == 1 and current_degree > 0:
                coef_str = ""
            elif coef == -1 and current_degree > 0:
                coef_str = "-"
            else:
                coef_str = str(int(coef) if coef.is_integer() else coef)
            
            # Formato de la variable
            if current_degree == 0:
                term = coef_str if coef_str != "" else "1"
            elif current_degree == 1:
                term = f"{coef_str}x"
            else:
                term = f"{coef_str}x^{current_degree}"
            
            terms.append(term)
        
        if not terms:
            return "0"
        
        # Unir términos con signos apropiados
        result = terms[0]
        for term in terms[1:]:
            if term.startswith('-'):
                result += f" - {term[1:]}"
            else:
                result += f" + {term}"
        
        return result
    
    def generate_ai_explanation(self, polynomial: str, root: float, quotient: List[float], remainder: float) -> str:
        """
        Genera explicación detallada del proceso usando IA
        """
        explanation = f"""
🤖 EXPLICACIÓN CON IA - MÉTODO DE RUFFINI

📊 PROBLEMA:
Dividir el polinomio: {polynomial}
Entre: (x - {root})

🔍 PROCESO PASO A PASO:

El método de Ruffini es una forma simplificada de la división polinómica.
Se utiliza específicamente para dividir un polinomio entre un binomio de la forma (x - a).

📋 PASOS REALIZADOS:
"""
        
        for i, step in enumerate(self.steps):
            explanation += f"\n{step['step']}. {step['description']}"
            explanation += f"\n   Fila 1: {step['row1']}"
            explanation += f"\n   Fila 2: {step['row2']}"
            explanation += f"\n   Resultado: {step['row3']}\n"
        
        quotient_poly = self.format_polynomial(quotient)
        
        explanation += f"""
✅ RESULTADO FINAL:
• Cociente: {quotient_poly}
• Resto: {remainder}

🎯 VERIFICACIÓN:
El resultado se puede verificar con: ({quotient_poly}) × (x - {root}) + {remainder}

💡 INTERPRETACIÓN:
"""
        
        if remainder == 0:
            explanation += f"Como el resto es 0, (x - {root}) es un factor del polinomio original."
        else:
            explanation += f"Como el resto es {remainder} ≠ 0, (x - {root}) no es un factor exacto del polinomio."
        
        return explanation
    
    def calculate(self, polynomial_str: str, root: float) -> Dict[str, Any]:
        """
        Función principal que realiza el cálculo completo
        """
        try:
            # Parsear el polinomio
            coefficients = self.parse_polynomial(polynomial_str)
            
            # Realizar división de Ruffini
            quotient, remainder = self.ruffini_division(coefficients, root)
            
            # Formatear resultado
            quotient_str = self.format_polynomial(quotient)
            
            # Generar explicación con IA
            explanation = self.generate_ai_explanation(
                polynomial_str, root, quotient, remainder
            )
            
            return {
                'success': True,
                'polynomial': polynomial_str,
                'root': root,
                'coefficients': coefficients,
                'quotient_coefficients': quotient,
                'quotient': quotient_str,
                'remainder': remainder,
                'steps': self.steps,
                'ai_explanation': explanation
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'ai_help': self.generate_error_help(str(e))
            }
    
    def generate_error_help(self, error: str) -> str:
        """
        Genera ayuda con IA para errores comunes
        """
        return f"""
🤖 AYUDA DE IA - ERROR DETECTADO

❌ Error: {error}

💡 SUGERENCIAS:
• Verifica que el polinomio esté en formato correcto (ej: x^3 + 2x^2 - 5x + 6)
• Asegúrate de usar ^ para exponentes
• Los coeficientes negativos deben incluir el signo -
• Usa * para multiplicación explícita si es necesario

📝 EJEMPLOS VÁLIDOS:
• x^3 + 2x^2 - 5x + 6
• 2x^2 - 3x + 1
• x^4 - 1
• 3x + 5

¿Necesitas más ayuda? Revisa la documentación o prueba con un ejemplo más simple.
"""

# Función de utilidad para usar desde línea de comandos
def main():
    """
    Función principal para uso desde línea de comandos
    """
    print("🧮 Calculadora de Ruffini con IA")
    print("=" * 40)
    
    calculator = RuffiniCalculator()
    
    while True:
        print("\n📝 Ingresa el polinomio (o 'salir' para terminar):")
        polynomial = input("Polinomio: ").strip()
        
        if polynomial.lower() in ['salir', 'exit', 'quit']:
            print("¡Hasta luego! 👋")
            break
        
        try:
            root = float(input("Raíz (valor de a en x-a): "))
            
            result = calculator.calculate(polynomial, root)
            
            if result['success']:
                print(f"\n✅ Resultado:")
                print(f"Cociente: {result['quotient']}")
                print(f"Resto: {result['remainder']}")
                print(f"\n{result['ai_explanation']}")
            else:
                print(f"\n❌ Error: {result['error']}")
                print(result['ai_help'])
                
        except ValueError:
            print("❌ Error: Por favor ingresa un número válido para la raíz")
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego! 👋")
            break

if __name__ == "__main__":
    main()
