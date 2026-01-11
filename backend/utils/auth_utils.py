from functools import wraps
from flask import request, jsonify
from backend.config import Config
import jwt


def generate_token(username: str) -> str:
    payload = {"username": username}
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "未提供认证令牌"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"error": "认证令牌格式错误"}), 401

        payload = verify_token(token)
        if payload is None:
            return jsonify({"error": "认证令牌无效或已过期"}), 401

        request.environ["user"] = payload
        return f(*args, **kwargs)

    return decorated_function
