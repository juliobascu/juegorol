from .entities.Usuario import *

class ModelUsuarios():

    @classmethod
    def login(self, mysql, usuario):
        try:
            cursor = mysql.connection.cursor()
            sql = """SELECT id, nombre, contraseña, rol FROM juegorol.usuarios
                    WHERE nombre = '{}'""".format(usuario.nombre)
            cursor.execute(sql)
            usuarioV = cursor.fetchone()
            if usuarioV != None:
                usuario = Usuario(usuarioV[0],usuarioV[1],Usuario.verificarContraseña(usuarioV[2], usuario.contraseña),usuarioV[3])
                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception(ex)