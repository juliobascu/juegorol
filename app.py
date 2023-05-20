from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'juegorol'




@app.route("/")
def login():
    return render_template('index.html')

@app.route('/usuarios')
def mostrar_usuarios():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM juegorol.usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/personajes')
def mostrar_personajes():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM juegorol.personajes")
    pj = cursor.fetchall()
    print(pj)
    cursor.close()
    return render_template('personajes.html', pj=pj)

mysql = MySQL(app)
if __name__ == '__main__':
    app.run(debug=True)
