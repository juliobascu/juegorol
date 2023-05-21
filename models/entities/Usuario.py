from flask_bcrypt import check_password_hash, generate_password_hash

class Usuario():

    def __init__(self, id, nombre, contraseña, rol):
        self.id = id
        self.nombre = nombre
        self.contraseña = contraseña
        self.rol = rol
    @classmethod
    def verificarContraseña(self, hashed_contraseña, contraseña):
        return check_password_hash(hashed_contraseña, contraseña)
    
#print(generate_password_hash("abc.123"))