from flask import Blueprint, jsonify, json, Response, request
from db import db
from models import Reserva
from models import Usuario
from models import Instalacion

bp = Blueprint('reservas', __name__, url_prefix='/reservas')

#Mostrar todas las reservas
@bp.route('/', methods=['GET'])
def get_reservas():
    reservas = Reserva.query.all()
    data = [{
        'id': r.id,
        'id_usuario': r.id_usuario,
        'id_instalacion': r.id_instalacion,
        'fecha': str(r.fecha),
        'hora': str(r.hora)
    } for r in reservas]
    
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )
    
# Obtener una reserva por ID
@bp.route('/<int:id>', methods=['GET'])
def get_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        return Response(
            json.dumps({'error': 'Reserva no encontrada'}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )

    
    usuario = Usuario.query.get(reserva.id_usuario) if reserva.id_usuario else None
    instalacion = Instalacion.query.get(reserva.id_instalacion) if reserva.id_instalacion else None

    
    response_data = {
        'id': reserva.id,
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
        } if instalacion else None,
        'fecha': reserva.fecha.strftime('%Y-%m-%d') if reserva.fecha else None,
        'hora': str(reserva.hora) if reserva.hora else None
    }

    return Response(
        json.dumps(response_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )
    
# Crear una nueva reserva
@bp.route('/', methods=['POST'])
def crear_reserva():
    data = request.get_json()

    if not data or not all(k in data for k in ("id_usuario", "id_instalacion", "fecha", "hora")):
        return jsonify({"error": "Datos incompletos"}), 400

    nueva_reserva = Reserva(
        id_usuario=data["id_usuario"],
        id_instalacion=data["id_instalacion"],
        fecha=data["fecha"],
        hora=data["hora"]
    )

    db.session.add(nueva_reserva)
    db.session.commit()

    return jsonify({"mensaje": "Reserva creada correctamente", "id": nueva_reserva.id}), 201


# Eliminar una reserva por ID
@bp.route('/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'message': 'Reserva eliminada correctamente'}), 200
