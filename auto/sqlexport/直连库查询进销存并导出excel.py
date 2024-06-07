from datetime import date

from auto.datalink.datalink import get_oracle_zjcs
from auto.utils.excelutil import execute_queries_save, read_excel, write_to_excel

# from auto.每天跟踪前一天完成率 import desktop_path
desktop_path = r'D:\download\桌面'

begindate=date.today()
print(begindate)

filename = f'配送.xlsx'
filename2 = f'采购.xlsx'
filename3 = f'库存.xlsx'
#
save_path = desktop_path + '\\' + filename
save_path2 = desktop_path + '\\' + filename2
save_path3 = desktop_path + '\\' + filename3

ps="""select * from V_SALE_NH_P001 where CJSJ between date'2024-01-01' and date'2024-01-10' """
cg="""select * from V_accept_NH_P001 where CJSJ between date'2024-01-01' and date'2024-02-01'"""
kc="""select * from V_kc_NH_P001"""

try:
    conn = get_oracle_zjcs()
    # 假设你有多个查询和对应的保存路径
    queries = [ps,cg,kc]
    save_paths = [save_path, save_path2,save_path3]
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

# 将数据框存入字典，键为Sheet名
dfs = {'配送': df1, '采购': df2, '库存': df3}

# 合并到一个Excel文件
output_file = desktop_path + '\\合并.xlsx'
write_to_excel(dfs, output_file)

# 使用Excel打开合并后的文件
subprocess.Popen([excel_exe_path, output_file])

