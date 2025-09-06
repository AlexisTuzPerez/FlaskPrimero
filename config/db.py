from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

load_dotenv()

mysql = MySQL()

def init_db(app):
    """Initialize MySQL with Flask app"""
    # Debug: Print environment variables
    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_USER: {os.getenv('DB_USER')}")
    print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
    print(f"DB_NAME: {os.getenv('DB_NAME')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")
    
    # Set MySQL configuration
    app.config['MYSQL_HOST'] = '127.0.0.1'  # Use IP instead of localhost
    app.config['MYSQL_USER'] = 'root'  # Use root user
    app.config['MYSQL_PASSWORD'] = ''  # No password for root
    app.config['MYSQL_DB'] = 'appTareas'
    app.config['MYSQL_PORT'] = 3306  # Standard MySQL port
    
    # For XAMPP MySQL, specify the socket path
    app.config['MYSQL_UNIX_SOCKET'] = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    
    mysql.init_app(app)
    print("Database initialized")

def get_db_connection():
    try:
        # Get a fresh connection
        connection = mysql.connection
        if not connection:
            raise Exception("No database connection available")
        
        # Test the connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        
        return cursor, connection
    except Exception as e:
        print(f"Database connection error: {e}")
        # Try to reconnect
        try:
            connection = mysql.connection
            if connection:
                connection.close()
        except:
            pass
        raise Exception(f"Error connecting to database: {e}")



