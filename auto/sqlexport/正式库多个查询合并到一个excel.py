from datetime import date

from auto.datalink.datalink import get_oracle_zjcs, get_oracle_prod
from auto.utils.excelutil import  read_excel, write_to_excel
from auto.utils.sqlutil import execute_queries_save

# from auto.每天跟踪前一天完成率 import desktop_path
desktop_path = r'D:\download\桌面'

begindate=date.today()
print(begindate)

filename = f'11.xlsx'
filename2 = f'22.xlsx'
filename3 = f'33.xlsx'
filename4 = f'44.xlsx'
#
save_path = desktop_path + '\\' + filename
save_path2 = desktop_path + '\\' + filename2
save_path3 = desktop_path + '\\' + filename3
save_path4 = desktop_path + '\\' + filename4

with open('./sqls/1.sql', 'r', encoding='utf-8') as file:
    sql1 = file.read()
with open('./sqls/2.sql', 'r', encoding='utf-8') as file:
    sql2 = file.read()
with open('./sqls/3.sql', 'r', encoding='utf-8') as file:
    sql3 = file.read()
with open('./sqls/4.sql', 'r', encoding='utf-8') as file:
    sql4 = file.read()


try:
    conn = get_oracle_prod()
    # 假设你有多个查询和对应的保存路径
    queries = [sql1,sql2,sql3,sql4]
    save_paths = [save_path, save_path2,save_path3,save_path4]
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
dfs = {'桐乡并跑排名': df1, '桐乡并跑明细': df2, '桐乡试点排名': df3,'桐乡试点明细':df4}

# 合并到一个Excel文件
output_file = desktop_path + '\\合并.xlsx'
write_to_excel(dfs, output_file)

# 使用Excel打开合并后的文件
subprocess.Popen([excel_exe_path, output_file])

