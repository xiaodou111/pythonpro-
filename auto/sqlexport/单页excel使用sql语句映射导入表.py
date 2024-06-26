import json

from auto.datalink.datalink import import_oracle_prod, get_oracle_zjcs, import_oracle_zjcs
from auto.utils.excelutil import rename_excel_onesheet, rename_desk_excel_onesheet, import_excel_to_oracle, \
    rename_desk_excel_one_and_import, rename_excel_one_import_sql, import_excel_to_oracle_usesql

mappings_file= "h2.json5"
with open(mappings_file, 'r',encoding='utf-8') as file:
    mappings = json.load(file)
    print(mappings)
mapping_key = mappings["d_sale_business1"]
print(mapping_key)
table="d_sale_business1"
coon=import_oracle_zjcs()
rename_excel_one_import_sql(mapping_key,coon,table)
# D:\download\桌面\门店销售24年6月 (1)_modified.xlsx