from flask import Blueprint

from controllers.main import login, refresh, logout

main_bp = Blueprint('main_bp', __name__)

main_bp.route("/login/", methods=['POST'])(login)
main_bp.route("/refresh/", methods=['POST'])(refresh)
main_bp.route("/logout/", methods=['DELETE'])(logout)
