# app/app.py
from flask import Flask,render_template, request, jsonify,redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
db = mysql.connector.connect(
    #host="mysql-pia-contenedor",
    user="cristian",
    password="12345678",
    database="pia_lenguajes",
    port=3306
)

# ...

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    # Obtener todos los usuarios
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuario/<int:user_id>', methods=['GET'])
def get_usuario(user_id):
    # Obtener un usuario por ID
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    
    # Renderizar la plantilla HTML y pasar la información del usuario
    return render_template('usuario.html', usuario=usuario)

@app.route('/usuario', methods=['POST'])
def crear_usuario():
    # Crear un nuevo usuario desde un formulario
    nombre = request.form.get('nombre')
    correo = request.form.get('correo_electronico')
    contrasena = request.form.get('contrasena')

    cursor = db.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, correo_electronico, contrasena) VALUES (%s, %s, %s)",
                   (nombre, correo, contrasena))
    db.commit()
    cursor.close()
    
    # Redirigir a la página de usuarios después de crear uno nuevo
    return redirect(url_for('get_usuarios'))

@app.route('/usuario/<int:user_id>/editar', methods=['GET'])
def editar_usuario(user_id):
    # Obtener un usuario por ID para mostrar en el formulario de edición
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuario/<int:user_id>/actualizar', methods=['POST'])
def actualizar_usuario(user_id):
    # Actualizar un usuario por ID
    data = request.form
    nombre = data.get('nombre')
    correo = data.get('correo_electronico')
    contrasena = data.get('contrasena')

    cursor = db.cursor()
    cursor.execute("UPDATE usuarios SET nombre=%s, correo_electronico=%s, contrasena=%s WHERE id=%s",
                   (nombre, correo, contrasena, user_id))
    db.commit()
    cursor.close()
    return redirect(url_for('get_usuarios'))

@app.route('/usuario/<int:user_id>/eliminar', methods=['POST'])
def eliminar_usuario(user_id):
    # Eliminar un usuario por ID
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()
    return redirect(url_for('get_usuarios'))
@app.route('/')
def index():
    return '¡Bienvenido a la página de inicio!'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
