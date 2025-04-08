from flask import Blueprint, jsonify, json, Response, request
from db import db
from models import Instalacion

bp = Blueprint('instalaciones', __name__, url_prefix='/instalaciones')

#Obtener todas las instalaciones
@bp.route('/', methods=['GET'])
def get_instalaciones():
    instalaciones = Instalacion.query.all()
    data = [{
        'id': i.id,
        'nombre': i.nombre,
        'foto': i.foto,
        'categoria': i.categoria,
        'disponibilidad': i.disponibilidad
    } for i in instalaciones]
    
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )
    

# Obtener una instalación por ID
@bp.route('/<int:id>', methods=['GET'])
def get_instalacion(id):
    instalacion = Instalacion.query.get(id)
    
    if not instalacion:
        return Response(
            json.dumps({'error': 'Instalación no encontrada'}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )
    
    instalacion_data = {
        'id': instalacion.id,
        'nombre': instalacion.nombre,
        'foto': instalacion.foto,
        'categoria': instalacion.categoria,
        'disponibilidad': instalacion.disponibilidad
    }
    
    return Response(
        json.dumps(instalacion_data, ensure_ascii=False),
        status=200,
        mimetype='application/json; charset=utf-8'
    )
    
    
# Crear una nueva instalación
@bp.route('/', methods=['POST'])
def create_instalacion():
    data = request.get_json()

    if not data or not all(key in data for key in ["nombre", "categoria", "disponibilidad"]):
        return jsonify({"error": "Datos incompletos"}), 400

    nueva_instalacion = Instalacion(
        nombre=data["nombre"],
        categoria=data["categoria"],
        disponibilidad=data["disponibilidad"]
    )

    db.session.add(nueva_instalacion)
    db.session.commit()

    return jsonify({"message": "Instalación creada exitosamente", "id": nueva_instalacion.id}), 201


# Actualizar una instalación por ID
@bp.route('/<int:id>', methods=['PUT'])
def actualizar_instalacion(id):
    data = request.get_json()
    instalacion = Instalacion.query.get(id)

    if not instalacion:
        return jsonify({"error": "Instalación no encontrada"}), 404

    if "nombre" in data:
        instalacion.nombre = data["nombre"]
    if "categoria" in data:
        instalacion.categoria = data["categoria"]
    if "disponibilidad" in data:
        instalacion.disponibilidad = data["disponibilidad"]

    db.session.commit()
    return jsonify({"mensaje": "Instalación actualizada correctamente"}), 200


# Eliminar una instalación por ID
@bp.route('/<int:id>', methods=['DELETE'])
def delete_instalacion(id):
    instalacion = Instalacion.query.get(id)
    if not instalacion:
        return jsonify({'error': 'Instalación no encontrada'}), 404
    db.session.delete(instalacion)
    db.session.commit()
    return jsonify({'message': 'Instalación eliminada correctamente'}), 200
