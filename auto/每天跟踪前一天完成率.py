import pandas as pd
from datetime import datetime, timedelta

from auto.datalink.datalink import get_rrt_mysql, get_oracle_prod, import_oracle_prod, get_qy_mysql,dml_oracle_table
from auto.utils.excelutil import query_save_to_excel, execute_queries_save, import_excel_to_oracle

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
#2.先删除前一天数据
df_yesterday='delete from d_rrtprod_memorder where ORDER_DATE=trunc(sysdate-1)'
conn = get_oracle_prod()
if conn:
     dml_oracle_table(conn,df_yesterday)
#3.连接oracle生产库并把qy库导出的excel导入到表D_RRTPROD_MEMORDER中
engine = import_oracle_prod()
print("连接成功，正在导入Excel数据！")
import_excel_to_oracle(engine, save_path, "D_RRTPROD_MEMORDER")
#4.执行瑞人堂和桐乡完成率的sql并分别导出结果excel到桌面

try:
    conn = get_oracle_prod()
    # 假设你有多个查询和对应的保存路径
    queries = [rrtwlc, txwlc]
    save_paths = [save_path2, save_path3]
    execute_queries_save(conn, queries, save_paths)
finally:
    # 最终关闭连接
    if conn:
        conn.close()
#4自动打开刚才的完成率两张表并格式化
import subprocess
# #excel打开PERSONAL.xlsb
excel_exe_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'
rrt_path = save_path2
tx_path = save_path3
#
subprocess.Popen([excel_exe_path, rrt_path])
subprocess.Popen([excel_exe_path, tx_path])
