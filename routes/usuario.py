import os 
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt

from config.db import get_db_connection
from flask_bcrypt import Bcrypt

load_dotenv()

usuario_bp = Blueprint('usuario', __name__)

bcrypt = Bcrypt()

@usuario_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.json

    nombre = data.get('nombre')
    email = data.get('email')
    contraseña = data.get('contraseña')

    if not nombre or not email or not contraseña:
        return jsonify({
            'message': 'Todos los campos son requeridos'
        }), 400
    
    cursor = None
    connection = None

    try:
        cursor, connection = get_db_connection()
        
        # Test connection before executing query
        if not connection or not cursor:
            return jsonify({
                'message': 'Error de conexión a la base de datos'
            }), 500
            
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({
                'message': 'El email ya está registrado'
            }), 400
        
        hashed_password = bcrypt.generate_password_hash(contraseña).decode('utf-8')
        cursor.execute("INSERT INTO usuarios (nombre, email, contraseña) VALUES (%s, %s, %s)", (nombre, email, hashed_password))
        connection.commit()
        return jsonify({
            'message': 'Usuario registrado correctamente'
        }), 201

    except Exception as e:
        print(f"Error en registrar: {e}")
        try:
            if connection:
                connection.rollback()
        except:
            pass
        return jsonify({
            'message': f'Error al registrar el usuario: {str(e)}'
        }), 500

    finally:
        # Safely close connections
        try:
            if cursor:
                cursor.close()
        except:
            pass
        try:
            if connection:
                connection.close()
        except:
            pass

@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    contraseña = data.get('contraseña')

    if not email or not contraseña:
        return jsonify({
            'message': 'Todos los campos son requeridos'
        }), 400

    cursor, connection = get_db_connection()
    try:
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({
                'message': 'Usuario no encontrado'
            }), 404
        
        if not bcrypt.check_password_hash(user[3], contraseña):
            return jsonify({
                'message': 'Contraseña incorrecta'
            }), 401
            
        access_token = create_access_token(identity=user[0])
        return jsonify({
            'message': 'Usuario logueado correctamente',
            'access_token': access_token,
            'user': {
                'id': user[0],
                'nombre': user[1],
                'email': user[2]
            }
        }), 200
        
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({
            'message': f'Error al loguear el usuario: {str(e)}'
        }), 500
    finally:
        cursor.close()
        connection.close()


    

