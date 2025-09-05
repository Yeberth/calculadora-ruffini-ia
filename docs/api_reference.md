# 🔌 Referencia de API - Calculadora de Ruffini

## Información General

**Base URL**: `http://localhost:5000`  
**Formato**: JSON  
**Métodos HTTP**: GET, POST  
**Content-Type**: `application/json`

## Endpoints

### 1. Cálculo de Ruffini

#### `POST /calculate`

Realiza el cálculo del método de Ruffini para un polinomio y una raíz dados.

**Request Body:**
```json
{
  "polynomial": "x^3 + 2x^2 - 5x + 6",
  "root": 2
}
```

**Parámetros:**
- `polynomial` (string, requerido): El polinomio en formato estándar
- `root` (number, requerido): La raíz para la división

**Response (200 OK):**
```json
{
  "success": true,
  "result": {
    "cociente": [1, 4, 3],
    "resto": 12,
    "tabla_ruffini": [
      [1, 2, -5, 6],
      [null, 2, 8, 6],
      [1, 4, 3, 12]
    ],
    "polinomio_cociente": "x² + 4x + 3",
    "explicacion_ia": "🤖 EXPLICACIÓN CON IA - MÉTODO DE RUFFINI...",
    "pasos": [
      "Paso 1: Escribimos los coeficientes del polinomio: [1, 2, -5, 6]",
      "Paso 2: Bajamos el primer coeficiente: 1",
      "Paso 3: Multiplicamos 1 × 2 = 2, sumamos 2 + 2 = 4",
      "Paso 4: Multiplicamos 4 × 2 = 8, sumamos -5 + 8 = 3",
      "Paso 5: Multiplicamos 3 × 2 = 6, sumamos 6 + 6 = 12"
    ]
  }
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Formato de polinomio inválido",
  "message": "El polinomio debe estar en formato: x^n + ... + c"
}
```

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:5000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "polynomial": "x^3 + 2x^2 - 5x + 6",
    "root": 2
  }'
```

### 2. Validación de Polinomios

#### `POST /validate`

Valida el formato de un polinomio sin realizar cálculos.

**Request Body:**
```json
{
  "polynomial": "x^3 + 2x^2 - 5x + 6"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "valid": true,
  "polynomial_info": {
    "grado": 3,
    "coeficientes": [1, 2, -5, 6],
    "formato_normalizado": "x³ + 2x² - 5x + 6"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "valid": false,
  "error": "Sintaxis inválida",
  "suggestions": [
    "Verificar el uso de ^ para potencias",
    "Usar solo variables 'x'",
    "Incluir coeficientes explícitos"
  ]
}
```

### 3. Ejemplos Predefinidos

#### `GET /examples`

Obtiene una lista de ejemplos predefinidos para práctica.

**Response (200 OK):**
```json
{
  "success": true,
  "examples": [
    {
      "id": 1,
      "title": "División Exacta",
      "polynomial": "x^3 - 6x^2 + 11x - 6",
      "root": 1,
      "description": "Ejemplo básico con resto cero"
    },
    {
      "id": 2,
      "title": "Con Resto",
      "polynomial": "x^3 + 2x^2 - 5x + 6",
      "root": 2,
      "description": "División con resto no nulo"
    },
    {
      "id": 3,
      "title": "Raíz Negativa",
      "polynomial": "x^3 + x^2 - 2x",
      "root": -2,
      "description": "Usando una raíz negativa"
    }
  ]
}
```

### 4. Tutor de IA

#### `POST /ai-tutor`

Proporciona explicaciones y respuestas educativas sobre el método de Ruffini.

**Request Body:**
```json
{
  "question": "¿Qué es el método de Ruffini?",
  "context": {
    "polynomial": "x^3 + 2x^2 - 5x + 6",
    "root": 2,
    "user_level": "intermedio"
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "response": "El método de Ruffini es una técnica simplificada para dividir polinomios...",
  "related_topics": [
    "División sintética",
    "Teorema del resto",
    "Factorización de polinomios"
  ],
  "examples": [
    {
      "polynomial": "x^2 + 3x + 2",
      "root": -1,
      "description": "Ejemplo más simple"
    }
  ]
}
```

### 5. Información de Estado

#### `GET /status`

Obtiene información sobre el estado del servidor.

**Response (200 OK):**
```json
{
  "success": true,
  "status": "running",
  "version": "1.0.0",
  "uptime": 3600,
  "calculations_performed": 1247
}
```

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 400 | Bad Request - Error en los parámetros |
| 404 | Not Found - Endpoint no encontrado |
| 405 | Method Not Allowed - Método HTTP incorrecto |
| 500 | Internal Server Error - Error del servidor |

## Manejo de Errores

Todas las respuestas de error siguen este formato:

```json
{
  "success": false,
  "error": "Código de error",
  "message": "Descripción detallada del error",
  "details": {
    "field": "Campo específico con error (si aplica)",
    "value": "Valor que causó el error (si aplica)"
  }
}
```

### Errores Comunes

#### Error de Formato de Polinomio
```json
{
  "success": false,
  "error": "INVALID_POLYNOMIAL_FORMAT",
  "message": "El polinomio debe usar la variable 'x' y el formato estándar",
  "details": {
    "field": "polynomial",
    "value": "2y^2 + 3y + 1",
    "expected_format": "x^n + ... + c"
  }
}
```

#### Error de Tipo de Raíz
```json
{
  "success": false,
  "error": "INVALID_ROOT_TYPE",
  "message": "La raíz debe ser un número",
  "details": {
    "field": "root",
    "value": "abc",
    "expected_type": "number"
  }
}
```

## Límites y Restricciones

- **Grado máximo del polinomio**: 10
- **Precisión decimal**: 6 decimales
- **Rate limiting**: 100 requests por minuto por IP
- **Timeout**: 30 segundos por request

## Autenticación

La API actual no requiere autenticación. Para uso en producción, se recomienda implementar autenticación basada en API keys.

## Ejemplos de Integración

### JavaScript (Fetch API)
```javascript
async function calcularRuffini(polynomial, root) {
  try {
    const response = await fetch('http://localhost:5000/calculate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ polynomial, root })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### Python (requests)
```python
import requests

def calcular_ruffini(polynomial, root):
    url = 'http://localhost:5000/calculate'
    data = {
        'polynomial': polynomial,
        'root': root
    }
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except requests.RequestException as e:
        print(f'Error: {e}')
        return None
```

## Versionado

La API sigue el versionado semántico (SemVer). La versión actual es `1.0.0`.

Para futuras versiones, se usará el header:
```
API-Version: 1.0
```

## Soporte

Para reportar bugs o solicitar nuevas funcionalidades en la API:
- GitHub Issues: https://github.com/Yeberth/calculadora-ruffini-ia/issues

---

**Última actualización**: Septiembre 2024  
**Versión de la API**: 1.0.0
