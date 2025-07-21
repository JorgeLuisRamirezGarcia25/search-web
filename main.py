#!/usr/bin/env python3
"""
Navegador Web con Python - Archivo Principal
Características: HTTPS, DuckDuckGo, Historial, Cookies, JavaScript, CRUD
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication

# Importar los módulos del navegador
from browser.main_window import MainWindow
from browser.database import DatabaseManager

def main():
    """Función principal para inicializar el navegador"""
    # Configurar la aplicación
    QCoreApplication.setApplicationName("PyWebBrowser")
    QCoreApplication.setApplicationVersion("1.0")
    QCoreApplication.setOrganizationName("PyBrowser")
    
    # Crear la aplicación Qt
    app = QApplication(sys.argv)
    
    # Configurar el directorio de datos
    data_dir = os.path.join(os.path.expanduser("~"), ".pybrowser")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Inicializar la base de datos
    db_manager = DatabaseManager(data_dir)
    db_manager.initialize_database()
    
    # Crear y mostrar la ventana principal
    main_window = MainWindow(data_dir)
    main_window.show()
    
    # Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
