"""
Entry point for the To-Do List Flask application.

Este archivo sirve como punto de entrada principal de la aplicación.
Importa la aplicación configurada desde el paquete 'todo_app'
y la ejecuta en modo desarrollo.
"""

from todo_app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='localhost', port=5000)
