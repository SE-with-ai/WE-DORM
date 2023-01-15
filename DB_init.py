#!/usr/bin/python
import psycopg2
conn = psycopg2.connect(database="wedorm", user="myfinal", password="cat_2333", host="192.168.0.107", port="5432") 
# conn = psycopg2.connect(database="opengauss", user="root", password="openGauss@123", host="172.30.64.1", port="15000") 

cur = conn.cursor()
# cur.execute("drop database wedorm;")
# cur.execute("create database wedorm owner myfinal;")

#创建用户表
cur.execute('''
       CREATE SEQUENCE sq_user_id
       START 1 
       INCREMENT 1
       CACHE 20; 
       CREATE TABLE USERS
       (UID INT PRIMARY KEY   NOT NULL UNIQUE DEFAULT nextval('sq_user_id'),
       NAME            TEXT   NOT NULL UNIQUE,
       DORM         TEXT  NOT NULL,
       EMAIL        CHAR(50));''')
#创建物品表
cur.execute('''
       CREATE SEQUENCE sq_item_id
       START 1 
       INCREMENT 1
       CACHE 20; 
       CREATE TABLE ITEMS
       (IID INT PRIMARY KEY   NOT NULL UNIQUE DEFAULT nextval('sq_item_id'),
       NAME            TEXT   NOT NULL,
       BRAND           TEXT,
       DESCRIPTION     TEXT,
       QTY             REAL  NOT NULL,
       IS_CONSUME      BOOL);''')
#创建拥有关系表
cur.execute('''
       CREATE SEQUENCE sq_owner_id
       START 1 
       INCREMENT 1
       CACHE 20; 
       CREATE TABLE OWN
       (OID INT PRIMARY KEY   NOT NULL UNIQUE DEFAULT nextval('sq_owner_id'),
       UID  INT        NOT NULL,
       IID  INT        NOT NULL,
       FOREIGN KEY(UID) REFERENCES USERS ON DELETE CASCADE,
       FOREIGN KEY(IID) REFERENCES ITEMS ON DELETE CASCADE);''')
# 创建分享表
cur.execute('''
       CREATE SEQUENCE sq_share_id
       START 1 
       INCREMENT 1
       CACHE 20; 
       CREATE TABLE SHARE
       (SID INT PRIMARY KEY NOT NULL UNIQUE DEFAULT nextval('sq_share_id'),
       UID  INT        NOT NULL,
       IID  INT        NOT NULL,
       MODIFIED DATE   NOT NULL,
       DDL  DATE       ,
       FOREIGN KEY(UID) REFERENCES USERS ON DELETE CASCADE,
       FOREIGN KEY(IID) REFERENCES ITEMS ON DELETE CASCADE);''')

#创建标签表
cur.execute('''CREATE TABLE TAGS
       (NAME TEXT      NOT NULL,
       IID  INT        NOT NULL,
       FOREIGN KEY(IID) REFERENCES ITEMS ON DELETE CASCADE);''')

#创建功德表
cur.execute('''CREATE TABLE VIRTUE
       (UID INT PRIMARY KEY     NOT NULL UNIQUE,
       VIRTUE           INT     NOT NULL,
       FOREIGN KEY(UID) REFERENCES USERS ON DELETE CASCADE);''')

# 日志
cur.execute('''CREATE TABLE VIRLOG
       (UID INT       NOT NULL,
       VIRLOG           text,
       FOREIGN KEY(UID) REFERENCES USERS ON DELETE CASCADE);''')

#插入数据       
cur.execute("INSERT INTO USERS (NAME,DORM,EMAIL) \
      VALUES ( 'ANDY', '405', '1755331362@QQ.COM' )");

cur.execute("INSERT INTO USERS (NAME,DORM) \
      VALUES ('CHEN', '格致园皇帝宿舍' )");

cur.execute("INSERT INTO ITEMS (NAME,DESCRIPTION,QTY,IS_CONSUME) \
      VALUES ('厕所', '普通的厕所', 1, 0 )");

cur.execute("INSERT INTO TAGS (NAME, IID) \
      VALUES ('厕所', 1)");
      
cur.execute("INSERT INTO ITEMS (NAME,BRAND,DESCRIPTION,QTY,IS_CONSUME) \
      VALUES ('连花清瘟胶囊', '以岭药业', '也许有用的药', 15, 1 )");

cur.execute("INSERT INTO OWN (OID,UID,IID) \
      VALUES (1, 2, 1)");

cur.execute("INSERT INTO SHARE (UID,IID,MODIFIED,DDL) \
      VALUES (1, 1, '2022-12-20 15:48', '2022-12-20 19:48' )");

cur.execute("INSERT INTO VIRTUE (UID,VIRTUE) \
      VALUES (1, 0 )");

cur.execute("INSERT INTO VIRTUE (UID,VIRTUE) \
      VALUES (2, 6 )");      
      
#查询结果
cur.execute("SELECT SID,UID,IID,MODIFIED,DDL from SHARE")
rows = cur.fetchall()
for row in rows:
   print("SID = ", row[0])
   print("MODIFIED = ", row[3])
   print("DDL = ", row[4])

conn.commit()
conn.close()