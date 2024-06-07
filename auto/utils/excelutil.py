import pandas as pd
#执行SQL查询并将结果保存为Excel文件。
import subprocess

from auto.utils.gui import get_filename

# #excel打开PERSONAL.xlsb
excel_exe_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'


def query_save_to_excel(connection, sql_query, save_path):
    """
    执行SQL查询并将结果保存为Excel文件。

    参数:
    connection (pymysql.connections.Connection): 数据库连接
    sql_query (str): 要执行的SQL查询语句
    save_path (str): Excel文件的保存路径
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            # 将查询结果转换为DataFrame
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
            # 导出DataFrame到Excel文件
            df.to_excel(save_path, index=False)
            print(f"文件已保存到 {save_path}")

    except Exception as e:
        print(f"处理数据或保存文件时发生错误: {e}")

#执行一系列查询并将结果保存到Excel文件。
def execute_queries_save(connection, queries, save_paths):
    """
    执行一系列查询并将结果保存到Excel文件。

    参数:
    connection (cx_Oracle.Connection): 数据库连接
    queries (list of str): 查询语句列表
    save_paths (list of str): 对应的保存路径列表
    """
    try:
        with connection.cursor() as cursor:
            for query, save_path in zip(queries, save_paths):
                cursor.execute(query)
                rows = cursor.fetchall()
                df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
                df.to_excel(save_path, index=False)
                print(f"文件已保存到 {save_path}")
    except Exception as e:
        print(f"处理数据或保存文件时发生错误: {e}")


import pandas as pd

#从Excel文件导入数据到Oracle数据库。
def import_excel_to_oracle(engine, excel_path, table_name):
    """
    从Excel文件导入数据到Oracle数据库。

    :param engine: 数据库连接引擎
    :param excel_path: Excel文件的路径
    :param table_name: 目标数据库表名
    """
    try:
        # 读取Excel数据
        df = pd.read_excel(excel_path)

        # 记录DataFrame的长度（即行数）
        num_rows = len(df)

        # 将DataFrame写入数据库
        df.to_sql(name=table_name, con=engine, index=False, if_exists='append')
        #     # # df2 = pd.read_excel('20240605_销售s.xlsx', parse_dates=['ORDER_DATE', 'CREATE_DTME'])
        #     #
        #     # # 如果原始数据中时间信息不全，添加默认的时分秒
        #     # # df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE']).dt.to_period('D').to_timestamp('D')
        #     # # df['CREATE_DTME'] = pd.to_datetime(df['CREATE_DTME']).dt.to_period('D').to_timestamp('D')
        #     # 输出导入成功的行数
        # 输出导入成功的行数
        print(f"导入成功，共导入 {num_rows} 行数据")
    except Exception as e:
        # 处理可能发生的错误
        print(f"数据导入失败：{e}")

# 读取Excel文件的函数
def read_excel(file_path):
    return pd.read_excel(file_path, engine='openpyxl')

# 写入Excel文件的函数
def write_to_excel(df_dict, output_file):
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

#输入源文件路径名,目标路径名,映射字典替换字段 只修改包含sheet页包含配送的excel
def rename_excel_ps(source_path, target_path=None, columns_mapping=None):
    # 读取Excel文件
    xls = pd.ExcelFile(source_path)
    sheet_names = xls.sheet_names

    # 创建一个字典，用于存储所有sheet的数据帧
    dataframes = {}

    # 如果没有指定目标路径，则默认保存在原位置
    if target_path is None:
        target_path = source_path

    # 如果没有提供列名映射，则使用默认映射
    if columns_mapping is None:
        columns_mapping = {
            '过账日期': 'ZDATE',
            '业务机构名称': 'NAME1',
            '单据类型': 'DJLX',
            '商品编码': 'WAREID',
            '生产企业': 'SCQY',
            '相关单位名称': 'ORGNAME',
            '入库数量': 'RKSL',
            '出库数量': 'CKSL',
            '批号': 'PH'
        }

    # 遍历所有sheet
    for sheet_name in sheet_names:
        # 读取单个sheet到DataFrame
        df = xls.parse(sheet_name)

        # 如果sheet名包含'配送'，则进行列名重命名
        if '配送' in sheet_name:
            df.rename(columns=columns_mapping, inplace=True)
            print(f"对工作表'{sheet_name}'进行了列重命名！")

        # 将DataFrame存储到字典中，key为sheet名
        dataframes[sheet_name] = df

    # 将修改后的DataFrame写回到Excel文件中
    with pd.ExcelWriter(target_path) as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"所有工作表已保存至Excel文件{target_path}。")
    #打开工作薄
    subprocess.Popen([excel_exe_path, target_path])
#单页任意excel清洗
def rename_excel_onesheet(source_path, target_path=None, columns_mapping=None):
    # 读取Excel文件
    xls = pd.ExcelFile(source_path)

    # 读取单个sheet到DataFrame
    df = xls.parse(xls.sheet_names[0])

    # 如果有列名映射，进行列名重命名
    if columns_mapping:
        df.rename(columns=columns_mapping, inplace=True)
        print(f"对工作表'{xls.sheet_names[0]}'进行了列重命名！")

    # 如果没有指定目标路径，则默认保存在原位置
    if target_path is None:
        target_path = source_path

    # 将修改后的DataFrame写回到Excel文件中
    with pd.ExcelWriter(target_path) as writer:
        df.to_excel(writer, sheet_name=xls.sheet_names[0], index=False)

    print(f"工作表已保存至Excel文件{target_path}。")

    # 打开工作簿

    try:
        subprocess.Popen([excel_exe_path, target_path])
    except Exception as e:
        print(f"打开文件失败，请手动打开文件。错误信息：{e}")

def rename_desk_excel_onesheet(columns_mapping):
    desktop_path = r'D:\download\桌面'
    # filename = input("请输入Excel文件名：")
    filename = get_filename()
    #
    save_path = desktop_path + '\\' + filename + '.xlsx'
    output_path = desktop_path + '\\' + filename + '_modified.xlsx'
    rename_excel_onesheet(save_path, output_path, columns_mapping)