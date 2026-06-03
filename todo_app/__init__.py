"""
Package initialization for the To-Do List application.

Este módulo configura la aplicación Flask, registra blueprints
e inicializa las estructuras de datos necesarias para el almacenamiento
en memoria de las tareas.
"""

from flask import Flask


# Almacenamiento global en memoria para las tareas
# Estructura: {id: {'id': int, 'titulo': str, 'completada': bool}}
tasks_db = {}
task_counter = [1]  # Usando lista para poder mutarla en funciones


def create_app():
    """
    Factory function para crear y configurar la aplicación Flask.
    
    Returns:
        Flask: Aplicación configurada con blueprints registrados
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Importar y registrar el blueprint de tareas
    from .routes import tareas_bp
    app.register_blueprint(tareas_bp, url_prefix='/')
    
    return app
