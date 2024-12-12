from datetime import date

from auto.datalink.datalink import get_oracle_zjcs, get_oracle_prod, con_oracle_qysjzl, get_oracle_qysjzl
from auto.utils.excelutil import  read_excel, write_to_excel
from auto.utils.sqlutil import execute_queries_save

# from auto.每天跟踪前一天完成率 import desktop_path
desktop_path = r'D:\download\桌面'

begindate=date.today()
print(begindate)

filename = f'配送.xlsx'
filename2 = f'库存.xlsx'
filename3 = f'采购.xlsx'
filename4 = f'纯销.xlsx'
#
save_path = desktop_path + '\\' + filename
save_path2 = desktop_path + '\\' + filename2
save_path3 = desktop_path + '\\' + filename3
save_path4 = desktop_path + '\\' + filename4

with open('./sqls/配送.sql', 'r', encoding='utf-8') as file:
    sql1 = file.read()
with open('./sqls/库存.sql', 'r', encoding='utf-8') as file:
    sql2 = file.read()
with open('./sqls/采购.sql', 'r', encoding='utf-8') as file:
    sql3 = file.read()
with open('./sqls/纯销.sql', 'r', encoding='utf-8') as file:
    sql4 = file.read()


try:
    conn = get_oracle_qysjzl()
    # 假设你有多个查询和对应的保存路径
    queries = [sql1,sql2,sql3,sql4]
    # queries = [sql1,sql2,sql3]
    save_paths = [save_path, save_path2,save_path3,save_path4]
    # save_paths = [save_path, save_path2,save_path3]
    execute_queries_save(conn, queries, save_paths)
finally:
    # 最终关闭连接
    if conn:
        conn.close()
import subprocess
# #excel打开PERSONAL.xlsb
excel_exe_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'


df1 = read_excel(save_path)
df2 = read_excel(save_path2)
df3 = read_excel(save_path3)
df4 = read_excel(save_path4)

# 将数据框存入字典，键为Sheet名
dfs = {'配送': df1, '期初库存': df2, '采购': df3,'期末库存':df4}
# dfs = {'配送': df1, '库存': df2, '采购': df3}

# 合并到一个Excel文件
output_file = desktop_path + '\\阿斯利康.xlsx'
write_to_excel(dfs, output_file)

# 使用Excel打开合并后的文件
subprocess.Popen([excel_exe_path, output_file])

