from flask import Blueprint, request, jsonify
from config.db import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

#Crear un blueprint 
tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/', methods=['GET'])
def get_tareas():
    return jsonify({
        'message': 'Tareas obtenidas correctamente',
    })




@tareas_bp.route('/create', methods=['POST'])
@jwt_required()
def create_tarea():
    data = request.json
    current_user_id = get_jwt_identity()

    descripcion = data.get('descripcion')

    if not descripcion:
        return jsonify({
            'message': 'La descripcion es requerida'
        }), 400
    
    cursor, connection = get_db_connection()

    try:
        # Obtener información del usuario
        cursor.execute('SELECT nombre FROM usuarios WHERE id = %s', (current_user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({
                'message': 'Usuario no encontrado'
            }), 404
        
        # Crear la tarea
        cursor.execute('INSERT INTO tareas (descripcion, user_id) VALUES (%s, %s)', (descripcion, current_user_id))
        connection.commit() 
        return jsonify({
            'message': f"Tarea creada para el usuario {user[0]}!"
        }), 201
    except Exception as e:
        connection.rollback() 
        return jsonify({
            'message': f"Error al crear la tarea: {e}"
        }), 500
    finally:
        cursor.close()




@tareas_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_tarea(id):
    data = request.json
    descripcion = data.get('descripcion')
    
    if not descripcion:
        return jsonify({
            'message': 'La descripcion es requerida'
        }), 400
    
    current_user_id = get_jwt_identity()
    cursor, connection = get_db_connection()
    
    try:
        query = 'SELECT * FROM tareas WHERE id = %s AND user_id = %s'
        cursor.execute(query, (id, current_user_id))
        tarea = cursor.fetchone()
        
        if not tarea:
            return jsonify({
                'message': f'Tarea con id {id} no encontrada o no pertenece al usuario'
            }), 404
        
        update_query = 'UPDATE tareas SET descripcion = %s WHERE id = %s AND user_id = %s'
        cursor.execute(update_query, (descripcion, id, current_user_id))
        connection.commit()
        
        return jsonify({
            'message': f'Tarea con id {id} actualizada correctamente'
        }), 200
        
    except Exception as e:
        connection.rollback()
        return jsonify({
            'message': f'Error al actualizar la tarea: {e}'
        }), 500
    finally:
        cursor.close()





@tareas_bp.route('/obtener', methods=['GET'])
@jwt_required()
def get_tareas_usuario():
    current_user_id = get_jwt_identity()
    cursor, connection = get_db_connection()
    query = 'SELECT * FROM tareas as a INNER JOIN usuarios as u ON a.user_id = u.id WHERE u.id = %s'
    cursor.execute(query, (current_user_id,))
    tareas = cursor.fetchall()

    if not list(tareas):
        return jsonify({
            'message': f"No se encontraron tareas para el usuario {current_user_id}",
        }), 404
    else:
        return jsonify({
            'message': f"Tareas obtenidas correctamente para el usuario {current_user_id}",
            'tareas': tareas
        }), 200
   


@tareas_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_tarea(id):
    current_user_id = get_jwt_identity()
    cursor, connection = get_db_connection()
    
    try:
        query = 'SELECT * FROM tareas WHERE id = %s AND user_id = %s'
        cursor.execute(query, (id, current_user_id))
        tarea = cursor.fetchone()
        
        if not tarea:
            return jsonify({
                'message': f'Tarea con id {id} no encontrada o no pertenece al usuario'
            }), 404
        
        # Eliminar la tarea
        delete_query = 'DELETE FROM tareas WHERE id = %s AND user_id = %s'
        cursor.execute(delete_query, (id, current_user_id))
        connection.commit()
        
        return jsonify({
            'message': f'Tarea con id {id} eliminada correctamente'
        }), 200
        
    except Exception as e:
        connection.rollback()
        return jsonify({
            'message': f'Error al eliminar la tarea: {e}'
        }), 500
    finally:
        cursor.close()





""" hacer crud de tareas 

con cada endpoint protegido 

solo el usuario puede acceder a las tareas


se hizo el obtener y modificar, se modifico el create

"""



