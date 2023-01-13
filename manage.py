#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-30 20:53:54
# @Author  : Bayi
# @Link    : https://blog.flywinky.top/

import os
import re
import json
from datetime import datetime
from function import *

from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context
from flask_vite import Vite

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')

db = SQLAlchemy(app)
auth = HTTPBasicAuth()
CSRF_ENABLED = True
app.debug = True


class JoinInfos(db.Model):
    __tablename__ = 'joininfos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phone = db.Column(db.String(30))
    profess = db.Column(db.String(64))
    grade = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True)
    group = db.Column(db.String(64))
    power = db.Column(db.Text(2000))
    pub_date = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key == 'pub_date':
                value = getattr(self, key).strftime("%Y-%m-%d %H:%M:%S")
            else:
                value = getattr(self, key)
            result[key] = value
        return result


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))

    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    # 密码解析
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    # 获取token，有效时间10min
    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        admin = Admin.query.get(data['id'])
        return admin

# name: /[\u4e00-\u9fa5]/
# phone: /^1[34578]\d{9}$/
# class: /[a-zA-Z0-9_\u4e00-\u9fa5]+/
# email: /^\w+@\w+\.\w+$/


# @app.route("/joinus", methods=['POST'])
# def joinus():
#     data = request.get_json(force=True)
#     # data = {'InfoName': '折蓉蓉', 'InfoPho': '13466777707','InfoProfess': '数学学院','InfoCls': '大一','InfoEmail':
#     # '266455@qq.com', 'InfoGroup': ['移动', '运营'], 'InfoPower': '测试'}
#     if data:
#         addGroup = ",".join(data['InfoGroup'])
#         addInfos = JoinInfos(
#             name=data['InfoName'],
#             phone=data['InfoPho'],
#             profess=data['InfoProfess'],
#             grade=data['InfoCls'],
#             email=data['InfoEmail'],
#             group=addGroup,
#             power=data['InfoPower']
#         )
#         db.session.add(addInfos)
#         db.session.commit()
#         return jsonify({"status": True})
#     else:
#         return jsonify({"status": False})


@auth.verify_password
def verify_password(name_or_token, password):
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    admin = Admin.verify_auth_token(name_or_token)
    if not admin:
        admin = Admin.query.filter_by(name=name_or_token).first()
        if not admin or not admin.verify_password(password):
            return False
    g.admin = admin
    return True


@app.route('/api/login', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.admin.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin.name})


@app.route('/api/setpwd', methods=['POST'])
@auth.login_required
def set_auth_pwd():
    data = json.loads(str(request.data, encoding="utf-8"))
    admin = Admin.query.filter_by(name=g.admin.name).first()
    if admin and admin.verify_password(data['oldpass']) and data['confirpass'] == data['newpass']:
        admin.hash_password(data['newpass'])
        return jsonify({'code': 200, 'msg': "密码修改成功"})
    else:
        return jsonify({'code': 500, 'msg': "请检查输入"})


@app.route('/api/users/listpage', methods=['GET'])
@auth.login_required
def get_user_list():
    page_size = 4
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '')
    query = db.session.query
    if name:
        Infos = query(JoinInfos).filter(
            JoinInfos.name.like('%{}%'.format(name)))
    else:
        Infos = query(JoinInfos)
    total = Infos.count()
    if not page:
        Infos = Infos.all()
    else:
        Infos = Infos.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'code': 200,
        'total': total,
        'page_size': page_size,
        'infos': [u.to_dict() for u in Infos]
    })


@app.route('/api/user/remove', methods=['GET'])
@auth.login_required
def remove_user():
    remove_id = request.args.get('id', type=int)
    if remove_id:
        remove_info = JoinInfos.query.get_or_404(remove_id)
        db.session.delete(remove_info)
        return jsonify({'code': 200, 'msg': "删除成功"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})


@app.route('/api/user/batchremove', methods=['GET'])
@auth.login_required
def batchremove_user():
    remove_ids = request.args.get('ids')
    is_current = False
    if remove_ids:
        for remove_id in remove_ids:
            remove_info = JoinInfos.query.get(remove_id)
            if remove_info:
                is_current = True
                db.session.delete(remove_info)
            else:
                pass
        print(remove_ids, remove_info)
        if is_current:
            return jsonify({'code': 200, 'msg': "删除成功"})
        else:
            return jsonify({'code': 404, 'msg': "请正确选择"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})


@app.route('/api/getdrawPieChart', methods=['GET'])
@auth.login_required
def getdrawPieChart():
    query = db.session.query
    Infos = query(JoinInfos)
    total = Infos.count()
    data_value = [0, 0, 0, 0, 0, 0, 0]  # 和下面组别一一对应
    group_value = ['视觉', '视频', '前端', '办公', '后端', '运营', '移动']
    for info in Infos:
        for num in range(0, 7):
            if group_value[num] in info.group:
                data_value[num] += 1
            else:
                pass
    return jsonify({'code': 200, 'value': data_value, 'total': total})


@app.route('/api/getdrawLineChart', methods=['GET'])
@auth.login_required
def getdrawLineChart():
    grade_value = []  # 年级汇总
    profess_value = []  # 学院汇总
    grade_data = {}  # 年级各学院字典
    Infos = JoinInfos.query.all()
    for info in Infos:
        if info.grade not in grade_value:
            grade_value.append(info.grade)
            grade_data[info.grade] = []
        if info.profess not in profess_value:
            profess_value.append(info.profess)
    for grade in grade_value:
        for profess in profess_value:
            grade_data[grade].append(0)
    for info in Infos:
        for grade in grade_value:
            for profess_local_num in range(0, len(profess_value)):
                if info.profess == profess_value[profess_local_num] and info.grade == grade:
                    grade_data[grade][profess_local_num] += 1
                else:
                    pass
    return jsonify({'code': 200, 'profess_value': profess_value, 'grade_value': grade_value, 'grade_data': grade_data})


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

#---------------------------------以下是功能接口---------------------------------

@app.route('/api/insert-item', methods=['GET'])
@auth.login_required
def provide_item(conn, arg, uid):
    """
    - 提供物品(insert)
        - 接口: add
            - POST
            - 参数: 名称-品牌-描述-数量-是消耗品-标签
              - dict(name:'',brand:'',disc:'',qty:'',is_con:'',label:'')
            - tag由最后一次query得到的物品的tag分析（split by comma）统计成set，保存成变量
            - 返回：HTTP状态
    """
    iid = insert_item(conn, arg)
    if not iid:
        return json.dumps({'code': 500, 'msg': "添加物品失败"})
    # sid = insert_share(conn, uid, modi, ddl)
    oid = insert_own(conn, uid, iid)
    if not oid:
        return json.dumps({'code': 500, 'msg': "添加拥有关系失败"})
    data = json.loads(arg)
    label = data['name']
    if get_data_by_name(conn, label, 'CLASSIFY'):
        return json.dumps({'code': 200, 'msg': "添加成功，已有标签"})
    if not insert_classify(conn, label, iid):
        return json.dumps({'code': 500, 'msg': "新建标签失败"})
    return json.dumps({'code': 200, 'msg': "添加成功，新增标签"})

@app.route('/api/virtue-query', methods=['GET'])
@auth.login_required
def virtue_query(conn, uid):
    """
    - 查询功德
        - 接口： virtue_query
            - POST
            - 返回： HTTP状态、功德值
    """
    sql = f"select * from VIRTUE where uid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (uid,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from databse')
    return json.dumps({'code': 200, 'virtue': result[1]})

@app.route('/api/virlog-query', methods=['GET'])
@auth.login_required
def virlog_query(conn, uid):
    """
    - 查询功德日志，实际上是在系统的提供/借用历史记录
        - 接口： virlog_query
            - POST
            - 返回： HTTP状态、功德日志
    """
    sql = f"select * from VIRLOG where uid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (uid,))
            result = cursor.fetchall()
            logger.info(f'select data<{result}> from virlog')
    return json.dumps({'code': 200, 'virtue log': result})
# - 查询物品
#   - 正在借用
#   - 所拥有
#     - 移出
#     - 借出
#   - 接口：index、query
#     - GET(index)、POST(query)
#     - 参数: tag
#       - 文本
#       - comma separated
#     - 返回：状态，一串表项（表项内容如下：）
#       - 状态：剩余n1,借出n2
#         借用中，剩余(时间长)
#       - 名称-品牌-描述-数量-是消耗品-标签
#       - 查询物品返回的状态是字符串，可以是“拥有n1个，已借出n2个”，“借用n个，还剩[还可使用时间]“

@app.route('/api/items', methods=['GET'])
@auth.login_required
def my_item_list(conn, uid):
    """查询我提供的和正在借出的物品"""
    sql = f"select * from OWN where uid = %s;"
    my_item = []
    borrowing_item = [] # 一串0和1， 1代表对应物品正在借出
    with conn.cursor() as cursor:
        cursor.execute(sql, (uid,))
        result = cursor.fetchall()
        # print(result)
        for row in result:
            iid = row[2]
            item_info = get_item_by_id(conn, iid)
            my_item.append(item_info)
            if get_sharing_by_item_id(conn, iid):
                borrowing_item.append(1)
            else:
                borrowing_item.append(0)
        logger.info(f'select data<{my_item}> from databse')
    return json.dumps({'code': 200, 'My item': my_item, 'is borrowing': borrowing_item})

@app.route('/api/borrow-list', methods=['GET'])
@auth.login_required
def my_borrow_list(conn, uid):
    """查询我正在借的物品"""
    sql = f"select * from SHARE where uid = %s;"
    item_info = []
    owner_info = []
    start_time = []
    ddl = []
    time_remain = []
    with conn.cursor() as cursor:
        cursor.execute(sql, (uid,))
        result = cursor.fetchall()
        for row in result:
            iid = row[2]
            owner_raw = get_sharing_by_item_id(conn, iid)
            owner_id = owner_raw[1]
            owner_info.append(get_user_by_id(conn, owner_id))
            item_info.append(get_item_by_id(conn, iid))
            start_time.append(str(row[3]))
            ddl.append(str(row[4]))
            time_remain.append(str(row[4] - row[3]))
        logger.info(f'select data<{result}> from databse')
    return json.dumps({'code': 200, 'borrow item list': item_info, 'owner': owner_info, 'borrow start from':start_time, 'ddl': ddl, 'time remain':time_remain})

@app.route('/api/update-item', methods=['GET'])
@auth.login_required
def update_my_item(conn, arg):
    """
    在不改变name的情况下更新物品信息，要求输入所有信息的更新。
    原信息用get_data_by_name函数获得，用户在原基础上修改后，把包括iid的全部表项传入此函数
    """
    data = json.loads(arg)
    sql = f"update ITEMS BRAND=%s, DESCRIPTION=%s, QTY=%s, IS_CONSUME=%s where iid=%s;"
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, (data[2], data[3], data[4], data[5], data[0]))
            result = cursor.fetchone()
            logger.info(f'update data<{result}> to the item')
            conn.commit()

@app.route('/api/update-virtue', methods=['POST'])
@auth.login_required
def update_virtue(conn, uid, num):
    """
    num是功德改变量，若减去则为负
    """
    sql = f"select * from VIRTUE where uid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (uid,))
            virtue_old = cursor.fetchone()[1]
            logger.info(f'select data<{virtue_old}> from virtue')

    sql = f"update VIRTUE VIRTUE=%s where uid=%s;"
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, (virtue_old + num, uid))
            result = cursor.fetchone()
            logger.info(f'update data<{result}> to the virtue')
            conn.commit()

@app.route('/api/search-item', methods=['POST'])
@auth.login_required
def search_item(conn, item_name: str):
    """fetch data by item_name

    Args:
        conn ([type]): the connection object

    Returns:
        物品信息列表，是否正在借出的列表，1代表借出中
    """
    sql = f"select * from ITEMS where NAME = %s;"
    item_info = []
    is_borrowing = []
    with conn.cursor() as cursor:
        cursor.execute(sql, (item_name,))
        result = cursor.fetchall()
        for row in result:
            item_info.append(row)
            if get_sharing_by_item_id(conn,row[0]):
                is_borrowing.append(1)
            else:
                is_borrowing.append(0)
        logger.info(f'select data<{result}> from item')
    return json.dumps({'code': 200, "item info" :result, 'borrow state':is_borrowing})

# 借流程：首先搜索物品，在返回的列表中选择是要借哪一个，把被选中的物品的id传入下面的borrow函数
# borrow函数没有判断是否可借，因为搜索的时候已经返回了可借列表

@app.route('/api/borrow-item', methods=['GET'])
@auth.login_required
def borrow_item(conn, uid, iid, modi, ddl):
    """
    记得传入modi最后修改时间和ddl时间，两者都是date格式
    - 借
        - 搜索借出对象
        - 消耗品：数量-1
        - 可以借：
        - 更新使用权，除非拥有者自用、消耗品
        - 功德+=2：借给非拥有者
        - 接口：borrow
            - POST
            - 参数: userid
            - 返回：HTTP状态
    """
    data = get_item_by_id(conn, iid)
    is_consume = data[5]
    qty = data[4]
    owner_id = get_owner_by_iid(conn, iid)[1]
    if not owner_id == uid:
        update_virtue(conn, owner_id, 2)
        item_name = get_item_by_id(conn, iid)[1]
        user_name = get_user_by_id(conn, uid)[1]
        log_content = f'<{str(modi)}> 借出<{item_name}> 给 <{user_name}>'
        insert_virlog(conn, owner_id, log_content)
    if is_consume: #消耗品
        sql = f"update ITEMS QTY=%s where iid=%s;"
        with conn:
            with conn.cursor() as cursor:
                result = cursor.execute(sql, (qty-1, iid))
                result = cursor.fetchone()
                logger.info(f'update data<{result}> to the databse')
                conn.commit()
    else:
        insert_share(conn, uid, iid, modi, ddl)


@app.route('/api/return-item', methods=['GET'])
@auth.login_required
def return_item(conn, uid, iid, time):
    """
    - 还
        - 可以还的条件：（使用 &&） !拥有
        - 若是消耗品则不需要归还
        - 超过最迟归还时间：功德-=2\*
            else 功德 += 1
        - 接口：return-item
            - param: 对象userid，物品id，数量
            - 返回：HTTP状态
    """

@app.route('/api/delete-item', methods=['GET'])
@auth.login_required
def delete_item(conn, iid):
    """
    - 移出物品
        - 条件：拥有者想要自用、借出消耗品
        - 接口：remove
            - param：物品id，数量
            - 返回：HTTP状态
    """
    sql1 = f"delete from ITEMS where iid = %s;"
    sql2 = f"delete from CLASSIFY where iid = %s;"
    if get_sharing_by_item_id(conn, iid):
        return json.dumps({'code': 500, 'msg': "物品正在借出，无法删除"})
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql1, (iid,))
            logger.info(f'delete data from items by id<{iid}>')
            cursor.execute(sql2, (iid,))
            logger.info(f'delete data from classify by id<{iid}>')
            conn.commit()
    return json.dumps({'code': 200, 'msg': "物品已删除"})

@app.route('/api/borrow-item', methods=['GET'])
@auth.login_required
def delete_user(conn, uid):
    sql = f"delete from USERS where uid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (uid,))
            logger.info(f'delete data from databse by id<{uid}>')
            conn.commit()
    return json.dumps({'code': 200, 'msg': "用户已删除"})

conn = create_conn()

print(search_item(conn, "厕所"))

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')