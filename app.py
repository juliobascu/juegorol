from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
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
                        return render_template("usuario.html", NombreU=usuario[1])
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

@app.route('/usuarios')
def mostrarUsuarios():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM juegorol.usuarios")
    usuarios = cursor.fetchall()
    nusuarios = len(usuarios)
    cursor.close()
    return render_template('usuarios.html', usuarios=usuarios, nusuarios=nusuarios)

@app.route('/personajes')
def mostrarPersonajes():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("""SELECT `vista_personaje1`.`ID_Personaje`,
    `vista_personaje1`.`Nombre_Jugador`,
    `vista_personaje1`.`Nombre_Personaje`,
    `vista_personaje1`.`Raza`,
    `vista_personaje1`.`Nivel`,
    `vista_personaje1`.`Nombre_Estado`,
    `vista_personaje1`.`Nombre_Habilidad`,
    `vista_personaje1`.`Nombre_Equipamiento`,
    `vista_personaje1`.`Nombre_Poder`
    FROM `juegorol`.`vista_personaje1`;""")
    pj = cursor.fetchall()

    cursor.close()
    return render_template('personajes.html', pj=pj)

if __name__ == '__main__':
    app.secret_key = "CRkETIkXn0fAU:"
    app.run(debug=True)
