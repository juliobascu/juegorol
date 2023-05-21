from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Models
from models.ModelUsuarios import *

# Entities
from models.entities.Usuario import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'CRkETIkXn0fAU:'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abc.123'
app.config['MYSQL_DB'] = 'juegorol'

mysql = MySQL(app)

@app.route("/", methods = ["GET", "POST"])
def index():
    return redirect(url_for("login"))

@app.route("/login" , methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = Usuario(0, request.form["nombre"], request.form["contraseña"], request.form["rol"])
        print(usuario.contraseña)
        usuarioLogeado = ModelUsuarios.login(mysql, usuario)
        print(usuarioLogeado.nombre)
        print(usuarioLogeado.contraseña)
        if usuarioLogeado != None:
            if usuarioLogeado.verificarContraseña():
                return redirect(url_for("paginaUsuario"))
            else:
                flash("Contraseña invalida...")
                return render_template('index.html')
        else:
            print("Usuario no encontrado..")
            flash("Usuario no encontrado...")
            return render_template("index.html")
    else:
        print("Metodo Invalido")
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
    cursor.execute("SELECT * FROM juegorol.personajes")
    pj = cursor.fetchall()
    print(pj)
    cursor.close()
    return render_template('personajes.html', pj=pj)

if __name__ == '__main__':
    app.run(debug=True)
