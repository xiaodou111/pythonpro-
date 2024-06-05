import pymysql

# 创建连接
try:
    # connection = pymysql.connect(host='172.20.139.17',
    #                              user='rrtselect',
    #                              password='3U5AWzwrrkS^=aSdc',
    #                              # database='your_database',
    #                              charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor)

    connection = pymysql.connect(host='192.168.254.169',
                                 user='yanjiangyi',
                                 password='c20ad4d76120528',
                                  database='qy_rrt',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    print("连接成功！")

    with connection.cursor() as cursor:
        # 创建一个新记录
        # sql = "INSERT INTO `your_table` (`column1`, `column2`) VALUES (%s, %s)"
        # cursor.execute(sql, ('value1', 'value2'))
        # connection.commit()

        # 查询数据
        sql = """
        select series,
       tenant_num_id,
       tml_num_id,
       so_no,
       customer_so_no
from
             sd_bl_so_tml_hdr_local
        """
        # cursor.execute(sql, ('value1',))
        cursor.execute(sql)
        # result = cursor.fetchone()
        result = cursor.fetchall()
        print(result)

finally:
    connection.close()