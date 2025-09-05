#!/usr/bin/env python3
"""
Ejemplos prácticos de uso de la Calculadora de Ruffini con IA
Demonstraciones interactivas y casos de uso comunes
"""

import sys
import os

# Agregar el directorio padre al path para importar la calculadora
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ruffini_calculator import RuffiniCalculator

class EjemplosRuffini:
    """
    Clase con ejemplos prácticos del método de Ruffini
    """
    
    def __init__(self):
        self.calculator = RuffiniCalculator()
    
    def ejemplo_basico(self):
        """Ejemplo básico: Polinomio cúbico simple"""
        print("🎯 EJEMPLO 1: POLINOMIO CÚBICO BÁSICO")
        print("=" * 50)
        
        polynomial = "x^3 + 2x^2 - 5x + 6"
        root = 2
        
        print(f"Dividir: {polynomial}")
        print(f"Entre: (x - {root})")
        print()
        
        result = self.calculator.calculate(polynomial, root)
        
        if result['success']:
            print("✅ RESULTADO:")
            print(f"Cociente: {result['quotient']}")
            print(f"Resto: {result['remainder']}")
            print()
            print(result['ai_explanation'])
        else:
            print(f"❌ Error: {result['error']}")
        
        print("\n" + "="*70 + "\n")
    
    def ejemplo_division_exacta(self):
        """Ejemplo de división exacta (resto = 0)"""
        print("🎯 EJEMPLO 2: DIVISIÓN EXACTA")
        print("=" * 50)
        
        polynomial = "x^3 - 6x^2 + 11x - 6"
        root = 1
        
        print(f"Dividir: {polynomial}")
        print(f"Entre: (x - {root})")
        print()
        print("💡 En este ejemplo esperamos encontrar una división exacta")
        print()
        
        result = self.calculator.calculate(polynomial, root)
        
        if result['success']:
            print("✅ RESULTADO:")
            print(f"Cociente: {result['quotient']}")
            print(f"Resto: {result['remainder']}")
            
            if result['remainder'] == 0:
                print("🎉 ¡División exacta! Esto significa que (x - 1) es un factor.")
            
            print()
            print(result['ai_explanation'])
        else:
            print(f"❌ Error: {result['error']}")
        
        print("\n" + "="*70 + "\n")
    
    def ejemplo_raiz_negativa(self):
        """Ejemplo con raíz negativa"""
        print("🎯 EJEMPLO 3: RAÍZ NEGATIVA")
        print("=" * 50)
        
        polynomial = "x^3 + x^2 - 2x"
        root = -2
        
        print(f"Dividir: {polynomial}")
        print(f"Entre: (x - ({root})) = (x + 2)")
        print()
        print("💡 Para dividir por (x + 2), usamos raíz = -2")
        print()
        
        result = self.calculator.calculate(polynomial, root)
        
        if result['success']:
            print("✅ RESULTADO:")
            print(f"Cociente: {result['quotient']}")
            print(f"Resto: {result['remainder']}")
            print()
            print(result['ai_explanation'])
        else:
            print(f"❌ Error: {result['error']}")
        
        print("\n" + "="*70 + "\n")
    
    def ejemplo_grado_alto(self):
        """Ejemplo con polinomio de grado alto"""
        print("🎯 EJEMPLO 4: POLINOMIO DE GRADO 4")
        print("=" * 50)
        
        polynomial = "x^4 - 10x^3 + 35x^2 - 50x + 24"
        root = 1
        
        print(f"Dividir: {polynomial}")
        print(f"Entre: (x - {root})")
        print()
        print("💡 Los polinomios de grado alto pueden tener múltiples factores")
        print()
        
        result = self.calculator.calculate(polynomial, root)
        
        if result['success']:
            print("✅ RESULTADO:")
            print(f"Cociente: {result['quotient']}")
            print(f"Resto: {result['remainder']}")
            print()
            
            if result['remainder'] == 0:
                print("🔥 ¡Excelente! Podemos continuar factorizando el cociente.")
                print("Consejo: Aplica Ruffini de nuevo al cociente para encontrar más factores.")
            
            print()
            print(result['ai_explanation'])
        else:
            print(f"❌ Error: {result['error']}")
        
        print("\n" + "="*70 + "\n")
    
    def ejemplo_coeficientes_fraccionarios(self):
        """Ejemplo con raíz fraccionaria"""
        print("🎯 EJEMPLO 5: RAÍZ FRACCIONARIA")
        print("=" * 50)
        
        polynomial = "2x^3 - 3x^2 + 1"
        root = 0.5
        
        print(f"Dividir: {polynomial}")
        print(f"Entre: (x - {root}) = (x - 1/2)")
        print()
        print("💡 Las raíces pueden ser números decimales o fracciones")
        print()
        
        result = self.calculator.calculate(polynomial, root)
        
        if result['success']:
            print("✅ RESULTADO:")
            print(f"Cociente: {result['quotient']}")
            print(f"Resto: {result['remainder']}")
            print()
            print(result['ai_explanation'])
        else:
            print(f"❌ Error: {result['error']}")
        
        print("\n" + "="*70 + "\n")
    
    def caso_estudio_factorizacion(self):
        """Caso de estudio: Factorización completa"""
        print("🎯 CASO DE ESTUDIO: FACTORIZACIÓN COMPLETA")
        print("=" * 60)
        
        polynomial = "x^3 - 6x^2 + 11x - 6"
        
        print(f"Objetivo: Factorizar completamente {polynomial}")
        print()
        print("Estrategia:")
        print("1. Usar el teorema del factor racional")
        print("2. Probar divisores del término independiente: ±1, ±2, ±3, ±6")
        print("3. Aplicar Ruffini sucesivamente")
        print()
        
        # Probar diferentes raíces
        possible_roots = [1, -1, 2, -2, 3, -3, 6, -6]
        factors = []
        current_poly = polynomial
        
        print("🔍 PROCESO DE FACTORIZACIÓN:")
        print()
        
        for root in possible_roots:
            print(f"Probando raíz = {root}...")
            result = self.calculator.calculate(current_poly, root)
            
            if result['success'] and result['remainder'] == 0:
                print(f"✅ ¡Raíz encontrada! (x - {root}) es un factor")
                factors.append(f"(x - {root})")
                current_poly = result['quotient']
                print(f"Nuevo polinomio a factorizar: {current_poly}")
                print()
                
                # Si llegamos a un polinomio cuadrático, podemos parar
                if len(result['quotient_coefficients']) <= 3:  # grado 2 o menos
                    print("📋 Factorización encontrada:")
                    factors_str = " × ".join(factors)
                    print(f"{polynomial} = {factors_str} × ({current_poly})")
                    
                    # Si el cociente final es cuadrático, podríamos factorizarlo más
                    if len(result['quotient_coefficients']) == 3:
                        print()
                        print("💡 El factor cuadrático se puede factorizar usando la fórmula cuadrática o")
                        print("   continuar con el método de Ruffini si tiene raíces racionales.")
                    
                    break
            else:
                print("❌ No es una raíz")
        
        print("\n" + "="*70 + "\n")
    
    def demostrar_teorema_resto(self):
        """Demostración del teorema del resto"""
        print("🎯 DEMOSTRACIÓN: TEOREMA DEL RESTO")
        print("=" * 50)
        
        polynomial = "x^3 - 4x^2 + 5x - 2"
        root = 3
        
        print("📚 TEOREMA DEL RESTO:")
        print("Si dividimos P(x) entre (x - a), el resto es P(a)")
        print()
        print(f"Polinomio: P(x) = {polynomial}")
        print(f"Dividir entre: (x - {root})")
        print()
        
        # Calcular P(a) directamente
        # P(3) = 3^3 - 4(3^2) + 5(3) - 2 = 27 - 36 + 15 - 2 = 4
        p_a = 3**3 - 4*(3**2) + 5*3 - 2
        print(f"🧮 Cálculo directo: P({root}) = {root}³ - 4({root})² + 5({root}) - 2")
        print(f"P({root}) = 27 - 36 + 15 - 2 = {p_a}")
        print()
        
        # Usar Ruffini
        result = self.calculator.calculate(polynomial, root)
        
        if result['success']:
            print(f"🎯 Resultado de Ruffini: Resto = {result['remainder']}")
            print()
            
            if abs(result['remainder'] - p_a) < 1e-10:  # Considerando errores de punto flotante
                print("✅ ¡VERIFICADO! El teorema del resto se cumple:")
                print(f"P({root}) = Resto = {result['remainder']}")
            else:
                print("❌ Error en el cálculo")
            
            print()
            print("💡 Aplicación práctica:")
            print("- Para verificar si 'a' es raíz de P(x), basta calcular P(a)")
            print("- Si P(a) = 0, entonces 'a' es raíz y (x - a) es factor")
            print("- El método de Ruffini nos da este resultado automáticamente")
        
        print("\n" + "="*70 + "\n")

def ejecutar_todos_ejemplos():
    """Ejecuta todos los ejemplos de forma secuencial"""
    ejemplos = EjemplosRuffini()
    
    print("🧮 CALCULADORA DE RUFFINI CON IA")
    print("📚 EJEMPLOS PRÁCTICOS Y CASOS DE ESTUDIO")
    print("=" * 70)
    print()
    
    try:
        ejemplos.ejemplo_basico()
        ejemplos.ejemplo_division_exacta()
        ejemplos.ejemplo_raiz_negativa()
        ejemplos.ejemplo_grado_alto()
        ejemplos.ejemplo_coeficientes_fraccionarios()
        ejemplos.caso_estudio_factorizacion()
        ejemplos.demostrar_teorema_resto()
        
        print("🎉 ¡Todos los ejemplos completados!")
        print("💡 Consejos adicionales:")
        print("- Siempre verifica tus resultados")
        print("- Usa el teorema del factor racional para encontrar candidatos a raíces")
        print("- La calculadora web ofrece explicaciones interactivas paso a paso")
        print("- Practica con diferentes tipos de polinomios")
        
    except KeyboardInterrupt:
        print("\\n\\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\\n❌ Error inesperado: {e}")

def menu_interactivo():
    """Menú interactivo para elegir ejemplos"""
    ejemplos = EjemplosRuffini()
    
    opciones = {
        '1': ('Ejemplo básico', ejemplos.ejemplo_basico),
        '2': ('División exacta', ejemplos.ejemplo_division_exacta),
        '3': ('Raíz negativa', ejemplos.ejemplo_raiz_negativa),
        '4': ('Grado alto', ejemplos.ejemplo_grado_alto),
        '5': ('Raíz fraccionaria', ejemplos.ejemplo_coeficientes_fraccionarios),
        '6': ('Factorización completa', ejemplos.caso_estudio_factorizacion),
        '7': ('Teorema del resto', ejemplos.demostrar_teorema_resto),
        '8': ('Todos los ejemplos', ejecutar_todos_ejemplos)
    }
    
    while True:
        print("\\n🧮 MENÚ DE EJEMPLOS - CALCULADORA RUFFINI")
        print("=" * 45)
        
        for key, (nombre, _) in opciones.items():
            print(f"{key}. {nombre}")
        
        print("0. Salir")
        print()
        
        opcion = input("Elige una opción (0-8): ").strip()
        
        if opcion == '0':
            print("¡Hasta luego! 👋")
            break
        
        if opcion in opciones:
            print()
            opciones[opcion][1]()
            input("\\nPresiona Enter para continuar...")
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Ejemplos de la Calculadora de Ruffini')
    parser.add_argument('--todos', action='store_true', help='Ejecutar todos los ejemplos')
    parser.add_argument('--interactivo', action='store_true', help='Menú interactivo')
    
    args = parser.parse_args()
    
    if args.todos:
        ejecutar_todos_ejemplos()
    elif args.interactivo:
        menu_interactivo()
    else:
        # Por defecto, mostrar menú interactivo
        menu_interactivo()
