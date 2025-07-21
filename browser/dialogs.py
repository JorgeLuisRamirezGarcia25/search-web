"""
Diálogos para el navegador web
Incluye historial, favoritos, cookies y configuración
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QListWidgetItem, QPushButton, QLabel, QLineEdit,
                             QDialogButtonBox, QMessageBox, QTabWidget, QWidget,
                             QTableWidget, QTableWidgetItem, QComboBox, QSpinBox,
                             QCheckBox, QGroupBox, QFormLayout, QTextEdit,
                             QHeaderView, QAbstractItemView, QSplitter)
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from PyQt5.QtGui import QFont
import json
from datetime import datetime

class HistoryDialog(QDialog):
    """Diálogo para mostrar y gestionar el historial"""
    
    url_selected = pyqtSignal(str)
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Historial de Navegación")
        self.setGeometry(200, 200, 800, 600)
        
        self.setup_ui()
        self.load_history()
    
    def setup_ui(self):
        """Configurar la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar en historial...")
        self.search_input.textChanged.connect(self.search_history)
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_history)
        search_layout.addWidget(self.search_button)
        
        layout.addLayout(search_layout)
        
        # Lista del historial
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.history_list)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.visit_button = QPushButton("Visitar")
        self.visit_button.clicked.connect(self.visit_selected)
        button_layout.addWidget(self.visit_button)
        
        self.favorite_button = QPushButton("Alternar Favorito")
        self.favorite_button.clicked.connect(self.toggle_favorite)
        button_layout.addWidget(self.favorite_button)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_selected)
        button_layout.addWidget(self.delete_button)
        
        self.clear_button = QPushButton("Limpiar Todo")
        self.clear_button.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        
        self.close_button = QPushButton("Cerrar")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
    
    def load_history(self, search_term=None):
        """Cargar el historial en la lista"""
        self.history_list.clear()
        
        if search_term:
            entries = self.db_manager.search_history(search_term)
        else:
            entries = self.db_manager.get_history()
        
        for entry in entries:
            item_text = f"{entry['title'] or 'Sin título'}\n{entry['url']}\n"
            item_text += f"Visitado: {entry['visit_time']} | Visitas: {entry['visit_count']}"
            if entry['is_favorite']:
                item_text += " ⭐"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, entry)
            self.history_list.addItem(item)
    
    def search_history(self):
        """Buscar en el historial"""
        search_term = self.search_input.text().strip()
        self.load_history(search_term if search_term else None)
    
    def on_item_double_clicked(self, item):
        """Manejar doble clic en un elemento"""
        self.visit_selected()
    
    def visit_selected(self):
        """Visitar la URL seleccionada"""
        current_item = self.history_list.currentItem()
        if current_item:
            entry = current_item.data(Qt.UserRole)
            self.url_selected.emit(entry['url'])
            self.close()
    
    def toggle_favorite(self):
        """Alternar el estado de favorito"""
        current_item = self.history_list.currentItem()
        if current_item:
            entry = current_item.data(Qt.UserRole)
            if self.db_manager.toggle_favorite(entry['id']):
                self.load_history()
                QMessageBox.information(self, "Favorito", 
                                      "Estado de favorito actualizado")
    
    def delete_selected(self):
        """Eliminar la entrada seleccionada"""
        current_item = self.history_list.currentItem()
        if current_item:
            entry = current_item.data(Qt.UserRole)
            reply = QMessageBox.question(self, "Eliminar", 
                                       f"¿Eliminar esta entrada del historial?\n{entry['url']}",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.db_manager.delete_history_entry(entry['id']):
                    self.load_history()
                    QMessageBox.information(self, "Eliminado", 
                                          "Entrada eliminada del historial")
    
    def clear_history(self):
        """Limpiar todo el historial"""
        reply = QMessageBox.question(self, "Limpiar Historial", 
                                   "¿Estás seguro de que quieres eliminar todo el historial?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.db_manager.clear_history():
                self.load_history()
                QMessageBox.information(self, "Historial Limpiado", 
                                      "Todo el historial ha sido eliminado")

class FavoritesDialog(QDialog):
    """Diálogo para mostrar y gestionar favoritos"""
    
    url_selected = pyqtSignal(str)
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Favoritos")
        self.setGeometry(200, 200, 600, 400)
        
        self.setup_ui()
        self.load_favorites()
    
    def setup_ui(self):
        """Configurar la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        
        # Lista de favoritos
        self.favorites_list = QListWidget()
        self.favorites_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.favorites_list)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.visit_button = QPushButton("Visitar")
        self.visit_button.clicked.connect(self.visit_selected)
        button_layout.addWidget(self.visit_button)
        
        self.remove_button = QPushButton("Quitar de Favoritos")
        self.remove_button.clicked.connect(self.remove_favorite)
        button_layout.addWidget(self.remove_button)
        
        button_layout.addStretch()
        
        self.close_button = QPushButton("Cerrar")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
    
    def load_favorites(self):
        """Cargar favoritos en la lista"""
        self.favorites_list.clear()
        
        favorites = self.db_manager.get_favorites()
        
        for favorite in favorites:
            item_text = f"{favorite['title'] or 'Sin título'}\n{favorite['url']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, favorite)
            self.favorites_list.addItem(item)
    
    def on_item_double_clicked(self, item):
        """Manejar doble clic en un elemento"""
        self.visit_selected()
    
    def visit_selected(self):
        """Visitar la URL seleccionada"""
        current_item = self.favorites_list.currentItem()
        if current_item:
            favorite = current_item.data(Qt.UserRole)
            self.url_selected.emit(favorite['url'])
            self.close()
    
    def remove_favorite(self):
        """Quitar de favoritos"""
        current_item = self.favorites_list.currentItem()
        if current_item:
            favorite = current_item.data(Qt.UserRole)
            reply = QMessageBox.question(self, "Quitar Favorito", 
                                       f"¿Quitar de favoritos?\n{favorite['url']}",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.db_manager.toggle_favorite(favorite['id']):
                    self.load_favorites()
                    QMessageBox.information(self, "Removido", 
                                          "Quitado de favoritos")

class CookiesDialog(QDialog):
    """Diálogo para gestionar cookies"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Gestión de Cookies")
        self.setGeometry(200, 200, 800, 500)
        
        self.setup_ui()
        self.load_cookies()
    
    def setup_ui(self):
        """Configurar la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        
        # Filtro por dominio
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por dominio:"))
        self.domain_filter = QLineEdit()
        self.domain_filter.setPlaceholderText("Todos los dominios")
        self.domain_filter.textChanged.connect(self.filter_cookies)
        filter_layout.addWidget(self.domain_filter)
        
        self.filter_button = QPushButton("Filtrar")
        self.filter_button.clicked.connect(self.filter_cookies)
        filter_layout.addWidget(self.filter_button)
        
        layout.addLayout(filter_layout)
        
        # Tabla de cookies
        self.cookies_table = QTableWidget()
        self.cookies_table.setColumnCount(7)
        self.cookies_table.setHorizontalHeaderLabels([
            "Dominio", "Nombre", "Valor", "Ruta", "Expira", "Segura", "HTTP Only"
        ])
        self.cookies_table.horizontalHeader().setStretchLastSection(True)
        self.cookies_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.cookies_table)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.delete_selected_button = QPushButton("Eliminar Seleccionadas")
        self.delete_selected_button.clicked.connect(self.delete_selected_cookies)
        button_layout.addWidget(self.delete_selected_button)
        
        self.delete_domain_button = QPushButton("Eliminar por Dominio")
        self.delete_domain_button.clicked.connect(self.delete_domain_cookies)
        button_layout.addWidget(self.delete_domain_button)
        
        self.clear_all_button = QPushButton("Eliminar Todas")
        self.clear_all_button.clicked.connect(self.clear_all_cookies)
        button_layout.addWidget(self.clear_all_button)
        
        button_layout.addStretch()
        
        self.close_button = QPushButton("Cerrar")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
    
    def load_cookies(self, domain=None):
        """Cargar cookies en la tabla"""
        cookies = self.db_manager.get_cookies(domain)
        
        self.cookies_table.setRowCount(len(cookies))
        
        for row, cookie in enumerate(cookies):
            self.cookies_table.setItem(row, 0, QTableWidgetItem(cookie['domain']))
            self.cookies_table.setItem(row, 1, QTableWidgetItem(cookie['name']))
            self.cookies_table.setItem(row, 2, QTableWidgetItem(cookie['value'][:50] + "..." if len(cookie['value']) > 50 else cookie['value']))
            self.cookies_table.setItem(row, 3, QTableWidgetItem(cookie['path']))
            self.cookies_table.setItem(row, 4, QTableWidgetItem(str(cookie['expires']) if cookie['expires'] else "Sesión"))
            self.cookies_table.setItem(row, 5, QTableWidgetItem("Sí" if cookie['secure'] else "No"))
            self.cookies_table.setItem(row, 6, QTableWidgetItem("Sí" if cookie['http_only'] else "No"))
    
    def filter_cookies(self):
        """Filtrar cookies por dominio"""
        domain = self.domain_filter.text().strip()
        self.load_cookies(domain if domain else None)
    
    def delete_selected_cookies(self):
        """Eliminar cookies seleccionadas"""
        selected_rows = set()
        for item in self.cookies_table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.information(self, "Sin Selección", 
                                  "Selecciona las cookies que quieres eliminar")
            return
        
        reply = QMessageBox.question(self, "Eliminar Cookies", 
                                   f"¿Eliminar {len(selected_rows)} cookies seleccionadas?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Nota: Esto requeriría una implementación más específica en el DatabaseManager
            # para eliminar cookies individuales
            QMessageBox.information(self, "Función Pendiente", 
                                  "Eliminación de cookies individuales en desarrollo")
    
    def delete_domain_cookies(self):
        """Eliminar cookies de un dominio específico"""
        domain = self.domain_filter.text().strip()
        if not domain:
            QMessageBox.information(self, "Dominio Requerido", 
                                  "Ingresa un dominio para eliminar sus cookies")
            return
        
        reply = QMessageBox.question(self, "Eliminar Cookies del Dominio", 
                                   f"¿Eliminar todas las cookies de {domain}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.db_manager.delete_cookies(domain):
                self.load_cookies()
                QMessageBox.information(self, "Cookies Eliminadas", 
                                      f"Cookies de {domain} eliminadas")
    
    def clear_all_cookies(self):
        """Eliminar todas las cookies"""
        reply = QMessageBox.question(self, "Eliminar Todas las Cookies", 
                                   "¿Estás seguro de que quieres eliminar todas las cookies?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.db_manager.delete_cookies():
                self.load_cookies()
                QMessageBox.information(self, "Cookies Eliminadas", 
                                      "Todas las cookies han sido eliminadas")

class SettingsDialog(QDialog):
    """Diálogo de configuración del navegador"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Configuración")
        self.setGeometry(200, 200, 500, 400)
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Configurar la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        
        # Pestañas de configuración
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Pestaña General
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        
        self.home_url_input = QLineEdit()
        self.home_url_input.setPlaceholderText("https://duckduckgo.com")
        general_layout.addRow("Página de inicio:", self.home_url_input)
        
        self.download_path_input = QLineEdit()
        general_layout.addRow("Directorio de descargas:", self.download_path_input)
        
        tab_widget.addTab(general_tab, "General")
        
        # Pestaña Privacidad
        privacy_tab = QWidget()
        privacy_layout = QFormLayout(privacy_tab)
        
        self.save_history_check = QCheckBox()
        self.save_history_check.setChecked(True)
        privacy_layout.addRow("Guardar historial:", self.save_history_check)
        
        self.accept_cookies_check = QCheckBox()
        self.accept_cookies_check.setChecked(True)
        privacy_layout.addRow("Aceptar cookies:", self.accept_cookies_check)
        
        self.javascript_enabled_check = QCheckBox()
        self.javascript_enabled_check.setChecked(True)
        privacy_layout.addRow("Habilitar JavaScript:", self.javascript_enabled_check)
        
        tab_widget.addTab(privacy_tab, "Privacidad")
        
        # Pestaña Avanzado
        advanced_tab = QWidget()
        advanced_layout = QFormLayout(advanced_tab)
        
        self.cache_size_spin = QSpinBox()
        self.cache_size_spin.setRange(10, 1000)
        self.cache_size_spin.setValue(100)
        self.cache_size_spin.setSuffix(" MB")
        advanced_layout.addRow("Tamaño de caché:", self.cache_size_spin)
        
        self.user_agent_input = QLineEdit()
        self.user_agent_input.setPlaceholderText("User Agent personalizado (opcional)")
        advanced_layout.addRow("User Agent:", self.user_agent_input)
        
        tab_widget.addTab(advanced_tab, "Avanzado")
        
        # Botones
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.close)
        layout.addWidget(button_box)
    
    def load_settings(self):
        """Cargar configuraciones actuales"""
        self.home_url_input.setText(
            self.db_manager.get_setting("home_url", "https://duckduckgo.com")
        )
        self.download_path_input.setText(
            self.db_manager.get_setting("download_path", "")
        )
        
        self.save_history_check.setChecked(
            self.db_manager.get_setting("save_history", "true") == "true"
        )
        self.accept_cookies_check.setChecked(
            self.db_manager.get_setting("accept_cookies", "true") == "true"
        )
        self.javascript_enabled_check.setChecked(
            self.db_manager.get_setting("javascript_enabled", "true") == "true"
        )
        
        self.cache_size_spin.setValue(
            int(self.db_manager.get_setting("cache_size", "100"))
        )
        self.user_agent_input.setText(
            self.db_manager.get_setting("user_agent", "")
        )
    
    def save_settings(self):
        """Guardar configuraciones"""
        try:
            # Guardar configuraciones generales
            self.db_manager.save_setting("home_url", self.home_url_input.text())
            self.db_manager.save_setting("download_path", self.download_path_input.text())
            
            # Guardar configuraciones de privacidad
            self.db_manager.save_setting("save_history", 
                                       "true" if self.save_history_check.isChecked() else "false")
            self.db_manager.save_setting("accept_cookies", 
                                       "true" if self.accept_cookies_check.isChecked() else "false")
            self.db_manager.save_setting("javascript_enabled", 
                                       "true" if self.javascript_enabled_check.isChecked() else "false")
            
            # Guardar configuraciones avanzadas
            self.db_manager.save_setting("cache_size", str(self.cache_size_spin.value()))
            self.db_manager.save_setting("user_agent", self.user_agent_input.text())
            
            QMessageBox.information(self, "Configuración Guardada", 
                                  "Las configuraciones han sido guardadas correctamente.\n"
                                  "Algunos cambios requieren reiniciar el navegador.")
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Error al guardar configuraciones: {str(e)}")

class AboutDialog(QDialog):
    """Diálogo de información sobre el navegador"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de PyWebBrowser")
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("PyWebBrowser")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Información
        info_text = """
        <p><b>Versión:</b> 1.0</p>
        <p><b>Desarrollado con:</b> Python 3.x + PyQt5</p>
        
        <p><b>Características:</b></p>
        <ul>
        <li>✓ Soporte HTTPS completo</li>
        <li>✓ Motor de búsqueda DuckDuckGo integrado</li>
        <li>✓ Historial de navegación persistente</li>
        <li>✓ Gestión completa de cookies</li>
        <li>✓ Soporte completo de JavaScript</li>
        <li>✓ Navegación por pestañas</li>
        <li>✓ Sistema de favoritos</li>
        <li>✓ Operaciones CRUD para datos</li>
        </ul>
        
        <p><b>Motor Web:</b> Chromium (via QtWebEngine)</p>
        <p><b>Base de Datos:</b> SQLite</p>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Botón cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
