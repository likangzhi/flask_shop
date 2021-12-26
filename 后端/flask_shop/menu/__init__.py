from flask import Blueprint
from flask_restful import Api

menu_bp = Blueprint('menu', __name__)
menu_api = Api(menu_bp)

from flask_shop.menu import view
