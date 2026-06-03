"""
Blueprint de Rutas para la aplicación To-Do List.

ARQUITECTURA:
- Uso de Blueprints para separar la lógica de rutas del punto de entrada
- Las operaciones CRUD se realizan sobre la estructura de datos global 'tasks_db'
- Respuestas JSON para facilitar integración con frontend
- Validación básica de entrada de datos

ALMACENAMIENTO:
- tasks_db: Diccionario global que almacena las tareas en memoria
- Estructura: {id: {'id': int, 'titulo': str, 'completada': bool}}
- task_counter: Contador global para generar IDs únicos
"""

from flask import Blueprint, jsonify, request

tareas_bp = Blueprint('tareas', __name__)


# ============================================================================
# RUTAS CRUD PARA LA APLICACIÓN TO-DO LIST
# ============================================================================

@tareas_bp.route('/', methods=['GET'])
def obtener_todas_las_tareas():
    """
    GET / - Mostrar todas las tareas
    
    DESCRIPCIÓN:
        Retorna una lista JSON con todas las tareas almacenadas en memory.
    
    RESPUESTA ESPERADA:
        {
            "success": true,
            "data": [
                {"id": 1, "titulo": "Tarea 1", "completada": false},
                {"id": 2, "titulo": "Tarea 2", "completada": true}
            ]
        }
    
    CÓDIGOS HTTP:
        - 200: OK, retorna lista de tareas (puede estar vacía)
    """
    pass


@tareas_bp.route('/add', methods=['POST'])
def crear_nueva_tarea():
    """
    POST /add - Crear una nueva tarea
    
    DESCRIPCIÓN:
        Recibe datos JSON con el título de la tarea, la almacena
        en memory y retorna el objeto creado con su ID asignado.
    
    CUERPO DE SOLICITUD ESPERADO:
        {
            "titulo": "Mi nueva tarea"
        }
    
    RESPUESTA ESPERADA:
        {
            "success": true,
            "data": {
                "id": 1,
                "titulo": "Mi nueva tarea",
                "completada": false
            }
        }
    
    CÓDIGOS HTTP:
        - 201: Created, tarea creada exitosamente
        - 400: Bad Request, falta el campo 'titulo' o está vacío
    """
    pass


@tareas_bp.route('/toggle/<int:id>', methods=['POST'])
def marcar_tarea_completada(id):
    """
    POST /toggle/<int:id> - Marcar una tarea como completada/incompleta
    
    DESCRIPCIÓN:
        Cambia el estado 'completada' de una tarea existente.
        Si completada es False, la cambia a True y viceversa.
    
    PARÁMETRO:
        - id (int): ID de la tarea a actualizar
    
    RESPUESTA ESPERADA:
        {
            "success": true,
            "data": {
                "id": 1,
                "titulo": "Mi tarea",
                "completada": true
            }
        }
    
    CÓDIGOS HTTP:
        - 200: OK, estado actualizado
        - 404: Not Found, la tarea con ese ID no existe
    """
    pass


@tareas_bp.route('/delete/<int:id>', methods=['POST'])
def eliminar_tarea(id):
    """
    POST /delete/<int:id> - Eliminar una tarea
    
    DESCRIPCIÓN:
        Elimina una tarea existente de la estructura de datos.
    
    PARÁMETRO:
        - id (int): ID de la tarea a eliminar
    
    RESPUESTA ESPERADA:
        {
            "success": true,
            "message": "Tarea eliminada correctamente"
        }
    
    CÓDIGOS HTTP:
        - 200: OK, tarea eliminada
        - 404: Not Found, la tarea con ese ID no existe
    """
    pass
