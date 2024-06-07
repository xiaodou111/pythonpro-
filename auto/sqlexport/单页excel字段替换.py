import json
from auto.utils.excelutil import rename_excel_onesheet, rename_desk_excel_onesheet
mappings_file="column_mappings.json"
with open(mappings_file, 'r',encoding='utf-8') as file:
    mappings = json.load(file)
    print(mappings)

mapping_key = mappings["nh_cx"]
print(mapping_key)


rename_desk_excel_onesheet(mapping_key)



