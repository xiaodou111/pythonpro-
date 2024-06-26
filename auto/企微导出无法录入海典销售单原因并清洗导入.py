import cx_Oracle

import pandas as pd
from auto.datalink.datalink import get_oracle_prod, dml_oracle_table, import_oracle_prod

from auto.utils.excelutil import merge_excel_sheet, import_excel_to_oracle
from auto.utils.gui import get_filename

# merge_excel_sheet()

# s = "2406134002052013"
# num = int(s)
# print(num)

filename = get_filename()
save_path = filename
base_name, extension = filename.rsplit('.', 1)  # 分离文件名和扩展名
output_path = f"{base_name}{'_clean'}.{extension}"  # 构建新的文件名
# 读取所有工作表
xls = pd.read_excel(save_path, sheet_name=None)
df = xls['6.2']
pd.set_option('display.float_format', lambda x: '%.0f' % x)
# print(df['销售单号'].dtype)
# print(df['销售单号'])
# 初始化一个空的 DataFrame
combined_df = pd.DataFrame()
# 合并所有工作表
for sheet_name, df in xls.items():
    df['Sheet_Name'] = sheet_name

    combined_df = pd.concat([combined_df, df], ignore_index=True)
# 写入新的 Excel 文件
df_none=combined_df.columns[combined_df.isnull().all()]
# print(df_none)
combined_df = combined_df.dropna(how='all', axis=1)  # 删除所有值都是 NaN 的列
#如果这些列为空,那么删除所在行
delete_rows=['销售单号']
# 删除这些列中任何一列值为 NaN 的行
combined_df = combined_df.dropna(subset=delete_rows)
# combined_df['销售单号'] = combined_df['销售单号'].apply(lambda x: str(x))
combined_df['销售单号'] = combined_df['销售单号'].astype(str)
# print(combined_df['销售单号'].dtype)
# print(combined_df['销售单号'])
print(combined_df)
combined_df = combined_df[['销售单号']].rename(columns={'销售单号': 'saleno'})

combined_df.to_excel(output_path, index=False)

df.rename(columns={"销售单号":"saleno"}, inplace=True)
#2.先删除前一天数据
delete_sql='delete from d_bp_exclude_sale'
conn = get_oracle_prod()
if conn:
     dml_oracle_table(conn,delete_sql)
#3.连接oracle生产库并把excel导入到表d_bp_exclude_sale中
engine = import_oracle_prod()
print("连接成功，正在导入Excel数据！")
import_excel_to_oracle(engine, output_path, "d_bp_exclude_sale")
connection = cx_Oracle.connect('h2/HDrrt_2021wbzD@10.118.4.10:1525/hydee')
update_sql="""UPDATE d_bp_exclude_sale SET SALENO = REGEXP_REPLACE(SALENO, '\.0$') WHERE REGEXP_LIKE(SALENO, '\.0$')"""
dml_oracle_table(connection, update_sql)