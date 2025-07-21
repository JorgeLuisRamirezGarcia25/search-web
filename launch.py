#!/usr/bin/env python3
"""
Launcher para PyWebBrowser
Detecta automáticamente qué versión ejecutar según las dependencias disponibles
"""

import sys
import os

def check_qtwebengine():
    """Verificar si QtWebEngine está disponible"""
    try:
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        return True
    except ImportError:
        return False

def check_pyqt5():
    """Verificar si PyQt5 está disponible"""
    try:
        from PyQt5.QtWidgets import QApplication
        return True
    except ImportError:
        return False

def main():
    """Función principal del launcher"""
    print("🌐 PyWebBrowser - Launcher")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_pyqt5():
        print("❌ Error: PyQt5 no está instalado")
        print("Por favor, instala PyQt5:")
        print("  sudo apt-get install python3-pyqt5")
        print("  o")
        print("  pip install PyQt5")
        return 1
    
    print("✅ PyQt5 detectado")
    
    # Verificar QtWebEngine
    if check_qtwebengine():
        print("✅ QtWebEngine detectado")
        print("🚀 Iniciando navegador completo...")
        
        try:
            # Importar y ejecutar navegador completo
            from browser.main_window import MainWindow
            from browser.database import DatabaseManager
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtCore import QCoreApplication
            
            # Configurar aplicación
            QCoreApplication.setApplicationName("PyWebBrowser")
            QCoreApplication.setApplicationVersion("1.0")
            QCoreApplication.setOrganizationName("PyBrowser")
            
            app = QApplication(sys.argv)
            
            # Configurar directorio de datos
            data_dir = os.path.join(os.path.expanduser("~"), ".pybrowser")
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # Inicializar base de datos
            db_manager = DatabaseManager(data_dir)
            db_manager.initialize_database()
            
            # Crear y mostrar ventana
            main_window = MainWindow(data_dir)
            main_window.show()
            
            print("📱 Navegador completo iniciado")
            return app.exec_()
            
        except Exception as e:
            print(f"❌ Error al iniciar navegador completo: {e}")
            print("🔄 Intentando con navegador simplificado...")
            return start_simple_browser()
    else:
        print("⚠️  QtWebEngine no detectado")
        print("🔄 Iniciando navegador simplificado...")
        return start_simple_browser()

def start_simple_browser():
    """Iniciar navegador simplificado"""
    try:
        from simple_browser import SimpleBrowser
        from PyQt5.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        app.setApplicationName("PyWebBrowser")
        app.setApplicationDisplayName("Navegador Web Simplificado")
        
        browser = SimpleBrowser()
        browser.show()
        
        print("📱 Navegador simplificado iniciado")
        print("💡 Para el navegador completo, instala: sudo apt-get install python3-pyqt5.qtwebengine")
        
        return app.exec_()
        
    except Exception as e:
        print(f"❌ Error al iniciar navegador simplificado: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
