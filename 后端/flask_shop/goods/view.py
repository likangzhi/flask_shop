from flask_shop.goods import good_api, good_bp
from flask_shop import modles, db
from flask import request, current_app
from flask_restful import Resource
from utils.messages import to_dict_msg
import hashlib
from time import time


@good_bp.route('/goods_list')
def get_goods_list():
    try:
        name = request.args.get('name')
        if name:
            goods = modles.Goods.query.filter(modles.Goods.name.like(f"%{name}%")).all()
        else:
            goods = modles.Goods.query.all()
        goods_list = [g.to_dict() for g in goods]
        return to_dict_msg(200, data=goods_list, msg="获取商品列表成功!!")
    except Exception:
        return to_dict_msg(20000)


class Goods(Resource):
    def post(self):
        try:
            attr_dynamic = request.form.get('attr_dynamic')
            attr_static = request.form.get('attr_static')
            pics = request.form.get('pics')

            cid_one = request.form.get('cid_one')
            cid_three = request.form.get('cid_three')
            cid_two = request.form.get('cid_two')
            introduce = request.form.get('introduce')
            name = request.form.get('name')
            number = request.form.get('number')
            price = request.form.get('price')
            weight = request.form.get('weight')

            goods = modles.Goods(name=name, number=number, price=price,
                          weight=weight, introduce=introduce,
                          cid_one=int(cid_one), cid_two=int(cid_two), cid_three=int(cid_three))
            db.session.add(goods)
            db.session.commit()

            for p in eval(pics):
                tp = modles.Picture(gid=goods.id, path=p)
                db.session.add(tp)
            for s in eval(attr_static):
                temp_s = modles.GoodsAttr(gid=goods.id, aid=s.get(
                    'id'), val=s.get('val'), _type='static')
                db.session.add(temp_s)
            for d in eval(attr_dynamic):
                temp_d = modles.GoodsAttr(gid=goods.id, aid=d.get(
                    'id'), val=d.get('val'), _type="dynamic")
                db.session.add(temp_d)
            db.session.commit()
            return to_dict_msg(200, msg="增加商品成功！！")
        except Exception as e:
            print(e)
            return to_dict_msg(20000)


    def delete(self):
        try:
            id = request.json.get('id')
            good = modles.Goods.query.get(id)
            if good:
                db.session.delete(good)
                db.session.commit()
                return to_dict_msg(200, msg="删除商品成功!!")
            return to_dict_msg(10022)
        except Exception:
            return to_dict_msg(20000)

good_api.add_resource(Goods, '/goods')


@good_bp.route('/upload_img', methods=['POST'])
def upload_img():
    img_files = request.files.get('file')
    if not img_files:
        return to_dict_msg(10023)
    if allowed_img(img_files.filename):
        folder = current_app.config.get('SERVER_IMG_UPLOAD')
        end_profix = img_files.filename.rsplit('.', 1)[1]
        file_name = md5_file()

        img_files.save(f'{folder}/{file_name}.{end_profix}')
        data = {
            'path': f'static/img/{file_name}.{end_profix}',
            'url': f'http://127.0.0.1:5000/static/img/{file_name}.{end_profix}'
        }
        return to_dict_msg(200, data=data, msg='上传图片成功！！！')


def allowed_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_IMG']


def md5_file():
    md5_obj = hashlib.md5()
    md5_obj.update(str(time()).encode())
    file_name = md5_obj.hexdigest()
    return file_name