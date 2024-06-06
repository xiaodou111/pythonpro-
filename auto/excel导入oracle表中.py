from sqlalchemy import create_engine
import cx_Oracle
import pandas as pd
from datetime import datetime, timedelta
import pymysql
# 获取昨天的日期
yesterday = datetime.now() - timedelta(days=1)
# 格式化日期为字符串
formatted_date = yesterday.strftime('%Y%m%d')
filename = f'{formatted_date}_销售.xlsx'
filename2 = f'{formatted_date}_瑞人堂完成率.xlsx'
filename3 = f'{formatted_date}_桐乡完成率.xlsx'
# filename = f'{formatted_date}_销售.csv'
desktop_path = r'D:\download\桌面'
save_path = desktop_path + '\\' + filename
save_path2 = desktop_path + '\\' + filename2
save_path3 = desktop_path + '\\' + filename3
print(f"save_path:{save_path}")
print(f"save_path2:{save_path2}")
print(f"save_path3:{save_path3}")
with open('./sql/qydc.sql', 'r', encoding='utf-8') as file:
    qydc = file.read()
with open('./sql/rrtwcl.sql', 'r', encoding='utf-8') as file:
    rrtwlc = file.read()
with open('./sql/txwcl.sql', 'r', encoding='utf-8') as file:
    txwlc = file.read()
#1.连接qy库并导出sql结果为excel到桌面
try:

    connection = pymysql.connect(host='172.20.139.17',
                                 user='rrtselect',
                                 port=5066,
                                 password='3U5AWzwrrkS^=aSdc',
                                 database='',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    print("连接成功！")
#
    with connection.cursor() as cursor:
        cursor.execute(qydc)
        rows = cursor.fetchall()
       # 将查询结果转换为DataFrame
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
       # 导出DataFrame到Excel文件
        df.to_excel(save_path, index=False)
       #  df.to_csv(save_path, index=False)
        # result = cursor.fetchone()
        # result = cursor.fetchall()
        print(f"文件已保存到 {save_path}")
#
finally:
    connection.close()
#2.连接oracle生产库并把qy库导出的excel导入到表D_RRTPROD_MEMORDER中
engine = create_engine('oracle+cx_oracle://h2:HDrrt_2021wbzD@10.118.4.10:1525/hydee')
print("连接成功！")
df2= pd.read_excel(save_path)

# 记录DataFrame的长度（即行数）
num_rows = len(df2)

try:
#     # 将DataFrame写入数据库
    df2.to_sql(name="D_RRTPROD_MEMORDER", con=engine, index=False, if_exists='append')
#     # # df2 = pd.read_excel('20240605_销售s.xlsx', parse_dates=['ORDER_DATE', 'CREATE_DTME'])
#     #
#     # # 如果原始数据中时间信息不全，添加默认的时分秒
#     # # df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE']).dt.to_period('D').to_timestamp('D')
#     # # df['CREATE_DTME'] = pd.to_datetime(df['CREATE_DTME']).dt.to_period('D').to_timestamp('D')
#     # 输出导入成功的行数
    print(f"导入成功，共导入 {num_rows} 行数据")
except Exception as e:
    # 处理可能发生的错误
    print(f"数据导入失败：{e}")
#3.执行瑞人堂和桐乡完成率的sql并分别导出结果excel到桌面
conn = cx_Oracle.connect('h2/HDrrt_2021wbzD@10.118.4.10:1525/hydee')

try:
    # 使用连接创建游标
    cursor = conn.cursor()
    # 执行SQL查询
    cursor.execute(rrtwlc)
    # 获取查询结果
    rows = cursor.fetchall()
    # 将查询结果转换为DataFrame
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    # 导出DataFrame到Excel文件
    df.to_excel(save_path2, index=False)
    print(f"文件:瑞人堂完成率已保存到: {save_path2}")

    cursor.execute(txwlc)
    # 获取查询结果
    rows = cursor.fetchall()
    # 将查询结果转换为DataFrame
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    # 导出DataFrame到Excel文件
    df.to_excel(save_path3, index=False)
    print(f"文件:桐乡完成率已保存到: {save_path3}")

finally:
    # 关闭游标和连接
    cursor.close()
    conn.close()
#4自动打开刚才的完成率两张表并格式化
