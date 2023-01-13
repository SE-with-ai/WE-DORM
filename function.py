import json
from datetime import date, datetime

import psycopg2 
import logging
            
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_conn():
    """get connection from envrionment variable by the conn factory

    Returns:
        [type]: the psycopg2's connection object
    """
    conn = psycopg2.connect(database="wedorm", 
                            user="myfinal", 
                            password="cat_2333", 
                            host="192.168.0.105", 
                            port="5432") 
    return conn

# insert 系列函数的返回值都是对应的id， 比如uid/sid/iid， 但是其他函数例如查询返回的是整个list，所以不要直接从前端调用这些基本函数
# 返回值没有json dumps的都是基本函数，用于实现更高一级的功能。

def insert_user(conn, arg) -> int:
    """添加用户
    分别添加一行user和一行virtue
    uid自增生成， arg需要传入name， dorm， email为key的字典
    Args:
        cnn ([type]): the connection object to the databse
    """
    usersql = f"insert into USERS (NAME,DORM,EMAIL) values (%s,%s,%s) RETURNING *;"
    virsql = f"insert into VIRTUE (UID, VIRTUE) values (%s,%s) RETURNING *;"
    with conn:
        with conn.cursor() as cursor:
            data = json.loads(arg)
            result = cursor.execute(usersql, (data['name'],data['dorm'],data['email']))
            result = cursor.fetchone()
            cursor.execute(virsql, (result[0],0)) # 功德初始值为0
            logger.info(f'add data<{result}> to the databse')
            conn.commit()
    return result[0] if result else None

def insert_share(conn, uid, iid, modi, ddl) -> int:
    """insert item data

    Args:
        cnn ([type]): the connection object to the databse
    """
    sql = f"insert into SHARE (UID,IID,MOD,DDL) values (%s,%s,%s,%s) RETURNING *;"
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, (uid, iid, modi, ddl))
            result = cursor.fetchone()
            logger.info(f'add data<{result}> to the databse')
            conn.commit()
    return result[0] if result else None

def insert_item(conn, arg) -> int:
    """insert item data

    Args:
        cnn ([type]): the connection object to the databse
    """
    sql = f"insert into ITEMS (NAME,BRAND,DESCRIPTION,QTY,IS_CONSUME) values (%s,%s,%s,%s,%s) RETURNING *;"
    with conn:
        with conn.cursor() as cursor:
            data = json.loads(arg)
            result = cursor.execute(sql, (data['name'],data['brand'],data['disc'],data['qty'],data['is_con']))
            result = cursor.fetchone()
            logger.info(f'add data<{result}> to the databse')
            conn.commit()
    return result[0] if result else None

def insert_own(conn, uid, iid) -> int:
    """insert item data

    Args:
        cnn ([type]): the connection object to the databse
    """
    sql = f"insert into OWN (UID,IID) values (%s,%s) RETURNING *;"
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, (uid,iid))
            result = cursor.fetchone()
            logger.info(f'add data<{result}> to the databse')
            conn.commit()
    return result[0] if result else None

def insert_classify(conn, cid, iid) -> int:
    """insert label data

    Args:
        cnn ([type]): the connection object to the databse
    """
    sql = f"insert into CLASSIFY (NAME,IID) values (%s,%s) RETURNING *;"
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, (cid, iid))
            result = cursor.fetchone()
            logger.info(f'add data<{result}> to the databse')
            conn.commit()
    return result[0] if result else None

def insert_virlog(conn, uid, log_content) -> int:
    """insert virtue log

    Args:
        cnn ([type]): the connection object to the databse
    """
    sql = f"insert into VIRTUE (VIRTUE) values (%s) RETURNING *;"
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, (uid, log_content))
            result = cursor.fetchone()
            logger.info(f'add data<{result}> to the virtue log')
            conn.commit()
    return result[0] if result else None

def get_item_by_id(conn, id: int):
    """fetch data by id

    Args:
        conn ([type]): the connection object
        id (int): the primary key of the table

    Returns:
        [type]: the tuple data of the table
    """
    sql = f"select * from ITEMS where iid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from item')
    return result

def get_owner_by_iid(conn, id: int):
    """fetch owner info by iid

    Args:
        conn ([type]): the connection object
        id (int): the primary key of the table

    Returns:
        [type]: the tuple data of the table
    """
    sql = f"select * from OWN where iid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from own')
    return result

def get_user_by_id(conn, id: int):
    """fetch data by id

    Args:
        conn ([type]): the connection object
        id (int): the primary key of the table

    Returns:
        [type]: the tuple data of the table
    """
    sql = f"select * from USERS where uid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from user')
    return result

def get_sharing_by_item_id(conn, id: int):
    """fetch data by id

    Args:
        conn ([type]): the connection object
        id (int): the primary key of the table

    Returns:
        [type]: the tuple data of the table
    """
    sql = f"select * from SHARE where iid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            logger.info(f'select data<{result}> from share')
    return result

def get_data_by_name(conn, item_name: str, table_name):
    """fetch data by item_name

    Args:
        conn ([type]): the connection object

    Returns:
        [type]: the tuple data of the table
    """
    sql = f"select * from {table_name} where NAME = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (item_name,))
            result = cursor.fetchall()
            logger.info(f'select data<{result}> from databse')
    return result

#---------------------------------以下是功能接口---------------------------------

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

# sid list是sid信息，不展示给用户，但是当用户选择要归还此物品时，需要记录这一物品借出记录的sid并传给return item函数
# 因为sid才是借用的唯一标识（可能存在同一个人同时借用多个同名物品1
def my_borrow_list(conn, uid):
    """查询我正在借的物品"""
    sql = f"select * from SHARE where uid = %s;"
    item_info = []
    owner_info = []
    start_time = []
    ddl = []
    time_remain = []
    sid_list = []
    with conn.cursor() as cursor:
        cursor.execute(sql, (uid,))
        result = cursor.fetchall()
        for row in result:
            iid = row[2]
            owner_raw = get_sharing_by_item_id(conn, iid)
            owner_id = owner_raw[1]
            share_id = owner_raw[0]
            sid_list.append(share_id)
            owner_info.append(get_user_by_id(conn, owner_id))
            item_info.append(get_item_by_id(conn, iid))
            start_time.append(str(row[3]))
            ddl.append(str(row[4]))
            time_remain.append(str(row[4] - row[3]))
        logger.info(f'select data<{result}> from databse')
    return json.dumps({'code': 200, 
                       'msg': "查询成功",
                       'borrow item list': item_info, 
                       'owner': owner_info, 
                       'borrow start from':start_time, 
                       'ddl': ddl, 
                       'time remain':time_remain, 
                       'sid list':sid_list})

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

def borrow_item(conn, uid, iid, modi, ddl, num):
    """
    记得传入modi最后修改时间和ddl时间，两者都是date格式
    num是要借的物品数量,暂未实现此功能。现在非消耗品不允许堆叠，即qty都为1.
    多个物品在items表记录为重复条目，借出归还一次只能一件物品（原子操作doge
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
        update_virtue(conn, owner_id, 3)
        item_name = get_item_by_id(conn, iid)[1]
        user_name = get_user_by_id(conn, uid)[1]
        log_content = f'<{str(modi)}> 借出<{item_name}> 给 <{user_name}，功德 +3>'
        insert_virlog(conn, owner_id, log_content)
    if is_consume: #消耗品
        # if qty-1==0:
        #     delete_item(conn, iid, uid)
        #     return json.dumps({'code': 200, 'msg': "全部借出，物品已删除"}) #这一部分改为借出至剩余0个时由owner来自行决定是补货update还是删除delete
        sql = f"update ITEMS QTY=%s where iid=%s;"
        with conn:
            with conn.cursor() as cursor:
                result = cursor.execute(sql, (qty-1, iid))
                result = cursor.fetchone()
                logger.info(f'update data<{result}> to the databse')
                conn.commit()
    else:
        insert_share(conn, uid, iid, modi, ddl)

# 先调用my_borrow_list，在页面中供用户选择要归还的项目，并从返回值中获得ownerid和借用的sid
# time是归还时的时间, num是归还数目
def return_item(conn, uid, owner, sid, time):
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
            conn.commit()
    if uid==owner:
        return json.dumps({'code': 200, 'msg': "自己借自己的东西并且成功归还"})
    item_name = get_item_by_id(conn, iid)[1]
    user_name = get_user_by_id(conn, owner)[1]
    if ddl>time:
        update_virtue(conn, uid, 1)
        log_content = f'<{str(time)}> 归还<{item_name}> 给 <{user_name}，准时，功德 +1>'
        insert_virlog(conn, uid, log_content)
        return json.dumps({'code': 200, 'msg': "成功按时归还"})
    update_virtue(conn, uid, -2)
    log_content = f'<{str(time)}> 归还<{item_name}> 给 <{user_name}，超时，功德 -2>'
    insert_virlog(conn, uid, log_content)
    return json.dumps({'code': 200, 'msg': "借用超时，成功归还"})

def delete_item(conn, iid, uid):
    """
    - 移出物品
        - 条件：拥有者想要自用、借出消耗品
        - 接口：remove
            - param：物品id，数量
            - 返回：HTTP状态
    """
    if not get_owner_by_iid(conn, iid)[1]==uid:
        return json.dumps({'code': 500, 'msg': "非物品拥有者，删除失败"})
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

def delete_user(conn, uid):
    """
    此函数未完成
    """
    sql = f"delete from USERS where uid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (uid,))
            logger.info(f'delete data from databse by id<{uid}>')
            conn.commit()
    return json.dumps({'code': 200, 'msg': "用户已删除"})
