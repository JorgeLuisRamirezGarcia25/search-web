"""
Utilidades y funciones auxiliares para el navegador
"""

import os
import re
import json
import hashlib
from urllib.parse import urlparse, urljoin, quote
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta

class URLUtils:
    """Utilidades para manejo de URLs"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Verificar si una URL es válida"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalizar una URL"""
        url = url.strip()
        
        # Si no tiene esquema, agregar https
        if not url.startswith(('http://', 'https://', 'ftp://')):
            # Verificar si parece un dominio
            if '.' in url and not url.startswith('www.'):
                url = 'https://' + url
            elif url.startswith('www.'):
                url = 'https://' + url
            else:
                # Buscar en DuckDuckGo
                return f"https://duckduckgo.com/?q={quote(url)}"
        
        return url
    
    @staticmethod
    def get_domain(url: str) -> str:
        """Obtener el dominio de una URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except:
            return ""
    
    @staticmethod
    def get_base_url(url: str) -> str:
        """Obtener la URL base (protocolo + dominio)"""
        try:
            parsed = urlparse(url)
            return f"{parsed.scheme}://{parsed.netloc}"
        except:
            return ""
    
    @staticmethod
    def is_secure(url: str) -> bool:
        """Verificar si la URL usa HTTPS"""
        return url.startswith('https://')
    
    @staticmethod
    def create_search_url(query: str, engine: str = "duckduckgo") -> str:
        """Crear URL de búsqueda"""
        engines = {
            "duckduckgo": "https://duckduckgo.com/?q={}",
            "google": "https://www.google.com/search?q={}",
            "bing": "https://www.bing.com/search?q={}"
        }
        
        template = engines.get(engine, engines["duckduckgo"])
        return template.format(quote(query))

class DataUtils:
    """Utilidades para manejo de datos"""
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Formatear tamaño de archivo en formato legible"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024.0 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Formatear fecha y hora"""
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 7:
            return dt.strftime("%Y-%m-%d %H:%M")
        elif diff.days > 0:
            return f"Hace {diff.days} días"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"Hace {hours} horas"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"Hace {minutes} minutos"
        else:
            return "Hace un momento"
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitizar nombre de archivo"""
        # Caracteres no permitidos en nombres de archivo
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limitar longitud
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:250-len(ext)] + ext
        
        return filename
    
    @staticmethod
    def generate_hash(text: str) -> str:
        """Generar hash MD5 de un texto"""
        return hashlib.md5(text.encode()).hexdigest()

class SecurityUtils:
    """Utilidades para seguridad"""
    
    @staticmethod
    def is_safe_url(url: str) -> bool:
        """Verificar si una URL es segura"""
        # Lista de dominios conocidos como maliciosos (esto debería ser más completo)
        malicious_domains = [
            'malware.com',
            'phishing.com',
            # Agregar más dominios maliciosos conocidos
        ]
        
        domain = URLUtils.get_domain(url)
        return domain.lower() not in malicious_domains
    
    @staticmethod
    def sanitize_html(html: str) -> str:
        """Sanitizar HTML básico"""
        # Eliminar scripts y elementos potencialmente peligrosos
        dangerous_tags = ['script', 'object', 'embed', 'iframe']
        for tag in dangerous_tags:
            html = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', html, flags=re.IGNORECASE | re.DOTALL)
        
        return html

class CookieUtils:
    """Utilidades para manejo de cookies"""
    
    @staticmethod
    def parse_cookie_string(cookie_string: str) -> Dict[str, str]:
        """Parsear string de cookie"""
        cookies = {}
        if cookie_string:
            for cookie in cookie_string.split(';'):
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    cookies[name.strip()] = value.strip()
        return cookies
    
    @staticmethod
    def format_cookie_string(cookies: Dict[str, str]) -> str:
        """Formatear cookies como string"""
        return '; '.join([f"{name}={value}" for name, value in cookies.items()])
    
    @staticmethod
    def is_cookie_expired(expires: str) -> bool:
        """Verificar si una cookie ha expirado"""
        if not expires:
            return False
        
        try:
            # Parsear fecha de expiración (formato RFC 2822)
            from email.utils import parsedate_to_datetime
            expire_date = parsedate_to_datetime(expires)
            return datetime.now() > expire_date
        except:
            return False

class HistoryUtils:
    """Utilidades para manejo de historial"""
    
    @staticmethod
    def extract_page_title(html: str) -> Optional[str]:
        """Extraer título de una página HTML"""
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()
            # Decodificar entidades HTML básicas
            title = title.replace('&amp;', '&')
            title = title.replace('&lt;', '<')
            title = title.replace('&gt;', '>')
            title = title.replace('&quot;', '"')
            title = title.replace('&#39;', "'")
            return title
        return None
    
    @staticmethod
    def group_history_by_date(history_entries: List[Dict]) -> Dict[str, List[Dict]]:
        """Agrupar historial por fecha"""
        grouped = {}
        
        for entry in history_entries:
            # Parsear fecha
            visit_time = entry.get('visit_time', '')
            if isinstance(visit_time, str):
                try:
                    dt = datetime.fromisoformat(visit_time.replace('Z', '+00:00'))
                except:
                    dt = datetime.now()
            else:
                dt = visit_time
            
            date_key = dt.strftime('%Y-%m-%d')
            
            if date_key not in grouped:
                grouped[date_key] = []
            
            grouped[date_key].append(entry)
        
        return grouped
    
    @staticmethod
    def search_history_entries(entries: List[Dict], query: str) -> List[Dict]:
        """Buscar en entradas de historial"""
        if not query:
            return entries
        
        query = query.lower()
        results = []
        
        for entry in entries:
            url = entry.get('url', '').lower()
            title = entry.get('title', '').lower()
            
            if query in url or query in title:
                results.append(entry)
        
        return results

class FileUtils:
    """Utilidades para manejo de archivos"""
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Asegurar que un directorio existe"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except:
            return False
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Obtener extensión de archivo"""
        return os.path.splitext(filename)[1].lower()
    
    @staticmethod
    def is_image_file(filename: str) -> bool:
        """Verificar si es un archivo de imagen"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
        return FileUtils.get_file_extension(filename) in image_extensions
    
    @staticmethod
    def is_video_file(filename: str) -> bool:
        """Verificar si es un archivo de video"""
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        return FileUtils.get_file_extension(filename) in video_extensions
    
    @staticmethod
    def read_json_file(filepath: str) -> Optional[Dict]:
        """Leer archivo JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    @staticmethod
    def write_json_file(filepath: str, data: Dict) -> bool:
        """Escribir archivo JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False

class ValidationUtils:
    """Utilidades para validación"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validar dirección de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_port(port: str) -> bool:
        """Validar número de puerto"""
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except:
            return False
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """Validar dirección IP"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            for part in parts:
                if not (0 <= int(part) <= 255):
                    return False
            
            return True
        except:
            return False

class NetworkUtils:
    """Utilidades para red"""
    
    @staticmethod
    def get_user_agent() -> str:
        """Obtener User Agent personalizado"""
        return "PyWebBrowser/1.0 (Linux; Python; QtWebEngine)"
    
    @staticmethod
    def get_default_headers() -> Dict[str, str]:
        """Obtener headers por defecto"""
        return {
            'User-Agent': NetworkUtils.get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    @staticmethod
    def extract_links_from_html(html: str, base_url: str = '') -> List[str]:
        """Extraer links de HTML"""
        links = []
        
        # Buscar tags <a> con href
        link_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(link_pattern, html, re.IGNORECASE)
        
        for match in matches:
            if base_url and not match.startswith(('http://', 'https://')):
                # Convertir a URL absoluta
                link = urljoin(base_url, match)
            else:
                link = match
            
            if link not in links:
                links.append(link)
        
        return links

# Funciones de conveniencia
def format_url(url: str) -> str:
    """Formatear URL para mostrar"""
    return URLUtils.normalize_url(url)

def is_secure_connection(url: str) -> bool:
    """Verificar si la conexión es segura"""
    return URLUtils.is_secure(url)

def extract_domain(url: str) -> str:
    """Extraer dominio de URL"""
    return URLUtils.get_domain(url)

def format_timestamp(timestamp: str) -> str:
    """Formatear timestamp"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return DataUtils.format_datetime(dt)
    except:
        return timestamp
