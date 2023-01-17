import json
from datetime import date, datetime
from functools import wraps
from flask import session,redirect
import psycopg2 
import logging
from flask import session,redirect
from functools import wraps
            
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def create_conn():
    """get connection from envrionment variable by the conn factory

    Returns:
        [type]: the psycopg2's connection object
    """
    conn = psycopg2.connect(database="wedorm", 
                            user="myfinal", 
                            password="cat_2333", 
                            host="192.168.0.107", 
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
            data = arg
            result = cursor.execute(usersql, (data,'',''))
            result = cursor.fetchone()
            cursor.execute(virsql, (result[0],0)) # 功德初始值为0
            logger.info(f'add data<{result}> to the databse')
            conn.commit()
    return result[0] if result else None

def insert_share(conn, uid, iid, modi, ddl,commit=True) -> int:
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
            if commit: conn.commit()
    return result[0] if result else None

def insert_item(conn, arg,commit=True) -> int:
    """insert item data

    Args:
        cnn ([type]): the connection object to the databse
    """
    sql = f"insert into ITEMS (NAME,BRAND,DESCRIPTION,QTY,IS_CONSUME) values (%s,%s,%s,%s,%s) RETURNING *;"
    with conn:
        with conn.cursor() as cursor:
            data = arg
            result = cursor.execute(sql, (data['name'],data['brand'],data['description'],data['qty'],data['is_consume']))
            result = cursor.fetchone()
            logger.info(f'add data<{result}> to the databse')
            if commit: conn.commit()
    return result[0] if result else None

def insert_own(conn, uid, iid,commit=True) -> int:
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
            if commit: conn.commit()
    return result[0] if result else None

def insert_tag(conn, cid, iid,commit=True) -> int:
    """insert label data

    Args:
        cnn ([type]): the connection object to the databse
    """
    sql = f"insert into TAGS (NAME,IID) values (%s,%s) RETURNING *;"
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql, (cid, iid))
            result = cursor.fetchone()
            print(result)
            logger.info(f'add data<{result}> to the databse')
            if commit: conn.commit()
    return result[0] if result else None

def insert_virlog(conn, uid, log_content,commit=True) -> int:
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
            if commit: conn.commit()
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

def get_tag_by_id(conn, id: int):
    """fetch data by id

    Args:
        conn ([type]): the connection object
        id (int): the primary key of the table

    Returns:
        [type]: the tuple data of the table
    """
    sql = f"select NAME from TAGS where iid = %s;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (id,))
            result = cursor.fetchall()
            logger.info(f'select data<{result}> from tags')
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
        item_name: name of data queried
        table_name: name of table queried, must by either USERS or ITEMS

    Returns:
        [type]: the tuple data of the table
    """
    sql = f"select * from {table_name} where NAME = %s;"
    if not table_name in ['USERS','ITEMS','TAGS']:
        return
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (item_name,))
            result = cursor.fetchall()
            logger.info(f'select data<{result}> from databse')
    return result


def update_virtue(conn, uid, num,commit=True):
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

# if __name__ == '__main__':
#     conn = create_conn()
#     print(insert_tag(conn,'药','2',True))
#     print(get_user_by_id(conn, 1))
