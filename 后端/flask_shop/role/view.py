from flask_shop import role
from flask_shop.role import role_api, role_bp
from flask_shop import modles, db
from flask import request
from flask_restful import Resource
from utils.messages import to_dict_msg


class Role(Resource):
    def get(self):
        role_list = []
        try:
            roles = modles.Role.query.all()
            role_list = [r.to_dict() for r in roles]
            return to_dict_msg(200, data=role_list,msg='获取角色列表成功！！')
        except Exception as e:
            return to_dict_msg(20000)
    
    def post(self):
        name = request.form.get('name')
        desc = request.form.get('desc')
        try:
            if name:
                role =modles.Role(name =name ,desc = desc)
                db.session.add(role)
                db.session.commit()
                return to_dict_msg(200,msg='增加角色成功！！')
            return to_dict_msg(10000)
        except Exception as e:
            print(e)
            return to_dict_msg(20000)

    def delete(self):
        try:
            id = int(request.form.get('id'))
            r = modles.Role.query.get(id)
            if r: # 是否找到？
                db.session.delete(r)
                db.session.commit()
                return to_dict_msg(200,msg='删除角色成功！！')
            return to_dict_msg(10000)
        except Exception as e:
            return to_dict_msg(20000)
    def put(self):
        try:
            id = int(request.form.get('id'))
            name =request.form.get('name').strip() if request.form.get('name') else ''
            desc =request.form.get('desc').strip() if request.form.get('desc') else ''
            if name:
                r = modles.Role.query.get(id)
                if r:
                    r.name = name
                    r.desc = desc
                    db.session.commit()
                    return to_dict_msg(200,msg='修改角色信息成功！！！')
                return to_dict_msg(10020)
            return to_dict_msg(10000)
        except Exception as e:
            return to_dict_msg(20000)
      

role_api.add_resource(Role, '/role')

@role_bp.route('/del_menu/<int:rid>/<int:mid>')
def del_menu(rid,mid):
    try:
        r = modles.Role.query.get(rid)
        m = modles.Menu.query.get(mid)
        if all([r,m]):
            if m in r.menus:
                r.menus.remove(m)
                if m.level ==1:
                    for temp_m in m.children:   # 获取删除当前根节点所有子节点
                        if temp_m in r.menus:   # 判断当前子节点是在当前权限
                            r.menus.remove(temp_m)
                db.session.commit()
                return to_dict_msg(200,data=r.get_menu_dict(),msg='删除权限成功！')
            return to_dict_msg(10021)
        return to_dict_msg(10000)
    except Exception as e:
        print(e)
        return to_dict_msg(20000)

@role_bp.route('/set_menu/<int:rid>',methods=['POST'])
def set_menu(rid):
    try:
        role = modles.Role.query.get(rid)
        mids = request.form.get('mids')
        if role:
            role.menus = []
            for m in mids.split(','):
                if m:
                    temp_menu = modles.Menu.query.get(int(m))
                    if temp_menu:
                        role.menus.append(temp_menu)
            db.session.commit()
            return to_dict_msg(200,msg='分配权限成功！！')
        return to_dict_msg(10020)
    except Exception as e:
        print(e)
        return to_dict_msg(20000)