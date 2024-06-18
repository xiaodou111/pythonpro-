import pandas as pd


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

        # 获取数据库表的列名
        table_columns = pd.read_sql(f"SELECT * FROM {table_name} WHERE ROWNUM <= 0", engine).columns
        df_column_names_upper = {col.lower() for col in df.columns.tolist()}
        table_columns_upper = {col.lower() for col in table_columns.tolist()}
        # 找出 DataFrame 缺失的列
        missing_cols = table_columns_upper - df_column_names_upper
        print('excel缺失的列',missing_cols)
        # 为 DataFrame 添加缺失的列，并填充 NULL 或默认值
        for col in missing_cols:
            df[col] = None  # 或者 df[col] = some_default_value

        # 找出 DataFrame 多余的列
        extra_cols = df_column_names_upper - table_columns_upper
        print('excel多余的列:',extra_cols)
        # 删除 DataFrame 中多余的列
        df.drop(columns=list(extra_cols), inplace=True)
        print(f'即将从excel:{excel_path}导入到表:{table_name}中的列:', df.columns)
        # 然后继续导入数据到数据库
        num_rows = len(df)
        print(num_rows)
        # df = convert_date_columns(df, date_columns)
        # 将DataFrame写入数据库
        df.to_sql(name=table_name, con=engine, index=False, if_exists='append')

        print(f"导入成功，共导入 {num_rows} 行数据")
    except Exception as e:
        # 处理可能发生的错误
        print(f"数据导入失败：{e}")

#把excel生成sql插入数据库表
def import_excel_to_oracle_usesql(engine, excel_path, table_name, column_mapping=None):
    try:
        # 读取Excel数据
        df = pd.read_excel(excel_path)

        # 记录DataFrame的长度（即行数）
        num_rows = len(df)

        insert_sql = []
        date_format = "'YYYY-MM-DD HH24:MI:SS'"  # Oracle 日期格式

        # 确定哪些列是日期时间类型
        datetime_columns = [col for col in df.columns if df[col].dtype == 'datetime64[ns]']

        for index, row in df.iterrows():
            values = []
            for col in column_mapping.values():
                if col in datetime_columns:
                    # 如果列是日期时间类型，使用 TO_DATE 转换
                    dt_value = row[col].strftime('%Y-%m-%d %H:%M:%S')  # 将日期时间格式化为字符串
                    values.append(f"TO_DATE({dt_value}, {date_format})")
                elif pd.notnull(row[col]):
                    values.append(f"'{row[col]}'")  # 对于非空的非日期时间列
                else:
                    values.append('NULL')  # 对于空值

            sql = f"INSERT INTO {table_name} ({', '.join(column_mapping.values())}) VALUES ({', '.join(values)});"
            insert_sql.append(sql)

        # 执行 SQL 插入语句
        with engine.connect() as connection:
            for sql in insert_sql:
                connection.execute(sql)
        print(f"导入成功，共导入 {num_rows} 行数据")
    except Exception as e:
        # 处理可能发生的错误
        print(f"数据导入失败：{e}")