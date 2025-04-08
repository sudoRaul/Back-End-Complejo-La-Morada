from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from flask_jwt_extended import JWTManager
from db import db

# Importamos las rutas
from routes import usuarios, instalaciones, reservas, eventos, contacto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['JSON_AS_ASCII'] = False
app.config['JWT_SECRET_KEY'] = 'q|w@e#r~t€'  # Usa una clave fuerte
jwt = JWTManager(app)
db.init_app(app)


# Registramos los blueprints
app.register_blueprint(usuarios.bp)
app.register_blueprint(instalaciones.bp)
app.register_blueprint(reservas.bp)
app.register_blueprint(eventos.bp)
app.register_blueprint(contacto.bp)

if __name__ == '__main__':
    app.run(debug=True)
