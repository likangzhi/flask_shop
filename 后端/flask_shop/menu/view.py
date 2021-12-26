from flask_shop.menu import menu_api
from flask_shop import modles, db
from flask import request
from flask_restful import Resource
from utils.messages import to_dict_msg

class Menu(Resource):
    def get(self):
        menu_list = []
        type__ = request.args.get('type')
        if type__ == 'list':
            mu = modles.Menu.query.filter(modles.Menu.level != 0).all()
            for m in mu:
                menu_list.append(m.to_dict())
        else:
            mu = modles.Menu.query.filter(modles.Menu.level == 1).all()
            for m in mu:
                first_mu = m.to_dict()
                first_mu['children'] = []
                for sm in m.children:
                    secd_dict = sm.to_dict()
                    secd_dict['children'] = sm.get_child_list()
                    first_mu['children'].append(secd_dict)
                menu_list.append(first_mu) 
        return to_dict_msg(200, data=menu_list)

menu_api.add_resource(Menu, '/menu')
