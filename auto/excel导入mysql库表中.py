import pymysql
from sqlalchemy import create_engine
import pandas as pd
import pymysql



    # connection = pymysql.connect(host='192.168.254.169',
    #                          user='yanjiangyi',
    #                          password='c20ad4d76120528',
    #                          database='qy_rrt',
    #                          charset='utf8mb4',
    #                          cursorclass=pymysql.cursors.DictCursor)
engine = create_engine('mysql+pymysql://yanjiangyi:c20ad4d76120528@192.168.254.169/qy_rrt')
print("连接成功！")

df2= pd.read_excel("20240605_销售s.xlsx")

# df2 = pd.read_excel('20240605_销售s.xlsx', parse_dates=['ORDER_DATE', 'CREATE_DTME'])

# 如果原始数据中时间信息不全，添加默认的时分秒
# df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE']).dt.to_period('D').to_timestamp('D')
# df['CREATE_DTME'] = pd.to_datetime(df['CREATE_DTME']).dt.to_period('D').to_timestamp('D')
#
# # 或者，如果你希望所有时间都设定为每天的00:00:00
# df['ORDER_DATE'] = df['ORDER_DATE'].dt.normalize()
# df['CREATE_DTME'] = df['CREATE_DTME'].dt.normalize()
df2.to_sql(name="d_rrtprod_memorder",con=engine,index=False,if_exists='append')
print("导入成功")
