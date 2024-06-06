
from sqlalchemy import create_engine
import cx_Oracle
import pandas as pd
engine = create_engine('oracle+cx_oracle://h2:HDrrt_2021wbzD@10.118.4.10:1525/hydee')
print("连接成功！")



df2= pd.read_excel("20240605_销售s.xlsx")

# 记录DataFrame的长度（即行数）
num_rows = len(df2)

try:
    # 将DataFrame写入数据库
    df2.to_sql(name="D_RRTPROD_MEMORDER_TEST", con=engine, index=False, if_exists='append')

    # 输出导入成功的行数
    print(f"导入成功，共导入 {num_rows} 行数据")
except Exception as e:
    # 处理可能发生的错误
    print(f"数据导入失败：{e}")
#
# # df2 = pd.read_excel('20240605_销售s.xlsx', parse_dates=['ORDER_DATE', 'CREATE_DTME'])
#
# # 如果原始数据中时间信息不全，添加默认的时分秒
# # df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE']).dt.to_period('D').to_timestamp('D')
# # df['CREATE_DTME'] = pd.to_datetime(df['CREATE_DTME']).dt.to_period('D').to_timestamp('D')
# #
# # # 或者，如果你希望所有时间都设定为每天的00:00:00
# # df['ORDER_DATE'] = df['ORDER_DATE'].dt.normalize()
# # df['CREATE_DTME'] = df['CREATE_DTME'].dt.normalize()
# df2.to_sql(name="D_RRTPROD_MEMORDER_TEST",con=engine,index=False,if_exists='append')
# print("导入成功")
