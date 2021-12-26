from flask import Blueprint
from flask_restful import Api

role_bp = Blueprint('role', __name__)
role_api = Api(role_bp)

from flask_shop.role import view
