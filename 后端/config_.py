import os

class Config():
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'shop_env'
    USERNAME = 'root'
    PASSWORD = 'root'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf' \
            '8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(18)
    
    ALLOWED_IMG = set(['bmp', 'jpg', 'jpeg', 'png', 'gif'])
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVER_IMG_UPLOAD = os.path.join(BASE_DIR, 'flask_shop','static', 'img')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

config_map={
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}