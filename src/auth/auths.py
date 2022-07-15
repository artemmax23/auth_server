import jwt
from datetime import datetime, timedelta

secret_key = "123"
algorithm = 'HS256'
jwt_minutes = 10


class Auth:

    @staticmethod
    def encode_jwt(username: str, password: str) -> str:
        payload = {
            'name': username,
            'password': password,
            'exp': datetime.now() + timedelta(minutes=jwt_minutes)
        }

        return jwt.encode(payload, secret_key, algorithm)

    @staticmethod
    def decode_jwt(token: str) -> str:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
