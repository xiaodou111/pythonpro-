import pymysql
import cx_Oracle
from datetime import datetime, timedelta
def get_qy_mysql():
    """返回数据库连接"""
    return pymysql.connect(
        host='172.20.139.17',
        user='rrtselect',
        port=5066,
        password='3U5AWzwrrkS^=aSdc',
        database='',  # 如果需要指定数据库，在这里填写
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_rrt_mysql():
    return  pymysql.connect(host='192.168.254.169',
                    user='yanjiangyi',
                    port=3306,
                    password='c20ad4d76120528',
                    database='qy_rrt',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)

def get_oracle_prod():
    return cx_Oracle.connect('h2/HDrrt_2021wbzD@10.118.4.10:1525/hydee')

def get_oracle_zjcs():
    return cx_Oracle.connect('zjcsprd/zjcsprd@10.118.4.4:1525/zjcs')

