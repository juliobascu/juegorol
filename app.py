from flask import Flask, render_template, request, redirect, url_for, flash, Response, session, jsonify
import bcrypt
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "abc.123"
app.config['MYSQL_DB'] = 'juegorol'

#app.config['MYSQL_HOST'] = 'db4free.net'
#app.config['MYSQL_USER'] = 'usuario1234'
#app.config['MYSQL_PASSWORD'] = "usuario1234"
#app.config['MYSQL_DB'] = 'juegorol'

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
                        nusuarios = len(usuarios)
                        session["GM_logeado"] = True
                        session["nombre_usuario"] = usuario[1]
                        session["usuariosTotales"] = nusuarios
                        return redirect(url_for("paginaGM"))
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
    
@app.route("/logOut")
def logOut():
    session.pop("GM_logeado", None)
    return redirect(url_for("index"))

@app.route("/paginaGM")
def paginaGM():
    if session.get("GM_logeado"):
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM juegorol.usuarios")
        usuariosN = cursor.fetchall()
        cursor.close()
        return render_template("GM.html", usuariosN=usuariosN, NombreU=session["nombre_usuario"], nusuarios=session["usuariosTotales"])         
    else:
        return redirect(url_for("login"))    

@app.route('/buscar_personaje', methods=['POST'])
def buscar_personaje():
    id_personaje = request.form['idpj']
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personajes WHERE ID_Personaje = %s", (id_personaje,))
    personaje = cursor.fetchone()
    print(personaje)
    cursor.execute("SELECT Nombre_Habilidad FROM habilidades a INNER JOIN personaje_habilidades aa ON a.ID_Habilidad = aa.ID_Habilidad WHERE aa.ID_Personaje = %s", (id_personaje,))
    habilidades = cursor.fetchall()
    print(habilidades)
    cursor.execute("SELECT Nombre_Poder FROM poderes p INNER JOIN personaje_poderes pp ON p.ID_Poder = pp.ID_Poder WHERE pp.ID_Personaje = %s", (id_personaje,))
    poderes = cursor.fetchall()
    print(poderes)
    cursor.execute("SELECT Nombre_Poder FROM poderes WHERE Raza = %s", (personaje[4],))
    poderesRaza = cursor.fetchall()
    print(poderesRaza)
    cursor.execute("SELECT Nombre_Equipamiento, Cantidad FROM equipamientos e INNER JOIN personaje_equipamientos ee ON e.ID_Equipamiento = ee.ID_Equipamiento WHERE ee.ID_Personaje = %s", (id_personaje,))
    equipamientos = cursor.fetchall()
    print(equipamientos)
    cursor.execute("SELECT * FROM razas")
    razas = cursor.fetchall()
    print(razas)
    cursor.close()

    return render_template("editorPj.html", personaje=personaje, habilidades=habilidades, poderes=poderes, poderesRaza=poderesRaza, equipamientos=equipamientos, razas=razas)


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

@app.route('/actualizarPoderes', methods=['POST'])
def actualizarPoderes():
    data = request.get_json()
    print(data)
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(f"SELECT Nombre_Poder FROM poderes WHERE Raza = '{data['raza']}'")
    poderes = cursor.fetchall()
    cursor.close()
    print(poderes)
    return {'poderes': poderes}

@app.route('/agregar_poder', methods=['POST'])
def agregar_poder():
    if request.method == "POST":
        nombre_poder = request.form['nombrePoder']
        detalle_poder = request.form['detallePoder']
        raza_poder = request.form['razaPoder']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO poderes (Nombre_Poder, Detalle, Raza) VALUES (%s, %s, %s)", (nombre_poder, detalle_poder, raza_poder))
        mysql.connection.commit()
        return redirect(url_for("paginaGM"))
    
@app.route('/agregar_habilidad', methods=['POST'])
def agregar_habilidad():
    if request.method == "POST":
        nombre_habilidad = request.form['nombreHabilidad']
        raza_habilidad = request.form['razaHabilidad']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO habilidades (Nombre_Habilidad, Condicional_Raza) VALUES (%s, %s)", (nombre_habilidad, raza_habilidad))
        mysql.connection.commit()
        return redirect(url_for("paginaGM"))

@app.route('/agregar_raza', methods=['POST'])
def agregar_raza():
    if request.method == "POST":
        nombre_raza = request.form['nombreRaza']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO poderes (Raza) VALUES (%s)", (nombre_raza,))
        mysql.connection.commit()
        return redirect(url_for("paginaGM"))

@app.route('/agregar_equipamiento', methods=['POST'])
def agregar_equipamiento():
    if request.method == "POST":
        nombre_equipamiento = request.form['nombreEquipamiento']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO equipamientos (Nombre_Equipamiento) VALUES (%s)", (nombre_equipamiento,))
        mysql.connection.commit()
        return redirect(url_for("paginaGM"))
    
@app.route('/agregar_estado', methods=['POST'])
def agregar_estado():
    if request.method == "POST":
        nombre_estado = request.form['nombreEstado']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO estados (Nombre_Estado) VALUES (%s)", (nombre_estado,))
        mysql.connection.commit()
        return redirect(url_for("paginaGM"))
    
    
@app.route('/actualizarHabilidades', methods=['POST'])
def actualizarHabilidades():
    data = request.get_json()
    print(data)
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(f"SELECT Nombre_Habilidad FROM habilidades WHERE Condicional_Raza = '{data['raza']}'")
    habilidades = cursor.fetchall()
    cursor.close()
    print(habilidades)
    return {'habilidades': habilidades}

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
    cursor.execute("SELECT Nombre_Poder FROM poderes")
    poderesT = cursor.fetchall()
    cursor.close()
    personaje.append(poderes_list)
    personaje.append(poderesT)
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

@app.route("/informe")
def generarInforme():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM informepj")
    pj = cursor.fetchall()
    print(pj)
    cursor.close()
    return render_template("informe.html", pj=pj)

if __name__ == '__main__':
    app.secret_key = "CRkETIkXn0fAU:"
    app.run(debug=True)

    
