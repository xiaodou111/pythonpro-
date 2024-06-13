import json

from auto.datalink.datalink import import_oracle_prod, get_oracle_zjcs, import_oracle_zjcs
from auto.utils.excelutil import rename_excel_onesheet, rename_desk_excel_onesheet, import_excel_to_oracle, \
    rename_desk_excel_one_and_import, rename_desk_excel_manysheet

mappings_file= "zjcs.json"
with open(mappings_file, 'r',encoding='utf-8') as file:
    mappings = json.load(file)

mapping_key = mappings["D_HFYF_SALE"]
print(mapping_key)

rename_desk_excel_manysheet(mapping_key)