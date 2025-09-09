from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
import os
from routes.tareas import tareas_bp
from config.db import init_db, mysql
from routes.usuario import usuario_bp


def create_app():
    app = Flask(__name__)
    

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    

    jwt = JWTManager(app)
    

    init_db(app)
 
    app.register_blueprint(tareas_bp, url_prefix='/tareas')
    app.register_blueprint(usuario_bp, url_prefix='/usuario')
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

""" ejecutar: 
pipenv run python app.py
"""



