import os

import pandas as pd
from datetime import datetime, timedelta

from auto.datalink.datalink import get_rrt_mysql, get_oracle_prod, import_oracle_prod, get_qy_mysql, dml_oracle_table, \
    get_qy_uatmysql
from auto.utils.excelutil import  import_excel_to_oracle
from auto.utils.sqlutil import execute_queries_save, query_save_to_excel

# 获取昨天的日期
yesterday = datetime.now() - timedelta(days=1)
# 格式化日期为字符串
formatted_date = yesterday.strftime('%Y%m%d')
out_file=f'{formatted_date}_完成率.xlsx'
file_sale = f'{formatted_date}_销售.xlsx'
file_qy_zsdc = f'{formatted_date}_药店通诊所挂号记录.xlsx'
file_rrtwcl = f'{formatted_date}_瑞人堂完成率.xlsx'
file_txwcl = f'{formatted_date}_桐乡完成率.xlsx'
file_rrt_o2owcl= f'{formatted_date}_瑞人堂o2o完成率.xlsx'
file_tx_o2owcl=f'{formatted_date}_桐乡o2o完成率.xlsx'
file_rrt_zswcl=f'{formatted_date}_瑞人堂诊所完成率.xlsx'
file_tx_zswcl=f'{formatted_date}_桐乡诊所完成率.xlsx'
# file_tx_o2o = f'{formatted_date}_桐乡o2o完成率.xlsx'
# filename = f'{formatted_date}_销售.csv'
desktop_path = r'D:\download\桌面'
output_file = os.path.join(desktop_path, out_file)
save_sale = os.path.join(desktop_path, file_sale)
save_qy_zsdc = os.path.join(desktop_path, file_qy_zsdc)
save_rrtwcl = os.path.join(desktop_path, file_rrtwcl)
save_txwcl = os.path.join(desktop_path, file_txwcl)
save_rrt_o2owcl = os.path.join(desktop_path, file_rrt_o2owcl)
save_tx_o2owcl = os.path.join(desktop_path, file_tx_o2owcl)
save_rrt_zswcl = os.path.join(desktop_path, file_rrt_zswcl)
save_tx_zswcl = os.path.join(desktop_path, file_tx_zswcl)

print(f"save_path:{save_sale}")
print(f"save_path2:{save_qy_zsdc}")
print(f"save_path3:{save_rrtwcl}")
print(f"save_path3:{save_txwcl}")
print(f"save_path3:{save_rrt_o2owcl}")
print(f"save_path3:{save_tx_o2owcl}")
print(f"save_path3:{save_rrt_zswcl}")
print(f"save_path3:{save_tx_zswcl}")
with open('./sql/qydc.sql', 'r', encoding='utf-8') as file:
    qydc = file.read()
with open('./sql/qyzsdc.sql', 'r', encoding='utf-8') as file:
    qyzsdc = file.read()
with open('./sql/rrto2owcl.sql.', 'r', encoding='utf-8') as file:
    rrto2owcl = file.read()
with open('./sql/rrtwcl.sql', 'r', encoding='utf-8') as file:
    rrtwlc = file.read()
with open('./sql/rrtzswcl.sql', 'r', encoding='utf-8') as file:
    rrtzswcl = file.read()
with open('./sql/txo2owcl.sql', 'r', encoding='utf-8') as file:
    txo2owcl = file.read()
with open('./sql/txwcl.sql', 'r', encoding='utf-8') as file:
    txwlc = file.read()
with open('./sql/txzswcl.sql', 'r', encoding='utf-8') as file:
    txzswcl = file.read()
#1.连接qy库并导出sql结果为excel到桌面
try:
    connection = get_qy_uatmysql()
    print("连接成功,导出数据中！")
    query_save_to_excel(connection,qydc,save_sale)
    query_save_to_excel(connection, qyzsdc, save_qy_zsdc)
finally:
    connection.close()
#2.先删除前一天数据
df_yesterday='delete from d_rrtprod_memorder where ORDER_DATE=trunc(sysdate)-1'
df_yesterday_zs='delete from D_QY_ZSDJ where ORDER_DATE=trunc(sysdate)-1'
conn = get_oracle_prod()
if conn:
     try:
         dml_oracle_table(conn,df_yesterday)
         dml_oracle_table(conn, df_yesterday_zs)
     finally:
         if conn:
             conn.close()
#3.连接oracle生产库并把qy库导出的excel导入到表D_RRTPROD_MEMORDER中
engine = import_oracle_prod()
print("连接成功，正在导入Excel数据！")
import_excel_to_oracle(engine, save_sale, "D_RRTPROD_MEMORDER")
import_excel_to_oracle(engine, save_qy_zsdc, "D_QY_ZSDJ")
#4.执行瑞人堂和桐乡完成率的sql并分别导出结果excel到桌面

try:
    conn = get_oracle_prod()
    # 假设你有多个查询和对应的保存路径
    queries = [rrtwlc,txwlc,rrto2owcl,txo2owcl,rrtzswcl,txzswcl]
    save_paths = [save_rrtwcl, save_txwcl,save_rrt_o2owcl,save_tx_o2owcl,save_rrt_zswcl,save_tx_zswcl]
    execute_queries_save(conn, queries, save_paths)
finally:
    # 最终关闭连接
    if conn:
        conn.close()
#5.合并sheet页
# output_file = desktop_path + '\\' + 'test.xlsx'
excel_data_dict = {}
# save_paths = [save_path2, save_path3,save_rrt_o2o]
# 遍历每个Excel文件
for file in save_paths:
    # 构建完整的文件路径

    # 读取Excel文件
    excel_data_dict[os.path.basename(file)] = pd.read_excel(file)

# 使用字典创建一个ExcelWriter对象
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 遍历字典，将每个DataFrame写入一个Sheet
    for sheet_name, df in excel_data_dict.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)
#6自动打开刚才合并的表并格式化
import subprocess
# #excel打开PERSONAL.xlsb
excel_exe_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'
# rrt_path = save_path2
# tx_path = save_path3
#
subprocess.Popen([excel_exe_path, output_file])
# subprocess.Popen([excel_exe_path, tx_path])
