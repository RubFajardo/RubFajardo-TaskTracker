from flask import Blueprint, request, jsonify
from api.models import db, User, Task
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt

api = Blueprint('api', __name__)

@api.route("/register", methods=["POST"])
def new_user():

    body = request.get_json()

    if not body.get("username"):
        return jsonify({"error": "el nombre no puede estar vacio"}), 400

    if not body.get("password"):
        return jsonify({"error": "la contraseña no puede estar vacia"}), 400


    coded_password = bcrypt.hashpw(body["password"].encode(), bcrypt.gensalt())

    new_user = User()
    new_user.username = body["username"]
    new_user.password = coded_password.decode()

    db.session.add(new_user)
    db.session.commit()

    return jsonify("usuario registrado"), 200

@api.route("/login", methods=["POST"])
def login():

    body = request.get_json()
    if not body.get("username"):
        return jsonify({"error": "username no valido"}), 400
    if not body.get("password"):
        return jsonify({"error": "Contraseña requerida."}), 400

    user = User.query.filter_by(username=body["username"]).first()
    if user is None:
        return jsonify("usuario no encontrado"), 404

    user_data = user.serialize()

    if not bcrypt.checkpw(body["password"].encode(), user.password.encode()):
        return jsonify("contraseña incorrecta"), 401

    access_token = create_access_token(identity=str(user_data["id"]))
    return jsonify({"token": access_token, "user": user_data}), 200


@api.route("/get_tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(user.get_all_tasks()), 200

@api.route('/add_task', methods=['POST'])
@jwt_required()
def add_task():

    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    body = request.get_json()

    new_task = Task(title=body["title"], done=False, author=user)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"tasks": user.get_all_tasks()}), 200

@api.route('/edit_task/<task_id>', methods=['PUT'])
@jwt_required()
def edit_task(task_id):

    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    body = request.get_json()

    task = db.session.get(Task, task_id)

    task.done = body["done"]

    db.session.commit()

    return jsonify({"tasks": user.get_all_tasks()}), 200

@api.route("/delete_task/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_user(task_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"tasks": user.get_all_tasks()}), 200