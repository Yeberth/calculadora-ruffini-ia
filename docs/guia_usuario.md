# 📖 Guía de Usuario - Calculadora de Ruffini con IA

## Introducción

La Calculadora de Ruffini con IA es una herramienta educativa que te ayuda a resolver divisiones polinómicas utilizando el método de Ruffini, con explicaciones detalladas generadas por inteligencia artificial.

## Primeros Pasos

### Acceso a la Aplicación

1. **Interfaz Web**: Abre tu navegador y visita `http://localhost:5000`
2. **Línea de Comandos**: Ejecuta `python src/ruffini_calculator.py`

### Formato de Entrada

#### Polinomios
- Formato estándar: `x^3 + 2x^2 - 5x + 6`
- Coeficientes negativos: `x^3 - 2x^2 + 5x - 6`
- Términos faltantes: `x^3 + 6` (equivale a `x^3 + 0x^2 + 0x + 6`)

#### Raíces
- Para dividir por `(x - 2)`, usar raíz: `2`
- Para dividir por `(x + 3)`, usar raíz: `-3`

## Uso de la Interfaz Web

### Paso 1: Ingresar el Polinomio
1. En el campo "Polinomio", escribe tu expresión
2. Ejemplo: `x^3 + 2x^2 - 5x + 6`

### Paso 2: Especificar la Raíz
1. En el campo "Raíz", ingresa el valor
2. Para `(x - a)`, usar `a`
3. Ejemplo: Para `(x - 2)`, usar `2`

### Paso 3: Calcular
1. Haz clic en "Calcular Ruffini"
2. Observa la tabla de resultados
3. Lee la explicación de IA

## Interpretación de Resultados

### Tabla de Ruffini
```
    |  1   2  -5   6
  2 |      2   8   6
    |  1   4   3  12
```

- **Primera fila**: Coeficientes del polinomio original
- **Segunda fila**: Productos parciales
- **Tercera fila**: Resultados (cociente + resto)

### Resultado Final
- **Cociente**: `x² + 4x + 3` (todos menos el último número)
- **Resto**: `12` (último número de la fila inferior)

## Ejemplos Prácticos

### Ejemplo 1: División Exacta
**Problema**: `x³ - 6x² + 11x - 6 ÷ (x - 1)`

**Solución**:
```
    |  1  -6  11  -6
  1 |      1  -5   6
    |  1  -5   6   0
```

**Resultado**: `x² - 5x + 6`, resto = 0

### Ejemplo 2: Con Resto
**Problema**: `x³ + 2x² - 5x + 6 ÷ (x - 2)`

**Solución**:
```
    |  1   2  -5   6
  2 |      2   8   6
    |  1   4   3  12
```

**Resultado**: `x² + 4x + 3`, resto = 12

## Funciones Avanzadas

### Validación Automática
- La aplicación verifica automáticamente el formato
- Sugiere correcciones para entradas inválidas
- Detecta errores comunes

### Explicaciones de IA
- Proceso paso a paso detallado
- Interpretación matemática
- Consejos pedagógicos personalizados

## Consejos y Trucos

### Para Estudiantes
1. **Practica regularmente**: Usa diferentes ejemplos
2. **Lee las explicaciones**: La IA proporciona contexto valioso
3. **Verifica manualmente**: Comprueba algunos pasos a mano
4. **Usa casos simples**: Comienza con polinomios de grado 2

### Para Profesores
1. **Ejemplos progresivos**: Usa la herramienta para mostrar dificultad creciente
2. **Análisis de errores**: Muestra qué pasa con entradas incorrectas
3. **Conexiones conceptuales**: Relaciona con factorización y teorema del resto

## Solución de Problemas

### Error: "Formato de polinomio inválido"
- **Causa**: Sintaxis incorrecta
- **Solución**: Usar formato `x^n + ... + c`

### Error: "Raíz debe ser un número"
- **Causa**: Entrada no numérica en el campo raíz
- **Solución**: Ingresar solo números (positivos o negativos)

### Resultados inesperados
- **Verificar**: Coeficientes del polinomio original
- **Comprobar**: Signo de la raíz (positivo/negativo)
- **Revisar**: Orden de los términos

## API para Desarrolladores

### Endpoint Básico
```bash
curl -X POST http://localhost:5000/calculate \
  -H "Content-Type: application/json" \
  -d '{"polynomial": "x^3+2x^2-5x+6", "root": 2}'
```

### Respuesta JSON
```json
{
  "cociente": [1, 4, 3],
  "resto": 12,
  "explicacion": "...",
  "pasos": [...]
}
```

## Recursos Adicionales

- [Referencia de API](api_reference.md)
- [Teoría Matemática](teoria_matematica.md)
- [Ejemplos Interactivos](../examples/ejemplos_practicos.py)

---

**¿Necesitas ayuda?** Visita nuestro [repositorio en GitHub](https://github.com/Yeberth/calculadora-ruffini-ia) o consulta la documentación adicional.
