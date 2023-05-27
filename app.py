from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
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
        cursor.execute("SELECT * FROM usuarios WHERE Nombre_Usuario = %s AND Contraseña = %s", (nombre, contraseña))
        usuario = cursor.fetchone()
        cursor.close()
        if usuario:
            return redirect(url_for("paginaUsuario"))
        else:
            error = 'Nombre de usuario o contraseña incorrectos'
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

@app.route("/usuario")
def paginaUsuario():
    return render_template("usuario.html")

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
    print(pj)

    cursor.close()
    return render_template('personajes.html', pj=pj)

if __name__ == '__main__':
    app.secret_key = "CRkETIkXn0fAU:"
    app.run(debug=True)
