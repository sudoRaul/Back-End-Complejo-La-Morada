from flask import Blueprint, jsonify, json, Response, request
from db import db
from models import Contacto

bp = Blueprint('contacto', __name__, url_prefix='/contacto')

# Obtener todos los contactos
@bp.route('/', methods=['GET'])
def get_contactos():
    contactos = Contacto.query.all()
    data = [{
        'id': c.id,
        'nombre': c.nombre,
        'apellido': c.apellido,
        'email': c.email,
        'telefono': c.telefono,
        'comentario': c.comentario
    } for c in contactos]
    
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )
    
# Obtener un contacto por ID
@bp.route('/<int:id>', methods=['GET'])
def get_contacto(id):
    contacto = Contacto.query.get(id)
    
    if not contacto:
        return Response(
            json.dumps({'error': 'Contacto no encontrado'}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )
    
    contacto_data = {
        'id': contacto.id,
        'nombre': contacto.nombre,
        'apellido': contacto.apellido,
        'email': contacto.email,
        'telefono': contacto.telefono,
        'comentario': contacto.comentario
    }
    
    return Response(
        json.dumps(contacto_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )


# Crear un nuevo contacto
@bp.route('/', methods=['POST'])
def create_contacto():
    data = request.get_json()

    if not data or not all(key in data for key in ["nombre", "apellido", "email", "telefono", "comentario"]):
        return jsonify({"error": "Datos incompletos"}), 400

    nuevo_contacto = Contacto(
        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        telefono=data["telefono"],
        comentario=data["comentario"]
    )

    db.session.add(nuevo_contacto)
    db.session.commit()

    return jsonify({"message": "Contacto registrado exitosamente", "id": nuevo_contacto.id}), 201


