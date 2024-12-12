import pymysql
import cx_Oracle
from datetime import datetime, timedelta
import psycopg2
from sqlalchemy import create_engine


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

def get_qy_uatmysql():
    """返回数据库连接"""
    return pymysql.connect(
        host='172.20.2.15',
        user='rrtuatquery',
        port=5066,
        password='x=^6fVC2pGS',
        database='',  # 如果需要指定数据库，在这里填写
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_qy_prodmysql():
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
    return  pymysql.connect(host='10.118.4.105',
                    user='yanjiangyi',
                    port=3308,
                    password='qyzjrrt@001yjy',
                    database='rrtprod',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)

def get_oracle_prod():
    try:
        connection = cx_Oracle.connect('h2/HDrrt_2021wbzD@10.118.4.10:1525/hydee')
        print("Oracle生产数据库连接成功！")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Oracle生产数据库连接失败：{error.message}")
        return None

def get_oracle_zjcs():
    try:
        connection = cx_Oracle.connect('zjcsprd/zjcsprd@10.118.4.4:1525/zjcs')
        print("Oracle数据直连库连接成功！")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Oracle生产数据库连接失败：{error.message}")
        return None
def get_oracle_qysjzl():
    try:
        connection = cx_Oracle.connect('qyzt_dev/qyRrtOraDev^2130#@172.20.139.130:1521/rrtdigital') #, echo=True)
        print("全亿Oracle直连数据库连接成功！")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"全亿Oracle直连数据库连接失败：{error.message}")
        return None
def import_oracle_zjcs():
    try:
        connection = create_engine('oracle+cx_oracle://zjcsprd:zjcsprd@10.118.4.4:1525/zjcs') #, echo=True)
        print("Oracle直连数据库连接成功！")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Oracle直连数据库连接失败：{error.message}")
        return None
def con_oracle_qysjzl():
    try:
        connection = create_engine('oracle+cx_oracle://qyzt_dev:qyRrtOraDev^2130#@172.20.139.130:1521/rrtdigital') #, echo=True)
        print("全亿Oracle直连数据库连接成功！")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"全亿Oracle直连数据库连接失败：{error.message}")
        return None
def import_oracle_prod():
    try:
        connection = create_engine('oracle+cx_oracle://h2:HDrrt_2021wbzD@10.118.4.10:1525/hydee')
        print("Oracle生产数据库连接成功！")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Oracle生产数据库连接失败：{error.message}")
        return None


def dml_oracle_table(connection, sql):
    try:
        sql = f"{sql}"
        print(f"执行语句: {sql}")

        # 使用with语句确保游标正确关闭
        with connection.cursor() as cursor:
            # 执行DML语句
            cursor.execute(sql)

            # 输出受影响的行数
            affected_rows = cursor.rowcount
            print(f"DML语句影响了 {affected_rows} 行。")

            # 提交事务
            connection.commit()
    except Exception as e:
        print(f"DML操作失败：{e}")
        # 可以在此处添加更多的错误处理逻辑，如记录到日志文件
        # logging.error(f"DML操作失败：{e}", exc_info=True)
    # finally:
    # 确保在所有情况下都关闭连接（如果适用）
    #         connection.close()  # 注意：这取决于你的连接管理策略


def import_postgres_prod():
    try:
        # PostgreSQL 数据库连接字符串
        db_url = 'postgresql://zt_rrt:SrrtDgYh@!Hwy2311F24313@172.20.132.37:8000/qybi2'

        # 创建数据库引擎
        engine = create_engine(db_url)

        print("PostgreSQL生产数据库连接成功！")
        return engine

    except Exception as e:
        print(f"PostgreSQL生产数据库连接失败：{str(e)}")
        return None

# def connect_to_postgres():
#     # PostgreSQL 数据库连接参数
#     conn_params = {
#         'dbname': 'qybi2',
#         'user': 'zt_rrt',
#         'password': 'SrrtDgYh@!Hwy2311F24313',
#         'host': '172.20.132.37',  # 或者是你的服务器地址
#         'port': '8000'  # 默认端口
#     }


