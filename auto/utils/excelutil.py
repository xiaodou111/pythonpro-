import pandas as pd
#执行SQL查询并将结果保存为Excel文件。
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



