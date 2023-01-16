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

from flask import Flask, g, jsonify,render_template, redirect, make_response, request,session as login_session
from flask_cors import CORS
# from flask_httpauth import HTTPBasicAuth
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import BadSignature, SignatureExpired
# from passlib.apps import custom_app_context
from flask import Flask
import os, logging, sys, datetime
from copy import deepcopy
from flask import Flask, flash, redirect, render_template, request, session as login_session, json
# from flask_session import Session 
from tempfile import mkdtemp
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask_sqlalchemy import SQLAlchemy

# from helpers import apology, login_required

# Configure application
app = Flask(__name__)
# app.config["SECRET_KEY"] = "\x87\xa5\xb1@\xe8\xb2r\x0b\xbb&\xf7\xe9\x84-\x17\xdc\xf8\xfc9l7\xbb\xe9q"
# app.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.debug = True
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response

# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')

# auth = HTTPBasicAuth()
CSRF_ENABLED = True
app.debug = True



def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db_conn'):
        g.db_conn = create_conn()
    return g.db_conn

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, bottom=escape(message)), code

@app.route('/',methods=['GET'])
@login_required
def main():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    """
    POST:
        if the user exists, then get the data belonged
        else create user and let him log in
    """
    # login_session.clear()
    if request.method == "POST":

        conn = get_db()
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)
        username = request.form.get("username")
        # Query database for username
        visitor = get_data_by_name(conn,username,'USERS')

        # print(visitor, visitor.id, visitor.hash, file=sys.stderr)

        # Ensure username exists and password is correct
        if not visitor :
            insert_user(conn,username)
            visitor = get_data_by_name(conn,username,'USERS')

        # Add user to login_session
        login_session["uid"] = visitor.id

        # Redirect user to home page
        return redirect("/")
        # return None

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html') 





@app.route('/api/insert-item', methods=['POST'])
@login_required
def insert_item(arg, uid):
    """
    提供物品
        - 接口: add
            - POST
            - 参数: 名称-品牌-描述-数量-是消耗品-标签
              - dict(name:'',brand:'',disc:'',qty:'',is_con:'',label:'')
            - tag由最后一次query得到的物品的tag分析（split by comma）统计成set，保存成变量
            - 返回：HTTP状态
    """
    conn = get_db()
    iid = insert_item(conn, arg)
    if not iid:
        return {'code': 500, 'msg': "添加物品失败"},500
    # sid = insert_share(conn, uid, modi, ddl)
    oid = insert_own(conn, uid, iid)
    if not oid:
        return {'code': 500, 'msg': "添加拥有关系失败"},500
    data = json.loads(arg)
    label = data['name']
    if get_data_by_name(conn, label, 'TAGS'):
        flag = insert_tag(conn, label, iid)
        if flag:
            return {'code': 200, 'msg': "添加成功，已有标签"},200
        return {'code': 500, 'msg': "新建标签失败"},500
    else:
        flag = insert_tag(conn, label, iid)
        if flag:
            return {'code': 200, 'msg': "添加成功，新增标签"},200
        return {'code': 500, 'msg': "新建标签失败"},500
    

@app.route('/api/virtue-query', methods=['POST'])
@login_required
def virtue_query():
    """
    - 查询功德
        - 接口： virtue_query
            - POST
            - 返回： HTTP状态、功德值
    """
    conn = get_db()
    uid = login_session['uid']
    sql = f"select * from VIRTUE where uid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (uid,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from databse')
    return result[1],200

@app.route('/api/virlog', methods=['POST'])
@login_required
def virlog_query():
    """
    - 查询功德日志，实际上是在系统的提供/借用历史记录
        - 接口： virlog_query
            - POST
            - 返回： HTTP状态、功德日志
    """
    conn = get_db()
    sql = f"select * from VIRLOG where uid = %s;"
    uid = login_session['uid']
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (uid,))
            result = cursor.fetchall()
            logger.info(f'select data<{result}> from virlog')
    return [tp[1] for tp in result],200
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

@app.route('/api/items', methods=['POST'])
@login_required
def my_item_list():
    """查询我提供的和正在借出的物品"""
    conn = get_db()
    sql = f"select * from OWN where uid = %s;"
    uid = request.form.get('uid')
    my_item = []
    with conn.cursor() as cursor:
        cursor.execute(sql, (uid,))
        result = cursor.fetchall()
        # print(result)
        for row in result:
            iid = row[2]
            item_info = get_item_by_id(conn, iid)

            tags = get_tag_by_id(conn, item_info[1])
            if tags: item_info['tag']= tags
            borrowing = False
            if get_sharing_by_item_id(conn, iid):
                borrowing=True
            item = {
                'iid':iid,
                'name':item_info[1],
                'brand':item_info[2],
                'description':item_info[3],
                'qty':item_info[4],
                'is_consume':item_info[5],
                'borrowing':borrowing,
                'tag':tags,
            }
            my_item.append(item)
        logger.info(f'select data<{my_item}> from databse')
    return my_item,200

# sid list是sid信息，不展示给用户，但是当用户选择要归还此物品时，需要记录这一物品借出记录的sid并传给return item函数
# 因为sid才是借用的唯一标识（可能存在同一个人同时借用多个同名物品1
@app.route('/api/borrow-list', methods=['POST'])
@login_required
def my_borrow_list():
    """查询我正在借用的物品"""
    conn = get_db()
    sql = f"select * from SHARE where uid = %s;"
    uid = login_session['uid']
    item_info = []
    with conn.cursor() as cursor:
        cursor.execute(sql, (uid,))
        result = cursor.fetchall()
        for row in result: # 
            iid = row[2]
            owner_raw = get_sharing_by_item_id(conn, iid)
            owner_id = owner_raw[1]
            share_id = owner_raw[0]

            # sid_list.append(share_id)
            owner_info = get_user_by_id(conn, owner_id)
            item = get_item_by_id(conn, iid)
            item_info.append({
                'sid':share_id,
                'iid':iid,
                'name':item[1],
                'owner_uid':owner_id,
                'owner_name':owner_info[1],
                'modified':row[4].isoformat(),
                'ddl':row[3].isoformat()
            })
        logger.info(f'select data<{result}> from databse')
    return item_info,200

@app.route('/api/update-item', methods=['POST'])
@login_required
def update_my_item():
    """
    在不改变name的情况下更新物品信息，要求输入所有信息的更新。
    原信息用get_data_by_name函数获得，用户在原基础上修改后，把包括iid的全部表项传入此函数
    """
    conn = get_db()
    data = request.form
    sql = f"update ITEMS BRAND=%s, DESCRIPTION=%s, QTY=%s, IS_CONSUME=%s where iid=%s;"
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, (data['brand'], data['description'], data['quantity'], data['is_'], data[0]))
            result = cursor.fetchone()
            logger.info(f'update data<{result}> to the item')
            conn.commit()
    return {"code":200},200


@app.route('/api/search-item', methods=['POST'])
@login_required
def search_item():
    """fetch data by item_name
    Returns:
        物品信息列表，是否正在借出的列表，1代表借出中
    """
    conn = get_db()
    sql = f"select * from ITEMS where NAME LIKE %%%s%%;"
    item_name: str = request.form.get['name']
    item_info = []
    with conn.cursor() as cursor:
        cursor.execute(sql, (item_name,))
        result = cursor.fetchall()
        for row in result:
            owner = get_owner_by_iid(conn,row[0])
            owner_name = get_user_by_id(conn,owner[1])[1]
            if not get_sharing_by_item_id(conn,row[0]):
                pass
                item_info.append({
                    'iid':row[0],
                    'name':row[1],
                    'owner_id':owner[1],
                    'owner_name':owner_name,
                })
        logger.info(f'select data<{result}> from item')
    return result,200

# 借流程：首先搜索物品，在返回的列表中选择是要借哪一个，把被选中的物品的id传入下面的borrow函数
# borrow函数没有判断是否可借，因为搜索的时候已经返回了可借列表

@app.route('/api/borrow-item', methods=['POST'])
@login_required
def borrow_item():
    """
    记得传入modi最后修改时间和ddl时间，两者都是date格式

    - 搜索借出对象
    - 消耗品：数量-1
    - 更新使用权，除非拥有者自用、消耗品
    - 功德+=2：借给非拥有者
    - 接口：borrow
        - POST
        - 参数: userid
        - 返回：HTTP状态
    """
    conn = get_db()
    uid, iid = login_session['uid'],request.form['iid']
    nw = datetime.now()
    modi, ddl = '-'.join([('0'if s < 10 else '')+str(s) for s in[nw.year,nw.month,nw.day]]),request.form['ddl']
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
        # if qty-1==0:
        #     delete_item(conn, iid, uid)
        #     return {'code': 200, 'msg': "全部借出，物品已删除"}) #这一部分改为借出至剩余0个时由owner来自行决定是补货update还是删除delete
        sql = f"update ITEMS QTY=%s where iid=%s;"
        with conn:
            with conn.cursor() as cursor:
                result = cursor.execute(sql, (qty-1, iid))
                result = cursor.fetchone()
                logger.info(f'update data<{result}> to the databse')
                conn.commit()
    else:
        insert_share(conn, uid, iid, modi, ddl)
    return {"code":200},200


@app.route('/api/return-item', methods=['POST'])
@login_required
def return_item(uid, iid, time):
    """
    先调用my_borrow_list，在页面中供用户选择要归还的项目，并从返回值中获得ownerid和借用的sid
    time是归还时的时间, num是归还数目
    
    可以还的条件：（使用 &&） !拥有
    若是消耗品则不需要归还
    超过最迟归还时间：功德-=2\*
        else 功德 += 1
    接口：return-item
    - param: 对象userid，物品id，数量
    - 返回：HTTP状态
    """
    conn = get_db()
    sid, iid = request.form['sid'],request.form['iid']
    nw = datetime.now()
    time = '-'.join([('0'if s < 10 else '')+str(s) for s in[nw.year,nw.month,nw.day]])
    sql = f"delete from SHARE where sid = %s;"
    sqlget = sql = f"select * from SHARE where sid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sqlget, (sid,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from share')
            ddl = result[4]
            iid = result[2]
            cursor.execute(sql, (sid,))
            logger.info(f'delete data from share by id<{sid}>')
            owner_id = get_owner_by_iid(conn, iid)[1]
            conn.commit()
    if uid==owner_id:
        return {'code': 200, 'msg': "自己借自己的东西并且成功归还"},200
    item_name = get_item_by_id(conn, iid)[1]
    user_name = get_user_by_id(conn, owner_id)[1]
    if ddl>time:
        update_virtue(conn, uid, 1)
        log_content = f'<{str(time)}> 归还<{item_name}> 给 <{user_name}，准时，功德 +1>'
        insert_virlog(conn, uid, log_content)
        return ({'code': 200, 'msg': "成功按时归还"}),200
    update_virtue(conn, uid, -2)
    log_content = f'<{str(time)}> 归还<{item_name}> 给 <{user_name}，超时，功德 -2>'
    insert_virlog(conn, uid, log_content)
    return {'code': 200, 'msg': "借用超时，成功归还"},200


@app.route('/api/delete-item', methods=['POST'])
@login_required
def delete_item():
    """
    - 移出物品
        - 条件：拥有者想要自用、借出消耗品
        - 接口：remove
            - param：物品id，数量
            - 返回：HTTP状态
    """
    conn = get_db()
    iid = request.form['iid']
    uid = login_session['uid']
    if not get_owner_by_iid(conn, iid)[1]==uid:
        return {'code': 500, 'msg': "非物品拥有者，删除失败"},500

    sql1 = f"delete from ITEMS where iid = %s;"
    sql2 = f"delete from TAGS where iid = %s;"
    if get_sharing_by_item_id(conn, iid):
        return {'code': 500, 'msg': "物品正在借出，无法删除"},500
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql1, (iid,))
            logger.info(f'delete data from items by id<{iid}>')
            cursor.execute(sql2, (iid,))
            logger.info(f'delete data from tags by id<{iid}>')
            conn.commit()
    return {'msg': "物品已删除"},200

@app.route('/api/delete-user', methods=['POST'])
@login_required
def delete_user():
    conn = get_db()
    uid = login_session['uid']
    sql = f"delete from USERS where uid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (uid,))
            logger.info(f'delete data from databse by id<{uid}>')
            conn.commit()
    del login_session['uid']
    return redirect('/')

@app.errorhandler(404)
def not_found(_):
    resp = make_response(render_template('error.html'), 404)
    return resp


# print(search_item(conn, "厕所"))

if __name__ == '__main__':
    app.run(host='192.168.0.105:15000')
