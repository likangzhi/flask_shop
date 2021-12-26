from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import config_

db = SQLAlchemy()
def create_app(config_name):
    app = Flask(__name__)
    obj = config_.config_map.get(config_name)
    app.config.from_object(obj)
    db.init_app(app)

    from flask_shop.user import user_bp
    app.register_blueprint(user_bp)

    from flask_shop.menu import menu_bp
    app.register_blueprint(menu_bp)

    from flask_shop.role import role_bp
    app.register_blueprint(role_bp)

    from flask_shop.category import category_bp, attribute_bp
    app.register_blueprint(category_bp)
    app.register_blueprint(attribute_bp)

    from flask_shop.goods import good_bp
    app.register_blueprint(good_bp)

    from flask_shop.order import order_bp
    app.register_blueprint(order_bp)

    return app 


