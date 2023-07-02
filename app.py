import os
import re
import json
from datetime import datetime,date
from function import *

from flask import Flask, g, jsonify,request,json
from flask_cors import CORS
# from flask_httpauth import HTTPBasicAuth
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import BadSignature, SignatureExpired
# from passlib.apps import custom_app_context
from flask import Flask
import os, datetime
from flask_session import Session 
from tempfile import mkdtemp
from contextlib import closing
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask_sqlalchemy import SQLAlchemy



IS_FRONTEND_DEBUG = os.path.exists('is_fusen.env') # DEBUG: to disable database usage
# Configure SQLite database
db=None



# Configure application
CSRF_ENABLED = True
app = Flask(__name__)
app.config["SECRET_KEY"] = "\x87\xa5\xb1@\xe8\xb2r\x0b\xbb&\xf7\xe9\x84-\x17\xdc\xf8\xfc9l7\xbb\xe9q"
app.debug = True





# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_USE_SIGNER"] = False
Session(app)

basedir = os.path.abspath(os.path.dirname(__file__))

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*',methods= ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"])

# auth = HTTPBasicAuth()
app.debug = True


def AppResponse(data,statuscode:int):
    return jsonify(data),statuscode #,[{'Access-Control-Allow-Origin':'*'}]


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """

    if not hasattr(g, 'db_conn'):
        g.db_conn = create_conn()
    return g.db_conn

@app.teardown_request
def release_db(_):
    if not IS_FRONTEND_DEBUG and hasattr(g,'db_conn'):
        g.db_conn.close()
        g.pop('db_conn')

# def apology(message, code=400):
#     """Render message as an apology to user."""
#     def escape(s):
#         """
#         Escape special characters.

#         https://github.com/jacebrowning/memegen#special-characters
#         """
#         for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
#                          ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
#             s = s.replace(old, new)
#         return s
#     return render_template("error.html", top=code, bottom=escape(message)), code

# @app.route('/',methods=['GET'])

# def main():
#     return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """
    POST:
        if the user exists, then get the data belonged
        else create user and let him log in
    """

    # Ensure username was submitted
    data = json.loads(list(request.form)[0],strict=False)
    username = data.get("username")
    # username = 'ANDY'
    if IS_FRONTEND_DEBUG:
        return AppResponse(username,200)
    # Query database for username
    conn = get_db()
    visitor = get_data_by_name(conn,username,'USERS')


    # Ensure username exists and password is correct
    if not visitor :
        insert_user(conn,data['username'])
        visitor = get_data_by_name(conn,username,'USERS')
    print('login: visitor is',visitor)
    assert(len(visitor)>0)
    # login_session["username"] = visitor[0][1]
    # print('login_session["uid"]:',login_session["uid"])
    print('visitor:',visitor)
    # Add user to login_session

    # Redirect user to home page
    return AppResponse(visitor[0][1],200)






@app.route('/api/insert-item', methods=['POST'])
def insertItem():
    """
    提供物品
        - 接口: add
            - 参数: 名称-品牌-描述-数量-是消耗品-标签
            - POST
              - dict(name:'',brand:'',disc:'',qty:'',is_con:'',label:'')
            - tag由最后一次query得到的物品的tag分析（split by comma）统计成set，保存成变量
            - 返回：HTTP状态
    """
    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    if not username:
        return AppResponse('请先登录',401)
    if IS_FRONTEND_DEBUG: 
        return AppResponse("添加成功",200)
    conn = get_db()
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    data = json.loads(request_data['item'])
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    print(username)
    iid = insert_item(conn, data,commit=False)
    if not iid:
        conn.rollback()
        return AppResponse("添加物品失败",500)
    # sid = insert_share(conn, uid, modi, ddl)
    oid = insert_own(conn, uid, iid,commit=False)
    if not oid:
        conn.rollback()
        return AppResponse("添加拥有关系失败",500)
    labels = data['tag'] # TODO: use tag
    # done = True
    for label in labels:
        if get_data_by_name(conn, label, 'TAGS'):
            flag = insert_tag(conn, label, iid) # tolerate tag insertion fail
            # if flag:
            #     conn.commit()

                # return AppResponse("添加成功，已有标签",200)
            # return AppResponse("新建标签失败",500)
        else:
            flag = insert_tag(conn, label, iid)
            # if flag:
            #     conn.commit()
            #     return AppResponse("添加成功，新增标签",200)
            # return AppResponse("新建标签失败",500)
    conn.commit()
    return AppResponse("添加成功",200)


@app.route('/api/virtue-query', methods=['POST'])
def virtueQuery():
    """
    - 查询功德
        - 接口： virtue_query
            - POST
            - 返回： HTTP状态、功德值
    """
    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')

    if not username:
        return AppResponse('请先登录',401)
    if IS_FRONTEND_DEBUG: 
        return AppResponse(114514,200)

    conn = get_db()
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    # request_data = json.loads(list(request.form)[0],strict=False)
    
    sql = f"select * from VIRTUE where uid = ?;"
    with conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(sql, (uid,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from databse')
    return AppResponse(result[1],200)


@app.route('/api/virlog', methods=['POST'])
def virlogQuery():
    """
    - 查询功德日志，实际上是在系统的提供/借用历史记录
        - 接口： virlog_query
            - POST
            - 返回： HTTP状态、功德日志
    """
    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    print('virlog: username is ',username)
    if not username or username=='undefined':
        return AppResponse('请先登录',401)
    if IS_FRONTEND_DEBUG: 
        return AppResponse(['this','is','a','test'],200)
    conn = get_db()
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    # request_data = json.loads(list(request.form)[0],strict=False)
    sql = f"select * from VIRLOG where uid = ?;"
    with conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(sql, (uid,))
            result = cursor.fetchall()
            logger.info(f'select data<{result}> from virlog')
    return AppResponse([tp[1] for tp in result],200)
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
#       - 查询物品返回的状态是字符串，可以是"拥有n1个，已借出n2个"，"借用n个，还剩[还可使用时间]"


@app.route('/api/items', methods=['POST','OPTIONS'])
def myItemList():
    """查询我提供的和正在借出的物品"""
    if IS_FRONTEND_DEBUG: 
        return AppResponse([{
                'iid':1,
                'name':'test item',
                'brand':'item_info[2]',
                'description':'item_info[3]',
                'qty':4,
                'is_consume':True,
                'borrowing':False,
                'tag':['tag1'],
            }],200)


    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    if not username:
        return AppResponse('请先登录',401)
    conn = get_db()
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    # request_data = json.loads(list(request.form)[0],strict=False)
    sql = f"select * from OWN where uid = ?;"
    my_item = []
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql, (uid,))
        result = cursor.fetchall()
        # print(result)
        for row in result:
            iid = row[2]
            item_info = get_item_by_id(conn, iid)
            if (item_info == None):
                continue
            tags = get_tag_by_id(conn, item_info[0])
            
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
                'tag':[t[0] for t in tags],
            }
            print(item['tag'])
            my_item.append(item)

        logger.info(f'select data<{my_item}> from databse')
    return AppResponse(my_item,200)

# sid list是sid信息，不展示给用户，但是当用户选择要归还此物品时，需要记录这一物品借出记录的sid并传给return AppResponse(item函数
# 因为sid才是借用的唯一标识（可能存在同一个人同时借用多个同名物品1

@app.route('/api/borrow-list', methods=['POST'])
def myBorrowList():
    """查询我正在借用的物品"""
    if IS_FRONTEND_DEBUG: 
        return AppResponse([{
                'sid':1,
                'iid':1,
                'name':'test_item_borrowed',
                'owner_uid':1,
                'owner_name':'owner_info[1]',
                'modified':date.today().isoformat(),
                'ddl':date.today().isoformat()
            }],200)

    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    if not username:
        return AppResponse('请先登录',401)
    conn = get_db()
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    # request_data = json.loads(list(request.form)[0],strict=False)
    sql = f"select * from SHARE where uid = ?;"
    item_info = []
    with closing(conn.cursor()) as cursor:
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
    return AppResponse(item_info,200)


@app.route('/api/update-item', methods=['POST'])
def updateMyItem():
    """
    在不改变name的情况下更新物品信息，要求输入所有信息的更新。
    原信息用get_data_by_name函数获得，用户在原基础上修改后，把包括iid的全部表项传入此函数
    """
    if IS_FRONTEND_DEBUG: 
        return AppResponse("OK",200)
    conn = get_db()
    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    if not username:
        return AppResponse('请先登录',401)
    sql = f"update ITEMS SET BRAND=?, DESCRIPTION=?, QTY=?, IS_CONSUME=? where iid=?;"
    with conn:
        with closing(conn.cursor()) as cursor:
            result = cursor.execute(sql, (request_data['brand'], request_data['description'], request_data['qty'], request_data['is_consume'], request_data['iid']))
            # if result[0] == "UPDATE 0": return AppResponse("failed", 500)
            # result = cursor.fetchone()
            logger.info(f'update data<{result}> to the item')
            conn.commit()
    return AppResponse("OK",200)



@app.route('/api/search-item', methods=['POST'])
def searchItem():
    """fetch data by item_name
    Returns:
        物品信息列表，是否正在借出的列表，1代表借出中
    """
    if IS_FRONTEND_DEBUG: 
        return AppResponse([{
                    'iid':1,
                    'name':'row[1]',
                    'owner_id':1,
                    'owner_name':'2',
                }],200)
    conn = get_db()
    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    if not username:
        return AppResponse('请先登录',401)
    sql = f"select * from ITEMS where NAME LIKE ?;"
    print("req_data:",request_data)
    item_name: str = request_data['name']
    item_info = []
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql, (item_name,))
        result = cursor.fetchall()
        for row in result:
            owner = get_owner_by_iid(conn,row[0])
            owner_name = get_user_by_id(conn,owner[1])
            if not get_sharing_by_item_id(conn,row[0]):
                # return items not borrowed
                print('searchItem:',owner_name)
                item_info.append({
                    'iid':row[0],
                    'name':row[1],
                    'owner_id':owner[1],
                    'owner_name':str(owner_name[1]),
                })
        logger.info(f'select data<{item_info}> from item')
    return AppResponse(item_info,200)

# 借流程：首先搜索物品，在返回的列表中选择是要借哪一个，把被选中的物品的id传入下面的borrow函数
# borrow函数没有判断是否可借，因为搜索的时候已经返回了可借列表


@app.route('/api/borrow-item', methods=['POST'])
def borrowItem():
    """
    记得传入modi最后修改时间和ddl时间，两者都是date格式

    - 消耗品：数量-1
    - 更新使用权，除非拥有者自用、消耗品
    - 功德+=2：借给非拥有者
    - 接口：borrow
        - POST
        - 参数: userid
        - 返回：HTTP状态
    """
    if IS_FRONTEND_DEBUG:
        return AppResponse("OK",200)
    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    if not username:
        return AppResponse('请先登录',401)
    conn = get_db()
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    iid = request_data['iid']
    ddl_list = request_data['ddl'].split('-')
    print(ddl_list)
    modi, ddl = datetime.datetime.now(),datetime.datetime(int(ddl_list[0]),int(ddl_list[1]),int(ddl_list[2]))
    data = get_item_by_id(conn, iid)
    # is_consume = request_data[qty]
    is_consume = 0
    qty = data[4]
    owner_id = get_owner_by_iid(conn, iid)[1]
    if owner_id == uid:
        conn.rollback()
        return AppResponse("拒绝理由：自己借给自己刷功德",500)
    update_virtue(conn, owner_id, 2,commit=False)
    item_name = get_item_by_id(conn, iid)[1]
    user_name = get_user_by_id(conn, uid)[1]
    log_content = f'<{str(modi)}> 借出<{item_name}> 给 <{user_name}>'
    insert_virlog(conn, owner_id, log_content,False)
    if is_consume: #消耗品，借出后不可归还
        # if qty-1==0:
        #     delete_item(conn, iid, uid)
        #     return AppResponse({'code': 200, 'msg': "全部借出，物品已删除"}) #这一部分改为借出至剩余0个时由owner来自行决定是补货update还是删除delete
        if qty == 0:
            conn.rollback()
            return AppResponse("物品已消耗完，请考虑补货或删除",500)
        sql = f"update ITEMS QTY=? where iid=?;"
        with conn:
            with closing(conn.cursor()) as cursor:
                result = cursor.execute(sql, (qty-1, iid))
                result = cursor.fetchone()
                logger.info(f'update data<{result}> to the databse')
                # conn.commit()
    else:
        insert_share(conn, uid, iid, modi, ddl,False)
    conn.commit()
    return AppResponse("OK",200)



@app.route('/api/return-item', methods=['POST'])
def returnItem():
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
    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    if not username:
        return AppResponse('请先登录',401)
    if IS_FRONTEND_DEBUG: 
        return AppResponse("OK",200)
    conn = get_db()
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    sid, iid = request_data['sid'],request_data['iid']
    time = datetime.datetime.now()
    sqlget = f"select * from SHARE where sid = ?;"
    sql = f"delete from SHARE where sid = ?;"
    with conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(sqlget, (sid,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from share')
            ddl = result[4]
            iid = result[2]
            cursor.execute(sql, (sid,))
            logger.info(f'delete data from share by id<{sid}>')
            sql = f"select * from OWN where iid = ?;"
            # with conn:
                # with closing(conn.cursor()) as cursor:
            cursor.execute(sql, (iid,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from own')
            owner_id = result[1]
            # owner_id = get_owner_by_iid(conn, iid)[1]
    # conn.commit()
    if uid==owner_id:
        conn.commit() # is oid == uid in SHARE acceptable?
        return AppResponse("自己借自己的东西并且成功归还，你比泰森厉害",200)
    item_name = get_item_by_id(conn, iid)[1]
    user_name = get_user_by_id(conn, owner_id)[1]
    if ddl>time:
        update_virtue(conn, uid, 1,commit=False)
        log_content = f'<{str(time)}> 归还<{item_name}> 给 <{user_name}，准时，功德 +1>'
        insert_virlog(conn, uid, log_content,commit=False)
        conn.commit()
        return AppResponse("成功按时归还",200)
    update_virtue(conn, uid, -2,commit=False)
    log_content = f'<{str(time)}> 归还<{item_name}> 给 <{user_name}，超时，功德 -2>'
    insert_virlog(conn, uid, log_content,commit=False)
    conn.commit()
    return AppResponse("借用超时，成功归还",200)



@app.route('/api/delete-item', methods=['POST'])
def deleteItem():
    """
    - 移出物品
        - 条件：拥有者想要自用、借出消耗品
        - 接口：remove
            - param：物品id，数量
            - 返回：HTTP状态
    """
    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    if not username:
        return AppResponse('请先登录',401)
    if IS_FRONTEND_DEBUG: 
        return AppResponse("OK",200)
    conn = get_db()
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    iid = request_data['iid']
    if not get_owner_by_iid(conn, iid)[1]==uid:
        conn.rollback()
        return AppResponse("非物品拥有者，删除失败",500)

    sql1 = f"delete from ITEMS where iid = ?;"
    sql2 = f"delete from TAGS where iid = ?;"
    if get_sharing_by_item_id(conn, iid):
        conn.rollback()
        return AppResponse("物品正在借出，无法删除",500)
    with conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(sql1, (iid,))
            logger.info(f'delete data from items by id<{iid}>')
            cursor.execute(sql2, (iid,))
            logger.info(f'delete data from tags by id<{iid}>')
            conn.commit()
    return AppResponse("物品已删除",200)


@app.route('/api/delete-user', methods=['POST'])
def deleteUser():
    request_data = json.loads(list(request.form)[0],strict=False)
    username = request_data.get('WEDORM-uid')
    if not username:
        return AppResponse('请先登录',401)
    conn = get_db()
    uid = get_data_by_name(conn,username,'USERS')[0][0]
    sql = f"delete from USERS where uid = ?;"
    with conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(sql, (uid,))
            logger.info(f'delete data from databse by id<{uid}>')
            conn.commit()
    
    return AppResponse("OK",200)

# @app.errorhandler(404)
# def not_found(_):
#     resp = make_response(render_template('error.html'), 404)
#     return resp


# print(search_item(conn, "厕所"))

if __name__ == '__main__':
    app.run(host='192.168.0.107:15000')
