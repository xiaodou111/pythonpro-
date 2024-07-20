import os

from auto.datalink.datalink import get_qy_uatmysql, get_oracle_prod, dml_oracle_table, import_oracle_prod
from auto.utils.sqlutil import query_save_to_excel, import_excel_to_oracle, execute_queries_save

desktop_path = r'D:\download\桌面\员工登录日志'
emp_file=f'员工登录总数.xlsx'
qy_emp_path = os.path.join(desktop_path, emp_file)

qy_empelog_sql="""SELECT auth_user_name AS userid
FROM rrtuat_platform.sys_user_wechat_auth_log
WHERE auth_user_name IS NOT NULL
  AND LENGTH(auth_user_name) <= 8
  AND auth_user_name NOT REGEXP '[^0-9]'
group by auth_user_name"""
print(f"员工登录总数表路径:{qy_emp_path}")

#1.连接qy库并导出sql结果为excel到桌面
try:
    connection = get_qy_uatmysql()
    print("连接成功,导出数据中！")
    query_save_to_excel(connection,qy_empelog_sql,qy_emp_path)
    # query_save_to_excel(connection, qyzsdc, save_qy_zsdc)
finally:
    connection.close()
#2.连接Oracle生产库并删除表数据
df_empelog='delete from d_ydt_ygdl'
conn = get_oracle_prod()
if conn:
     try:
         dml_oracle_table(conn,df_empelog)
         # dml_oracle_table(conn, df_yesterday_zs)
     finally:
         if conn:
             conn.close()
#3.连接oracle生产库并把qy库导出的excel导入到表d_ydt_ygdl中
engine = import_oracle_prod()
print("连接成功，正在导入Excel数据！")
import_excel_to_oracle(engine, qy_emp_path, "d_ydt_ygdl")
oracle_emp_sql="""select USERID,USERNAME from S_USER_BASE where USERID in (select userid from d_ydt_ygdl)"""
#4.导出oracle生产库多个查询结果到对应路径
oracle_emp_path=os.path.join(desktop_path, '员工登录明细.xlsx')
try:
    conn = get_oracle_prod()
    # 假设你有多个查询和对应的保存路径
    queries = [oracle_emp_sql]
    save_paths = [oracle_emp_path]
    execute_queries_save(conn, queries, save_paths)
finally:
    # 最终关闭连接
    if conn:
        conn.close()
