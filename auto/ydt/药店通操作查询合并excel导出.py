import os

import pandas as pd
from datetime import datetime, timedelta

from auto.datalink.datalink import get_rrt_mysql, get_oracle_prod, import_oracle_prod, get_qy_mysql, dml_oracle_table, \
    get_qy_uatmysql
from auto.utils.excelutil import import_excel_to_oracle
from auto.utils.sqlutil import execute_queries_save, query_save_to_excel

# 获取昨天的日期
# yesterday = datetime.now() - timedelta(days=1)
today=datetime.now()
# 格式化日期为字符串
formatted_date = today.strftime('%Y%m%d')
out_file = f'{formatted_date}_操作情况.xlsx'

files = [
    f'{formatted_date}_小宝.xlsx',
    f'{formatted_date}_补货.xlsx',
    f'{formatted_date}_退仓.xlsx',
    f'{formatted_date}_调拨.xlsx',
    f'{formatted_date}_到货验收.xlsx',
    f'{formatted_date}_养护.xlsx',
    f'{formatted_date}_温湿度记录.xlsx',
    f'{formatted_date}_处方登记.xlsx',
    f'{formatted_date}_医生开方.xlsx'
]
desktop_path = r'D:\download\桌面\药店通其他操作'
save_paths = [os.path.join(desktop_path, file) for file in files]
# for path in save_paths:
#     print(path)

output_file = os.path.join(desktop_path, out_file)

# SQL文件所在的目录
sql_dir = './sqls'

# 需要读取的SQL文件名及其对应的变量名
sql_files = {
    '2-1.sql': 'xiaobao',
    '3-1.sql': 'buhuo',
    '3-2.sql': 'tuicang',
    '3-3.sql': 'diaoru',
    '3-4.sql': 'yanshou',
    '4-1.sql': 'yanghu',
    '4-2.sql': 'wenshidu',
    '4-3.sql': 'chufang',
    '5-2.sql': 'kaifang',
}

# 创建一个空列表，用于存储SQL查询
queries = []

# 遍历字典中的文件名和变量名
for file_name, _ in sql_files.items():
    # 构建完整的文件路径
    file_path = os.path.join(sql_dir, file_name)

    # 打开并读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 将文件内容添加到列表中
    queries.append(content)

# 打印或使用查询列表
# for i, query in enumerate(queries):
#     print(f"Query {i + 1}: {query[:50]}...")


try:
    connection = get_qy_uatmysql()
    print("连接成功,导出数据中！")
    # queries = [xiaobao, buhuo, tuicang, diaoru, kaifang, yanshou, chufang, yanghu, kaifang, tuicang]
    # save_paths = [save_xiaobao, save_buhuo, save_tuicang, save_diaoru, save_diaochu, save_yanshou, save_yanghu,
    #               save_wenshidu, save_chufang, save_kaifang]
    execute_queries_save(connection, queries, save_paths)
finally:
    connection.close()

# 5.合并sheet页
excel_data_dict = {}

# 遍历每个Excel文件
for file in save_paths:
    # 构建完整的文件路径

    # 读取Excel文件
    excel_data_dict[os.path.basename(file)] = pd.read_excel(file)

# 使用字典创建一个ExcelWriter对象
try:
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 遍历字典，将每个DataFrame写入一个Sheet
        for sheet_name, df in excel_data_dict.items():
          df.to_excel(writer, sheet_name=sheet_name, index=False)
except Exception as e:
         print(f"请先关闭{output_file}")
# 6自动打开刚才合并的表并格式化
import subprocess

# #excel打开PERSONAL.xlsb
excel_exe_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'
# rrt_path = save_path2
# tx_path = save_path3
#
subprocess.Popen([excel_exe_path, output_file])
# subprocess.Popen([excel_exe_path, tx_path])


# 遍历每个文件路径并尝试删除文件
for path in save_paths:
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted: {path}")
        else:
            print(f"File does not exist: {path}")
    except Exception as e:
        print(f"Error deleting {path}: {e}")
