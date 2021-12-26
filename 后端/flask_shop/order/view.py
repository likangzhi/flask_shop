from flask_shop.order import order_api, order_bp
from flask_shop import modles, db
from flask import request
from flask_restful import Resource
from utils.messages import to_dict_msg


@order_bp.route('/order_list')
def order_list():
    try:
        id = request.args.get('id')
        if id:
            order = modles.Order.query.get(id)
            if order:
                return to_dict_msg(200, data=order.to_dict(), msg='获取订单成功')
            else:
                return to_dict_msg(10022)
        else:
            orders = modles.Order.query.all()
            return to_dict_msg(200, data=[o.to_dict() for o in orders], msg='获取订单列表成功')
    except Exception:
        return to_dict_msg(20000)


@order_bp.route('/express')
def get_express():
    try:
        oid = request.args.get('oid')
        if oid:
            exps = modles.Express.query.filter(modles.Express.oid == oid).order_by(
                modles.Express.update_time.desc())
            return to_dict_msg(200, [e.to_dict() for e in exps])
        else:
            return to_dict_msg(10000)
    except Exception as e:
        print(e)
        return to_dict_msg(20000)
