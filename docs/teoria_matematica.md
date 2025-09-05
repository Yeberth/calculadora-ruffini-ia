# 📐 Teoría Matemática - Método de Ruffini

## Introducción

El **Método de Ruffini** (también conocido como **División Sintética**) es una técnica algebraica desarrollada por el matemático italiano Paolo Ruffini (1765-1822) para dividir polinomios de manera eficiente.

## Fundamentos Teóricos

### División de Polinomios

La división de polinomios es análoga a la división aritmética. Dado un polinomio dividendo `P(x)` y un divisor `D(x)`, buscamos un cociente `Q(x)` y un resto `R(x)` tales que:

```
P(x) = D(x) · Q(x) + R(x)
```

Donde el grado de `R(x)` es menor que el grado de `D(x)`.

### Caso Específico: Divisor Lineal

El método de Ruffini se aplica específicamente cuando el divisor es un binomio de la forma:
```
D(x) = x - a
```

Donde `a` es una constante (la raíz).

## Teorema del Resto

**Teorema**: Si un polinomio `P(x)` se divide por `(x - a)`, entonces el resto es igual a `P(a)`.

**Demostración**:
```
P(x) = (x - a) · Q(x) + R
```

Evaluando en `x = a`:
```
P(a) = (a - a) · Q(a) + R = 0 · Q(a) + R = R
```

### Corolario: Teorema del Factor

Si `P(a) = 0`, entonces `(x - a)` es un factor de `P(x)`.

## Algoritmo de Ruffini

### Configuración Inicial

Para dividir `P(x) = a_n x^n + a_{n-1} x^{n-1} + ... + a_1 x + a_0` entre `(x - r)`:

1. Escribir los coeficientes: `[a_n, a_{n-1}, ..., a_1, a_0]`
2. Colocar la raíz `r` a la izquierda
3. Crear la tabla de trabajo

### Proceso Iterativo

**Tabla inicial:**
```
    | a_n  a_{n-1}  ...  a_1  a_0
  r |
    | a_n
```

**Para cada posición `i` (desde 1 hasta n):**
1. Multiplicar el valor de abajo anterior por `r`
2. Sumar con el coeficiente de arriba
3. Escribir el resultado abajo

**Fórmula recursiva:**
```
b_0 = a_n
b_i = a_{n-i} + r · b_{i-1}  para i = 1, 2, ..., n
```

### Interpretación de Resultados

- **Cociente**: `Q(x) = b_0 x^{n-1} + b_1 x^{n-2} + ... + b_{n-2} x + b_{n-1}`
- **Resto**: `R = b_n`

## Ejemplos Matemáticos Detallados

### Ejemplo 1: División Exacta

**Problema**: Dividir `P(x) = x³ - 6x² + 11x - 6` entre `(x - 1)`

**Coeficientes**: `[1, -6, 11, -6]`  
**Raíz**: `r = 1`

**Tabla de Ruffini**:
```
    |  1  -6  11  -6
  1 |      1  -5   6
    |  1  -5   6   0
```

**Cálculos paso a paso**:
- `b₀ = 1` (bajamos el primer coeficiente)
- `b₁ = -6 + 1×1 = -5`
- `b₂ = 11 + 1×(-5) = 6`
- `b₃ = -6 + 1×6 = 0`

**Resultado**: `Q(x) = x² - 5x + 6`, `R = 0`

**Verificación**: `x³ - 6x² + 11x - 6 = (x - 1)(x² - 5x + 6) + 0` ✓

### Ejemplo 2: Con Resto No Nulo

**Problema**: Dividir `P(x) = 2x⁴ - 3x³ + x² - 5x + 7` entre `(x + 2)`

**Coeficientes**: `[2, -3, 1, -5, 7]`  
**Raíz**: `r = -2` (porque `x + 2 = x - (-2)`)

**Tabla de Ruffini**:
```
    |  2  -3   1  -5   7
 -2 |     -4  14 -30  70
    |  2  -7  15 -35  77
```

**Resultado**: `Q(x) = 2x³ - 7x² + 15x - 35`, `R = 77`

## Propiedades Matemáticas

### 1. Reducción de Grado
El cociente siempre tiene grado `n-1` si el dividendo tiene grado `n`.

### 2. Preservación de Coeficientes Principales
Si el coeficiente principal del dividendo es `a_n`, entonces el coeficiente principal del cociente también es `a_n`.

### 3. Relación con Derivadas
El método de Ruffini está relacionado con la evaluación de derivadas mediante la fórmula de Taylor.

### 4. Estabilidad Numérica
El algoritmo es numéricamente estable para la mayoría de casos prácticos.

## Casos Especiales

### Polinomios con Coeficientes Faltantes

Para `P(x) = x⁴ - 5x² + 6`, los coeficientes son `[1, 0, -5, 0, 6]`.

### Raíces Complejas

El método también funciona con raíces complejas:
- Para dividir por `(x - (2+3i))`, usar `r = 2+3i`

### Múltiples Aplicaciones

Para factorizar completamente, aplicar Ruffini sucesivamente:
```
P(x) → (x-r₁)Q₁(x) → (x-r₁)(x-r₂)Q₂(x) → ...
```

## Conexiones con Otros Conceptos

### 1. Horner's Method
El método de Ruffini es equivalente al método de Horner para evaluar polinomios.

### 2. Diferencias Finitas
Relacionado con el cálculo de diferencias finitas de polinomios.

### 3. Interpolación
Útil en métodos de interpolación polinómica.

### 4. Análisis Numérico
Base para algoritmos de encontrar raíces (método de Newton-Raphson).

## Limitaciones y Consideraciones

### 1. Solo Divisores Lineales
El método estándar solo funciona con divisores de la forma `(x - a)`.

### 2. Precisión Numérica
Con aritmética de punto flotante, pueden acumularse errores.

### 3. Raíces Múltiples
Para raíces de multiplicidad `k > 1`, se debe aplicar el método `k` veces.

## Extensiones del Método

### División Sintética Generalizada
Extensión para divisores cuadráticos `ax² + bx + c`.

### Método de Ruffini-Horner
Combinación para evaluación simultánea de polinomio y derivadas.

## Aplicaciones Prácticas

### 1. Factorización de Polinomios
Encontrar factores lineales sistemáticamente.

### 2. Resolución de Ecuaciones
Reducir el grado de ecuaciones polinómicas.

### 3. Gráficas de Funciones
Encontrar intersecciones con el eje x.

### 4. Cálculo Diferencial
Simplificar funciones racionales para integración.

## Ejercicios Propuestos

### Nivel Básico
1. Dividir `x² + 5x + 6` entre `(x + 2)`
2. Dividir `x³ - 1` entre `(x - 1)`

### Nivel Intermedio
3. Dividir `2x⁴ - x³ + 3x - 5` entre `(x + 1)`
4. Encontrar el resto de `x⁵⁰ + x⁴⁹ + ... + x + 1` dividido por `(x - 1)`

### Nivel Avanzado
5. Factorizar completamente `x⁴ - 10x² + 9`
6. Demostrar que si `P(x)` tiene grado `n`, entonces `P(x) - P(a) = (x-a)Q(x)` donde `Q(x)` tiene grado `n-1`

## Referencias Históricas

- **Paolo Ruffini** (1765-1822): Matemático italiano que desarrolló el método
- **Conexión con Abel-Ruffini**: Teorema sobre la imposibilidad de resolver ecuaciones de grado ≥5 por radicales
- **William Horner** (1786-1837): Método de Horner para evaluación de polinomios

---

**Para más información**, consulta:
- [Guía de Usuario](guia_usuario.md)
- [Referencia de API](api_reference.md)
- Repositorio: https://github.com/Yeberth/calculadora-ruffini-ia
