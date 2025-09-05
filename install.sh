#!/bin/bash
# 🧮 Script de instalación para Calculadora de Ruffini con IA

echo "🚀 INSTALANDO CALCULADORA DE RUFFINI CON IA"
echo "============================================="

# Verificar si estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Función para detectar el sistema operativo
detect_os() {
    if command -v apt >/dev/null 2>&1; then
        echo "ubuntu/debian"
    elif command -v yum >/dev/null 2>&1; then
        echo "rhel/fedora"
    elif command -v pacman >/dev/null 2>&1; then
        echo "arch"
    elif command -v brew >/dev/null 2>&1; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Detectar sistema operativo
OS=$(detect_os)
echo "🔍 Sistema detectado: $OS"

# Instalar dependencias del sistema
install_system_deps() {
    case $OS in
        "ubuntu/debian")
            echo "📦 Instalando dependencias para Ubuntu/Debian..."
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv python3-flask
            ;;
        "rhel/fedora")
            echo "📦 Instalando dependencias para RHEL/Fedora..."
            sudo dnf install -y python3 python3-pip python3-venv python3-flask
            ;;
        "arch")
            echo "📦 Instalando dependencias para Arch Linux..."
            sudo pacman -S python python-pip python-flask
            ;;
        "macos")
            echo "📦 Instalando dependencias para macOS..."
            brew install python3
            pip3 install flask
            ;;
        *)
            echo "⚠️  Sistema no reconocido, intentando instalación manual..."
            ;;
    esac
}

# Crear entorno virtual si es posible
setup_virtualenv() {
    if command -v python3 >/dev/null 2>&1; then
        echo "🌐 Creando entorno virtual..."
        
        if python3 -m venv --help >/dev/null 2>&1; then
            python3 -m venv venv
            echo "✅ Entorno virtual creado"
            
            # Activar entorno virtual
            source venv/bin/activate
            
            # Instalar dependencias
            echo "📥 Instalando dependencias Python..."
            pip install -r requirements.txt
            echo "✅ Dependencias instaladas"
        else
            echo "⚠️  python3-venv no disponible, usando instalación del sistema"
            install_system_deps
        fi
    else
        echo "❌ Python3 no encontrado"
        exit 1
    fi
}

# Verificar instalación
verify_installation() {
    echo "🧪 Verificando instalación..."
    
    # Verificar que Python funciona
    if ! python3 -c "from src.ruffini_calculator import RuffiniCalculator; print('✅ Calculadora OK')"; then
        echo "❌ Error en la calculadora"
        return 1
    fi
    
    # Verificar Flask si está disponible
    if python3 -c "import flask; print('✅ Flask OK')" 2>/dev/null; then
        echo "✅ Flask disponible"
        FLASK_AVAILABLE=true
    else
        echo "⚠️  Flask no disponible - solo modo consola"
        FLASK_AVAILABLE=false
    fi
}

# Crear script de ejecución
create_run_script() {
    echo "📝 Creando scripts de ejecución..."
    
    # Script para modo consola
    cat > run_console.sh << 'EOF'
#!/bin/bash
echo "🧮 Calculadora de Ruffini - Modo Consola"
echo "========================================"
python3 src/ruffini_calculator.py
EOF
    chmod +x run_console.sh
    
    # Script para ejemplos
    cat > run_examples.sh << 'EOF'
#!/bin/bash
echo "📚 Ejemplos de Ruffini"
echo "===================="
python3 examples/ejemplos_practicos.py --interactivo
EOF
    chmod +x run_examples.sh
    
    # Script para servidor web (si Flask está disponible)
    if [ "$FLASK_AVAILABLE" = true ]; then
        cat > run_server.sh << 'EOF'
#!/bin/bash
echo "🌐 Iniciando servidor web..."
echo "Disponible en: http://localhost:5000"
echo "Presiona Ctrl+C para detener"
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 app.py
EOF
        chmod +x run_server.sh
    fi
}

# Mostrar instrucciones
show_instructions() {
    echo ""
    echo "🎉 ¡INSTALACIÓN COMPLETADA!"
    echo "=========================="
    echo ""
    echo "📋 Comandos disponibles:"
    echo "  ./run_console.sh    - Calculadora en consola"
    echo "  ./run_examples.sh   - Ejecutar ejemplos interactivos"
    
    if [ "$FLASK_AVAILABLE" = true ]; then
        echo "  ./run_server.sh     - Iniciar servidor web"
    fi
    
    echo ""
    echo "📖 Documentación:"
    echo "  cat README.md       - Ver documentación completa"
    echo ""
    echo "🧮 ¡Disfruta usando la Calculadora de Ruffini con IA!"
}

# Ejecutar instalación
main() {
    install_system_deps
    setup_virtualenv
    verify_installation
    create_run_script
    show_instructions
}

# Ejecutar función principal
main
