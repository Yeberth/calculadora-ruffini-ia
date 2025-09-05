#!/bin/bash

# 🚀 Script rápido para subir a GitHub
# Calculadora de Ruffini con IA

echo "🚀 SUBIENDO CALCULADORA DE RUFFINI A GITHUB"
echo "==========================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Función para pedir username de GitHub
get_github_username() {
    read -p "🐙 Ingresa tu username de GitHub: " GITHUB_USERNAME
    
    if [ -z "$GITHUB_USERNAME" ]; then
        echo "❌ Username requerido"
        exit 1
    fi
    
    echo "✅ Username: $GITHUB_USERNAME"
}

# Verificar configuración de Git
check_git_config() {
    GIT_USER=$(git config user.name)
    GIT_EMAIL=$(git config user.email)
    
    if [ -z "$GIT_USER" ] || [ -z "$GIT_EMAIL" ]; then
        echo "⚙️  Configurando Git..."
        read -p "Nombre completo: " USER_NAME
        read -p "Email: " USER_EMAIL
        
        git config user.name "$USER_NAME"
        git config user.email "$USER_EMAIL"
        
        echo "✅ Git configurado"
    else
        echo "✅ Git ya está configurado: $GIT_USER <$GIT_EMAIL>"
    fi
}

# Función principal
main() {
    echo "📋 Estado actual del repositorio:"
    git status
    echo ""
    
    check_git_config
    get_github_username
    
    echo ""
    echo "🔗 PASOS A SEGUIR:"
    echo ""
    echo "1️⃣  CREAR REPOSITORIO EN GITHUB:"
    echo "   - Ve a: https://github.com/new"
    echo "   - Repository name: calculadora-ruffini-ia" 
    echo "   - Description: 🧮 Calculadora inteligente del método de Ruffini con IA"
    echo "   - ✅ Public"
    echo "   - ❌ NO marques 'Initialize with README'"
    echo "   - Clic en 'Create repository'"
    echo ""
    
    read -p "¿Ya creaste el repositorio en GitHub? (y/n): " CREATED
    
    if [ "$CREATED" != "y" ]; then
        echo "⏸️  Crea el repositorio primero y luego ejecuta este script de nuevo"
        exit 0
    fi
    
    echo ""
    echo "2️⃣  CONECTANDO CON GITHUB:"
    
    # Configurar remote origin
    REPO_URL="https://github.com/$GITHUB_USERNAME/calculadora-ruffini-ia.git"
    
    # Verificar si ya existe el remote
    if git remote get-url origin >/dev/null 2>&1; then
        echo "🔄 Actualizando remote origin..."
        git remote set-url origin $REPO_URL
    else
        echo "➕ Agregando remote origin..."
        git remote add origin $REPO_URL
    fi
    
    echo "✅ Remote configurado: $REPO_URL"
    
    echo ""
    echo "3️⃣  SUBIENDO A GITHUB:"
    
    # Asegurar que estamos en branch main
    git branch -M main
    
    # Agregar cambios si los hay
    if ! git diff --cached --quiet; then
        echo "📝 Hay cambios pendientes, agregando..."
        git add .
        git commit -m "🔧 Configuración para deployment en producción"
    fi
    
    # Hacer push
    echo "⬆️  Subiendo archivos..."
    if git push -u origin main; then
        echo ""
        echo "🎉 ¡SUBIDA EXITOSA!"
        echo "========================="
        echo ""
        echo "🔗 Tu repositorio está en:"
        echo "   https://github.com/$GITHUB_USERNAME/calculadora-ruffini-ia"
        echo ""
        echo "📋 PRÓXIMOS PASOS:"
        echo "1. 🌐 Deploy en Heroku: ./deploy.sh"
        echo "2. 📄 Ver guía completa: cat GUIA_DEPLOYMENT.md"
        echo "3. 🚀 Tu calculadora estará en la web!"
        echo ""
        echo "💡 URLs después del deploy:"
        echo "   Heroku: https://tu-app-name.herokuapp.com"
        echo "   Vercel: https://calculadora-ruffini-ia-$GITHUB_USERNAME.vercel.app"
        echo ""
    else
        echo ""
        echo "❌ Error al subir. Posibles soluciones:"
        echo "1. Verificar que creaste el repositorio en GitHub"
        echo "2. Verificar tu username: $GITHUB_USERNAME"
        echo "3. Verificar permisos de tu cuenta GitHub"
        echo ""
        echo "🔧 Comando manual:"
        echo "   git remote -v"
        echo "   git push -u origin main"
    fi
}

# Ejecutar función principal
main
