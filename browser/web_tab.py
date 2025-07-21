"""
WebTab - Clase para manejar cada pestaña del navegador
Incluye el motor web y la integración con la base de datos
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from urllib.parse import urlparse

class WebTab(QWebEngineView):
    """Pestaña del navegador web"""
    
    # Señales personalizadas
    titleChanged = pyqtSignal(str)
    urlChanged = pyqtSignal(QUrl)
    loadProgress = pyqtSignal(int)
    loadFinished = pyqtSignal(bool)
    
    def __init__(self, profile: QWebEngineProfile, db_manager):
        super().__init__()
        self.db_manager = db_manager
        
        # Configurar la página web con el perfil personalizado
        self.web_page = QWebEnginePage(profile, self)
        self.setPage(self.web_page)
        
        # Conectar señales internas
        self.page().titleChanged.connect(self.on_title_changed)
        self.page().urlChanged.connect(self.on_url_changed)
        self.page().loadProgress.connect(self.on_load_progress)
        self.page().loadFinished.connect(self.on_load_finished)
        
        # Variables de estado
        self.current_url = None
        self.current_title = None
        
    def on_title_changed(self, title: str):
        """Manejar el cambio de título de la página"""
        self.current_title = title
        self.titleChanged.emit(title)
        
        # Actualizar en la base de datos si tenemos URL
        if self.current_url:
            self.db_manager.add_history_entry(self.current_url, title)
    
    def on_url_changed(self, url: QUrl):
        """Manejar el cambio de URL"""
        url_string = url.toString()
        self.current_url = url_string
        self.urlChanged.emit(url)
        
        # Agregar al historial solo si es una URL válida
        if url_string and not url_string.startswith(('about:', 'chrome:', 'data:')):
            # Si ya tenemos título, actualizar inmediatamente
            if self.current_title:
                self.db_manager.add_history_entry(url_string, self.current_title)
            else:
                # Agregar sin título por ahora
                self.db_manager.add_history_entry(url_string)
    
    def on_load_progress(self, progress: int):
        """Manejar el progreso de carga"""
        self.loadProgress.emit(progress)
    
    def on_load_finished(self, success: bool):
        """Manejar la finalización de la carga"""
        self.loadFinished.emit(success)
        
        # Si la carga fue exitosa y tenemos URL y título, actualizar historial
        if success and self.current_url and self.current_title:
            self.db_manager.add_history_entry(self.current_url, self.current_title)
    
    def load_url(self, url_string: str):
        """Cargar una URL específica"""
        if not url_string.startswith(('http://', 'https://')):
            url_string = 'https://' + url_string
        
        self.load(QUrl(url_string))
    
    def get_domain(self) -> str:
        """Obtener el dominio de la URL actual"""
        if self.current_url:
            parsed = urlparse(self.current_url)
            return parsed.netloc
        return ""
    
    def is_secure(self) -> bool:
        """Verificar si la conexión actual es segura (HTTPS)"""
        if self.current_url:
            return self.current_url.startswith('https://')
        return False
    
    def get_page_info(self) -> dict:
        """Obtener información de la página actual"""
        return {
            'url': self.current_url,
            'title': self.current_title,
            'domain': self.get_domain(),
            'secure': self.is_secure(),
            'can_go_back': self.history().canGoBack(),
            'can_go_forward': self.history().canGoForward()
        }
