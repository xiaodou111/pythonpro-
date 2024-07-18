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
out_file=f'{formatted_date}_操作情况.xlsx'
file_xiaobao = f'{formatted_date}_小宝.xlsx'
file_buhuo = f'{formatted_date}_补货.xlsx'
file_tuicang = f'{formatted_date}_退仓.xlsx'
file_diaoru = f'{formatted_date}_调拨调入.xlsx'
file_diaochu = f'{formatted_date}_调拨调出.xlsx'
file_yanshou = f'{formatted_date}_到货验收.xlsx'
file_yanghu = f'{formatted_date}_养护.xlsx'
file_wenshidu = f'{formatted_date}_温湿度记录.xlsx'
file_chufang = f'{formatted_date}_处方登记.xlsx'
file_kaifang = f'{formatted_date}_医生开方.xlsx'


desktop_path = r'D:\download\桌面\其他操作'

output_file = os.path.join(desktop_path, out_file)
save_xiaobao=os.path.join(desktop_path, file_xiaobao)
save_buhuo=os.path.join(desktop_path, file_buhuo)
save_tuicang=os.path.join(desktop_path, file_tuicang)
save_diaoru=os.path.join(desktop_path, file_diaoru)
save_diaochu=os.path.join(desktop_path, file_diaoru)
save_yanshou=os.path.join(desktop_path, file_yanshou)
save_yanghu=os.path.join(desktop_path, file_yanghu)
save_wenshidu=os.path.join(desktop_path, file_wenshidu)
save_chufang=os.path.join(desktop_path, file_chufang)
save_kaifang=os.path.join(desktop_path, file_kaifang)

print(f"save_path:{save_xiaobao}")

with open('./sqls/2-1.sql', 'r', encoding='utf-8') as file:
    xiaobao = file.read()
with open('./sqls/3-1.sql', 'r', encoding='utf-8') as file:
    buhuo = file.read()
with open('./sqls/3-2.sql', 'r', encoding='utf-8') as file:
    tuicang = file.read()
with open('./sqls/3-3.sql', 'r', encoding='utf-8') as file:
    diaoru = file.read()
with open('./sqls/3-3-2.sql', 'r', encoding='utf-8') as file:
    diaochu = file.read()
with open('./sqls/3-4.sql', 'r', encoding='utf-8') as file:
    yanshou = file.read()
with open('./sqls/4-1.sql', 'r', encoding='utf-8') as file:
    yanghu = file.read()
with open('./sqls/4-2.sql', 'r', encoding='utf-8') as file:
    wenshidu = file.read()
with open('./sqls/4-3.sql', 'r', encoding='utf-8') as file:
    chufang = file.read()
with open('./sqls/5-2.sql', 'r', encoding='utf-8') as file:
    kaifang = file.read()


try:
    connection = get_qy_uatmysql()
    print("连接成功,导出数据中！")
    queries = [xiaobao, buhuo, tuicang, diaoru, kaifang, yanshou, chufang, yanghu, kaifang, tuicang]
    save_paths = [save_xiaobao, save_buhuo, save_tuicang, save_diaoru,save_diaochu,save_yanshou,save_yanghu,save_wenshidu,save_chufang,save_kaifang]
    execute_queries_save(connection, queries, save_paths)
finally:
    connection.close()


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

