from flask import Blueprint, request, jsonify
from config.db import get_db_connection

#Crear un blueprint 
tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/', methods=['GET'])
def get_tareas():
    return jsonify({
        'message': 'Tareas obtenidas correctamente',
    })




@tareas_bp.route('/create', methods=['POST'])
def create_tarea():
    data = request.json

    descripcion = data.get('descripcion')

    if not descripcion:
        return jsonify({
            'message': 'La descripcion es requerida'
        }), 400
    
    cursor, connection = get_db_connection()

    try:
        cursor.execute('INSERT INTO tareas (descripcion) VALUES (%s)', (descripcion,))
        connection.commit()  # ¡IMPORTANTE! Hacer commit de la transacción
        return jsonify({
            'message': f"Tarea creada!"
        }), 201
    except Exception as e:
        connection.rollback()  # Rollback en caso de error
        return jsonify({
            'message': f"Error al crear la tarea: {e}"
        }), 500
    finally:
        cursor.close()




@tareas_bp.route('/update/<int:id>', methods=['PUT'])
def update_tarea(id):
    data = request.json
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    return jsonify({
        'message': f"User con id {id} actualizado: {nombre} {apellido}!",
    })





