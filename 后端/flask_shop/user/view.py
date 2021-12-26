from flask_shop.user import user_bp, user_api
from flask_shop import modles, db
from flask import request
from flask_restful import Resource, reqparse
import re
from utils.messages import to_dict_msg
from utils.tokens import generate_auth_token, verify_auth_token, login_required
from flask_shop.modles import User


@user_bp.route('/')
def index():
    return 'User hello!!!'


class User1(Resource):
    def get(self):
        try:
            id = int(request.args.get('id').strip())
            usr = modles.User.query.filter_by(id = id).first()
            if usr:
                return to_dict_msg(200, usr.to_dict(), '获取用户成功')
            else:
                return to_dict_msg(200, [], '没有此用户')
        except Exception:
            return to_dict_msg(10000) 

    def post(self):
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        real_pwd = request.form.get('real_pwd')
        nick_name = request.form.get('nick_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        uid = request.form.get('uid')
        print(name, pwd, real_pwd)
        if not all([name, pwd, real_pwd]):
            return to_dict_msg(10000)
        if len(name) < 2:
            return to_dict_msg(10011)
        if len(pwd) < 2:
            return to_dict_msg(10012)
        if pwd != real_pwd:
            return to_dict_msg(10013)
        if not re.match(r'1[3578]\d{9}', phone):
            return to_dict_msg(10014)
        if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return to_dict_msg(10015)
        try:
            uid = int(request.form.get('role_name').strip()) if request.form.get('role_name') else 0
            usr = User(name=name, password= pwd,nick_name=nick_name, phone=phone, email=email, uid=uid)
            db.session.add(usr)
            db.session.commit()
            return {'status': 200, 'msg': '成功'}
        except Exception as f:
            return to_dict_msg(20000)

    def put(self):
        try:
            id = int(request.form.get('id').strip())
            email = request.form.get('email').strip() if request.form.get('email') else ''
            phone = request.form.get('phone').strip() if request.form.get('phone') else ''
            uid = int(request.form.get('role_name').strip()) if request.form.get('role_name') else 0
            usr = modles.User.query.get(id)
            if usr:
                usr.email = email
                usr.phone = phone
                usr.uid = uid
                db.session.commit()
                return to_dict_msg(200, '修改数据成功！')
            else:
                return to_dict_msg(10018)
        except Exception as e:
            print(e)
            return to_dict_msg(10000)

    def delete(self):
        try:
            id = request.json.get('id')
            usr = modles.User.query.get(id)
            if usr:
                db.session.delete(usr)
                db.session.commit()
                return to_dict_msg(200, '删除用户成功!')
            else:
                return to_dict_msg(10019)
        except Exception:
            return to_dict_msg(20000)

user_api.add_resource(User1, '/user')

class UserList(Resource):
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('name', type=str)
        parse.add_argument('pnum', type=int)
        parse.add_argument('psize', type=int)
        try:
            args = parse.parse_args()
            name = args.get('name') 
            pnum = args.get('pnum') if args.get('pnum') else 1
            psize = args.get('psize') if args.get('psize') else 2
            if name:
                user_p = modles.User.query.filter(modles.User.name.like(f'%{name}%')).paginate(pnum, psize)
            else:
                user_p = modles.User.query.paginate(pnum, psize)
            data = {
                'pnum': pnum,
                'totalPage': user_p.total,
                'users': [ u.to_dict() for u in user_p.items]
            }
            return to_dict_msg(200, data, '获取用户列表成功')
        except Exception:
            return to_dict_msg(20000)

user_api.add_resource(UserList, '/user_list')

@user_bp.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    pwd = request.form.get('pwd')

    if not all([name, pwd]):
        return {'status': 10000, 'msg': '数据不完整'}
    if len(name) > 1:
        user = modles.User.query.filter_by(name=name).first()
        if user:
            if user.check_password(pwd):
                token = generate_auth_token(user.id, 20000)
                verify_auth_token(token)
                return to_dict_msg(200, data={'token': token})
    return {'status': 10001, 'msg': '用户名或密码错误'}

@user_bp.route('/reset', methods=["GET"])
def reset():
    try:
        id = int(request.args.get('id'))
        urs = modles.User.query.get(id)
        urs.password = "123"
        db.session.commit()
        return to_dict_msg(200, msg='修改密码成功')
    except Exception:
        return to_dict_msg(20000)

@user_bp.route('/test/')
@login_required
def tset_login_req():
    return to_dict_msg(200)
    