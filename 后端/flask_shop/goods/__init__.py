from flask import Blueprint
from flask_restful import Api

good_bp = Blueprint('good', __name__)
good_api = Api(good_bp)

from flask_shop.goods import view