import pymysql
import cx_Oracle
from datetime import datetime, timedelta

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

def get_rrt_mysql():
    return  pymysql.connect(host='192.168.254.169',
                    user='yanjiangyi',
                    port=3306,
                    password='c20ad4d76120528',
                    database='qy_rrt',
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

def import_oracle_zjcs():
    try:
        connection = create_engine('oracle+cx_oracle://zjcsprd:zjcsprd@10.118.4.4:1525/zjcs', echo=True)
        print("Oracle直连数据库连接成功！")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Oracle直连数据库连接失败：{error.message}")
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
    finally:
    # 确保在所有情况下都关闭连接（如果适用）
            connection.close()  # 注意：这取决于你的连接管理策略


