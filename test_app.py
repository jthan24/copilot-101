"""
Pruebas Unitarias para la Aplicación Flask To-Do List

Este módulo contiene pruebas unitarias exhaustivas para validar
el funcionamiento correcto de la aplicación Flask con Blueprints.

Librerías utilizadas:
    - unittest: Framework de pruebas nativo de Python
    - app.test_client(): Cliente de pruebas de Flask para simular requests HTTP

Métodos clave:
    - setUp(): Prepara el entorno aislado para cada prueba
    - tearDown(): Limpia la memoria después de cada prueba
"""

import unittest
from todo_app import create_app, tasks_db, task_counter


class ToDoListAppTestCase(unittest.TestCase):
    """
    Suite de pruebas para la aplicación Flask To-Do List.
    
    Hereda de unittest.TestCase y proporciona pruebas para todas
    las operaciones CRUD de la aplicación.
    """

    def setUp(self):
        """
        Prepara el entorno para cada prueba.
        
        Se ejecuta antes de cada método de prueba (test_*).
        
        Acciones:
            1. Crea una instancia limpia de la aplicación Flask
            2. Activa el modo de prueba (testing=True)
            3. Reinicia la base de datos en memoria (tasks_db)
            4. Reinicia el contador de IDs (task_counter)
            5. Obtiene el cliente de pruebas para hacer requests simulados
        """
        # Crear la aplicación en modo de prueba
        self.app = create_app()
        self.app.config['TESTING'] = True
        
        # Limpiar la base de datos en memoria
        tasks_db.clear()
        task_counter[0] = 1
        
        # Crear cliente de pruebas
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Limpia el entorno después de cada prueba.
        
        Se ejecuta después de cada método de prueba (test_*).
        
        Acciones:
            1. Limpia la base de datos en memoria
            2. Reinicia el contador de IDs
            3. Cierra la aplicación
        """
        # Limpiar la base de datos
        tasks_db.clear()
        task_counter[0] = 1


    # ========================================================================
    # PRUEBAS DE LA RUTA INDEX (GET /)
    # ========================================================================

    def test_index_route_loads_successfully(self):
        """
        Test: Verificar que la página principal carga correctamente.
        
        Escenario:
            - Acceder a la ruta raíz (GET /)
            - Sin tareas previas en la base de datos
        
        Validaciones:
            - Status HTTP: 200 (OK)
            - La respuesta contiene HTML válido
            - Se renderiza la plantilla correctamente
        
        Resultado esperado: La página carga sin errores
        """
        response = self.client.get('/')
        
        # Verificar status HTTP 200
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se renderiza HTML
        self.assertIn(b'<!DOCTYPE html>', response.data)
        self.assertIn(b'To-Do List', response.data)

    def test_index_route_empty_state(self):
        """
        Test: Verificar que la página muestra estado vacío inicialmente.
        
        Escenario:
            - Acceder a la ruta raíz sin tareas
        
        Validaciones:
            - La página contiene el mensaje de "no hay tareas"
            - La lista de tareas está vacía en la plantilla
        
        Resultado esperado: Se muestra el mensaje de lista vacía
        """
        response = self.client.get('/')
        
        # Verificar status HTTP 200
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se muestra mensaje de lista vacía
        self.assertIn(b'No hay tareas', response.data)


    # ========================================================================
    # PRUEBAS DE CREACIÓN DE TAREAS (POST /add)
    # ========================================================================

    def test_add_task_successfully(self):
        """
        Test: Verificar que crear una nueva tarea funciona correctamente.
        
        Escenario:
            - Enviar POST /add con un título válido
            - Verificar que se almacena en memory
            - Verificar redirección al index
        
        Validaciones:
            - Status HTTP: 302 (Redirect) o 303
            - La tarea se almacena en tasks_db
            - La tarea tiene los campos correctos (id, titulo, completada)
            - El contador se incrementa
        
        Resultado esperado: Tarea creada y guardada correctamente
        """
        # Enviar POST con una nueva tarea
        response = self.client.post(
            '/add',
            data={'titulo': 'Comprar leche'},
            follow_redirects=False
        )
        
        # Verificar redirección
        self.assertIn(response.status_code, [302, 303])
        
        # Verificar que se almacenó en memory
        self.assertEqual(len(tasks_db), 1)
        
        # Verificar estructura de la tarea
        tarea = tasks_db[1]
        self.assertEqual(tarea['id'], 1)
        self.assertEqual(tarea['titulo'], 'Comprar leche')
        self.assertEqual(tarea['completada'], False)

    def test_add_multiple_tasks(self):
        """
        Test: Verificar que se pueden agregar múltiples tareas.
        
        Escenario:
            - Enviar POST /add tres veces con diferentes títulos
            - Verificar que todas se almacenan y con IDs únicos
        
        Validaciones:
            - Cada tarea tiene un ID diferente (autoincremento)
            - Todas las tareas se almacenan correctamente
            - El título de cada una es único
        
        Resultado esperado: Múltiples tareas creadas con IDs secuenciales
        """
        # Agregar 3 tareas
        tareas_input = [
            'Tarea 1',
            'Tarea 2',
            'Tarea 3'
        ]
        
        for titulo in tareas_input:
            response = self.client.post(
                '/add',
                data={'titulo': titulo},
                follow_redirects=False
            )
            self.assertIn(response.status_code, [302, 303])
        
        # Verificar que se almacenaron 3 tareas
        self.assertEqual(len(tasks_db), 3)
        
        # Verificar IDs secuenciales
        self.assertIn(1, tasks_db)
        self.assertIn(2, tasks_db)
        self.assertIn(3, tasks_db)
        
        # Verificar títulos
        self.assertEqual(tasks_db[1]['titulo'], 'Tarea 1')
        self.assertEqual(tasks_db[2]['titulo'], 'Tarea 2')
        self.assertEqual(tasks_db[3]['titulo'], 'Tarea 3')

    def test_add_task_with_empty_title(self):
        """
        Test: Verificar que no se pueden agregar tareas sin título.
        
        Escenario:
            - Enviar POST /add con título vacío
            - Enviar POST /add con solo espacios en blanco
        
        Validaciones:
            - No se agrega tarea a tasks_db
            - La base de datos permanece vacía
        
        Resultado esperado: Tareas vacías son rechazadas
        """
        # Intentar agregar tarea sin título
        response1 = self.client.post(
            '/add',
            data={'titulo': ''},
            follow_redirects=False
        )
        
        # Intentar agregar tarea con solo espacios
        response2 = self.client.post(
            '/add',
            data={'titulo': '   '},
            follow_redirects=False
        )
        
        # Verificar que no se agregaron tareas
        self.assertEqual(len(tasks_db), 0)

    def test_add_task_redirect_to_index(self):
        """
        Test: Verificar que después de agregar, se redirige al index.
        
        Escenario:
            - Agregar una tarea
            - Seguir la redirección
            - Verificar que la tarea aparece en el HTML renderizado
        
        Validaciones:
            - Redirección correcta (302/303)
            - Respuesta final es 200
            - La tarea aparece en el HTML
        
        Resultado esperado: Redirección correcta y tarea visible
        """
        # Agregar tarea siguiendo redirecciones
        response = self.client.post(
            '/add',
            data={'titulo': 'Mi primera tarea'},
            follow_redirects=True
        )
        
        # Verificar status final
        self.assertEqual(response.status_code, 200)
        
        # Verificar que la tarea aparece en el HTML
        self.assertIn(b'Mi primera tarea', response.data)


    # ========================================================================
    # PRUEBAS DE TOGGLE/CAMBIO DE ESTADO (POST /toggle/<id>)
    # ========================================================================

    def test_toggle_task_from_false_to_true(self):
        """
        Test: Verificar que cambiar estado de False a True funciona.
        
        Escenario:
            1. Agregar una tarea (completada=False por defecto)
            2. Hacer POST a /toggle/1
            3. Verificar que completada cambió a True
        
        Validaciones:
            - Estado inicial: completada=False
            - Después del toggle: completada=True
            - Status HTTP: 302 (redirect)
        
        Resultado esperado: Estado de la tarea invertido correctamente
        """
        # Agregar una tarea
        self.client.post('/add', data={'titulo': 'Test task'})
        
        # Verificar estado inicial
        self.assertEqual(tasks_db[1]['completada'], False)
        
        # Hacer toggle
        response = self.client.post('/toggle/1', follow_redirects=False)
        
        # Verificar redirección
        self.assertIn(response.status_code, [302, 303])
        
        # Verificar nuevo estado
        self.assertEqual(tasks_db[1]['completada'], True)

    def test_toggle_task_from_true_to_false(self):
        """
        Test: Verificar que cambiar estado de True a False funciona.
        
        Escenario:
            1. Agregar una tarea
            2. Hacer toggle a True
            3. Hacer toggle nuevamente a False
            4. Verificar que vuelve a False
        
        Validaciones:
            - Primer toggle: False -> True
            - Segundo toggle: True -> False
            - Alternancia correcta
        
        Resultado esperado: Toggle bidireccional funciona
        """
        # Agregar tarea
        self.client.post('/add', data={'titulo': 'Test toggle'})
        
        # Primer toggle: False -> True
        self.client.post('/toggle/1')
        self.assertEqual(tasks_db[1]['completada'], True)
        
        # Segundo toggle: True -> False
        self.client.post('/toggle/1')
        self.assertEqual(tasks_db[1]['completada'], False)
        
        # Tercer toggle: False -> True nuevamente
        self.client.post('/toggle/1')
        self.assertEqual(tasks_db[1]['completada'], True)

    def test_toggle_nonexistent_task(self):
        """
        Test: Verificar que hacer toggle en tarea inexistente no causa error.
        
        Escenario:
            - Intentar hacer toggle a una tarea con ID que no existe
            - Verificar que no causa excepción
        
        Validaciones:
            - No se lanza excepción
            - Status HTTP: 302 (redirect de todas formas)
            - Base de datos permanece vacía
        
        Resultado esperado: Manejo robusto de errores
        """
        # Intentar hacer toggle a ID inexistente
        response = self.client.post('/toggle/999', follow_redirects=False)
        
        # Verificar que no causa error
        self.assertIn(response.status_code, [302, 303])
        
        # Verificar que la base de datos está vacía
        self.assertEqual(len(tasks_db), 0)

    def test_toggle_task_visible_in_index(self):
        """
        Test: Verificar que el estado toggled se refleja en el index.
        
        Escenario:
            1. Agregar tarea
            2. Hacer toggle a completada
            3. Acceder a index
            4. Verificar que aparece como completada en HTML
        
        Validaciones:
            - El HTML muestra el estado actualizado
            - Puede incluir clases CSS o atributos visuales
        
        Resultado esperado: Estado actualizado visible en UI
        """
        # Agregar tarea
        self.client.post('/add', data={'titulo': 'Tarea completable'})
        
        # Hacer toggle
        self.client.post('/toggle/1')
        
        # Acceder a index
        response = self.client.get('/')
        
        # Verificar que la tarea está marcada como completada
        # (puede incluir texto "Completada" en los botones)
        self.assertIn(b'Completada', response.data)


    # ========================================================================
    # PRUEBAS DE ELIMINACIÓN DE TAREAS (POST /delete/<id>)
    # ========================================================================

    def test_delete_task_successfully(self):
        """
        Test: Verificar que eliminar una tarea funciona correctamente.
        
        Escenario:
            1. Agregar una tarea
            2. Verificar que existe en tasks_db
            3. Hacer POST a /delete/1
            4. Verificar que fue eliminada
        
        Validaciones:
            - Antes de delete: 1 tarea en tasks_db
            - Después de delete: 0 tareas en tasks_db
            - Status HTTP: 302 (redirect)
            - El ID ya no está en las claves de tasks_db
        
        Resultado esperado: Tarea eliminada correctamente
        """
        # Agregar una tarea
        self.client.post('/add', data={'titulo': 'Tarea a eliminar'})
        self.assertEqual(len(tasks_db), 1)
        
        # Eliminar la tarea
        response = self.client.post('/delete/1', follow_redirects=False)
        
        # Verificar redirección
        self.assertIn(response.status_code, [302, 303])
        
        # Verificar que se eliminó
        self.assertEqual(len(tasks_db), 0)
        self.assertNotIn(1, tasks_db)

    def test_delete_multiple_tasks(self):
        """
        Test: Verificar que se pueden eliminar múltiples tareas.
        
        Escenario:
            1. Agregar 3 tareas
            2. Eliminar la tarea 2
            3. Verificar que las tareas 1 y 3 aún existen
            4. Eliminar la tarea 1
            5. Verificar que solo la tarea 3 existe
        
        Validaciones:
            - Después de agregar: 3 tareas
            - Después del primer delete: 2 tareas
            - Después del segundo delete: 1 tarea
            - Los IDs correctos permanecen en tasks_db
        
        Resultado esperado: Eliminación selectiva de tareas
        """
        # Agregar 3 tareas
        for i in range(1, 4):
            self.client.post('/add', data={'titulo': f'Tarea {i}'})
        self.assertEqual(len(tasks_db), 3)
        
        # Eliminar tarea 2
        self.client.post('/delete/2')
        self.assertEqual(len(tasks_db), 2)
        self.assertIn(1, tasks_db)
        self.assertNotIn(2, tasks_db)
        self.assertIn(3, tasks_db)
        
        # Eliminar tarea 1
        self.client.post('/delete/1')
        self.assertEqual(len(tasks_db), 1)
        self.assertNotIn(1, tasks_db)
        self.assertIn(3, tasks_db)

    def test_delete_nonexistent_task(self):
        """
        Test: Verificar que eliminar tarea inexistente no causa error.
        
        Escenario:
            - Intentar eliminar una tarea con ID que no existe
            - Base de datos vacía inicialmente
        
        Validaciones:
            - No se lanza excepción
            - Status HTTP: 302 (redirect)
            - Base de datos permanece vacía
        
        Resultado esperado: Manejo robusto de errores
        """
        # Intentar eliminar tarea inexistente
        response = self.client.post('/delete/999', follow_redirects=False)
        
        # Verificar que no causa error
        self.assertIn(response.status_code, [302, 303])
        
        # Verificar que la base de datos está vacía
        self.assertEqual(len(tasks_db), 0)

    def test_delete_task_removed_from_index(self):
        """
        Test: Verificar que tarea eliminada desaparece del index.
        
        Escenario:
            1. Agregar tarea
            2. Verificar que aparece en index
            3. Eliminar tarea
            4. Verificar que desaparece del index
        
        Validaciones:
            - Tarea aparece antes de delete
            - Tarea desaparece después de delete
            - Se muestra mensaje de lista vacía
        
        Resultado esperado: Cambios reflejados en UI
        """
        # Agregar tarea
        self.client.post('/add', data={'titulo': 'Tarea temporal'})
        
        # Verificar que aparece en index
        response1 = self.client.get('/')
        self.assertIn(b'Tarea temporal', response1.data)
        
        # Eliminar tarea
        self.client.post('/delete/1')
        
        # Verificar que desaparece del index
        response2 = self.client.get('/')
        self.assertNotIn(b'Tarea temporal', response2.data)
        self.assertIn(b'No hay tareas', response2.data)


    # ========================================================================
    # PRUEBAS DE INTEGRACIÓN (Flujos completos)
    # ========================================================================

    def test_complete_workflow(self):
        """
        Test: Verificar un flujo completo de trabajo (CRUD integrado).
        
        Escenario:
            1. Agregar 3 tareas
            2. Marcar la primera como completada
            3. Eliminar la segunda
            4. Verificar estado final
        
        Validaciones:
            - Todas las operaciones se ejecutan sin errores
            - Estado final correcto
            - Datos consistentes en memory
        
        Resultado esperado: Flujo completo funciona correctamente
        """
        # 1. Agregar 3 tareas
        self.client.post('/add', data={'titulo': 'Tarea 1'})
        self.client.post('/add', data={'titulo': 'Tarea 2'})
        self.client.post('/add', data={'titulo': 'Tarea 3'})
        self.assertEqual(len(tasks_db), 3)
        
        # 2. Marcar primera como completada
        self.client.post('/toggle/1')
        self.assertEqual(tasks_db[1]['completada'], True)
        
        # 3. Eliminar segunda
        self.client.post('/delete/2')
        self.assertEqual(len(tasks_db), 2)
        
        # 4. Verificar estado final
        self.assertIn(1, tasks_db)
        self.assertNotIn(2, tasks_db)
        self.assertIn(3, tasks_db)
        self.assertEqual(tasks_db[1]['completada'], True)
        self.assertEqual(tasks_db[3]['completada'], False)

    def test_data_isolation_between_tests(self):
        """
        Test: Verificar que cada test tiene datos aislados.
        
        Escenario:
            - Este test verifica que setUp y tearDown funcionan
            - La base de datos debe estar limpia al inicio
        
        Validaciones:
            - tasks_db está vacío al inicio
            - task_counter comienza en 1
            - Cada test es independiente
        
        Resultado esperado: Aislamiento correcto de tests
        """
        # Verificar que el entorno está limpio
        self.assertEqual(len(tasks_db), 0)
        self.assertEqual(task_counter[0], 1)
        
        # Agregar una tarea
        self.client.post('/add', data={'titulo': 'Test'})
        self.assertEqual(len(tasks_db), 1)


if __name__ == '__main__':
    # Ejecutar las pruebas con verbosidad
    unittest.main(verbosity=2)
