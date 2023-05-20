from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'juegorol'

mysql = MySQL(app)

@app.route("/" , methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form["nombre"])
        print(request.form["contraseña"])
        print(request.form["rol"])
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route("/usuario/<nombre>")
def paginaUsuario():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM juegorol.usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template("usuario.html")

@app.route('/usuarios')
def mostrarUsuarios():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM juegorol.usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('usuarios.html', usuarios=usuarios)

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
