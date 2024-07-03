import json
import subprocess

import json5

from auto.datalink.datalink import import_oracle_prod, get_oracle_zjcs, import_oracle_zjcs
from auto.utils.excelutil import rename_excel_onesheet, rename_desk_excel_onesheet, import_excel_to_oracle, \
    rename_desk_excel_one_and_import
#注意 excel后缀名为xslx,_clean文件不能为打开状态
mappings_file= "zjcs.json5"
with open(mappings_file, 'r',encoding='utf-8') as file:
    mappings = json5.load(file)
    # print(mappings)
table="d_yp_ps_py"
#通过表明找映射关系
mapping_key = mappings[table]
print(mapping_key)


# date_columns = ['ZDATE']
# rename_desk_excel_onesheet(mapping_key)
# table="D_NH_PS_PY"
# coon=import_oracle_zjcs()
# rename_desk_excel_onesheet(mapping_key)
#清洗表格字段,同时生成_clean文件并打开
try:
    output_path=rename_desk_excel_onesheet(mapping_key)
    engine = import_oracle_zjcs()
    print("连接成功，正在导入Excel数据！")
    import_excel_to_oracle(engine, output_path, table)
except Exception as e:
    print(f"请选择单页面文件并先关闭_clean文件并检查是否为xlsx格式文件。错误信息：{e}")
#导入excel数据
