import os


def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def load_sql_files(directory):
    sql_files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.sql'):
            filepath = os.path.join(directory, filename)
            sql_files[filename[:-4]] = read_file_content(filepath)
    return sql_files


# 使用函数读取目录下所有SQL文件
sql_directory = '../sql'
sql_queries = load_sql_files(sql_directory)
qydc=sql_queries['qydc']
qyzsdc=sql_queries['qyzsdc']
rrto2owcl=sql_queries['rrto2owcl']
rrtwcl=sql_queries['rrtwcl']
txwcl=sql_queries['txwcl']
zsdjwcl=sql_queries['zsdjwcl']



print(sql_queries['qydc'])
# print(os.getcwd())