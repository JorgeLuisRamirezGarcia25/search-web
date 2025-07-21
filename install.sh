#!/bin/bash

# Script de instalación para PyWebBrowser
# Este script automatiza la instalación en sistemas Linux

echo "🌐 Instalación de PyWebBrowser"
echo "==============================="


# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python no está instalado. Por favor, instálalo primero."
    exit 1
fi

echo "✅ Python encontrado: $(python --version)"

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "❌ pip no está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install python-pip -y
fi

echo "✅ pip encontrado: $(pip --version)"

# Detectar el sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Sistema detectado: Linux"
    
    # Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        echo "📦 Instalando dependencias del sistema para Ubuntu/Debian..."
        sudo apt-get update
        sudo apt-get install -y python3-pyqt5 python3-pyqt5.qtwebengine python3-venv
    
    # CentOS/RHEL/Fedora
    elif command -v yum &> /dev/null; then
        echo "📦 Instalando dependencias del sistema para CentOS/RHEL/Fedora..."
        sudo yum install -y python3-qt5 python3-qt5-webengine python3-virtualenv
    
    # Arch Linux
    elif command -v pacman &> /dev/null; then
        echo "📦 Instalando dependencias del sistema para Arch Linux..."
        sudo pacman -S python-pyqt5 python-pyqt5-webengine --noconfirm
    
    else
        echo "⚠️  Sistema Linux no reconocido. Instala PyQt5 y PyQtWebEngine manualmente."
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Sistema detectado: macOS"
    
    # Verificar si Homebrew está instalado
    if command -v brew &> /dev/null; then
        echo "📦 Instalando dependencias con Homebrew..."
        brew install pyqt5
    else
        echo "⚠️  Homebrew no encontrado. Por favor, instala PyQt5 manualmente."
    fi
else
    echo "⚠️  Sistema operativo no soportado automáticamente."
fi


# Crear entorno virtual
echo "🔧 Creando entorno virtual..."
if [ ! -d ".venv" ]; then
    python -m venv .venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source .venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias de Python
echo "📚 Instalando dependencias de Python..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencias instaladas"
else
    echo "⚠️  Archivo requirements.txt no encontrado. Instalando dependencias básicas..."
    pip install PyQt5 PyQtWebEngine requests
fi

# Verificar instalación
echo "🧪 Verificando instalación..."
python -c "
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    print('✅ PyQt5 y QtWebEngine están correctamente instalados')
except ImportError as e:
    print(f'❌ Error de importación: {e}')
    exit(1)
"

# Crear acceso directo (opcional)
echo "🔗 ¿Deseas crear un acceso directo? (y/n)"
read -r create_shortcut

if [[ $create_shortcut == "y" || $create_shortcut == "Y" ]]; then
    # Crear script de ejecución
    cat > run_pybrowser.sh << EOF
#!/bin/bash
cd "$(dirname "\$0")"
source .venv/bin/activate
python main.py
EOF
    
    chmod +x run_pybrowser.sh
    echo "✅ Acceso directo creado: ./run_pybrowser.sh"
    
    # Crear .desktop file para sistemas con entorno de escritorio
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        mkdir -p ~/.local/share/applications
        cat > ~/.local/share/applications/pybrowser.desktop << EOF
[Desktop Entry]
Name=PyWebBrowser
Comment=Navegador web desarrollado en Python
Exec=$(pwd)/run_pybrowser.sh
Icon=applications-internet
Terminal=false
Type=Application
Categories=Network;WebBrowser;
EOF
        echo "✅ Entrada de escritorio creada"
    fi
fi

echo ""
echo "🎉 ¡Instalación completada!"
echo "==============================="
echo ""
echo "Para ejecutar PyWebBrowser:"
echo "1. Activar entorno virtual: source .venv/bin/activate"
echo "2. Ejecutar: python main.py"
echo ""
if [[ $create_shortcut == "y" || $create_shortcut == "Y" ]]; then
    echo "O simplemente ejecuta: ./run_pybrowser.sh"
    echo ""
fi
echo "📖 Lee el README.md para más información sobre el uso."
echo "🐛 Si encuentras problemas, revisa la sección de troubleshooting."
echo ""
echo "¡Disfruta navegando! 🌐"
