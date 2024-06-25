import json

from auto.datalink.datalink import import_oracle_prod, get_oracle_zjcs, import_oracle_zjcs
from auto.utils.excelutil import rename_excel_onesheet, rename_desk_excel_onesheet, import_excel_to_oracle, \
    rename_desk_excel_one_and_import

mappings_file= "h2.json"
with open(mappings_file, 'r',encoding='utf-8') as file:
    mappings = json.load(file)
    # print(mappings)

mapping_key = mappings["D_TSL_BUSINESS"]
print(mapping_key)


# date_columns = ['ZDATE']
# rename_desk_excel_onesheet(mapping_key)
# table="D_NH_PS_PY"
# coon=import_oracle_zjcs()
rename_desk_excel_onesheet(mapping_key)



