import redis
import os
import humanfriendly as hf
from datetime import timedelta
from flask import jsonify, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from models.db_interface import DBInterface

from models.model import Users
from flask_jwt_extended import JWTManager
from user.repository import Repository

db: DBInterface = Repository.connect()

jwt_redis_blocklist = redis.StrictRedis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT_NUMBER'),
    db=0,
    decode_responses=True
)

jwt: JWTManager = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti: str = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


def login():
    name: str = str(request.form['name'])
    password: str = str(request.form['password'])

    user: Users = db.get(name)

    if user is None:
        return jsonify('Такого пользователя не существует!'), 401
    elif user.password != password:
        return jsonify('Неверный пароль!'), 401
    else:
        payload: dict = {
            'id': user.id,
            'name': name
        }
        access_token: str = create_access_token(identity=payload)
        refresh_token: str = create_refresh_token(identity=payload)

        return jsonify(access_token=access_token, refresh_token=refresh_token)


@jwt_required(refresh=True)
def refresh():
    identity: dict = get_jwt_identity()
    access_token: str = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@jwt_required(verify_type=False)
def logout():
    token: dict = get_jwt()
    jti: str = token["jti"]
    ttype: str = token["type"]
    jwt_redis_blocklist.set(jti, "", ex=timedelta(seconds=
                                                  hf.parse_timespan(os.getenv('ACCESS_LIFETIME', '30m'))))
    return jsonify({"msg": f"{ttype.capitalize()} token successfully revoked"}), 200
