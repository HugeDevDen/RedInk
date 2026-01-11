from flask import Blueprint, request, jsonify
from backend.config import Config
from backend.utils.auth_utils import generate_token


def create_auth_blueprint():
    bp = Blueprint("auth", __name__)

    @bp.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        if not data:
            return jsonify({"error": "请提供账号和密码"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "账号和密码不能为空"}), 400

        if username == Config.LOGIN_USERNAME and password == Config.LOGIN_PASSWORD:
            token = generate_token(username)
            return jsonify({"success": True, "token": token, "username": username}), 200
        else:
            return jsonify({"error": "账号或密码错误"}), 401

    @bp.route("/verify", methods=["GET"])
    def verify():
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"valid": False}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"valid": False}), 401

        from backend.utils.auth_utils import verify_token

        payload = verify_token(token)

        if payload:
            return jsonify({"valid": True, "username": payload.get("username")}), 200
        else:
            return jsonify({"valid": False}), 401

    return bp
