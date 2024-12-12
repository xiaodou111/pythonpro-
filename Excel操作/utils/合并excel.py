

import os
import pandas as pd
from glob import glob


def merge_excel_files(folder_path, output_folder, sheet_name=None, start_row=1, field_value=None):
    """
    合并指定文件夹中的所有Excel文件，并在合并后的文件的最后一列添加指定的字段值。

    :param folder_path: 包含Excel文件的文件夹路径
    :param output_folder: 输出文件的文件夹路径
    :param sheet_name: 要合并的Sheet名称，默认为第一个Sheet
    :param start_row: 数据从第几行开始，默认从第二行开始
    :param field_value: 要添加到最后一列的字段值，默认不添加
    """
    # 获取当前文件夹中的所有.xlsx文件
    file_paths = glob(os.path.join(folder_path, '*.xlsx'))

    if not file_paths:
        print(f"文件夹 {folder_path} 中没有Excel文件。")
        return

    # 创建一个空的DataFrame用于存储所有Excel文件的数据
    all_data = pd.DataFrame()

    # 创建一个字典来记录每个文件的行数
    row_counts = {}

    # 遍历文件夹中的所有文件
    for file in file_paths:
        try:
            # 读取Excel文件，指定工作表和起始行
            df = pd.read_excel(file, sheet_name=sheet_name, skiprows=start_row - 1)

            # 记录当前文件的行数
            row_counts[file] = len(df)

            # 如果指定了字段值，则添加一个新列来标记字段值
            if field_value:
                df['文件类别'] = field_value

            # 将读取的数据追加到all_data DataFrame中
            all_data = pd.concat([all_data, df], ignore_index=True)
        except Exception as e:
            print(f"处理文件 {file} 时发生错误: {e}")

    # 构建输出文件路径
    output_file = os.path.join(output_folder, f"{os.path.basename(folder_path)}.xlsx")

    # 保存合并后的数据到新的Excel文件
    all_data.to_excel(output_file, index=False)

    # 打印每个文件的行数
    for file, count in row_counts.items():
        print(f'{file}: {count} 行')

    print(f"文件夹 {folder_path} 中的Excel文件已成功合并为 {output_file}")


# # 示例调用
# root_folder = r"D:\download\桌面\kdd"
# output_folder = r"D:\download\桌面\kdd"
#
# # 遍历根目录下的所有子文件夹
# for root, dirs, files in os.walk(root_folder):
#     for dir_name in dirs:
#         folder_path = os.path.join(root, dir_name)
#         last_two_folders = os.path.basename(os.path.dirname(folder_path)) + '-' + os.path.basename(folder_path)
#         merge_excel_files(folder_path, output_folder, sheet_name='订单明细', start_row=2, field_value=last_two_folders)
