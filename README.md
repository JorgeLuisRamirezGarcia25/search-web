# PyWebBrowser 🌐

Un navegador web completo desarrollado en Python con PyQt5, que incluye todas las características modernas de navegación web.

## 🚀 Características

### ✅ Funcionalidades Implementadas

- **🔒 Soporte HTTPS Completo**: Conexiones seguras con validación de certificados
- **🔍 Motor de Búsqueda DuckDuckGo**: Integración directa con DuckDuckGo como motor de búsqueda predeterminado
- **📖 Historial de Navegación**: Almacenamiento persistente de todas las páginas visitadas
- **🍪 Gestión de Cookies**: Sistema completo de manejo y persistencia de cookies
- **⚡ Soporte JavaScript**: Motor Chromium integrado con soporte completo de JavaScript
- **📑 Navegación por Pestañas**: Múltiples pestañas con gestión completa
- **⭐ Sistema de Favoritos**: Marcar y gestionar páginas favoritas
- **💾 Persistencia de Datos**: Todos los datos se guardan automáticamente
- **🔧 Operaciones CRUD**: Crear, leer, actualizar y eliminar datos de historial y cookies

### 🎨 Interfaz de Usuario

- Diseño moderno y limpio
- Barra de navegación intuitiva
- Gestión de pestañas con cierre individual
- Menús contextuales y atajos de teclado
- Diálogos de configuración avanzada
- Tema visual consistente

### 🛠️ Tecnologías Utilizadas

- **Python 3.6+**: Lenguaje principal
- **PyQt5**: Framework de interfaz gráfica
- **QtWebEngine**: Motor de renderizado web (Chromium)
- **SQLite**: Base de datos para persistencia
- **Requests**: Biblioteca HTTP adicional

## 📦 Instalación

### Requisitos Previos

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebengine

# CentOS/RHEL/Fedora
sudo yum install python3 python3-pip
sudo yum install python3-qt5 python3-qt5-webengine

# macOS (con Homebrew)
brew install python@3.9
brew install pyqt5
```

### Instalación del Navegador

1. **Clonar o descargar el proyecto**:
   ```bash
   git clone <repository-url>
   cd search\ web
   ```

2. **Crear entorno virtual**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Linux/macOS
   # .venv\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el navegador**:
   ```bash
   python main.py
   ```

## 🖥️ Uso

### Navegación Básica

- **Nueva pestaña**: `Ctrl+T` o clic en el botón "+"
- **Cerrar pestaña**: `Ctrl+W` o clic en la "X" de la pestaña
- **Actualizar página**: `F5` o `Ctrl+R`
- **Ir atrás/adelante**: Botones de navegación o `Alt+←`/`Alt+→`
- **Página de inicio**: `Ctrl+Home` o botón de inicio

### Funciones Avanzadas

- **Ver historial**: `Ctrl+H`
- **Gestionar favoritos**: `Ctrl+B`
- **Configuración**: `Ctrl+,`
- **Gestión de cookies**: Menú Herramientas > Gestionar Cookies

### Búsquedas

- Escribir términos de búsqueda directamente en la barra de direcciones
- El navegador automáticamente detecta si es una URL o una búsqueda
- Todas las búsquedas se redirigen a DuckDuckGo

## 📁 Estructura del Proyecto

```
search web/
├── main.py                 # Archivo principal de ejecución
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Documentación
└── browser/               # Módulo principal del navegador
    ├── __init__.py        # Inicialización del paquete
    ├── main_window.py     # Ventana principal del navegador
    ├── web_tab.py         # Clase para pestañas individuales
    ├── database.py        # Gestor de base de datos (SQLite)
    ├── dialogs.py         # Diálogos de interfaz (historial, favoritos, etc.)
    ├── config.py          # Configuración y estilos
    └── utils.py           # Utilidades y funciones auxiliares
```

## 🗄️ Base de Datos

El navegador utiliza SQLite para almacenar:

### Tabla `history`
- `id`: Identificador único
- `url`: URL visitada
- `title`: Título de la página
- `visit_time`: Fecha y hora de visita
- `visit_count`: Número de visitas
- `is_favorite`: Si está marcado como favorito

### Tabla `cookies`
- `id`: Identificador único
- `domain`: Dominio de la cookie
- `name`: Nombre de la cookie
- `value`: Valor de la cookie
- `path`: Ruta de la cookie
- `expires`: Fecha de expiración
- `secure`: Si es una cookie segura
- `http_only`: Si es solo HTTP

### Tabla `settings`
- `key`: Clave de configuración
- `value`: Valor de configuración
- `updated_time`: Fecha de actualización

## ⚙️ Configuración

### Configuraciones Disponibles

- **Página de inicio**: URL que se carga al abrir nuevas pestañas
- **Directorio de descargas**: Carpeta para archivos descargados
- **Guardar historial**: Activar/desactivar el guardado de historial
- **Aceptar cookies**: Permitir o bloquear cookies
- **JavaScript**: Habilitar/deshabilitar JavaScript
- **Tamaño de caché**: Espacio en disco para caché
- **User Agent**: Identificador personalizado del navegador

### Archivos de Configuración

Los datos se almacenan en:
- **Linux**: `~/.pybrowser/`
- **Windows**: `%USERPROFILE%\.pybrowser\`
- **macOS**: `~/.pybrowser/`

## 🔧 Operaciones CRUD

### Historial

- **Crear**: Las páginas se agregan automáticamente al visitarlas
- **Leer**: Ver historial completo con búsqueda y filtrado
- **Actualizar**: Marcar/desmarcar como favorito, actualizar contadores de visita
- **Eliminar**: Borrar entradas individuales o limpiar todo el historial

### Cookies

- **Crear**: Las cookies se almacenan automáticamente
- **Leer**: Ver todas las cookies por dominio
- **Actualizar**: Las cookies se actualizan automáticamente
- **Eliminar**: Borrar cookies por dominio o eliminar todas

### Configuraciones

- **Crear/Actualizar**: Modificar configuraciones desde el diálogo de preferencias
- **Leer**: Cargar configuraciones al iniciar
- **Eliminar**: Restablecer a valores por defecto

## 🚀 Características Técnicas

### Seguridad

- ✅ Validación de certificados SSL/TLS
- ✅ Detección básica de URLs maliciosas
- ✅ Sanitización de HTML
- ✅ Cookies seguras con flags HTTP-only

### Rendimiento

- ✅ Caché de páginas web
- ✅ Carga asíncrona de recursos
- ✅ Optimización de base de datos con índices
- ✅ Gestión eficiente de memoria

### Compatibilidad

- ✅ Soporte para estándares web modernos
- ✅ HTML5, CSS3, ECMAScript 6+
- ✅ WebGL y tecnologías multimedia
- ✅ Responsive design

## 🐛 Resolución de Problemas

### Problemas Comunes

1. **El navegador no inicia**:
   - Verificar que PyQt5 y PyQtWebEngine estén instalados
   - Comprobar permisos de escritura en el directorio de datos

2. **JavaScript no funciona**:
   - Verificar configuración en Herramientas > Configuración
   - Reiniciar el navegador después de cambiar configuraciones

3. **Problemas con certificados**:
   - Actualizar certificados del sistema
   - Verificar configuración de proxy si se usa

4. **Rendimiento lento**:
   - Aumentar tamaño de caché en configuración
   - Limpiar historial y cookies antiguas

### Logs y Depuración

Los errores se muestran en la consola donde se ejecuta el navegador. Para debug:

```bash
python main.py --debug
```

## 🤝 Contribución

### Cómo Contribuir

1. Fork del repositorio
2. Crear rama para nueva característica: `git checkout -b feature/nueva-caracteristica`
3. Commit de cambios: `git commit -am 'Agregar nueva característica'`
4. Push a la rama: `git push origin feature/nueva-caracteristica`
5. Crear Pull Request

### Estándares de Código

- Seguir PEP 8 para estilo de Python
- Documentar funciones y clases
- Escribir tests para nuevas características
- Usar type hints cuando sea posible

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🔮 Próximas Características

### En Desarrollo

- [ ] Sistema de descargas integrado
- [ ] Bloqueador de anuncios básico
- [ ] Modo incógnito/privado
- [ ] Sincronización de datos entre dispositivos
- [ ] Extensiones y plugins
- [ ] Modo oscuro/claro
- [ ] Exportar/importar marcadores
- [ ] Capturas de pantalla de páginas
- [ ] Lector de PDF integrado
- [ ] Traductor automático

### Mejoras Planificadas

- [ ] Optimización de rendimiento
- [ ] Mejor gestión de memoria
- [ ] Soporte para más motores de búsqueda
- [ ] Interfaz más personalizable
- [ ] Mejor integración con el sistema operativo

## 📞 Soporte

Para reportar bugs o solicitar características:

1. Crear un issue en el repositorio
2. Incluir información del sistema operativo
3. Describir pasos para reproducir el problema
4. Adjuntar logs si es posible

## 👥 Autores

- **Desarrollador Principal**: [Tu Nombre]
- **Contribuidores**: Ver lista de contributors en GitHub

## 🙏 Agradecimientos

- PyQt Team por el excelente framework
- Chromium Project por el motor web
- DuckDuckGo por el motor de búsqueda privado
- Comunidad Python por las bibliotecas utilizadas

---

**¡Disfruta navegando con PyWebBrowser!** 🌐✨
