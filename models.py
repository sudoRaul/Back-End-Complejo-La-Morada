from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    rol = db.Column(db.String(20), nullable=False)

class Instalacion(db.Model):
    __tablename__ = 'instalaciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(255), nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    disponibilidad = db.Column(db.String(50), nullable=False)

class Reserva(db.Model):
    __tablename__ = 'reservas'  # Debe coincidir con MySQL
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # Coincide con MySQL
    id_instalacion = db.Column(db.Integer, db.ForeignKey('instalaciones.id'), nullable=False)  # Coincide con MySQL
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)

class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_instalacion = db.Column(db.Integer, db.ForeignKey('instalaciones.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    rango_edad = db.Column(db.String(20), nullable=False)

class Contacto(db.Model):
    __tablename__ = 'contacto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
