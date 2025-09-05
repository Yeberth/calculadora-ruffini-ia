#!/bin/bash

# 🚀 Script de Deployment - Calculadora de Ruffini con IA
# Automatiza el proceso de deployment en diferentes plataformas

echo "🚀 DEPLOYMENT - CALCULADORA DE RUFFINI CON IA"
echo "============================================="

# Función para mostrar opciones
show_menu() {
    echo ""
    echo "📋 OPCIONES DE DEPLOYMENT:"
    echo "1. 🌐 Heroku"
    echo "2. ⚡ Vercel"
    echo "3. 📄 GitHub Pages (solo frontend)"
    echo "4. 🔧 Manual Setup"
    echo "5. ❌ Cancelar"
    echo ""
}

# Función para deployment en Heroku
deploy_heroku() {
    echo "🌐 DEPLOYMENT EN HEROKU"
    echo "======================="
    
    # Verificar si Heroku CLI está instalado
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI no está instalado"
        echo "📥 Instala desde: https://devcenter.heroku.com/articles/heroku-cli"
        return 1
    fi
    
    echo "📝 Configurando Heroku..."
    
    # Crear aplicación en Heroku
    read -p "Nombre de la aplicación Heroku: " APP_NAME
    
    if [ -z "$APP_NAME" ]; then
        APP_NAME="calculadora-ruffini-$(date +%s)"
        echo "🔄 Usando nombre automático: $APP_NAME"
    fi
    
    # Crear app
    heroku create $APP_NAME
    
    # Configurar variables de entorno
    heroku config:set FLASK_ENV=production --app $APP_NAME
    heroku config:set SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(16))") --app $APP_NAME
    
    # Deploy
    echo "🚀 Subiendo a Heroku..."
    git push heroku main
    
    # Abrir en navegador
    heroku open --app $APP_NAME
    
    echo "✅ Deployment completado!"
    echo "🌐 URL: https://$APP_NAME.herokuapp.com"
}

# Función para deployment en Vercel
deploy_vercel() {
    echo "⚡ DEPLOYMENT EN VERCEL"
    echo "======================"
    
    # Verificar si Vercel CLI está instalado
    if ! command -v vercel &> /dev/null; then
        echo "❌ Vercel CLI no está instalado"
        echo "📥 Instala con: npm i -g vercel"
        return 1
    fi
    
    echo "🚀 Subiendo a Vercel..."
    vercel --prod
    
    echo "✅ Deployment completado!"
}

# Función para GitHub Pages (solo frontend)
deploy_github_pages() {
    echo "📄 DEPLOYMENT EN GITHUB PAGES"
    echo "============================="
    
    echo "⚠️  GitHub Pages solo soporta contenido estático"
    echo "🔄 Creando versión estática..."
    
    # Crear directorio docs para GitHub Pages
    mkdir -p docs
    
    # Copiar archivos estáticos
    cp templates/index.html docs/
    cp -r static docs/
    
    # Modificar HTML para funcionar sin servidor
    sed -i 's|href="../static/css/styles.css"|href="static/css/styles.css"|g' docs/index.html
    sed -i 's|src="../static/js/app.js"|src="static/js/app.js"|g' docs/index.html
    
    echo "📁 Archivos copiados a /docs"
    echo "⚙️  Configuración necesaria:"
    echo "   1. Sube el repositorio a GitHub"
    echo "   2. Ve a Settings > Pages"
    echo "   3. Selecciona 'Deploy from branch'"
    echo "   4. Elige 'main' branch, '/docs' folder"
    
    echo "⚠️  Nota: Solo funcionará el frontend (sin IA backend)"
}

# Función para setup manual
manual_setup() {
    echo "🔧 SETUP MANUAL"
    echo "==============="
    
    echo "📋 INSTRUCCIONES PARA DEPLOYMENT MANUAL:"
    echo ""
    echo "🐧 LINUX/UBUNTU SERVER:"
    echo "1. sudo apt update && sudo apt install python3 python3-pip python3-venv nginx"
    echo "2. git clone [tu-repo-url]"
    echo "3. cd calculadora-ruffini-ia"
    echo "4. python3 -m venv venv"
    echo "5. source venv/bin/activate"
    echo "6. pip install -r requirements.txt"
    echo "7. python app.py (o usar gunicorn para producción)"
    echo ""
    echo "🪟 WINDOWS:"
    echo "1. Instalar Python 3.7+"
    echo "2. git clone [tu-repo-url]"
    echo "3. cd calculadora-ruffini-ia"
    echo "4. python -m venv venv"
    echo "5. venv\\Scripts\\activate"
    echo "6. pip install -r requirements.txt"
    echo "7. python app.py"
    echo ""
    echo "🍎 macOS:"
    echo "1. brew install python3 git"
    echo "2. git clone [tu-repo-url]"
    echo "3. cd calculadora-ruffini-ia"
    echo "4. python3 -m venv venv"
    echo "5. source venv/bin/activate"
    echo "6. pip install -r requirements.txt"
    echo "7. python app.py"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que Git está configurado
if [ ! -d ".git" ]; then
    echo "⚠️  Repositorio Git no inicializado"
    echo "🔄 Inicializando..."
    git init
    git add .
    git commit -m "🎉 Commit inicial - Calculadora de Ruffini con IA"
fi

# Menú principal
while true; do
    show_menu
    read -p "Selecciona una opción (1-5): " choice
    
    case $choice in
        1)
            deploy_heroku
            break
            ;;
        2)
            deploy_vercel
            break
            ;;
        3)
            deploy_github_pages
            break
            ;;
        4)
            manual_setup
            break
            ;;
        5)
            echo "❌ Deployment cancelado"
            exit 0
            ;;
        *)
            echo "❌ Opción no válida. Intenta de nuevo."
            ;;
    esac
done

echo ""
echo "🎉 ¡Proceso completado!"
echo "💡 Recuerda actualizar las URLs en tu README.md"
