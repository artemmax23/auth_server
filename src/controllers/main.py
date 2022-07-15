from flask import jsonify, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from models.model import Users
from user.repository import Repository

db = Repository.connect()

blacklist = set()

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token: dict) -> bool:
    jti = decrypted_token['jti']
    return jti in blacklist


def login():
    name: str = str(request.form['name'])
    password: str = str(request.form['password'])

    user: Users = db.get(name)

    if user is None:
        return jsonify('Такого пользователя не существует!'), 401
    elif user.password != password:
        return jsonify('Неверный пароль!'), 401
    else:
        payload = {
            'id': user.id,
            'name': name
        }
        access_token = create_access_token(identity=payload)
        refresh_token = create_refresh_token(identity=payload)

        return jsonify(access_token=access_token, refresh_token=refresh_token)


@jwt_required(refresh=True)
def refresh():
    identity: dict = get_jwt_identity()
    access_token: str = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@jwt_required(verify_type=False)
def logout():
    token: dict = get_jwt()
    jti: dict = token["jti"]
    ttype: str = token["type"]
    blacklist.add(jti)
    return jsonify({"msg": f"{ttype.capitalize()} token successfully revoked"}), 200
