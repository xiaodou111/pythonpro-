# 示例调用
import os

from Excel操作.utils.合并excel import merge_excel_files

# root_folder = r"D:\download\桌面\kdd\饿了么平台\快递店"
folder_path=r"D:\download\桌面\kdd\饿了么平台\饿了么快递店"
output_folder = r"D:\download\桌面\kdd"

# 遍历根目录下的所有子文件夹
# for root, dirs, files in os.walk(root_folder):
#     print(root, dirs, files)
#     for dir_name in dirs:
#         folder_path = os.path.join(root, dir_name)
#         last_two_folders = os.path.basename(os.path.dirname(folder_path)) + '-' + os.path.basename(folder_path)
#         print(111)
#         merge_excel_files(folder_path, output_folder, sheet_name='订单明细', start_row=2, field_value=last_two_folders)

last_folders = os.path.basename(os.path.dirname(folder_path))
merge_excel_files(folder_path, output_folder, sheet_name='订单明细', field_value=last_folders)