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
    

    app.config['MYSQL_HOST'] = 'turntable.proxy.rlwy.net'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'bZUVyCtCkxyZgeEWJEKOCMZAGfGJGhtq'
    app.config['MYSQL_DB'] = 'railway'
    app.config['MYSQL_PORT'] = 27504
    
    mysql.init_app(app)
    print("Database initialized")
    

    init_tables(app)

def get_db_connection():
    try:

        connection = mysql.connection
        if not connection:
            raise Exception("No database connection available")
        

        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        
        return cursor, connection
    except Exception as e:
        print(f"Database connection error: {e}")
        try:
            connection = mysql.connection
            if connection:
                connection.close()
        except:
            pass
        raise Exception(f"Error  : {e}")

def init_tables(app):
    """Initialize database tables manually"""
    try:
        with app.app_context():
            cursor, connection = get_db_connection()
            
            print("Dropping existing tables...")
            try:
                cursor.execute("DROP TABLE IF EXISTS tareas")
                cursor.execute("DROP TABLE IF EXISTS usuarios")
                print("Existing tables dropped")
            except Exception as e:
                print(f"Warning dropping tables: {e}")
            
            print("Creating usuarios table...")
            cursor.execute("""
                CREATE TABLE usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    contraseña VARCHAR(255) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("Usuarios table created")
            
            print("Creating tareas table...")
            cursor.execute("""
                CREATE TABLE tareas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    descripcion TEXT DEFAULT NULL,
                    user_id INT NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("Tareas table created")
            


            cursor.execute("""
                INSERT INTO usuarios (nombre, email, contraseña) VALUES 
                ('Primera ', ' tarea', '$2b$12$70BNyK2gIEVVw9g85VZKsuxShH7TOgeYZEpJQCb0XOmj1vUoU9jda'),
                ('Primera ', ' tareaa', '$2b$12$iyUscDv0ElXqpSrLYIEW1etIUn.GN8C0FnjOEZNYwUCdx1dVFae/y'),
                ('Primera ', ' tareaaa', '$2b$12$RFs5l4B6nnodp6/OuPqipOKZbXm6CThEWJTU7vdfYJbyf/Wql/bdK'),
                ('Primera ', ' tareaajja', '$2b$12$dipRyRVNHKBBejYmdc5xm.4x7uklkphT7SfmuikNDPVRYpvoA5CcG')
            """)
            

            cursor.execute("""
                INSERT INTO tareas (descripcion, user_id) VALUES 
                ('Primera tarea', 1),
                ('Una tarea', 1),
                ('Una tarea', 2),
                ('Una tarea', 2)
            """)
            
            connection.commit()
            print("Database tables initialized successfully with sample data")
                
    except Exception as e:
        print(f"Error initializing database tables: {e}")
        import traceback
        traceback.print_exc()


