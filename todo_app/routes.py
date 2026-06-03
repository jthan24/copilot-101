"""
Blueprint de Rutas para la aplicación To-Do List.

ARQUITECTURA:
- Uso de Blueprints para separar la lógica de rutas del punto de entrada
- Las operaciones CRUD se realizan sobre la estructura de datos global 'tasks_db'
- Renderizado de plantillas HTML con Jinja2
- Redirecciones después de operaciones de modificación (Add, Toggle, Delete)

ALMACENAMIENTO:
- tasks_db: Diccionario global que almacena las tareas en memoria
- Estructura: {id: {'id': int, 'titulo': str, 'completada': bool}}
- task_counter: Contador global para generar IDs únicos
"""

from flask import Blueprint, render_template, request, redirect, url_for
from . import tasks_db, task_counter

tareas_bp = Blueprint('tareas', __name__)


# ============================================================================
# RUTAS CRUD PARA LA APLICACIÓN TO-DO LIST
# ============================================================================

@tareas_bp.route('/', methods=['GET'])
def obtener_todas_las_tareas():
    """
    GET / - Mostrar todas las tareas
    
    DESCRIPCIÓN:
        Renderiza la plantilla 'index.html' con todas las tareas almacenadas.
        Las tareas se ordenan por ID para mantener el orden de inserción.
    
    RETORNA:
        - Plantilla HTML con lista de tareas
    """
    # Ordenar tareas por ID
    tareas_ordenadas = sorted(tasks_db.values(), key=lambda t: t['id'])
    return render_template('index.html', tareas=tareas_ordenadas)


@tareas_bp.route('/add', methods=['POST'])
def crear_nueva_tarea():
    """
    POST /add - Crear una nueva tarea
    
    DESCRIPCIÓN:
        Recibe datos del formulario con el título de la tarea, la almacena
        en memory y redirige a la vista principal.
    
    DATOS DEL FORMULARIO ESPERADOS:
        - titulo: string (requerido, no vacío)
    
    COMPORTAMIENTO:
        - Si el título es válido: crea la tarea y redirige a '/'
        - Si el título es inválido: redirige a '/' (se puede mejorar con mensajes flash)
    
    CÓDIGOS HTTP:
        - 302/303: Redirect a la vista principal
    """
    titulo = request.form.get('titulo', '').strip()
    
    # Validación: el título no debe estar vacío
    if not titulo:
        return redirect(url_for('tareas.obtener_todas_las_tareas'))
    
    # Generar nuevo ID
    nuevo_id = task_counter[0]
    task_counter[0] += 1
    
    # Crear tarea
    nueva_tarea = {
        'id': nuevo_id,
        'titulo': titulo,
        'completada': False
    }
    
    # Almacenar en la base de datos
    tasks_db[nuevo_id] = nueva_tarea
    
    # Redirigir a la vista principal
    return redirect(url_for('tareas.obtener_todas_las_tareas'))


@tareas_bp.route('/toggle/<int:id>', methods=['POST'])
def marcar_tarea_completada(id):
    """
    POST /toggle/<int:id> - Marcar una tarea como completada/incompleta
    
    DESCRIPCIÓN:
        Cambia el estado 'completada' de una tarea existente.
        Si completada es False, la cambia a True y viceversa.
    
    PARÁMETRO:
        - id (int): ID de la tarea a actualizar
    
    COMPORTAMIENTO:
        - Si la tarea existe: alterna su estado y redirige a '/'
        - Si la tarea no existe: redirige a '/' (sin cambios)
    
    CÓDIGOS HTTP:
        - 302/303: Redirect a la vista principal
        - 404: Implícito si la tarea no existe (se redirige de todas formas)
    """
    if id in tasks_db:
        # Cambiar el estado de completada
        tasks_db[id]['completada'] = not tasks_db[id]['completada']
    
    # Redirigir a la vista principal
    return redirect(url_for('tareas.obtener_todas_las_tareas'))


@tareas_bp.route('/delete/<int:id>', methods=['POST'])
def eliminar_tarea(id):
    """
    POST /delete/<int:id> - Eliminar una tarea
    
    DESCRIPCIÓN:
        Elimina una tarea existente de la estructura de datos y redirige
        a la vista principal.
    
    PARÁMETRO:
        - id (int): ID de la tarea a eliminar
    
    COMPORTAMIENTO:
        - Si la tarea existe: la elimina y redirige a '/'
        - Si la tarea no existe: redirige a '/' (sin cambios)
    
    CÓDIGOS HTTP:
        - 302/303: Redirect a la vista principal
    """
    if id in tasks_db:
        # Eliminar la tarea
        del tasks_db[id]
    
    # Redirigir a la vista principal
    return redirect(url_for('tareas.obtener_todas_las_tareas'))
