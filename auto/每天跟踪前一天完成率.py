import pandas as pd
from datetime import datetime, timedelta

from auto.datalink.datalink import get_rrt_mysql, get_oracle_prod, import_oracle_prod, get_qy_mysql
from auto.utils.excelutil import query_save_to_excel

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
    connection = get_qy_mysql()
    print("连接成功！")
    query_save_to_excel(connection,qydc,save_path)
finally:
    connection.close()
#2.连接oracle生产库并把qy库导出的excel导入到表D_RRTPROD_MEMORDER中
engine = import_oracle_prod()
print("连接成功,正在导入excel数据！")
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
try:
    conn = get_oracle_prod()
    print("成功连接到oracle-prod")
    query_save_to_excel(conn, rrtwlc, save_path2)
finally:
    # 关闭游标和连接
    conn.close()

try:
    conn = get_oracle_prod()
    print("成功连接到oracle-prod")
    query_save_to_excel(conn, txwlc, save_path3)
finally:
    # 关闭游标和连接
    conn.close()
#4自动打开刚才的完成率两张表并格式化
# import subprocess
# #excel打开PERSONAL.xlsb
# excel_exe_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'
# rrt_path = save_path2
# tx_path = save_path3
#
# subprocess.Popen([excel_exe_path, save_path2])
# subprocess.Popen([excel_exe_path, save_path3])
