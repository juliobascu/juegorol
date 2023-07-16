from flask import Flask, render_template, request, redirect, url_for, flash, Response, session, jsonify
import bcrypt
from flask_mysqldb import MySQL, MySQLdb
import ast

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
                        session["jugador_logeado"] = True
                        session["nombre_usuario"] = usuario[1]
                        session["IDU"] = usuario[0]
                        return render_template("jugador.html", IDU = usuario[0], NombreU=usuario[1], usuariosN=usuariosN, nusuarios = nusuarios)
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
        cursor.execute("SELECT * FROM razas")
        razas = cursor.fetchall()
        cursor.close()
        return render_template("GM.html", usuariosN=usuariosN, NombreU=session["nombre_usuario"], nusuarios=session["usuariosTotales"], razas=razas)         
    else:
        return redirect(url_for("login"))    

@app.route('/buscar_personaje', methods=['POST'])
def buscar_personaje():
    id_personaje = request.form['idpj']
    if id_personaje is None:
        redirect(url_for("paginaGM"))
    else:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personajes WHERE ID_Personaje = %s", (id_personaje,))
        personaje = cursor.fetchone()
        if personaje is None:
            return redirect(url_for("paginaGM"))
        cursor.execute("SELECT a.ID_Habilidad, a.Nombre_Habilidad FROM habilidades a INNER JOIN personaje_habilidades aa ON a.ID_Habilidad = aa.ID_Habilidad WHERE aa.ID_Personaje = %s", (id_personaje,))
        habilidades = cursor.fetchall()
        cursor.execute(f"SELECT Id_Habilidad, Nombre_Habilidad FROM habilidades WHERE Condicional_Raza = '{personaje[4]}'")
        habilidadesRaza = cursor.fetchall()
        cursor.execute("SELECT p.ID_Poder, p.Nombre_Poder FROM poderes p INNER JOIN personaje_poderes pp ON p.ID_Poder = pp.ID_Poder WHERE pp.ID_Personaje = %s", (id_personaje,))
        poderes = cursor.fetchall()
        cursor.execute("SELECT Id_Poder, Nombre_Poder FROM poderes WHERE Raza = %s", (personaje[4],))
        poderesRaza = cursor.fetchall()
        cursor.execute("SELECT e.ID_Equipamiento, e.Nombre_Equipamiento, ee.Cantidad FROM equipamientos e INNER JOIN personaje_equipamientos ee ON e.ID_Equipamiento = ee.ID_Equipamiento WHERE ee.ID_Personaje = %s", (id_personaje,))
        equipamientos = cursor.fetchall()
        cursor.execute("SELECT Id_Equipamiento, Nombre_Equipamiento FROM equipamientos")
        equipamientosTotal = cursor.fetchall()
        cursor.execute("SELECT * FROM razas")
        razas = cursor.fetchall()
        cursor.execute("SELECT e.Nombre_Estado FROM estados e INNER JOIN personajes p ON e.Nombre_Estado = p.Estado WHERE p.ID_Personaje = %s", (id_personaje,))
        estados = cursor.fetchall()
        cursor.execute("SELECT Nombre_Estado FROM estados")
        estadosTotal = cursor.fetchall()
        cursor.close()
        return render_template("editorPj.html", personaje=personaje, habilidades=habilidades, habilidadesRaza=habilidadesRaza, poderes=poderes, poderesRaza=poderesRaza, equipamientos=equipamientos, equipamientosTotal=equipamientosTotal, razas=razas, estados=estados, estadosTotal=estadosTotal)

@app.route("/actualizarPersonaje", methods=['GET', 'POST'])
def actualizarPersonaje():
    if request.method == "POST":
        id_personaje = request.form["id"]
        nombre_personaje = request.form["nombrepj"]
        nivel_personaje = request.form["nivel"]
        estado_personaje = request.form["estado"]
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute(f"UPDATE personajes SET Nombre_Personaje = '{nombre_personaje}', Nivel = '{nivel_personaje}', Estado = '{estado_personaje}' WHERE Id_Personaje = '{id_personaje}'")
        mysql.connection.commit()
    #Habilidades
        habilidades_seleccionadas = []
        for i in range(1, 9):
            habilidad = request.form.get("habilidad" + str(i))
            if habilidad:
                habilidades_seleccionadas.append(int(habilidad))

        cursor.execute("SELECT ID_Habilidad FROM personaje_habilidades WHERE ID_Personaje = %s", (id_personaje,))
        habilidades_existentes = cursor.fetchall()
        habilidades_existentes = [habilidad[0] for habilidad in habilidades_existentes]

        habilidades_a_eliminar = list(set(habilidades_existentes) | set(habilidades_seleccionadas))
        habilidades_a_insertar = list(set(habilidades_existentes) | set(habilidades_seleccionadas))

        if len(habilidades_a_eliminar) > 2:
            placeholders = ', '.join(['%s'] * len(habilidades_a_eliminar))
            query_eliminar = f"DELETE FROM personaje_habilidades WHERE ID_Personaje = %s AND ID_Habilidad IN ({placeholders})"
            params_eliminar = (id_personaje,) + tuple(habilidades_a_eliminar)
            cursor.execute(query_eliminar, params_eliminar)
            conn.commit()

        for id_habilidad in habilidades_a_insertar:
            cursor.execute("INSERT INTO personaje_habilidades (ID_Personaje, ID_Habilidad) VALUES (%s, %s)",
                        (id_personaje, id_habilidad))
            conn.commit()
    #PODERES
        poderes_seleccionados = []
        for i in range(2, 5):
            poder = request.form.get("poder" + str(i))
            if poder:
                poderes_seleccionados.append(int(poder))
        
        cursor.execute("SELECT ID_Poder FROM personaje_poderes WHERE ID_Personaje = %s", (id_personaje,))
        poderes_existentes = cursor.fetchall()
        poderes_existentes = [poder[0] for poder in poderes_existentes]
        
        poderes_a_eliminar = list(set(poderes_existentes) | set(poderes_seleccionados))
        poderes_a_insertar = list(set(poderes_existentes) | set(poderes_seleccionados))

        if len(poderes_a_eliminar) > 1:
            placeholders = ', '.join(['%s'] * len(poderes_a_eliminar))
            query_eliminar = f"DELETE FROM personaje_poderes WHERE ID_Personaje = %s AND ID_Poder IN ({placeholders})"
            params_eliminar = (id_personaje,) + tuple(poderes_a_eliminar)
            cursor.execute(query_eliminar, params_eliminar)
            conn.commit()
        for id_poder in poderes_a_insertar:
            cursor.execute("INSERT INTO personaje_poderes (ID_Personaje, ID_Poder) VALUES (%s, %s)",
                (id_personaje, id_poder))
            conn.commit()
    #EQUIPAMIENTOS
        equipamientos = []
        cantidades = []
        cantidad1 = request.form.get("cantidad1")
        cantidades.append(int(cantidad1))
        for i in range(2, 9):
            equipamiento = request.form.get("equipamiento" + str(i))
            cantidad = request.form.get("cantidad" + str(i))

            if equipamiento and cantidad:
                equipamientos.append(int(equipamiento))
                cantidades.append(int(cantidad))

        cursor.execute("SELECT ID_Equipamiento FROM personaje_equipamientos WHERE ID_Personaje = %s", (id_personaje,))
        equipamientos_existentes = cursor.fetchall()
        equipamientos_existentes = [equipamiento[0] for equipamiento in equipamientos_existentes]

        equipamientos_a_eliminar = list(set(equipamientos_existentes) | set(equipamientos))
        equipamientos_a_insertar = list(set(equipamientos_existentes) | set(equipamientos))

        if len(equipamientos_a_eliminar) > 0:
            placeholders = ', '.join(['%s'] * len(equipamientos_a_eliminar))
            query_eliminar = f"DELETE FROM personaje_equipamientos WHERE ID_Personaje = %s AND ID_Equipamiento IN ({placeholders})"
            params_eliminar = (id_personaje,) + tuple(equipamientos_a_eliminar)
            cursor.execute(query_eliminar, params_eliminar)
            conn.commit()

        for equipamiento, cantidad in zip(equipamientos_a_insertar, cantidades):
            cursor.execute("INSERT INTO personaje_equipamientos (ID_Personaje, ID_Equipamiento, cantidad) VALUES (%s, %s, %s)",(id_personaje, equipamiento, cantidad))
            conn.commit()
        flash("Personaje Actualizado")
        cursor.close()
        return redirect(url_for("paginaGM"))
    else:
        return redirect(url_for("actualizarPersonaje"))    

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
    cursor.execute(f"SELECT ID_Poder, Nombre_Poder FROM poderes WHERE Raza = '{data['raza']}'")
    poderes = cursor.fetchall()
    cursor.close()
    return {'poderes': poderes}

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    if request.method == "POST":
        nombre_usuario = request.form['nombreUsuario']
        contraseña = request.form['contraUsuario']
        es_gm = request.form['rolUsuario']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (Nombre_Usuario, Contraseña, Es_GM) VALUES (%s, %s, %s)", (nombre_usuario, contraseña, es_gm))
        mysql.connection.commit()
        flash("Usuario Agergado")
        cursor.close()
        return redirect(url_for("paginaGM"))

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
        flash("Poder Agergado")
        cursor.close()
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
        flash("Habilidad Agergada")
        cursor.close()
        return redirect(url_for("paginaGM"))

@app.route('/agregar_raza', methods=['POST'])
def agregar_raza():
    if request.method == "POST":
        nombre_raza = request.form['nombreRaza']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO poderes (Raza) VALUES (%s)", (nombre_raza,))
        mysql.connection.commit()
        flash("Raza Agergada")
        cursor.close()
        return redirect(url_for("paginaGM"))

@app.route('/agregar_equipamiento', methods=['POST'])
def agregar_equipamiento():
    if request.method == "POST":
        nombre_equipamiento = request.form['nombreEquipamiento']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO equipamientos (Nombre_Equipamiento) VALUES (%s)", (nombre_equipamiento,))
        mysql.connection.commit()
        flash("Equipamiento Agergado")
        cursor.close()
        return redirect(url_for("paginaGM"))
    
@app.route('/agregar_estado', methods=['POST'])
def agregar_estado():
    if request.method == "POST":
        nombre_estado = request.form['nombreEstado']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO estados (Nombre_Estado) VALUES (%s)", (nombre_estado,))
        mysql.connection.commit()
        flash("Estado Agergado")
        cursor.close()
        return redirect(url_for("paginaGM"))
    
    
@app.route('/actualizarHabilidades', methods=['POST'])
def actualizarHabilidades():
    data = request.get_json()
    print(data)
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(f"SELECT ID_Habilidad, Nombre_Habilidad FROM habilidades WHERE Condicional_Raza = '{data['raza']}'")
    habilidades = cursor.fetchall()
    cursor.close()
    print(habilidades)
    return {'habilidades': habilidades}

@app.context_processor
def utility_processor():
    def obtenerEquipamientos():
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT iD_Equipamiento, Nombre_Equipamiento FROM equipamientos")
        equipamientos = cursor.fetchall()
        cursor.close()
        return equipamientos

    return dict(obtenerEquipamientos=obtenerEquipamientos)

@app.route("/informe")
def generarInforme():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM informepj")
    pj = cursor.fetchall()
    print(pj)
    cursor.close()
    return render_template("informe.html", pj=pj)

@app.route('/crearPersonaje', methods=['POST'])
def crearPersonaje():
    if request.method == "POST":
        print(request.form)
        idUsuario = request.form["idUsuario"]
        nombreJugador = request.form["nombreJ"]
        nombrePersonaje = request.form['nombreP']
        nivel = request.form['nivel']
        estado = request.form['estado']
        raza = request.form['raza']
        habilidad1 = request.form['habilidad1']
        habilidad2 = request.form['habilidad2']
        poder = request.form['poder']
        equipamiento = request.form['equipamiento']
        conn = mysql.connection
        cursor = conn.cursor()
        # cursor.execute(f"""
        #     INSERT INTO personajes (ID_Usuario, Nombre_Jugador, Nombre_Personaje, Raza, Nivel, Estado) VALUES ('{idUsuario}', '{nombreJugador}', '{nombrePersonaje}', '{raza}', '{nivel}', '{estado}');
        #     SET @idPersonaje = LAST_INSERT_ID();
        #     SELECT ID_Habilidad INTO @idHabilidad1 FROM habilidades where Nombre_Habilidad = '{habilidad1}' limit 1;
        #     SELECT ID_Habilidad INTO @idHabilidad2 FROM habilidades where Nombre_Habilidad = '{habilidad2}' limit 1;
        #     SELECT ID_Poder INTO @idPoder FROM poderes where Nombre_Poder = '{poder}' limit 1; 
        #     SELECT ID_Equipamiento INTO @idEquipamiento FROM equipamientos where Nombre_Equipamiento = '{equipamiento}' limit 1;
        #     INSERT INTO personaje_habilidades values (@idPersonaje, @idHabilidad1), (@idPersonaje, @idHabilidad2); 
        #     INSERT INTO personaje_poderes values (@idPersonaje, @idPoder);
        #     INSERT INTO personaje_equipamientos values (@idPersonaje, @idEquipamiento, 1); 
        #     """)
        cursor.execute(f"""
            INSERT INTO personajes (ID_Usuario, Nombre_Jugador, Nombre_Personaje, Raza, Nivel, Estado) VALUES ('{idUsuario}', '{nombreJugador}', '{nombrePersonaje}', '{raza}', '{nivel}', '{estado}');
            SET @idPersonaje = LAST_INSERT_ID();
            SELECT ID_Equipamiento INTO @idEquipamiento FROM equipamientos where Nombre_Equipamiento = '{equipamiento}' limit 1;
            INSERT INTO personaje_habilidades values (@idPersonaje, {habilidad1}), (@idPersonaje, {habilidad2}); 
            INSERT INTO personaje_poderes values (@idPersonaje, {poder});
            INSERT INTO personaje_equipamientos values (@idPersonaje, {equipamiento}, 1); 
            """)
        cursor.close()
        mysql.connection.commit()
        return redirect(url_for("paginaJugador"))

@app.route("/paginaJugador")
def paginaJugador():
    if session.get("jugador_logeado"):
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM juegorol.usuarios")
        usuariosN = cursor.fetchall()
        cursor.close()
        return render_template("jugador.html", usuariosN=usuariosN, NombreU=session["nombre_usuario"], IDU=session["IDU"], nusuarios=session["usuariosTotales"])         
    else:
        return redirect(url_for("login"))

if __name__ == '__main__':
    app.secret_key = "CRkETIkXn0fAU:"
    app.run(debug=True)

    
