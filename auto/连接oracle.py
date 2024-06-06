import cx_Oracle
import pandas as pd
# 创建连接
# dsn = cx_Oracle.makedsn('10.118.4.10', '1525', service_name='hydee')
# connection = cx_Oracle.connect(user='h2', password='HDrrt_2021wbzD', dsn=dsn)
conn = cx_Oracle.connect('h2/HDrrt_2021wbzD@10.118.4.10:1525/hydee')#这里的顺序是用户名/密码@oracleserver的ip地址/数据库名字
cursor = conn.cursor()
print('连接数据库成功！')

try:
    # 使用连接创建游标
    cursor = conn.cursor()

    # 执行SQL查询
    cursor.execute('select * from d_o2o_mdzj where YSNAME is not null')

    # 获取查询结果
    rows = cursor.fetchall()

    # 将查询结果转换为DataFrame
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

    # 导出DataFrame到Excel文件
    # df.to_excel('output.xlsx', index=False)

finally:
    # 关闭游标和连接
    cursor.close()
    conn.close()