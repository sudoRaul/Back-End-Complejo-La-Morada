from flask import Blueprint, jsonify, json, Response, request
from db import db
from models import Evento
from models import Usuario
from models import Instalacion

bp = Blueprint('eventos', __name__, url_prefix='/eventos')

#Obtener todos los eventos
@bp.route('/', methods=['GET'])
def get_eventos():
    eventos = Evento.query.all()
    data = [{
        'id': e.id,
        'id_usuario': e.id_usuario,
        'id_instalacion': e.id_instalacion,
        'nombre': e.nombre,
        'descripcion': e.descripcion,
        'fecha': str(e.fecha),
        'hora': str(e.hora),
        'rango_edad': e.rango_edad
    } for e in eventos]
    
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )
    
# Obtener un evento por ID 
@bp.route('/<int:id>', methods=['GET'])
def get_evento(id):
    evento = Evento.query.get(id)
    if not evento:
        return Response(
            json.dumps({'error': 'Evento no encontrado'}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )

    # Obtenemos relaciones con protección contra nulos
    usuario = Usuario.query.get(evento.id_usuario) if evento.id_usuario else None
    instalacion = Instalacion.query.get(evento.id_instalacion) if evento.id_instalacion else None

    # Construimos la respuesta estructurada
    evento_data = {
        'id': evento.id,
        'nombre': evento.nombre,
        'descripcion': evento.descripcion,
        'fecha': evento.fecha.strftime('%Y-%m-%d') if evento.fecha else None,
        'hora': str(evento.hora) if evento.hora else None,
        'rango_edad': evento.rango_edad,
        'usuario': {
            'id': usuario.id if usuario else None,
            'nombre': usuario.nombre if usuario else None,
            'apellido': usuario.apellido if usuario else None,
            'email': usuario.email if usuario else None,
            'edad': usuario.edad if usuario else None,
            'rol': usuario.rol if usuario else None
        } if usuario else None,
        'instalacion': {
            'id': instalacion.id if instalacion else None,
            'nombre': instalacion.nombre if instalacion else None,
            'categoria': instalacion.categoria if instalacion else None,
            'disponibilidad': instalacion.disponibilidad if instalacion else None
        } if instalacion else None
    }

    return Response(
        json.dumps(evento_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )
    
    
# Crear un nuevo evento
@bp.route('/', methods=['POST'])
def create_evento():
    data = request.get_json()

    if not data or not all(key in data for key in ["id_usuario", "id_instalacion", "nombre", "descripcion", "fecha", "hora", "rango_edad"]):
        return jsonify({"error": "Datos incompletos"}), 400

    nuevo_evento = Evento(
        id_usuario=data["id_usuario"],
        id_instalacion=data["id_instalacion"],
        nombre=data["nombre"],
        descripcion=data["descripcion"],
        fecha=data["fecha"],
        hora=data["hora"],
        rango_edad=data["rango_edad"]
    )

    db.session.add(nuevo_evento)
    db.session.commit()

    return jsonify({"message": "Evento creado exitosamente", "id": nuevo_evento.id}), 201

# Actualizar un evento por ID
@bp.route('/<int:id>', methods=['PUT'])
def actualizar_evento(id):
    data = request.get_json()
    evento = Evento.query.get(id)

    if not evento:
        return jsonify({"error": "Evento no encontrado"}), 404

    if "nombre" in data:
        evento.nombre = data["nombre"]
    if "descripcion" in data:
        evento.descripcion = data["descripcion"]
    if "fecha" in data:
        evento.fecha = data["fecha"]
    if "hora" in data:
        evento.hora = data["hora"]
    if "rango_edad" in data:
        evento.rango_edad = data["rango_edad"]

    db.session.commit()
    return jsonify({"mensaje": "Evento actualizado correctamente"}), 200


# Eliminar un evento por ID
@bp.route('/<int:id>', methods=['DELETE'])
def delete_evento(id):
    evento = Evento.query.get(id)
    if not evento:
        return jsonify({'error': 'Evento no encontrado'}), 404
    db.session.delete(evento)
    db.session.commit()
    return jsonify({'message': 'Evento eliminado correctamente'}), 200
