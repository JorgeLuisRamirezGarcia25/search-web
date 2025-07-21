#!/usr/bin/env python3
"""
Navegador Web Simplificado - Versión básica para sistemas sin QtWebEngine
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QTextEdit, QMenuBar, 
                             QMenu, QAction, QStatusBar, QMessageBox, QTabWidget,
                             QLabel, QSplitter)
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import urllib.request
import urllib.parse
import json
import re
from html.parser import HTMLParser

class SimpleHTMLParser(HTMLParser):
    """Parser simple para extraer texto de HTML"""
    
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.title = ""
        self.in_title = False
        
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'title':
            self.in_title = True
        elif tag.lower() in ['br', 'p', 'div']:
            self.text_content.append('\n')
            
    def handle_endtag(self, tag):
        if tag.lower() == 'title':
            self.in_title = False
        elif tag.lower() in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.text_content.append('\n\n')
            
    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        else:
            self.text_content.append(data)
    
    def get_text(self):
        return ''.join(self.text_content)

class WebLoader(QThread):
    """Hilo para cargar páginas web"""
    
    content_loaded = pyqtSignal(str, str, str)  # url, title, content
    error_occurred = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        
    def run(self):
        try:
            # Verificar si es una búsqueda de DuckDuckGo
            if not self.url.startswith(('http://', 'https://')):
                # Es una búsqueda, redirigir a DuckDuckGo
                search_query = urllib.parse.quote(self.url)
                self.url = f"https://duckduckgo.com/?q={search_query}"
            
            # Crear request con headers
            req = urllib.request.Request(
                self.url,
                headers={
                    'User-Agent': 'PyWebBrowser/1.0 (Python; Simple)',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                }
            )
            
            # Abrir URL
            with urllib.request.urlopen(req, timeout=10) as response:
                # Leer contenido
                html_content = response.read().decode('utf-8', errors='ignore')
                
                # Parsear HTML
                parser = SimpleHTMLParser()
                parser.feed(html_content)
                
                title = parser.title or self.url
                text_content = parser.get_text()
                
                # Emitir señal con el contenido
                self.content_loaded.emit(self.url, title, text_content)
                
        except Exception as e:
            self.error_occurred.emit(f"Error al cargar {self.url}: {str(e)}")

class SimpleWebTab(QWidget):
    """Pestaña simple del navegador"""
    
    url_changed = pyqtSignal(str)
    title_changed = pyqtSignal(str)
    loading_finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_url = ""
        self.current_title = "Nueva pestaña"
        self.history = []
        self.history_index = -1
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de la pestaña"""
        layout = QVBoxLayout(self)
        
        # Área de contenido
        self.content_area = QTextEdit()
        self.content_area.setReadOnly(True)
        self.content_area.setFont(QFont("Arial", 12))
        layout.addWidget(self.content_area)
        
        # Mostrar mensaje inicial
        self.content_area.setHtml("""
        <h1>PyWebBrowser - Navegador Simplificado</h1>
        <p>Bienvenido al navegador web simplificado desarrollado en Python.</p>
        <p><strong>Características:</strong></p>
        <ul>
        <li>✅ Navegación web básica</li>
        <li>✅ Búsquedas en DuckDuckGo</li>
        <li>✅ Múltiples pestañas</li>
        <li>✅ Historial de navegación</li>
        <li>✅ Modo texto para mayor velocidad</li>
        </ul>
        <p><strong>Para empezar:</strong></p>
        <p>• Escribe una URL en la barra de direcciones</p>
        <p>• O escribe términos de búsqueda para buscar en DuckDuckGo</p>
        <p>• Ejemplos: "wikipedia.org", "python programming", "https://example.com"</p>
        """)
        
    def load_url(self, url):
        """Cargar una URL"""
        if not url.strip():
            return
            
        # Mostrar mensaje de carga
        self.content_area.setHtml(f"<h2>Cargando...</h2><p>Obteniendo contenido de: {url}</p>")
        
        # Agregar al historial
        if url != self.current_url:
            # Eliminar entradas futuras si estamos en el medio del historial
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            
            self.history.append(url)
            self.history_index = len(self.history) - 1
            
        self.current_url = url
        self.url_changed.emit(url)
        
        # Cargar contenido en hilo separado
        self.loader = WebLoader(url)
        self.loader.content_loaded.connect(self.on_content_loaded)
        self.loader.error_occurred.connect(self.on_error)
        self.loader.start()
        
    def on_content_loaded(self, url, title, content):
        """Manejar contenido cargado"""
        self.current_title = title
        self.title_changed.emit(title)
        
        # Formatear contenido para mostrar
        formatted_content = f"""
        <div style="padding: 20px; line-height: 1.6;">
        <h1 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
        {title}
        </h1>
        <p style="color: #7f8c8d; margin-bottom: 20px;">
        <strong>URL:</strong> <a href="{url}" style="color: #3498db;">{url}</a>
        </p>
        <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin-bottom: 20px;">
        <strong>Nota:</strong> Esta es una vista simplificada en modo texto. 
        El contenido original puede incluir imágenes, estilos y JavaScript que no se muestran aquí.
        </div>
        <div style="white-space: pre-wrap; font-family: Arial, sans-serif;">
        {self.clean_text(content)}
        </div>
        </div>
        """
        
        self.content_area.setHtml(formatted_content)
        self.loading_finished.emit()
        
    def clean_text(self, text):
        """Limpiar y formatear texto"""
        # Eliminar espacios excesivos
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Limitar longitud para evitar contenido excesivo
        if len(text) > 10000:
            text = text[:10000] + "\n\n[Contenido truncado por longitud...]"
            
        return text.strip()
        
    def on_error(self, error_message):
        """Manejar errores de carga"""
        self.content_area.setHtml(f"""
        <div style="padding: 20px;">
        <h1 style="color: #e74c3c;">Error de Conexión</h1>
        <p style="color: #7f8c8d;">{error_message}</p>
        <h3>Posibles soluciones:</h3>
        <ul>
        <li>Verifica tu conexión a internet</li>
        <li>Asegúrate de que la URL sea correcta</li>
        <li>Intenta con una búsqueda en lugar de una URL directa</li>
        <li>Algunas páginas pueden bloquear este tipo de acceso</li>
        </ul>
        <p><strong>Sugerencia:</strong> Prueba buscando "{self.current_url}" en DuckDuckGo</p>
        </div>
        """)
        self.loading_finished.emit()
        
    def can_go_back(self):
        """Verificar si se puede ir atrás"""
        return self.history_index > 0
        
    def can_go_forward(self):
        """Verificar si se puede ir adelante"""
        return self.history_index < len(self.history) - 1
        
    def go_back(self):
        """Ir a la página anterior"""
        if self.can_go_back():
            self.history_index -= 1
            url = self.history[self.history_index]
            self.load_url(url)
            
    def go_forward(self):
        """Ir a la página siguiente"""
        if self.can_go_forward():
            self.history_index += 1
            url = self.history[self.history_index]
            self.load_url(url)

class SimpleBrowser(QMainWindow):
    """Navegador web simplificado"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyWebBrowser - Navegador Simplificado")
        self.setGeometry(100, 100, 1000, 700)
        
        self.setup_ui()
        self.setup_menu()
        
        # Crear primera pestaña
        self.add_new_tab()
        
    def setup_ui(self):
        """Configurar la interfaz"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Barra de navegación
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 5, 10, 5)
        
        # Botones de navegación
        self.back_button = QPushButton("←")
        self.back_button.setFixedSize(30, 30)
        self.back_button.setToolTip("Atrás")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        
        self.forward_button = QPushButton("→")
        self.forward_button.setFixedSize(30, 30)
        self.forward_button.setToolTip("Adelante")
        self.forward_button.clicked.connect(self.go_forward)
        self.forward_button.setEnabled(False)
        
        self.refresh_button = QPushButton("⟳")
        self.refresh_button.setFixedSize(30, 30)
        self.refresh_button.setToolTip("Actualizar")
        self.refresh_button.clicked.connect(self.refresh)
        
        self.home_button = QPushButton("🏠")
        self.home_button.setFixedSize(30, 30)
        self.home_button.setToolTip("Inicio")
        self.home_button.clicked.connect(self.go_home)
        
        # Barra de direcciones
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Escribe una URL o término de búsqueda...")
        self.url_bar.returnPressed.connect(self.navigate)
        
        # Botón de búsqueda
        self.search_button = QPushButton("🔍")
        self.search_button.setFixedSize(30, 30)
        self.search_button.setToolTip("Buscar")
        self.search_button.clicked.connect(self.navigate)
        
        # Agregar a layout
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.refresh_button)
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.search_button)
        
        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)
        layout.addWidget(nav_widget)
        
        # Pestañas
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        
        # Botón nueva pestaña
        new_tab_button = QPushButton("+")
        new_tab_button.setFixedSize(25, 25)
        new_tab_button.clicked.connect(self.add_new_tab)
        self.tab_widget.setCornerWidget(new_tab_button)
        
        layout.addWidget(self.tab_widget)
        
        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo - Navegador web simplificado")
        
    def setup_menu(self):
        """Configurar menú"""
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu("Archivo")
        
        new_tab_action = QAction("Nueva pestaña", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Salir", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menú Ayuda
        help_menu = menubar.addMenu("Ayuda")
        
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def add_new_tab(self, url=""):
        """Agregar nueva pestaña"""
        tab = SimpleWebTab()
        
        # Conectar señales
        tab.url_changed.connect(self.update_url_bar)
        tab.title_changed.connect(self.update_tab_title)
        tab.loading_finished.connect(self.update_navigation_buttons)
        
        # Agregar pestaña
        index = self.tab_widget.addTab(tab, "Nueva pestaña")
        self.tab_widget.setCurrentIndex(index)
        
        # Cargar URL si se proporciona
        if url:
            tab.load_url(url)
            
        return tab
        
    def close_tab(self, index):
        """Cerrar pestaña"""
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            self.close()
            
    def tab_changed(self, index):
        """Manejar cambio de pestaña"""
        if index >= 0:
            tab = self.tab_widget.widget(index)
            if tab:
                self.update_url_bar(tab.current_url)
                self.update_navigation_buttons()
                
    def get_current_tab(self):
        """Obtener pestaña actual"""
        return self.tab_widget.currentWidget()
        
    def navigate(self):
        """Navegar a URL"""
        url = self.url_bar.text().strip()
        if url:
            current_tab = self.get_current_tab()
            if current_tab:
                current_tab.load_url(url)
                
    def go_back(self):
        """Ir atrás"""
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.go_back()
            
    def go_forward(self):
        """Ir adelante"""
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.go_forward()
            
    def refresh(self):
        """Actualizar página"""
        current_tab = self.get_current_tab()
        if current_tab and current_tab.current_url:
            current_tab.load_url(current_tab.current_url)
            
    def go_home(self):
        """Ir a inicio"""
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.load_url("https://duckduckgo.com")
            
    def update_url_bar(self, url):
        """Actualizar barra de direcciones"""
        self.url_bar.setText(url)
        
    def update_tab_title(self, title):
        """Actualizar título de pestaña"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            # Limitar longitud del título
            if len(title) > 20:
                title = title[:17] + "..."
            self.tab_widget.setTabText(current_index, title)
            
    def update_navigation_buttons(self):
        """Actualizar botones de navegación"""
        current_tab = self.get_current_tab()
        if current_tab:
            self.back_button.setEnabled(current_tab.can_go_back())
            self.forward_button.setEnabled(current_tab.can_go_forward())
            
    def show_about(self):
        """Mostrar información"""
        QMessageBox.about(self, "Acerca de PyWebBrowser", 
                         "PyWebBrowser - Versión Simplificada\n\n"
                         "Un navegador web básico desarrollado en Python con PyQt5\n\n"
                         "Características:\n"
                         "• Navegación web en modo texto\n"
                         "• Búsquedas en DuckDuckGo\n"
                         "• Múltiples pestañas\n"
                         "• Historial de navegación\n"
                         "• Interfaz limpia y rápida\n\n"
                         "Ideal para consultas rápidas y navegación ligera.")

def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Configurar aplicación
    app.setApplicationName("PyWebBrowser")
    app.setApplicationDisplayName("Navegador Web Simplificado")
    
    # Crear y mostrar navegador
    browser = SimpleBrowser()
    browser.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
