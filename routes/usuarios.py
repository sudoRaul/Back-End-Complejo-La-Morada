from flask import Blueprint, json, Response, request, jsonify
from werkzeug.security import generate_password_hash
from db import db
from models import Usuario

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

#Obtener todos los usuarios
@bp.route('/', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    data = [{
        'id': u.id,
        'nombre': u.nombre,
        'apellido': u.apellido,
        'email': u.email,
        'edad': u.edad,
        'rol': u.rol
    } for u in usuarios]
    
    
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )
    
# Obtener un usuario por ID
@bp.route('/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    
    if not usuario:
        # Para el error también usamos el formato correcto
        return Response(
            json.dumps({'error': 'Usuario no encontrado'}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )
    
    # Estructura de datos del usuario
    usuario_data = {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'email': usuario.email,
        'edad': usuario.edad,
        'rol': usuario.rol
    }
    
    return Response(
        json.dumps(usuario_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )
    
# Crear un nuevo usuario
@bp.route('/', methods=['POST'])
def create_usuario():
    data = request.get_json()

    if not data or not all(key in data for key in ["nombre", "apellido", "email", "contraseña", "edad", "rol"]):
        return jsonify({"error": "Datos incompletos"}), 400

    nuevo_usuario = Usuario(
        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        contraseña=data["contraseña"],
        edad=data["edad"],
        rol=data["rol"]
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente", "id": nuevo_usuario.id}), 201

# Actualizar un usuario por ID
@bp.route('/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.get_json()
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if "nombre" in data:
        usuario.nombre = data["nombre"]
    if "apellido" in data:
        usuario.apellido = data["apellido"]
    if "email" in data:
        usuario.email = data["email"]
    if "edad" in data:
        usuario.edad = data["edad"]
    if "rol" in data:
        usuario.rol = data["rol"]
    if "contraseña" in data:
        usuario.contraseña = generate_password_hash(data["contraseña"])  # Se hashea la nueva contraseña

    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200


# Eliminar un usuario por ID
@bp.route('/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario eliminado correctamente'}), 200