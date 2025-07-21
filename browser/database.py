"""
Gestor de Base de Datos para el navegador
Maneja historial, cookies y otras operaciones CRUD
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """Clase para manejar todas las operaciones de base de datos"""
    
    def __init__(self, data_dir: str):
        """
        Inicializar el gestor de base de datos
        
        Args:
            data_dir: Directorio donde se almacenarán los datos
        """
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "browser_data.db")
        
    def initialize_database(self):
        """Crear las tablas necesarias si no existen"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla para el historial
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    title TEXT,
                    visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    visit_count INTEGER DEFAULT 1,
                    is_favorite BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Tabla para cookies (respaldo)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cookies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain TEXT NOT NULL,
                    name TEXT NOT NULL,
                    value TEXT,
                    path TEXT DEFAULT '/',
                    expires TIMESTAMP,
                    secure BOOLEAN DEFAULT FALSE,
                    http_only BOOLEAN DEFAULT FALSE,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla para configuraciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Índices para mejorar el rendimiento
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_url ON history(url)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_time ON history(visit_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_cookies_domain ON cookies(domain)')
            
            conn.commit()
    
    def add_history_entry(self, url: str, title: str = None) -> bool:
        """
        Agregar una entrada al historial
        
        Args:
            url: URL visitada
            title: Título de la página
            
        Returns:
            True si se agregó correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar si la URL ya existe
                cursor.execute('SELECT id, visit_count FROM history WHERE url = ?', (url,))
                existing = cursor.fetchone()
                
                if existing:
                    # Actualizar contador de visitas y tiempo
                    cursor.execute('''
                        UPDATE history 
                        SET visit_count = visit_count + 1, 
                            visit_time = CURRENT_TIMESTAMP,
                            title = COALESCE(?, title)
                        WHERE id = ?
                    ''', (title, existing[0]))
                else:
                    # Insertar nueva entrada
                    cursor.execute('''
                        INSERT INTO history (url, title) 
                        VALUES (?, ?)
                    ''', (url, title))
                
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error al agregar al historial: {e}")
            return False
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """
        Obtener el historial de navegación
        
        Args:
            limit: Número máximo de entradas a devolver
            
        Returns:
            Lista de diccionarios con datos del historial
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, url, title, visit_time, visit_count, is_favorite
                    FROM history 
                    ORDER BY visit_time DESC 
                    LIMIT ?
                ''', (limit,))
                
                columns = ['id', 'url', 'title', 'visit_time', 'visit_count', 'is_favorite']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al obtener historial: {e}")
            return []
    
    def search_history(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Buscar en el historial
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de entradas que coinciden con la búsqueda
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                search_term = f"%{query}%"
                cursor.execute('''
                    SELECT id, url, title, visit_time, visit_count, is_favorite
                    FROM history 
                    WHERE url LIKE ? OR title LIKE ?
                    ORDER BY visit_count DESC, visit_time DESC
                    LIMIT ?
                ''', (search_term, search_term, limit))
                
                columns = ['id', 'url', 'title', 'visit_time', 'visit_count', 'is_favorite']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al buscar en historial: {e}")
            return []
    
    def delete_history_entry(self, entry_id: int) -> bool:
        """
        Eliminar una entrada del historial
        
        Args:
            entry_id: ID de la entrada a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM history WHERE id = ?', (entry_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar entrada del historial: {e}")
            return False
    
    def clear_history(self, days: int = None) -> bool:
        """
        Limpiar el historial
        
        Args:
            days: Si se especifica, eliminar entradas más antiguas que X días
            
        Returns:
            True si se limpió correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if days is not None:
                    cursor.execute('''
                        DELETE FROM history 
                        WHERE visit_time < datetime('now', '-{} days')
                    '''.format(days))
                else:
                    cursor.execute('DELETE FROM history')
                
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error al limpiar historial: {e}")
            return False
    
    def toggle_favorite(self, entry_id: int) -> bool:
        """
        Alternar el estado de favorito de una entrada
        
        Args:
            entry_id: ID de la entrada
            
        Returns:
            True si se actualizó correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE history 
                    SET is_favorite = NOT is_favorite 
                    WHERE id = ?
                ''', (entry_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar favorito: {e}")
            return False
    
    def get_favorites(self) -> List[Dict]:
        """
        Obtener todas las páginas marcadas como favoritas
        
        Returns:
            Lista de favoritos
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, url, title, visit_time, visit_count
                    FROM history 
                    WHERE is_favorite = TRUE
                    ORDER BY title ASC
                ''')
                
                columns = ['id', 'url', 'title', 'visit_time', 'visit_count']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al obtener favoritos: {e}")
            return []
    
    def add_cookie(self, domain: str, name: str, value: str, path: str = '/', 
                   expires: datetime = None, secure: bool = False, 
                   http_only: bool = False) -> bool:
        """
        Agregar una cookie a la base de datos
        
        Args:
            domain: Dominio de la cookie
            name: Nombre de la cookie
            value: Valor de la cookie
            path: Ruta de la cookie
            expires: Fecha de expiración
            secure: Si la cookie es segura
            http_only: Si la cookie es solo HTTP
            
        Returns:
            True si se agregó correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Eliminar cookie existente con el mismo dominio, nombre y ruta
                cursor.execute('''
                    DELETE FROM cookies 
                    WHERE domain = ? AND name = ? AND path = ?
                ''', (domain, name, path))
                
                # Insertar nueva cookie
                cursor.execute('''
                    INSERT INTO cookies (domain, name, value, path, expires, secure, http_only)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (domain, name, value, path, expires, secure, http_only))
                
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error al agregar cookie: {e}")
            return False
    
    def get_cookies(self, domain: str = None) -> List[Dict]:
        """
        Obtener cookies de la base de datos
        
        Args:
            domain: Si se especifica, solo cookies de este dominio
            
        Returns:
            Lista de cookies
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if domain:
                    cursor.execute('''
                        SELECT domain, name, value, path, expires, secure, http_only
                        FROM cookies 
                        WHERE domain = ?
                        ORDER BY name ASC
                    ''', (domain,))
                else:
                    cursor.execute('''
                        SELECT domain, name, value, path, expires, secure, http_only
                        FROM cookies 
                        ORDER BY domain ASC, name ASC
                    ''')
                
                columns = ['domain', 'name', 'value', 'path', 'expires', 'secure', 'http_only']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al obtener cookies: {e}")
            return []
    
    def delete_cookies(self, domain: str = None) -> bool:
        """
        Eliminar cookies
        
        Args:
            domain: Si se especifica, solo eliminar cookies de este dominio
            
        Returns:
            True si se eliminaron correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if domain:
                    cursor.execute('DELETE FROM cookies WHERE domain = ?', (domain,))
                else:
                    cursor.execute('DELETE FROM cookies')
                
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error al eliminar cookies: {e}")
            return False
    
    def save_setting(self, key: str, value: str) -> bool:
        """
        Guardar una configuración
        
        Args:
            key: Clave de la configuración
            value: Valor de la configuración
            
        Returns:
            True si se guardó correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO settings (key, value)
                    VALUES (?, ?)
                ''', (key, value))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    def get_setting(self, key: str, default_value: str = None) -> str:
        """
        Obtener una configuración
        
        Args:
            key: Clave de la configuración
            default_value: Valor por defecto si no existe
            
        Returns:
            Valor de la configuración
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
                result = cursor.fetchone()
                return result[0] if result else default_value
        except sqlite3.Error as e:
            print(f"Error al obtener configuración: {e}")
            return default_value
