# Flask MySQL App

A Flask application connected to MySQL database using XAMPP with clean separation of database operations.

## Prerequisites

1. **XAMPP** installed and running
2. **Python 3.9+** installed
3. **pipenv** or **pip** for dependency management

## Database Setup

### 1. Start XAMPP
- Open XAMPP Control Panel
- Start Apache and MySQL services
- Make sure MySQL is running on port 3306

### 2. Create Database and User
In phpMyAdmin (http://localhost/phpmyadmin):

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS appTareas;

-- Create user (if not exists)
CREATE USER IF NOT EXISTS 'appUser'@'localhost' IDENTIFIED BY '';

-- Grant privileges
GRANT ALL PRIVILEGES ON appTareas.* TO 'appUser'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Create tareas table
```sql
CREATE TABLE tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    estado ENUM('pendiente', 'en_progreso', 'completada') DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Installation

### Using pipenv (recommended)
```bash
# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Run the application
python app.py
```

### Using pip
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Usage

The application will be available at `http://localhost:5001`

### Available Endpoints

#### Database Operations
- `GET /test-db` - Test database connection

#### Task Management (CRUD)
- `GET /tareas` - Get all tasks
- `GET /tareas/<id>` - Get a specific task by ID
- `POST /tareas` - Create a new task
- `PUT /tareas/<id>` - Update an existing task
- `DELETE /tareas/<id>` - Delete a task
- `GET /tareas/search?q=<term>` - Search tasks by title or description

#### Example API Usage

**Create a new task:**
```bash
curl -X POST http://localhost:5001/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Nueva tarea", "descripcion": "Descripción de la tarea", "estado": "pendiente"}'
```

**Update a task:**
```bash
curl -X PUT http://localhost:5001/tareas/1 \
  -H "Content-Type: application/json" \
  -d '{"estado": "completada"}'
```

**Search tasks:**
```bash
curl "http://localhost:5001/tareas/search?q=importante"
```

## Project Structure

```
flaskPrimero/
├── app.py              # Main Flask application with routes
├── db.py               # Database operations and connection management
├── env_config.py       # Configuration variables
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Database Schema

### Table: tareas
- `id` - Primary key (auto-increment)
- `titulo` - Task title (VARCHAR, required)
- `descripcion` - Task description (TEXT, optional)
- `estado` - Task status (ENUM: pendiente, en_progreso, completada)
- `fecha_creacion` - Creation timestamp
- `fecha_actualizacion` - Last update timestamp

## Features

- **Clean Architecture**: Database operations separated from route handlers
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Logging**: Database operations are logged for debugging
- **RESTful API**: Full CRUD operations for tasks
- **Search Functionality**: Search tasks by title or description
- **Input Validation**: Basic validation for required fields

## Troubleshooting

### Common Issues

1. **Connection refused**: Make sure XAMPP MySQL service is running
2. **Access denied**: Verify user 'appUser' has proper privileges
3. **Database not found**: Create database 'appTareas' in phpMyAdmin
4. **Module not found**: Install required dependencies with pip

### Check MySQL Status
```bash
# Check if MySQL is running
sudo netstat -tlnp | grep 3306

# Or check XAMPP control panel
```

## Development

To add new features:
1. Add new methods to the `DatabaseManager` class in `db.py`
2. Create corresponding routes in `app.py`
3. Test endpoints with tools like Postman or curl
4. All database operations are centralized in `db.py` for easy maintenance
