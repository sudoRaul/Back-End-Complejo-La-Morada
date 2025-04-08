from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import Usuario  # Importa el modelo de usuarios
from db import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Buscar usuario por email
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or usuario.contraseña != password:  # 🔴 En producción usa hashing de contraseña
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # Crear token con el ID y rol del usuario
    access_token = create_access_token(identity={"id": usuario.id, "rol": usuario.rol})
    
    return jsonify(access_token=access_token)
