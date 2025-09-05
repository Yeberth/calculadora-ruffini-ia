/**
 * Calculadora de Ruffini con IA - Frontend JavaScript
 * Maneja la interfaz de usuario y la comunicación con el backend
 */

class RuffiniApp {
    constructor() {
        this.calculator = new RuffiniCalculatorJS();
        this.initializeElements();
        this.attachEventListeners();
        this.examples = [
            { polynomial: 'x^3 + 2x^2 - 5x + 6', root: 2 },
            { polynomial: 'x^4 - 1', root: 1 },
            { polynomial: '2x^3 - 3x^2 + x - 2', root: 2 },
            { polynomial: 'x^2 - 5x + 6', root: 3 }
        ];
    }

    initializeElements() {
        // Formulario
        this.form = document.getElementById('ruffiniForm');
        this.polynomialInput = document.getElementById('polynomial');
        this.rootInput = document.getElementById('root');
        
        // Botones
        this.clearBtn = document.getElementById('clearBtn');
        this.exampleBtn = document.getElementById('exampleBtn');
        this.toggleExplanationBtn = document.getElementById('toggleExplanation');
        
        // Secciones
        this.loadingSection = document.getElementById('loading');
        this.resultsSection = document.getElementById('results');
        this.errorSection = document.getElementById('error');
        
        // Elementos de resultado
        this.quotientElement = document.getElementById('quotient');
        this.remainderElement = document.getElementById('remainder');
        this.ruffiniTable = document.getElementById('ruffiniTable');
        this.aiExplanation = document.getElementById('aiExplanation');
        this.verification = document.getElementById('verification');
        
        // Elementos de error
        this.errorMessage = document.getElementById('errorMessage');
        this.aiHelp = document.getElementById('aiHelp');
    }

    attachEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.clearBtn.addEventListener('click', () => this.clearForm());
        this.exampleBtn.addEventListener('click', () => this.loadExample());
        this.toggleExplanationBtn.addEventListener('click', () => this.toggleExplanation());
        
        // Auto-guardar en localStorage
        this.polynomialInput.addEventListener('input', () => this.saveToStorage());
        this.rootInput.addEventListener('input', () => this.saveToStorage());
        
        // Cargar datos guardados al iniciar
        this.loadFromStorage();
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const polynomial = this.polynomialInput.value.trim();
        const root = parseFloat(this.rootInput.value);
        
        if (!polynomial || isNaN(root)) {
            this.showError('Por favor completa todos los campos correctamente');
            return;
        }

        this.showLoading();
        
        try {
            // Simular delay de IA
            await new Promise(resolve => setTimeout(resolve, 800));
            
            const result = this.calculator.calculate(polynomial, root);
            
            if (result.success) {
                this.showResults(result);
            } else {
                this.showError(result.error, result.ai_help);
            }
        } catch (error) {
            this.showError('Error inesperado: ' + error.message);
        }
    }

    showLoading() {
        this.hideAllSections();
        this.loadingSection.style.display = 'block';
        this.scrollToSection(this.loadingSection);
    }

    showResults(result) {
        this.hideAllSections();
        
        // Mostrar resultado rápido
        this.quotientElement.textContent = result.quotient;
        this.remainderElement.textContent = result.remainder;
        
        // Generar tabla de Ruffini
        this.generateRuffiniTable(result);
        
        // Mostrar explicación de IA
        this.aiExplanation.innerHTML = `<pre>${result.ai_explanation}</pre>`;
        
        // Mostrar verificación
        this.generateVerification(result);
        
        this.resultsSection.style.display = 'block';
        this.scrollToSection(this.resultsSection);
    }

    showError(error, aiHelp = null) {
        this.hideAllSections();
        
        this.errorMessage.textContent = error;
        
        if (aiHelp) {
            this.aiHelp.innerHTML = `<pre>${aiHelp}</pre>`;
            this.aiHelp.style.display = 'block';
        } else {
            this.aiHelp.style.display = 'none';
        }
        
        this.errorSection.style.display = 'block';
        this.scrollToSection(this.errorSection);
    }

    hideAllSections() {
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.errorSection.style.display = 'none';
    }

    generateRuffiniTable(result) {
        const steps = result.steps;
        if (!steps || steps.length === 0) return;
        
        const n = steps[0].row1.length;
        
        let html = '<thead><tr><th>Paso</th>';
        for (let i = 0; i < n; i++) {
            html += `<th>Col ${i + 1}</th>`;
        }
        html += '</tr></thead><tbody>';
        
        // Fila de coeficientes originales
        html += '<tr><td><strong>Coeficientes</strong></td>';
        for (let coef of steps[0].row1) {
            html += `<td>${this.formatNumber(coef)}</td>`;
        }
        html += '</tr>';
        
        // Filas de pasos
        for (let step of steps.slice(1)) {
            html += `<tr><td>Paso ${step.step}</td>`;
            for (let i = 0; i < n; i++) {
                const value = step.row2[i] || '';
                html += `<td class="${value !== 0 && value !== '' ? 'highlight' : ''}">${value !== 0 && value !== '' ? this.formatNumber(value) : ''}</td>`;
            }
            html += '</tr>';
        }
        
        // Fila de resultados finales
        const lastStep = steps[steps.length - 1];
        html += '<tr style="border-top: 3px solid var(--primary-color);"><td><strong>Resultado</strong></td>';
        for (let value of lastStep.row3) {
            html += `<td><strong>${this.formatNumber(value)}</strong></td>`;
        }
        html += '</tr>';
        
        html += '</tbody>';
        this.ruffiniTable.innerHTML = html;
    }

    generateVerification(result) {
        const verification = `
            <h4>🎯 Verificación del resultado:</h4>
            <p><strong>Polinomio original:</strong> ${result.polynomial}</p>
            <p><strong>División:</strong> (${result.polynomial}) ÷ (x - ${result.root})</p>
            <p><strong>Cociente:</strong> ${result.quotient}</p>
            <p><strong>Resto:</strong> ${result.remainder}</p>
            <br>
            <p><strong>Verificación:</strong> (${result.quotient}) × (x - ${result.root}) + ${result.remainder} = ${result.polynomial}</p>
            ${result.remainder === 0 ? 
                '<p style="color: var(--success-color);"><strong>✅ División exacta:</strong> El resto es 0, por lo que (x - ' + result.root + ') es un factor del polinomio.</p>' :
                '<p style="color: var(--warning-color);"><strong>⚠️ División con resto:</strong> El resto es ' + result.remainder + ', por lo que (x - ' + result.root + ') no es un factor exacto.</p>'
            }
        `;
        
        this.verification.innerHTML = verification;
    }

    toggleExplanation() {
        const explanationBody = this.aiExplanation;
        const toggleBtn = this.toggleExplanationBtn;
        const icon = toggleBtn.querySelector('i');
        
        if (explanationBody.classList.contains('expanded')) {
            explanationBody.classList.remove('expanded');
            icon.className = 'fas fa-chevron-down';
        } else {
            explanationBody.classList.add('expanded');
            icon.className = 'fas fa-chevron-up';
        }
    }

    clearForm() {
        this.polynomialInput.value = '';
        this.rootInput.value = '';
        this.hideAllSections();
        this.clearStorage();
        this.polynomialInput.focus();
    }

    loadExample() {
        const randomExample = this.examples[Math.floor(Math.random() * this.examples.length)];
        this.polynomialInput.value = randomExample.polynomial;
        this.rootInput.value = randomExample.root;
        this.saveToStorage();
        
        // Efecto visual
        this.polynomialInput.style.background = '#e3f2fd';
        this.rootInput.style.background = '#e3f2fd';
        
        setTimeout(() => {
            this.polynomialInput.style.background = '';
            this.rootInput.style.background = '';
        }, 1000);
    }

    formatNumber(num) {
        if (num === 0) return '0';
        if (Number.isInteger(num)) return num.toString();
        return num.toFixed(2).replace(/\.?0+$/, '');
    }

    scrollToSection(section) {
        setTimeout(() => {
            section.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 100);
    }

    saveToStorage() {
        localStorage.setItem('ruffini-polynomial', this.polynomialInput.value);
        localStorage.setItem('ruffini-root', this.rootInput.value);
    }

    loadFromStorage() {
        const polynomial = localStorage.getItem('ruffini-polynomial');
        const root = localStorage.getItem('ruffini-root');
        
        if (polynomial) this.polynomialInput.value = polynomial;
        if (root) this.rootInput.value = root;
    }

    clearStorage() {
        localStorage.removeItem('ruffini-polynomial');
        localStorage.removeItem('ruffini-root');
    }
}

/**
 * Implementación JavaScript de la calculadora de Ruffini
 * (Versión frontend simplificada de la clase Python)
 */
class RuffiniCalculatorJS {
    constructor() {
        this.steps = [];
    }

    parsePolynomial(polyStr) {
        // Normalizar la cadena
        polyStr = polyStr.replace(/\s/g, '').replace(/-/g, '+-');
        
        // Encontrar el grado máximo
        const degreeMatches = polyStr.match(/x\^(\d+)/g);
        let maxDegree = 0;
        
        if (degreeMatches) {
            maxDegree = Math.max(...degreeMatches.map(match => parseInt(match.split('^')[1])));
        } else if (polyStr.includes('x')) {
            maxDegree = 1;
        }
        
        // Inicializar coeficientes
        const coefficients = new Array(maxDegree + 1).fill(0);
        
        // Encontrar todos los términos
        const terms = polyStr.match(/[+-]?[^+-]+/g) || [];
        
        for (let term of terms) {
            term = term.trim();
            if (!term) continue;
            
            if (!term.includes('x')) {
                // Término constante
                coefficients[maxDegree] = parseFloat(term);
            } else {
                // Extraer coeficiente
                let coefStr = term.replace(/x.*/, '');
                let coef;
                
                if (coefStr === '' || coefStr === '+') {
                    coef = 1;
                } else if (coefStr === '-') {
                    coef = -1;
                } else {
                    coef = parseFloat(coefStr);
                }
                
                // Extraer grado
                let degree;
                if (term.includes('^')) {
                    const degreeMatch = term.match(/x\^(\d+)/);
                    degree = degreeMatch ? parseInt(degreeMatch[1]) : 1;
                } else {
                    degree = 1;
                }
                
                coefficients[maxDegree - degree] = coef;
            }
        }
        
        return coefficients;
    }

    ruffiniDivision(coefficients, root) {
        this.steps = [];
        const n = coefficients.length;
        
        // Paso inicial
        this.steps.push({
            step: 0,
            description: 'Coeficientes del polinomio original',
            row1: [...coefficients],
            row2: new Array(n).fill(0),
            row3: [coefficients[0]]
        });
        
        const result = [coefficients[0]];
        
        for (let i = 1; i < n; i++) {
            const product = result[i - 1] * root;
            const newCoef = coefficients[i] + product;
            result.push(newCoef);
            
            const row2 = new Array(n).fill(0);
            row2[i] = product;
            
            this.steps.push({
                step: i,
                description: `Paso ${i}: Multiplicar ${result[i-1]} × ${root} = ${product}, luego sumar ${coefficients[i]} + ${product} = ${newCoef}`,
                row1: [...coefficients],
                row2: row2,
                row3: [...result]
            });
        }
        
        const remainder = result[result.length - 1];
        const quotient = result.slice(0, -1);
        
        return { quotient, remainder };
    }

    formatPolynomial(coefficients) {
        if (!coefficients || coefficients.length === 0) return '0';
        
        const terms = [];
        const degree = coefficients.length - 1;
        
        for (let i = 0; i < coefficients.length; i++) {
            const coef = coefficients[i];
            if (coef === 0) continue;
            
            const currentDegree = degree - i;
            let coefStr;
            
            if (coef === 1 && currentDegree > 0) {
                coefStr = '';
            } else if (coef === -1 && currentDegree > 0) {
                coefStr = '-';
            } else {
                coefStr = coef.toString();
            }
            
            let term;
            if (currentDegree === 0) {
                term = coefStr || '1';
            } else if (currentDegree === 1) {
                term = `${coefStr}x`;
            } else {
                term = `${coefStr}x^${currentDegree}`;
            }
            
            terms.push(term);
        }
        
        if (terms.length === 0) return '0';
        
        let result = terms[0];
        for (let i = 1; i < terms.length; i++) {
            const term = terms[i];
            if (term.startsWith('-')) {
                result += ` - ${term.substring(1)}`;
            } else {
                result += ` + ${term}`;
            }
        }
        
        return result;
    }

    generateAIExplanation(polynomial, root, quotient, remainder) {
        const quotientPoly = this.formatPolynomial(quotient);
        
        let explanation = `🤖 EXPLICACIÓN CON IA - MÉTODO DE RUFFINI

📊 PROBLEMA:
Dividir el polinomio: ${polynomial}
Entre: (x - ${root})

🔍 PROCESO PASO A PASO:

El método de Ruffini es una forma simplificada de la división polinómica.
Se utiliza específicamente para dividir un polinomio entre un binomio de la forma (x - a).

📋 PASOS REALIZADOS:
`;

        for (const step of this.steps) {
            explanation += `\n${step.step}. ${step.description}`;
            explanation += `\n   Fila 1: [${step.row1.join(', ')}]`;
            explanation += `\n   Fila 2: [${step.row2.join(', ')}]`;
            explanation += `\n   Resultado: [${step.row3.join(', ')}]\n`;
        }
        
        explanation += `
✅ RESULTADO FINAL:
• Cociente: ${quotientPoly}
• Resto: ${remainder}

🎯 VERIFICACIÓN:
El resultado se puede verificar con: (${quotientPoly}) × (x - ${root}) + ${remainder}

💡 INTERPRETACIÓN:
`;
        
        if (remainder === 0) {
            explanation += `Como el resto es 0, (x - ${root}) es un factor del polinomio original.`;
        } else {
            explanation += `Como el resto es ${remainder} ≠ 0, (x - ${root}) no es un factor exacto del polinomio.`;
        }
        
        return explanation;
    }

    calculate(polynomialStr, root) {
        try {
            const coefficients = this.parsePolynomial(polynomialStr);
            const { quotient, remainder } = this.ruffiniDivision(coefficients, root);
            const quotientStr = this.formatPolynomial(quotient);
            const aiExplanation = this.generateAIExplanation(polynomialStr, root, quotient, remainder);
            
            return {
                success: true,
                polynomial: polynomialStr,
                root: root,
                coefficients: coefficients,
                quotient_coefficients: quotient,
                quotient: quotientStr,
                remainder: remainder,
                steps: this.steps,
                ai_explanation: aiExplanation
            };
            
        } catch (error) {
            return {
                success: false,
                error: error.message,
                ai_help: this.generateErrorHelp(error.message)
            };
        }
    }

    generateErrorHelp(error) {
        return `🤖 AYUDA DE IA - ERROR DETECTADO

❌ Error: ${error}

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

¿Necesitas más ayuda? Prueba con el botón "Ejemplo" o revisa la sección de ayuda.`;
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new RuffiniApp();
    console.log('🧮 Calculadora de Ruffini con IA iniciada');
});
