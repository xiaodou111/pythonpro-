import os
import sys
import time

import pandas as pd
import psycopg2
from datetime import datetime, timedelta

from auto.datalink.datalink import get_qy_uatmysql, get_qy_prodmysql
from auto.utils.sqlutil import execute_queries_save


def save_to_excel(excel_data_dict, output_file, max_retries=5, retry_delay=5):
    retries = 0
    success = False

    while retries < max_retries and not success:
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # 遍历字典，将每个DataFrame写入一个Sheet
                for sheet_name, df in excel_data_dict.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            success = True
            print(f"Data saved to {output_file} successfully.")
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Attempt {retries + 1} failed. Retrying in {retry_delay} seconds...")
            retries += 1
            time.sleep(retry_delay)

    if not success:
        print(f"Failed to save data to {output_file} after {max_retries} attempts.")
def uat_excel_pldc():

    today = datetime.now()
    # 格式化日期为字符串
    formatted_date = today.strftime('%Y%m%d')
    out_file = f'生产库大屏情况.xlsx'
    files = [
        f'正式门店登录.xlsx',
        f'正式机台登录.xlsx',
        f'正式用户登录.xlsx',
        f'正式零售销售.xlsx',
        f'正式零售退单.xlsx',
        f'正式医保销售.xlsx',
        f'正式医保退单.xlsx',
        f'正式O2O转单.xlsx',
        f'正式诊所开方.xlsx',
        f'正式诊所销售.xlsx',
        f'正式药店非医保处方.xlsx',
        f'正式药店医保外配处方.xlsx',
        f'正式日结对账.xlsx',
        f'正式工号角色登录.xlsx',
        f'正式零售销售明细.xlsx',
    ]
    desktop_path = r"\\192.168.101.136\dashboard"
    save_paths = [os.path.join(desktop_path, file) for file in files]
    # for path in save_paths:
    #     print(path)

    output_file = os.path.join(desktop_path, out_file)

    # SQL文件所在的目录
    sql_dir = './sqls'
    sql_files = {
        '1mdlogin.sql': 'a',
        '2jtlogin.sql': 'b',
        '3userlogin.sql': 'c',
        '4sale.sql': 'd',
        '5salere.sql': 'e',
        '6ybsale.sql': 'f',
        '7ybsalere.sql': 'g',
        '8o2o.sql': 'h',
        '9zskf.sql': 'i',
        '10zssale.sql': 'j',
        '11ydfybcf.sql': 'k',
        '12ydybwpcf.sql': 'l',
        '13rjdz.sql': 'm',
        '14yhzdl.sql': 'n',
        '15lsmx.sql': 'n',
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
    try:
        # # 创建连接
        # connection = psycopg2.connect(**conn_params)
        # print("Connected to the PostgreSQL server successfully")
        execute_queries_save(connection, queries, save_paths)
    finally:
        # 关闭游标和连接
        pass
        # if (connection):
        #     connection.close()
        #     print("PostgreSQL connection is closed")
    # 5.合并sheet页
    excel_data_dict = {}

    # 遍历每个Excel文件
    for file in save_paths:
        # 构建完整的文件路径

        # 读取Excel文件
        excel_data_dict[os.path.basename(file)] = pd.read_excel(file)

    save_to_excel(excel_data_dict, output_file, max_retries=5, retry_delay=5)

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

connection = get_qy_prodmysql()
print("prod连接成功,导出数据中！")
while True:
     uat_excel_pldc()
     for remaining in range(30, 0, -1):
         sys.stdout.write(f"{remaining}.")
         sys.stdout.flush()
         time.sleep(1)
     print("Retrying...")
