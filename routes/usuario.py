import os 
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity

import datetime
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
    cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
    user = cursor.fetchone()
    if user and bcrypt.check_password_hash(user[3], contraseña):
        expires = datetime.timedelta(minutes=60)
        access_token = create_access_token(identity=str(user[0]), expires_delta=expires)
        return jsonify({
            'access_token': access_token
        }), 200
    else:
        return jsonify({
            'message': 'Credenciales incorrectas'
        }), 401
  


@usuario_bp.route('/datos', methods=['GET'])
@jwt_required()
def datos():
    current_user = get_jwt_identity()
    cursor, connection = get_db_connection()
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (current_user,))
    user = cursor.fetchone()
    return jsonify({
        'message': 'Datos del usuario',
        'user': user
    }), 200