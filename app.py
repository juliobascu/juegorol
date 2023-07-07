from flask import Flask, render_template, request, redirect, url_for, flash, Response, session, jsonify
import bcrypt
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abc.123'
app.config['MYSQL_DB'] = 'juegorol'

mysql = MySQL(app)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login" , methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        nombre = request.form["nombre"]
        contraseña = request.form["contraseña"]
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE Nombre_Usuario = %s", (nombre,))
        usuarios = cursor.fetchall()

        if usuarios:
            for usuario in usuarios:
                if usuario[2] == contraseña:
                    if usuario[3] == 0:
                        conn = mysql.connection
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM juegorol.usuarios")
                        usuariosN = cursor.fetchall()
                        nusuarios = len(usuarios)
                        cursor.close()
                        return render_template("jugador.html", NombreU=usuario[1], usuariosN=usuariosN, nusuarios = nusuarios)
                    else:
                        conn = mysql.connection
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM juegorol.usuarios")
                        usuariosN = cursor.fetchall()
                        nusuarios = len(usuarios)
                        cursor.close()
                        return render_template("GM.html", NombreU=usuario[1], usuariosN=usuariosN, nusuarios = nusuarios)             
                else:
                    flash("Contraseña incorrecta...")
                    cursor.close()
                    return render_template("index.html")
        else:
            flash("Usuario no encontrado...")
            cursor.close()
            return render_template("index.html")
        cursor.close()
    else:
        return render_template("index.html")

@app.context_processor
def utility_processor():
    def obtenerPersonajes(id_usuario):
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personajes WHERE ID_Usuario = %s", (id_usuario,))
        personajes = cursor.fetchall()
        cursor.close()
        return personajes

    return dict(obtenerPersonajes=obtenerPersonajes)

@app.context_processor
def utility_processor():
    def obtenerRazas():
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT raza FROM poderes GROUP BY raza")
        razas = cursor.fetchall()
        cursor.close()
        return razas

    return dict(obtenerRazas=obtenerRazas)

@app.context_processor
def utility_processor():
    def obtenerPoderes():
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre_Poder FROM poderes")
        poderes = cursor.fetchall()
        cursor.close()
        return poderes

    return dict(obtenerPoderes=obtenerPoderes)

@app.context_processor
def utility_processor():
    def obtenerEquipamientos():
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre_Equipamiento FROM equipamientos")
        equipamientos = cursor.fetchall()
        cursor.close()
        return equipamientos

    return dict(obtenerEquipamientos=obtenerEquipamientos)

def obtenerDetallesPersonaje(id_personaje):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personajes WHERE ID_Personaje = %s", (id_personaje,))
    personaje = list(cursor.fetchone())
    cursor.execute("SELECT Nombre_Poder FROM poderes p INNER JOIN personaje_poderes pp ON p.ID_Poder = pp.ID_Poder WHERE pp.ID_Personaje = %s", (id_personaje,))
    poderes = cursor.fetchall()
    poderes_list = [p[0] for p in poderes]
    cursor.close()
    personaje.append(poderes_list)
    return personaje

@app.route('/personaje/<int:id>', methods=['GET'])
def obtener_detalles_personaje(id):
    personaje = obtenerDetallesPersonaje(id)
    if personaje:
        return jsonify(personaje), 200
    else:
        return jsonify({'error': 'Personaje no encontrado'}), 404

@app.context_processor
def utility_processor():
    return dict(obtenerDetallesPersonaje=obtenerDetallesPersonaje)

if __name__ == '__main__':
    app.secret_key = "CRkETIkXn0fAU:"
    app.run(debug=True)

    
