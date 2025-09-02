from flask import Flask, jsonify
import os
from routes.tareas import tareas_bp
from config.db import init_db

def create_app():
    app = Flask(__name__)
    
    # Initialize database
    init_db(app)
    
    app.register_blueprint(tareas_bp, url_prefix='/tareas')
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

""" ejecutar: 
pipenv run python app.py
"""