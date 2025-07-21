"""
Configuración y estilos para el navegador
"""

# Configuración por defecto
DEFAULT_CONFIG = {
    "window": {
        "width": 1200,
        "height": 800,
        "title": "PyWebBrowser"
    },
    "network": {
        "user_agent": "PyWebBrowser/1.0 (Python; QtWebEngine)",
        "timeout": 30,
        "max_redirects": 10
    },
    "urls": {
        "home": "https://duckduckgo.com",
        "search_engine": "https://duckduckgo.com/?q={query}",
        "new_tab": "https://duckduckgo.com"
    },
    "database": {
        "max_history_entries": 10000,
        "auto_save_interval": 30  # segundos
    },
    "ui": {
        "show_status_bar": True,
        "show_toolbar": True,
        "tab_close_button": True
    }
}

# Estilos CSS para la interfaz
BROWSER_STYLES = """
QMainWindow {
    background-color: #f5f5f5;
}

QToolBar {
    background-color: #ffffff;
    border: none;
    spacing: 5px;
    padding: 5px;
}

QToolBar QPushButton {
    background-color: #e9ecef;
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 14px;
    min-width: 30px;
}

QToolBar QPushButton:hover {
    background-color: #dee2e6;
    border-color: #adb5bd;
}

QToolBar QPushButton:pressed {
    background-color: #ced4da;
}

QToolBar QPushButton:disabled {
    background-color: #f8f9fa;
    color: #6c757d;
    border-color: #e9ecef;
}

QLineEdit {
    padding: 8px 12px;
    font-size: 14px;
    border: 2px solid #ced4da;
    border-radius: 4px;
    background-color: white;
}

QLineEdit:focus {
    border-color: #007bff;
    outline: none;
}

QTabWidget::pane {
    border: 1px solid #ced4da;
    background-color: white;
}

QTabWidget::tab-bar {
    alignment: left;
}

QTabBar::tab {
    background-color: #e9ecef;
    border: 1px solid #ced4da;
    border-bottom: none;
    padding: 8px 16px;
    margin-right: 2px;
    min-width: 100px;
    max-width: 200px;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom: 1px solid white;
}

QTabBar::tab:hover {
    background-color: #dee2e6;
}

QTabBar::close-button {
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwLjUgMy41TDMuNSAxMC41IiBzdHJva2U9IiM2Yzc1N2QiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+CjxwYXRoIGQ9Ik0zLjUgMy41TDEwLjUgMTAuNSIgc3Ryb2tlPSIjNmM3NTdkIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
    margin: 2px;
}

QTabBar::close-button:hover {
    background-color: #ff6b6b;
    border-radius: 2px;
}

QStatusBar {
    background-color: #f8f9fa;
    border-top: 1px solid #e9ecef;
    padding: 4px;
}

QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e9ecef;
}

QMenuBar::item {
    padding: 6px 12px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #e9ecef;
}

QMenu {
    background-color: white;
    border: 1px solid #ced4da;
    padding: 4px;
}

QMenu::item {
    padding: 6px 12px;
    border: none;
}

QMenu::item:selected {
    background-color: #007bff;
    color: white;
}

QDialog {
    background-color: #f8f9fa;
}

QListWidget {
    background-color: white;
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 4px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #e9ecef;
}

QListWidget::item:selected {
    background-color: #007bff;
    color: white;
}

QListWidget::item:hover {
    background-color: #e9ecef;
}

QTableWidget {
    background-color: white;
    border: 1px solid #ced4da;
    border-radius: 4px;
    gridline-color: #e9ecef;
}

QTableWidget::item {
    padding: 6px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #007bff;
    color: white;
}

QHeaderView::section {
    background-color: #e9ecef;
    border: none;
    border-right: 1px solid #ced4da;
    border-bottom: 1px solid #ced4da;
    padding: 8px;
    font-weight: bold;
}

QPushButton {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #0056b3;
}

QPushButton:pressed {
    background-color: #004085;
}

QPushButton:disabled {
    background-color: #6c757d;
    color: #adb5bd;
}

QPushButton.secondary {
    background-color: #6c757d;
}

QPushButton.secondary:hover {
    background-color: #545b62;
}

QPushButton.danger {
    background-color: #dc3545;
}

QPushButton.danger:hover {
    background-color: #c82333;
}

QPushButton.success {
    background-color: #28a745;
}

QPushButton.success:hover {
    background-color: #1e7e34;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #ced4da;
    border-radius: 4px;
    margin-top: 8px;
    padding-top: 8px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px 0 4px;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #ced4da;
    border-radius: 3px;
    background-color: white;
}

QCheckBox::indicator:checked {
    background-color: #007bff;
    border-color: #007bff;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
}

QSpinBox {
    padding: 6px 8px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    background-color: white;
}

QComboBox {
    padding: 6px 8px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    background-color: white;
    min-width: 100px;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgNC41TDYgNy41TDkgNC41IiBzdHJva2U9IiM2Yzc1N2QiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
}

QTextEdit {
    border: 1px solid #ced4da;
    border-radius: 4px;
    background-color: white;
    padding: 8px;
}

QScrollBar:vertical {
    background-color: #f8f9fa;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #ced4da;
    border-radius: 6px;
    min-height: 20px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: #adb5bd;
}

QScrollBar:horizontal {
    background-color: #f8f9fa;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #ced4da;
    border-radius: 6px;
    min-width: 20px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #adb5bd;
}

QSplitter::handle {
    background-color: #ced4da;
}

QSplitter::handle:horizontal {
    width: 3px;
}

QSplitter::handle:vertical {
    height: 3px;
}
"""

# Configuración de JavaScript personalizado para inyectar en páginas
CUSTOM_JAVASCRIPT = """
// Script personalizado para el navegador
(function() {
    // Agregar funcionalidad adicional si es necesario
    console.log('PyWebBrowser - Script personalizado cargado');
    
    // Función para reportar el título de la página
    function reportTitle() {
        if (window.pywebkit && window.pywebkit.reportTitle) {
            window.pywebkit.reportTitle(document.title);
        }
    }
    
    // Reportar cambios en el título
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', reportTitle);
    } else {
        reportTitle();
    }
    
    // Observer para cambios en el título
    const titleObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                reportTitle();
            }
        });
    });
    
    if (document.querySelector('title')) {
        titleObserver.observe(document.querySelector('title'), {
            childList: true,
            subtree: true
        });
    }
})();
"""
