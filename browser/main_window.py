"""
Ventana Principal del Navegador Web
Incluye interfaz gráfica, navegación, y gestión de tabs
"""

import os
import re
from urllib.parse import urlparse, urljoin
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QLineEdit, QPushButton, QTabWidget, QMenuBar, 
                             QMenu, QAction, QToolBar, QStatusBar, QMessageBox,
                             QDialog, QListWidget, QListWidgetItem, QLabel,
                             QDialogButtonBox, QSplitter, QTextEdit, QComboBox,
                             QCheckBox, QSpinBox, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QKeySequence, QFont
from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEnginePage, 
                                     QWebEngineProfile, QWebEngineSettings)

from .database import DatabaseManager
from .web_tab import WebTab

class MainWindow(QMainWindow):
    """Ventana principal del navegador"""
    
    def __init__(self, data_dir: str):
        super().__init__()
        self.data_dir = data_dir
        self.db_manager = DatabaseManager(data_dir)
        
        # Configurar la ventana
        self.setWindowTitle("PyWebBrowser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Inicializar componentes
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_status_bar()
        self.setup_web_profile()
        
        # Crear la primera pestaña
        self.add_new_tab("https://duckduckgo.com")
        
        # Timer para guardar historial automáticamente
        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self.auto_save)
        self.save_timer.start(30000)  # Guardar cada 30 segundos
        
        # Aplicar estilos CSS
        from .config import BROWSER_STYLES
        self.setStyleSheet(BROWSER_STYLES)
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra de navegación
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(5, 5, 5, 5)
        
        # Botones de navegación
        self.back_button = QPushButton("←")
        self.back_button.setToolTip("Atrás")
        self.back_button.clicked.connect(self.navigate_back)
        self.back_button.setEnabled(False)
        
        self.forward_button = QPushButton("→")
        self.forward_button.setToolTip("Adelante")
        self.forward_button.clicked.connect(self.navigate_forward)
        self.forward_button.setEnabled(False)
        
        self.refresh_button = QPushButton("⟳")
        self.refresh_button.setToolTip("Actualizar")
        self.refresh_button.clicked.connect(self.refresh_page)
        
        self.home_button = QPushButton("🏠")
        self.home_button.setToolTip("Inicio")
        self.home_button.clicked.connect(self.navigate_home)
        
        # Barra de direcciones
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Escribe una URL o término de búsqueda...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        # Botón de búsqueda
        self.search_button = QPushButton("🔍")
        self.search_button.setToolTip("Buscar en DuckDuckGo")
        self.search_button.clicked.connect(self.navigate_to_url)
        
        # Agregar widgets al layout de navegación
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.refresh_button)
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.search_button)
        
        # Widget contenedor para la barra de navegación
        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)
        main_layout.addWidget(nav_widget)
        
        # Pestañas del navegador
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        
        # Botón para agregar nueva pestaña
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setToolTip("Nueva pestaña")
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab())
        self.tab_widget.setCornerWidget(self.new_tab_button)
        
        main_layout.addWidget(self.tab_widget)
    
    def setup_menu(self):
        """Configurar el menú principal"""
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu("Archivo")
        
        new_tab_action = QAction("Nueva pestaña", self)
        new_tab_action.setShortcut(QKeySequence.AddTab)
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        file_menu.addAction(new_tab_action)
        
        new_window_action = QAction("Nueva ventana", self)
        new_window_action.setShortcut(QKeySequence.New)
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Salir", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menú Navegación
        nav_menu = menubar.addMenu("Navegación")
        
        back_action = QAction("Atrás", self)
        back_action.setShortcut(QKeySequence.Back)
        back_action.triggered.connect(self.navigate_back)
        nav_menu.addAction(back_action)
        
        forward_action = QAction("Adelante", self)
        forward_action.setShortcut(QKeySequence.Forward)
        forward_action.triggered.connect(self.navigate_forward)
        nav_menu.addAction(forward_action)
        
        refresh_action = QAction("Actualizar", self)
        refresh_action.setShortcut(QKeySequence.Refresh)
        refresh_action.triggered.connect(self.refresh_page)
        nav_menu.addAction(refresh_action)
        
        home_action = QAction("Inicio", self)
        home_action.triggered.connect(self.navigate_home)
        nav_menu.addAction(home_action)
        
        # Menú Herramientas
        tools_menu = menubar.addMenu("Herramientas")
        
        history_action = QAction("Historial", self)
        history_action.setShortcut(QKeySequence("Ctrl+H"))
        history_action.triggered.connect(self.show_history)
        tools_menu.addAction(history_action)
        
        favorites_action = QAction("Favoritos", self)
        favorites_action.setShortcut(QKeySequence("Ctrl+B"))
        favorites_action.triggered.connect(self.show_favorites)
        tools_menu.addAction(favorites_action)
        
        cookies_action = QAction("Gestionar Cookies", self)
        cookies_action.triggered.connect(self.show_cookies)
        tools_menu.addAction(cookies_action)
        
        tools_menu.addSeparator()
        
        settings_action = QAction("Configuración", self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        # Menú Ayuda
        help_menu = menubar.addMenu("Ayuda")
        
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_toolbar(self):
        """Configurar la barra de herramientas"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Agregar acciones comunes
        toolbar.addAction("⟲", self.navigate_back)
        toolbar.addAction("⟳", self.navigate_forward)
        toolbar.addAction("↻", self.refresh_page)
        toolbar.addAction("🏠", self.navigate_home)
        toolbar.addSeparator()
        toolbar.addAction("📖", self.show_history)
        toolbar.addAction("⭐", self.show_favorites)
        toolbar.addAction("🍪", self.show_cookies)
        toolbar.addSeparator()
        toolbar.addAction("⚙", self.show_settings)
    
    def setup_status_bar(self):
        """Configurar la barra de estado"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo")
    
    def setup_web_profile(self):
        """Configurar el perfil web para cookies persistentes"""
        profile_path = os.path.join(self.data_dir, "browser_profile")
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        
        self.web_profile = QWebEngineProfile("PyWebBrowser")
        self.web_profile.setPersistentStoragePath(profile_path)
        self.web_profile.setCachePath(os.path.join(profile_path, "cache"))
        
        # Configurar las opciones del navegador
        settings = self.web_profile.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
    
    def add_new_tab(self, url: str = None):
        """Agregar una nueva pestaña"""
        if url is None:
            url = "https://duckduckgo.com"
        
        web_tab = WebTab(self.web_profile, self.db_manager)
        
        # Conectar señales
        web_tab.urlChanged.connect(self.update_url_bar)
        web_tab.titleChanged.connect(self.update_tab_title)
        web_tab.loadProgress.connect(self.update_load_progress)
        web_tab.loadFinished.connect(self.update_navigation_buttons)
        
        # Agregar la pestaña
        index = self.tab_widget.addTab(web_tab, "Nueva pestaña")
        self.tab_widget.setCurrentIndex(index)
        
        # Navegar a la URL
        web_tab.load(QUrl(url))
        
        return web_tab
    
    def close_tab(self, index: int):
        """Cerrar una pestaña"""
        if self.tab_widget.count() > 1:
            widget = self.tab_widget.widget(index)
            self.tab_widget.removeTab(index)
            widget.deleteLater()
        else:
            self.close()
    
    def tab_changed(self, index: int):
        """Manejar el cambio de pestaña"""
        if index >= 0:
            current_tab = self.tab_widget.widget(index)
            if current_tab:
                self.update_url_bar(current_tab.url())
                self.update_navigation_buttons()
    
    def get_current_tab(self) -> WebTab:
        """Obtener la pestaña actual"""
        return self.tab_widget.currentWidget()
    
    def navigate_to_url(self):
        """Navegar a la URL ingresada en la barra de direcciones"""
        url_text = self.url_bar.text().strip()
        if not url_text:
            return
        
        current_tab = self.get_current_tab()
        if not current_tab:
            return
        
        # Verificar si es una URL válida
        if self.is_valid_url(url_text):
            url = url_text
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
        else:
            # Si no es una URL, buscar en DuckDuckGo
            url = f"https://duckduckgo.com/?q={url_text}"
        
        current_tab.load(QUrl(url))
    
    def is_valid_url(self, text: str) -> bool:
        """Verificar si el texto es una URL válida"""
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        # También considerar URLs sin protocolo pero con dominio
        domain_pattern = re.compile(
            r'^(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$', 
            re.IGNORECASE)
        
        return bool(url_pattern.match(text)) or bool(domain_pattern.match(text))
    
    def navigate_back(self):
        """Navegar hacia atrás"""
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.back()
    
    def navigate_forward(self):
        """Navegar hacia adelante"""
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.forward()
    
    def refresh_page(self):
        """Actualizar la página actual"""
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.reload()
    
    def navigate_home(self):
        """Navegar a la página de inicio"""
        home_url = self.db_manager.get_setting("home_url", "https://duckduckgo.com")
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.load(QUrl(home_url))
    
    def update_url_bar(self, url: QUrl):
        """Actualizar la barra de direcciones"""
        self.url_bar.setText(url.toString())
        self.status_bar.showMessage(f"Cargando: {url.toString()}")
    
    def update_tab_title(self, title: str):
        """Actualizar el título de la pestaña"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            # Limitar la longitud del título
            if len(title) > 20:
                title = title[:17] + "..."
            self.tab_widget.setTabText(current_index, title or "Sin título")
    
    def update_load_progress(self, progress: int):
        """Actualizar el progreso de carga"""
        if progress < 100:
            self.status_bar.showMessage(f"Cargando... {progress}%")
        else:
            self.status_bar.showMessage("Página cargada")
    
    def update_navigation_buttons(self):
        """Actualizar el estado de los botones de navegación"""
        current_tab = self.get_current_tab()
        if current_tab:
            self.back_button.setEnabled(current_tab.history().canGoBack())
            self.forward_button.setEnabled(current_tab.history().canGoForward())
    
    def show_history(self):
        """Mostrar el diálogo de historial"""
        from .dialogs import HistoryDialog
        dialog = HistoryDialog(self.db_manager, self)
        dialog.url_selected.connect(self.load_url_in_current_tab)
        dialog.exec_()
    
    def show_favorites(self):
        """Mostrar el diálogo de favoritos"""
        from .dialogs import FavoritesDialog
        dialog = FavoritesDialog(self.db_manager, self)
        dialog.url_selected.connect(self.load_url_in_current_tab)
        dialog.exec_()
    
    def show_cookies(self):
        """Mostrar el diálogo de gestión de cookies"""
        from .dialogs import CookiesDialog
        dialog = CookiesDialog(self.db_manager, self)
        dialog.exec_()
    
    def show_settings(self):
        """Mostrar el diálogo de configuración"""
        from .dialogs import SettingsDialog
        dialog = SettingsDialog(self.db_manager, self)
        dialog.exec_()
    
    def show_about(self):
        """Mostrar información sobre el navegador"""
        QMessageBox.about(self, "Acerca de PyWebBrowser", 
                         "PyWebBrowser v1.0\n\n"
                         "Un navegador web completo construido con Python y PyQt5\n\n"
                         "Características:\n"
                         "• Soporte HTTPS\n"
                         "• Integración con DuckDuckGo\n"
                         "• Historial de navegación\n"
                         "• Gestión de cookies\n"
                         "• Soporte completo de JavaScript\n"
                         "• Pestañas múltiples\n"
                         "• Favoritos\n"
                         "• Persistencia de datos")
    
    def load_url_in_current_tab(self, url: str):
        """Cargar una URL en la pestaña actual"""
        current_tab = self.get_current_tab()
        if current_tab:
            current_tab.load(QUrl(url))
        else:
            self.add_new_tab(url)
    
    def new_window(self):
        """Crear una nueva ventana del navegador"""
        new_window = MainWindow(self.data_dir)
        new_window.show()
    
    def auto_save(self):
        """Guardar automáticamente los datos"""
        # Aquí se podrían agregar operaciones de guardado automático
        pass
    
    def closeEvent(self, event):
        """Manejar el cierre de la ventana"""
        # Guardar configuraciones antes de cerrar
        try:
            # Guardar la geometría de la ventana
            geometry = self.saveGeometry()
            self.db_manager.save_setting("window_geometry", geometry.toHex().data().decode())
            
            # Guardar las URLs abiertas
            open_urls = []
            for i in range(self.tab_widget.count()):
                tab = self.tab_widget.widget(i)
                if tab:
                    open_urls.append(tab.url().toString())
            
            if open_urls:
                import json
                self.db_manager.save_setting("open_tabs", json.dumps(open_urls))
                
        except Exception as e:
            print(f"Error al guardar configuraciones: {e}")
        
        event.accept()
