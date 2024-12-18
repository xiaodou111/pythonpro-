# 1. 导入必要的库
import os
from datetime import date
from auto.datalink.datalink import get_oracle_qysjzl
from auto.utils.excelutil import read_excel, write_to_excel
from auto.utils.sqlutil import execute_queries_save
import subprocess
from pathlib import Path
# 2. 定义函数：获取文件夹中的所有SQL文件
def get_sql_files(folder_path):
    sql_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.sql'):
            file_path = os.path.join(folder_path, filename)
            sheet_name = os.path.splitext(filename)[0]  # 获取文件名（不带扩展名）
            sql_files.append((file_path, sheet_name))
    return sql_files
# 3. 读取SQL文件内容
def read_sql_files(sql_files):
    sql_dict = {}
    for file_path, _ in sql_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
            sql_dict[file_path] = sql_content
    return sql_dict
# 4. 执行SQL查询并保存结果
def execute_and_save_queries(conn, sql_dict, temp_folder):
    queries = list(sql_dict.values())
    save_paths = [os.path.join(temp_folder, f"temp_{i}.xlsx") for i in range(len(queries))]
    execute_queries_save(conn, queries, save_paths)
    return save_paths
# 5. 读取临时文件并合并到一个Excel文件
def merge_to_excel(save_paths, sql_files, output_file):
    dfs = {}
    for i, (save_path, (file_path, sheet_name)) in enumerate(zip(save_paths, sql_files)):
        df = read_excel(save_path)
        dfs[sheet_name] = df
    write_to_excel(dfs, output_file)
# 6. 清理临时文件
def cleanup_temp_files(temp_folder):
    for filename in os.listdir(temp_folder):
        if filename.startswith('temp_') and filename.endswith('.xlsx'):
            os.remove(os.path.join(temp_folder, filename))
# 7. 主程序逻辑


if __name__ == "__main__":
    # 指定文件夹路径和输出文件路径
    sql_folder = r'./进销存汇总/阿斯利康'  # SQL文件夹路径
    desktop_path = r'D:\download\桌面'
    temp_folder = r'D:\download\temp'  # 临时文件夹路径
    # 获取 sql_folder 最后一层文件夹的名称
    folder_name = Path(sql_folder).name
    # 构建输出文件路径，使用最后一层文件夹名称作为文件名
    output_file = os.path.join(desktop_path, f'{folder_name}.xlsx')

    # 确保临时文件夹存在
    os.makedirs(temp_folder, exist_ok=True)

    try:
        # 获取SQL文件及其对应的Sheet名称
        sql_files = get_sql_files(sql_folder)

        # 读取SQL文件内容
        sql_dict = read_sql_files(sql_files)

        # 连接数据库
        conn = get_oracle_qysjzl()

        # 执行SQL查询并保存结果到临时文件
        save_paths = execute_and_save_queries(conn, sql_dict, temp_folder)

        # 合并临时文件到一个Excel文件
        merge_to_excel(save_paths, sql_files, output_file)

        # 使用Excel打开合并后的文件
        excel_exe_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'
        subprocess.Popen([excel_exe_path, output_file])

    finally:
        # 关闭数据库连接
        if conn:
            conn.close()

        # 清理临时文件
        cleanup_temp_files(temp_folder)