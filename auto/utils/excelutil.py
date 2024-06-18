import pandas as pd
#执行SQL查询并将结果保存为Excel文件。
import subprocess

from openpyxl.reader.excel import load_workbook
from openpyxl.styles import NumberFormatDescriptor

from auto.datalink.datalink import import_oracle_prod, get_oracle_zjcs
from auto.utils.convert_date import convert_date_columns
from auto.utils.gui import get_filename
from auto.utils.sqlutil import import_excel_to_oracle, import_excel_to_oracle_usesql

# #excel打开PERSONAL.xlsb
excel_exe_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'







import pandas as pd



# 读取Excel文件的函数
def read_excel(file_path):
    return pd.read_excel(file_path, engine='openpyxl')

def rename_desk_excel_manysheet(columns_mapping):
    desktop_path = r'D:\download\桌面'
    # filename = input("请输入Excel文件名：")
    filename  = get_filename()
    #
    # save_path = desktop_path + '\\' + filename + '.xlsx'
    save_path = filename
    base_name, extension = filename.rsplit('.', 1)  # 分离文件名和扩展名
    output_path = f"{base_name}{'_clean'}.{extension}"  # 构建新的文件名
    # output_path = desktop_path + '\\' + filename + '_clean.xlsx'
    rename_excel_ps(save_path, output_path, columns_mapping)
# 写入Excel文件的函数
def write_to_excel(df_dict, output_file):
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

#输入源文件路径名,目标路径名,映射字典替换字段 只修改包含sheet页包含配送的excel
def rename_excel_ps(source_path, target_path=None, columns_mapping=None):
    # 读取Excel文件
    xls = pd.ExcelFile(source_path)
    sheet_names = xls.sheet_names
    print("读取到的sheet_names:",sheet_names)
    # 创建一个字典，用于存储所有sheet的数据帧
    dataframes = {}
    # 如果没有指定目标路径，则默认保存在原位置
    if target_path is None:
        target_path = source_path
    # 遍历所有sheet
    for sheet_name in sheet_names:
        # 读取单个sheet到DataFrame
        df = xls.parse(sheet_name)

        # 如果sheet名包含'配送'，则进行列名重命名
        if '配送' in sheet_name:
            df_column_names_upper = {col.lower() for col in df.columns.tolist()}
            mapping_columns_upper = {col.lower() for col in columns_mapping.keys()}
            missing_cols = mapping_columns_upper - df_column_names_upper
            print('excel缺失的列', missing_cols)
            for col in missing_cols:
                df[col] = None
                # 找出 DataFrame 多余的列
            extra_cols = df_column_names_upper - mapping_columns_upper
            print('excel多余的列:', extra_cols)
            # 删除 DataFrame 中多余的列
            df.drop(columns=list(extra_cols), inplace=True)
            print('删除的excel多余的列:', extra_cols)
            #重命名列
            df.rename(columns=columns_mapping, inplace=True)
            print(f"对工作表'{sheet_name}'进行了列重命名！")
            for old_name, new_name in columns_mapping.items():
                print(f"原始列名: '{old_name}' -> 新列名: '{new_name}'")
        # 将DataFrame存储到字典中，key为sheet名
        dataframes[sheet_name] = df
    # 将修改后的DataFrame写回到Excel文件中
    try:
        with pd.ExcelWriter(target_path, engine='openpyxl') as writer:
            for sheet_name, df in dataframes.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"所有工作表已保存至Excel文件{target_path}。")
    except Exception as e:
        print(f"在写入Excel文件时发生错误：{e}")
    try:
        print("正在打开excel文件中-------")
        subprocess.Popen([excel_exe_path, target_path])
    except Exception as e:
        print(f"打开文件失败，请手动打开文件。错误信息：{e}")
#单页任意excel清洗
def rename_excel_onesheet(source_path, target_path=None, columns_mapping=None):
    # 读取Excel文件
    xls = pd.ExcelFile(source_path)

    # 读取单个sheet到DataFrame
    df = xls.parse(xls.sheet_names[0])

    # 如果有列名映射，进行列名重命名
    if columns_mapping:
        df.rename(columns=columns_mapping, inplace=True)
        print(f"对工作表'{xls.sheet_names[0]}'进行了列重命名！")

    # 如果没有指定目标路径，则默认保存在原位置
    if target_path is None:
        target_path = source_path

    # 将修改后的DataFrame写回到Excel文件中
    with pd.ExcelWriter(target_path) as writer:
        df.to_excel(writer, sheet_name=xls.sheet_names[0], index=False)

    print(f"工作表已保存至Excel文件{target_path}。")

    # 打开工作簿

    try:
        print("正在打开excel文件中-------")
        subprocess.Popen([excel_exe_path, target_path])
    except Exception as e:
        print(f"打开文件失败，请手动打开文件。错误信息：{e}")

def rename_desk_excel_onesheet(columns_mapping):
    desktop_path = r'D:\download\桌面'
    # filename = input("请输入Excel文件名：")
    filename  = get_filename()
    #
    # save_path = desktop_path + '\\' + filename + '.xlsx'
    save_path = filename
    base_name, extension = filename.rsplit('.', 1)  # 分离文件名和扩展名
    output_path = f"{base_name}{'_clean'}.{extension}"  # 构建新的文件名
    # output_path = desktop_path + '\\' + filename + '_clean.xlsx'
    rename_excel_onesheet(save_path, output_path, columns_mapping)

def rename_desk_excel_one_and_import(columns_mapping,coon,table,*date_columns):
    desktop_path = r'D:\download\桌面'
    # filename = input("请输入Excel文件名：")
    filename = get_filename()
    #
    save_path = desktop_path + '\\' + filename + '.xlsx'
    output_path = desktop_path + '\\' + filename + '_modified.xlsx'
    rename_excel_onesheet(save_path, output_path, columns_mapping)
    engine = coon
    print("连接成功，正在导入Excel数据！")
    import_excel_to_oracle(engine, output_path,table,*date_columns)
def rename_excel_one_import_sql(columns_mapping,coon,table):
    desktop_path = r'D:\download\桌面'
    # filename = input("请输入Excel文件名：")
    filename = get_filename()
    #
    save_path = desktop_path + '\\' + filename + '.xlsx'
    output_path = desktop_path + '\\' + filename + '_modified.xlsx'
    rename_excel_onesheet(save_path, output_path, columns_mapping)
    engine = coon
    print("连接成功，正在导入Excel数据！")
    import_excel_to_oracle_usesql(engine, output_path,table,columns_mapping)
#合并多页excel到一页

def merge_excel_sheet():
# 定义输入和输出文件       路径
      # filename = input("请输入Excel文件名：")
      filename = get_filename()
      # save_path = desktop_path + '\\' + filename + '.xlsx'
      save_path = filename
      base_name, extension = filename.rsplit('.', 1)  # 分离文件名和扩展名
      output_path = f"{base_name}{'_clean'}.{extension}"  # 构建新的文件名
      # 读取所有工作表
      xls = pd.read_excel(save_path, sheet_name=None)
      # df = xls['6.2']
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
      print(df_none)
      combined_df = combined_df.dropna(how='all', axis=1)  # 删除所有值都是 NaN 的列
      #如果这些列为空,那么删除所在行
      # delete_rows=['销售单号']
      # 删除这些列中任何一列值为 NaN 的行
      # combined_df = combined_df.dropna(subset=delete_rows)
      # combined_df['销售单号'] = combined_df['销售单号'].apply(lambda x: str(x))
      # combined_df['销售单号'] = combined_df['销售单号'].astype(str)
      # print(combined_df['销售单号'].dtype)
      # print(combined_df['销售单号'])
      combined_df.to_excel(output_path, index=False)
      try:
          print("正在打开excel文件中-------")
          subprocess.Popen([excel_exe_path, output_path])
      except Exception as e:
          print(f"打开文件失败，请手动打开文件。错误信息：{e}")
